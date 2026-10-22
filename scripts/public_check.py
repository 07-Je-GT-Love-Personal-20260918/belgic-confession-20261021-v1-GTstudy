from pathlib import Path
import concurrent.futures, hashlib, json, requests, datetime, sys
base=Path(__file__).resolve().parent.parent
hosts={
 'github':'https://07-je-gt-love-personal-20260918.github.io/belgic-confession-20261021-v1-GTstudy/',
 'surge':'https://belgic-confession-20261021-v1-gtstudy.surge.sh/',
 'vercel':'https://belgic-confession-20261021-v1-gtstudy.vercel.app/'
}
files=['index.html','reader.html','style.css','app.js','originals.json','favicon.svg','source-report.html','source-baseline.json','source-recheck.json']
normalize=lambda b:b.replace(b'\r\n',b'\n')
def check(item):
 name,root,file=item
 try:
  response=requests.get(root+file,timeout=(10,30))
  local=(base/'dist'/file).read_bytes()
  ok=response.status_code==200 and normalize(response.content)==normalize(local)
  row={'host':name,'file':file,'url':root+file,'status':response.status_code,'matches_local_ignoring_line_endings':ok,'public_sha256':hashlib.sha256(response.content).hexdigest()}
  if file=='originals.json' and response.status_code==200:
   d=response.json();row['original_sections']=sum(len(x['sections']) for x in d.get('documents',[]))
  return row
 except Exception as ex:return {'host':name,'file':file,'url':root+file,'status':'error','error':str(ex),'matches_local_ignoring_line_endings':False}
previous=None
if '--retry-failed' in sys.argv:
 previous=json.loads((base/'qa/public-check.json').read_text(encoding='utf8'))
 items=[(r['host'],hosts[r['host']],r['file']) for r in previous['checks'] if not r['matches_local_ignoring_line_endings']]
else:items=[(name,url,file) for name,url in hosts.items() for file in files]
with concurrent.futures.ThreadPoolExecutor(max_workers=3 if previous else 6) as ex:fetched=list(ex.map(check,items))
if previous:
 replacements={(r['host'],r['file']):r for r in fetched}
 rows=[replacements.get((r['host'],r['file']),r) for r in previous['checks']]
else:rows=fetched
report={'date':'2026-10-22','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hosts':hosts,'method':'Unauthenticated HTTPS GET; compare each response to local release bytes, ignoring CRLF/LF differences only.','checks':rows,'passed':sum(r['matches_local_ignoring_line_endings'] for r in rows),'total':len(rows)}
if previous:report['retry']={'previous_checked_at_utc':previous['checked_at_utc'],'previous_passed':previous['passed'],'retried_resources':len(items)}
(base/'qa/public-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'passed':report['passed'],'total':report['total'],'issues':[r for r in rows if not r['matches_local_ignoring_line_endings']]}))

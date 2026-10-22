from pathlib import Path
import json, re, hashlib
base=Path(__file__).resolve().parent.parent
baseline=json.loads((base.parent/'reformed-three-creeds-20261017-v1/qa/v3-source-recheck.json').read_text(encoding='utf8'))
baseline['meta'].pop('permission',None)
baseline['meta']['provenance']='Existing project verification record, reused as dated baseline, not a new live fetch by this edition.'
baseline['meta']['reused_for_release']='2026-10-22'
docs=json.loads((base/'dist/originals.json').read_text(encoding='utf8'))['documents']
rows={(r['document'],r['section']):r for r in baseline['sections']}
for d in docs:
 for i,s in enumerate(d['sections'],1):
  row=rows[d['key'],i]
  assert row['match']
  assert row['source']==s['source']
  assert row['archived_normalized_sha256']==hashlib.sha256(re.sub(r'\s+','',s['text']).encode()).hexdigest()
(base/'qa/source-baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf8')
print('All 232 current text units match the dated baseline hashes.')

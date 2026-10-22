import concurrent.futures, datetime, hashlib, json, re, time
from pathlib import Path
import requests
from bs4 import BeautifulSoup

base = Path(__file__).resolve().parent.parent
data = json.loads((base/'dist/originals.json').read_text(encoding='utf-8'))
urls = sorted({s['source'] for d in data['documents'] for s in d['sections']})

def extract(el):
    for x in el.select('nav,script,style'): x.decompose()
    ps=[]
    for x in el.find_all(['p','h2','h3','h4','h5','li']):
        if x.find_parent(['p','li']): continue
        t=x.get_text('',strip=False).strip()
        if t: ps.append(t)
    return '\n\n'.join(ps) if ps else el.get_text('',strip=False).strip()

def fetch(url):
    start=time.monotonic()
    try:
        r=requests.get(url,timeout=(10,35),headers={'User-Agent':'GTstudy source verification/3.0'})
        r.raise_for_status()
        soup=BeautifulSoup(r.content,'html.parser')
        if '/creeds/' in url:
            els=soup.select('.article-body .alert-primary')
        elif 'heidelberg-catechism' in url:
            els=soup.select('#block-tulip-content .entity-reference > span > article')
        else:
            els=soup.select('#block-tulip-content > article > div')
        texts=[extract(x) for x in els]
        return url,dict(status=r.status_code,final_url=r.url,seconds=round(time.monotonic()-start,2),raw_sha256=hashlib.sha256(r.content).hexdigest(),blocks=len(texts)),texts
    except Exception as e:
        return url,dict(status='error',error=str(e),seconds=round(time.monotonic()-start,2)),[]

cache={}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
    for n,(url,info,texts) in enumerate(ex.map(fetch,urls),1):
        cache[url]=(info,texts)
        if n%20==0: print(f'fetched {n}/{len(urls)}',flush=True)

# Retry transport failures only; retain successful responses in this execution.
for url,(info,texts) in list(cache.items()):
    if info['status']=='error':
        _,retry_info,retry_texts=fetch(url)
        retry_info['initial_error']=info.get('error')
        retry_info['retry_success']=retry_info['status']==200
        cache[url]=(retry_info,retry_texts)

def normalize(t): return re.sub(r'\s+','',t)
checks=[]
for d in data['documents']:
    for idx,s in enumerate(d['sections']):
        info,texts=cache[s['source']]
        matches=[t for t in texts if normalize(t)==normalize(s['text'])]
        row=dict(document=d['key'],section=idx+1,title=s['title'],source=s['source'],match=bool(matches),archived_normalized_sha256=hashlib.sha256(normalize(s['text']).encode()).hexdigest())
        if not matches:
            row['reason']='source_fetch_error' if info['status']=='error' else ('selector_empty' if not texts else 'text_difference')
            if texts:
                candidate=next((t for t in texts if t.startswith(s['text'][:12])),texts[0])
                a,b=normalize(s['text']),normalize(candidate)
                pos=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
                row['difference_sample']=dict(position=pos,archived=a[max(0,pos-15):pos+25],live=b[max(0,pos-15):pos+25],archived_length=len(a),live_length=len(b))
        checks.append(row)
out=dict(meta=dict(date='2026-10-21',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Live HTTP GET once per unique source in this execution; no prior disk cache; concurrency 5; original extraction selectors; paragraph blocks p/h2/h3/h4/h5/li, nested p/li excluded; only Unicode whitespace ignored',input='User-supplied PDF; current CCI translation checked against source.'),summary=dict(total_sections=len(checks),matched=sum(r['match'] for r in checks),differences=sum(not r['match'] for r in checks),unique_sources=len(urls),sources_ok=sum(i['status']==200 for i,t in cache.values())),sources=[dict(url=u,**i) for u,(i,t) in cache.items()],sections=checks)
(base/'qa/source-recheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out['summary']),flush=True)

from pathlib import Path
from html.parser import HTMLParser
import json, re, hashlib
base=Path(__file__).resolve().parent.parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.scripts=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if tag=='a' and 'href'in a:self.links.append(a['href'])
  if tag=='script' and 'src'in a:self.scripts.append(a['src'])
checks=[]
for p in (base/'dist').glob('*.html'):
 text=p.read_text(encoding='utf8');parser=Parser();parser.feed(text)
 assert len(parser.ids)==len(set(parser.ids)),f'duplicate IDs {p}'
 for href in parser.links+parser.scripts:
  if href.startswith(('http:','https:','mailto:','data:')):continue
  target,_,anchor=href.partition('#');target=target.split('?')[0]
  if not target:
   assert not anchor or anchor in parser.ids,f'broken anchor {p.name} {href}'
  else:assert (base/'dist'/target).is_file(),f'broken local link {p.name} {href}'
 assert not re.search(r'github_pat_|gh[pousr]_[A-Za-z0-9]{20}',text),'credential-like text'
 checks.append({'file':p.name,'ids':len(parser.ids),'links':len(parser.links),'local_links_ok':True})
originals=json.loads((base/'dist/originals.json').read_text(encoding='utf8'))
reader=(base/'dist/reader.html').read_text(encoding='utf8')
count=0
for doc in originals['documents']:
 for s in doc['sections']:
  assert hashlib.sha256(s['text'].encode()).hexdigest()==s['sha256']
  assert s['html'] in reader
  count+=1
assert count==232
assert (base/'dist/index.html').read_text(encoding='utf8').count('class="article-card"')==37
result={'date':'2026-10-21','original_sections':count,'commentary_articles':37,'pages':checks,'result':'PASS'}
(base/'qa/static-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result))

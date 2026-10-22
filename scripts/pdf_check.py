from pathlib import Path
import json, hashlib, re, difflib
from pypdf import PdfReader
base=Path(__file__).resolve().parent.parent
source=Path('E:/敬拜赞美手册出版（2015）.pdf')
r=PdfReader(source)
texts=[p.extract_text() or '' for p in r.pages]
norm=lambda s:re.sub(r'\s+','',s)
docs=json.loads((base/'dist/originals.json').read_text(encoding='utf8'))['documents']
creeds=[]
for d in docs[:3]:
 website=norm(d['sections'][0]['text'])
 # Record opening location, not a claim that all PDF characters equal the web.
 needle=website[:12]
 hits=[i+1 for i,t in enumerate(texts) if needle in norm(t)]
 creeds.append({'title':d['title'],'opening_page_candidates':hits,'website_normalized_characters':len(website)})
out={'date':'2026-10-21','input_filename':source.name,'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pages':len(r.pages),'text_pages':sum(bool(t.strip()) for t in texts),'creeds':creeds,'method':'Read-only pypdf text extraction of current user-supplied file. Existing translation corpus is independently checked against current CCI website. PDF identity is not evidence of character-for-character website equality.','publication':'The full PDF is not copied to dist or the repository.'}
(base/'qa/pdf-input-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
try:
 import fitz
 doc=fitz.open(source)
 doc[3].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(base/'qa/pdf-creed-preview.png')
except ImportError: pass
print(json.dumps({'pages':out['pages'],'text_pages':out['text_pages'],'bytes':out['bytes']}))

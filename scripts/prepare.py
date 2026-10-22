from pathlib import Path
import json
base=Path(__file__).resolve().parent.parent
workspace=base.parent
d=json.loads((workspace/'research/fulltexts.json').read_text(encoding='utf8'))
d['meta'].pop('permission',None)
d['meta']['accessed']='2026-10-21'
d['meta']['input']='用户提供 E:/敬拜赞美手册出版（2015）.pdf；以指定网站中文译文核对，非古代原语版本。'
(base/'dist/originals.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
s=(workspace/'reformed-three-creeds-20261017-v1/qa/v3-source-recheck.py').read_text(encoding='utf8').replace('content/fulltexts.json','dist/originals.json').replace('qa/v3-source-recheck.json','qa/source-recheck.json').replace("permission='User supplied PDF and confirmed permission for public use.'","input='User-supplied PDF; current CCI translation checked against source.'")
(base/'scripts/source_check.py').write_text(s,encoding='utf8')

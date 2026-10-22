from pathlib import Path
import json
base=Path(__file__).resolve().parent.parent
p=base/'research/overview.json'
d=json.loads(p.read_text(encoding='utf8'))
d['timeline'][-1]['text']='本站采用指定网站2015版译本体系与2026-10-21成功核验基线，10月22日发布；本次批量访问超时另行记录。中文原文在此指指定中文译文，不指法文、希腊文或拉丁文初版。'
d['sources'].append({'title':'Natural Earth · 底图公有领域许可','url':'https://www.naturalearthdata.com/about/terms-of-use/','use':'地图现代轮廓的1:110m地理数据，非1561年疆界。'}) if not any('Natural Earth' in x['title'] for x in d['sources']) else None
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
p=base/'build.py';s=p.read_text(encoding='utf8').replace('2026.10.21','2026.10.22').replace("'date':'2026-10-21'","'date':'2026-10-22'");p.write_text(s,encoding='utf8')
p=base/'research/articles-1-19.json';a=json.loads(p.read_text(encoding='utf8'));a[11]['related']='比利时13—15、37；海德堡26—28';p.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8')
p=base/'dist/originals.json';d=json.loads(p.read_text(encoding='utf8'))
d['meta']['pdf_comparison']='本次用户提供245页2015版PDF；与网站属同译本体系，但不声称逐字一致。正文以CCI保存中文译文为准，不依据PDF静默改写。'
d['meta']['input']='用户提供的《敬拜赞美手册出版（2015）.pdf》；原文为指定网站中文译文，非古代原语文本。'
d['meta']['edition_scope']='多特依指定网站保存版本：59条正面教义与4组完整驳谬；未用其他译本补入独立结语。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
p=base/'build.py';s=p.read_text(encoding='utf8');escaped="'<"+chr(92)+"/'";s=s.replace(escaped,'r'+escaped);p.write_text(s,encoding='utf8')

"""History atlas, progressive maps, and small per-document readers. No build dependencies."""
import json, re, html
from pathlib import Path
E=lambda v:html.escape(str(v),quote=True)
ICONS={
 'back':'M15 18l-6-6 6-6','forward':'M9 18l6-6-6-6','up':'M6 14l6-6 6 6','down':'M6 10l6 6 6-6',
 'home':'M3 11l9-8 9 8M5 10v11h5v-7h4v7h5V10','map':'M3 5l6-2 6 2 6-2v16l-6 2-6-2-6 2V5M9 3v16M15 5v16',
 'book':'M12 5v16M3 3c4 0 6 0 9 2 3-2 5-2 9-2v16c-4 0-6 0-9 2-3-2-5-2-9-2V3',
 'cross':'M12 3v18M5 9h14','scroll':'M7 3h13v15a3 3 0 01-6 0V6H4a3 3 0 010-6M7 3v18h10',
 'press':'M7 3h10v5H7V3M5 8h14v9H5V8M7 14h10v7H7v-7M8 11h.1',
 'flame':'M12 2c2 6 8 7 8 13a8 8 0 01-16 0c0-3 2-6 5-8-1 5 1 6 2 6 3-2 2-6 1-11Z',
 'people':'M16 21v-3a4 4 0 00-4-4H6a4 4 0 00-4 4v3M19 8a3 3 0 010 6M22 21v-3a4 4 0 00-3-4M13 7a4 4 0 11-8 0 4 4 0 018 0',
 'language':'M3 5h12M9 2v3M5 5c1 5 4 8 8 10M13 5c-1 5-4 8-9 10M14 21l4-10 4 10M16 18h4',
 'shield':'M12 2l9 4v6c0 5-4 8-9 10-5-2-9-5-9-10V6l9-4M8 12l3 3 5-6',
 'note':'M4 3h16v18H4V3M8 7h8M8 11h8M8 15h5','close':'M6 6l12 12M18 6L6 18',
 'spark':'M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3 3-7','menu':'M5 7h14M5 12h14M5 17h14',
 'pin':'M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1116 0ZM15 10a3 3 0 11-6 0 3 3 0 016 0',
 'arrow':'M4 12h16M14 6l6 6-6 6','undo':'M4 10h10a6 6 0 010 12M4 10l6-6M4 10l6 6'
}
def icon(name): return f'<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{ICONS.get(name,ICONS["spark"])}"/></svg>'
def city_data(overview):
 cities=[dict(c,group='reformed') for c in overview['cities']]
 cities += [dict(id='rome',name='罗马',en='Roma / Rome',lat=41.9028,lon=12.4964,group='ancient',role='西方洗礼认信传统',text='现代意大利城市定位；使徒信经的历史形成关联西方教会传统，并非十二使徒在此共同执笔。'),dict(id='nicaea',name='尼西亚',en='İznik / Nicaea',lat=40.429,lon=29.721,group='ancient',role='325年尼西亚会议',text='现代土耳其伊兹尼克；教会承认子受生而非被造、与父同质。'),dict(id='constantinople',name='君士坦丁堡',en='İstanbul / Constantinople',lat=41.0082,lon=28.9784,group='ancient',role='381年会议的历史城市',text='现代土耳其伊斯坦布尔；现代城市定位不等于古代会议会址的精确考古定位。')]
 return cities
def map_panel(cities,compact=False):
 return f'''<section class="live-map-card" id="modern-map" aria-labelledby="liveMapTitle"><div class="live-map-heading"><div><p class="eyebrow">MODERN MAP · 现代地理对照</p><h3 id="liveMapTitle">把历史城市，放回真实世界。</h3></div><span class="map-badge">Esri · 备用图层</span></div><p class="map-description">历史示意帮助理解关系；现代地图可缩放、平移和定位。地名与疆界属于现代资料，卫星图不是实时直播。</p><div class="map-toolbar"><label>城市 <select id="mapCity">{''.join(f'<option value="{E(c["id"])}">{E(c["name"])}</option>' for c in cities)}</select></label><label>底图 <select id="mapProvider"><option value="esri">Esri 街道地图</option><option value="imagery">Esri 卫星影像</option><option value="osm">OpenStreetMap 备用</option></select></label><button type="button" id="mapExtent">{icon('map')} 看全部城市</button></div><div class="live-map-frame"><div id="liveMap" class="live-map" aria-label="可缩放平移的现代地图"></div><div class="map-start" id="mapStart"><div class="map-start-symbol">{icon('pin')}</div><strong>在线地图按需载入</strong><p>先读示意图；需要真实地理位置时再打开。在线图层失败不会影响历史正文。</p><button type="button" id="loadMap" class="primary">{icon('map')} 载入现代地图</button></div></div><p id="mapStatus" class="map-status" role="status">示意图已随页面保存；尚未请求在线瓦片。</p><div class="map-external"><a id="mapExternal" href="https://www.bing.com/maps?cp=50.606~3.389&amp;lvl=12" target="_blank" rel="noopener noreferrer">在 Bing 地图打开 ↗</a><a id="mapOsmExternal" href="https://www.openstreetmap.org/?mlat=50.606&amp;mlon=3.389#map=12/50.606/3.389" target="_blank" rel="noopener noreferrer">在 OpenStreetMap 打开 ↗</a><button type="button" id="stopMap">暂停在线地图</button></div><noscript><p>现代地图交互需要JavaScript；上方示意与独立地图链接仍可阅读。</p></noscript></section>'''
def tools():
 nav='<nav class="quick-nav" aria-label="快捷阅读导航"><div class="quick-items" id="quickItems" hidden>'
 for id,label,ico in [('navBack','返回上一页','back'),('navForward','前进一页','forward')]:nav+=f'<button type="button" id="{id}" aria-label="{label}" title="{label}">{icon(ico)}</button>'
 nav+=f'<a href="index.html" aria-label="返回主页" title="主页">{icon("home")}</a><a href="atlas.html" aria-label="历史地图馆" title="历史地图">{icon("map")}</a><button type="button" id="navTop" aria-label="到页面顶部" title="到顶部">{icon("up")}</button><button type="button" id="navBottom" aria-label="到页面底部" title="到底部">{icon("down")}</button><button type="button" id="openMarks" aria-label="打开重点笔记" title="重点笔记">{icon("note")}<span id="markCount" class="mark-count">0</span></button></div><button type="button" class="quick-toggle" id="quickToggle" aria-label="展开快捷导航" aria-controls="quickItems" aria-expanded="false">{icon("menu")}</button></nav>'
 nav+='<div class="mark-toolbar" id="markToolbar" role="toolbar" aria-label="选中文字重点标记" hidden><span class="mark-toolbar-label">重点</span>'
 for style,label,content in [('bold','加粗','B'),('ink-blue','蓝色文字','蓝'),('ink-rose','玫红文字','红'),('gold','金色底纹','金'),('green','绿色底纹','绿'),('underline','蓝色实线','线'),('dash','玫红虚线','虚'),('block','紫色区块','块')]:nav+=f'<button type="button" class="mark-style style-{style}" data-mark-style="{style}" aria-label="{label}" title="{label}">{content}</button>'
 nav+=f'<button type="button" id="undoMark" aria-label="撤销最近标记" title="撤销">{icon("undo")}</button><button type="button" id="closeMarkToolbar" aria-label="关闭标记工具">{icon("close")}</button></div>'
 nav+=f'''<aside class="marks-drawer" id="marksDrawer" role="dialog" aria-modal="true" aria-labelledby="marksTitle" hidden><div class="drawer-head"><div><p class="eyebrow">MY READING MARKS</p><h2 id="marksTitle">重点笔记</h2></div><button type="button" id="closeMarks" aria-label="关闭重点笔记">{icon('close')}</button></div><p class="muted">选中同一段中的文字，可加粗、着色、加底纹或画线。标记保存在当前浏览器，不改动认信原文。</p><div class="mark-legend"><span class="style-gold">核心</span><span class="style-green">应许</span><span class="style-underline">逻辑</span><span class="style-dash">难点</span></div><div class="toolbar"><button type="button" id="exportMarks">导出重点</button><label class="button import-label">导入重点<input type="file" id="importMarks" accept=".json,application/json"></label><a class="button" href="index.html#memory">笔记与学习进度</a></div><div id="marksList"></div></aside><button type="button" class="marks-backdrop" id="marksBackdrop" aria-label="关闭重点笔记" hidden></button><div class="study-toast" id="studyToast" role="status" hidden></div>'''
 return nav
def enhance_page(page,cities,main=False):
 page=page.replace('</head>','<link rel="stylesheet" href="enhance.css"><script src="enhance.js" defer></script></head>')
 page=page.replace('class="backtop"','class="backtop legacy-backtop"')
 page=page.replace('v1.0.0','v2.0.0').replace('2026.10.22','2026.10.24')
 if main:
  page=page.replace('<p class="toc-title">','<a class="atlas-toc-link" href="atlas.html">'+icon('map')+' 历史 · 地图 · 文化 ↗</a><p class="toc-title">',1)
  page=page.replace('<div class="map-layout">','<div class="atlas-invite"><div><p class="eyebrow">NEW · 历史地图馆</p><h3>从地名，读到信条为什么这样写。</h3><p>六个历史场景，四个文化因素；示意图与现代地图互相对照。</p></div><a class="button primary" href="atlas.html">'+icon('map')+' 进入历史地图馆 ↗</a></div><div class="map-layout">',1)
  page=page.replace('</div></div></div></section><section class="chapter" id="covenant">','</div></div></div>'+map_panel(cities)+'</section><section class="chapter" id="covenant">',1)
  # Explicit stable anchors for unchanged commentary text, including future inline formatting.
  page=re.sub(r'(<article class="article-card" id="article-(\d+)".*?)(?=<article class="article-card"|</div><p id="noResults")',lambda m:annotate_article(m.group(0),m.group(2)),page,flags=re.S)
  page=page.replace('<h3>六站记忆路径</h3>','<h3>六站记忆路径</h3><p class="mark-hint">'+icon('note')+' 选中文字即可标记；右下角“重点笔记”可回看、删除与导出。</p>',1)
 page=page.replace('</body>',tools()+'<script type="application/json" id="mapCities">'+json.dumps(cities,ensure_ascii=False).replace('</',r'<\/')+'</script></body>')
 return page
def annotate_article(s,n):
 s=s.replace('<div class="core"><span>本质核心</span><p>',f'<div class="core"><span>本质核心</span><p data-note-block="article-{n}-core">',1)
 for field in ['logic','biblical','covenant','context','error','application']:
  s=re.sub(r'(<section class="analysis-field '+field+r'">.*?</h4><p)>',lambda m:m.group(1)+f' data-note-block="article-{n}-{field}">',s,count=1,flags=re.S)
 return s
def concept_map():
 positions=[('geneva','日内瓦','法语 · 训练网络',95,300,'#397b87'),('tournai','图尔奈','1561 · 公开认信',285,135,'#aa7137'),('valenciennes','瓦朗谢讷','1567 · 殉道盼望',320,335,'#b65e72'),('antwerp','安特卫普','1566 · 修订接纳',510,115,'#49764e'),('heidelberg','海德堡','1563 · 要理教导',720,310,'#7566a4'),('dordrecht','多德雷赫特','1618—19 · 联合认信',735,85,'#367b9b')]
 svg='<svg class="concept-map" viewBox="0 0 900 470" role="img" aria-label="低地改革宗城市关系概念图，非比例地图，也非精确旅行路线"><defs><marker id="conceptArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#b6a37c"/></marker></defs><path class="concept-cloud" d="M60 110Q60 20 170 55Q260-15 345 70Q440 10 495 70Q600 10 665 50Q800-10 855 100Q920 210 825 250Q910 390 765 405Q670 490 560 410Q430 465 350 408Q190 475 150 385Q20 365 65 270Q-10 180 60 110Z"/>'
 for path in ['M140 290Q160 170 250 145','M325 165Q370 230 335 300','M330 125Q410 65 470 110','M555 115Q640 40 690 85','M700 290Q640 200 720 115']:
  svg+=f'<path class="concept-link" d="{path}" marker-end="url(#conceptArrow)"/>'
 for id,name,role,x,y,col in positions:
  svg+=f'<g class="concept-city" data-city="{id}" tabindex="0" role="button" aria-label="定位{name}" style="--city-color:{col}" transform="translate({x} {y})"><circle class="concept-halo" r="48"/><circle r="33"/><path d="M-15 10V-7h8v-13l7-9 7 9v13h8v17M-20 11h40M-3 10V1h6v9"/><text y="69">{name}</text><text class="concept-role" y="91">{role}</text></g>'
 svg+='<text class="concept-caption" x="28" y="451">城市关系教学示意 · 非比例、非疆界、非精确旅行路线</text></svg>'
 return svg
def make_atlas(root,head,topbar,overview):
 data=json.loads((root/'research/atlas.json').read_text(encoding='utf8'));cities=city_data(overview)
 p=head('历史 · 地图 · 文化｜比利时信条 · GTstudy')+topbar(True)+'<main id="main" class="atlas-main"><section class="atlas-hero" id="top"><div><p class="eyebrow">THE GEOGRAPHY OF CONFESSION · 历史地图馆</p><h1>城与城之间，<br><span>真理怎样被传下去。</span></h1><p>抓住三件事：谁在承认、为什么此时承认、怎样成为教会共同的声音。</p><div class="toolbar"><a class="button primary" href="#scenes">'+icon('scroll')+' 进入六个历史场景</a><a class="button" href="#modern-map">'+icon('map')+' 查看现代地图</a><a class="button" href="index.html#article-36">读第36—37条 ↗</a></div></div><div class="atlas-hero-art">'+concept_map()+'</div></section>'
 p+='<section id="scenes" class="atlas-section"><div class="section-heading"><span class="section-no">01</span><div><p class="eyebrow">HISTORY → CULTURE → CONFESSION</p><h2>历史不只是一列年份。</h2><p class="lede">选择场景，跟随问题读历史；城市定位会与下方地图联动。</p></div></div><div class="scene-tabs" role="tablist" aria-label="历史场景">'
 for i,s in enumerate(data['scenes']):p+=f'<button type="button" role="tab" id="tab-{s["id"]}" aria-controls="scene-{s["id"]}" aria-selected="{"true" if i==0 else "false"}" tabindex="{0 if i==0 else -1}" data-scene="{s["id"]}">{icon(s["icon"])}<span><b>{E(s["year"])}</b>{E(s["title"])}</span></button>'
 p+='</div><div class="scene-panels">'
 for i,s in enumerate(data['scenes']):
  p+=f'<article class="scene-panel" id="scene-{s["id"]}" role="tabpanel" aria-labelledby="tab-{s["id"]}" data-city="{s["city"]}" {"hidden" if i else ""}><div class="scene-question"><span>{E(s["year"])}</span><h3>{E(s["question"])}</h3><button type="button" class="locate-scene" data-city="{s["city"]}">{icon("pin")} 地图定位</button></div><div class="scene-grid"><section><h4>{icon("scroll")} 发生了什么</h4><p data-note-block="atlas-{s["id"]}-history">{E(s["history"])}</p></section><section><h4>{icon("people")} 文化怎样影响问题</h4><p data-note-block="atlas-{s["id"]}-culture">{E(s["culture"])}</p></section></div><div class="scene-core"><span>本质核心</span><p data-note-block="atlas-{s["id"]}-core">{E(s["core"])}</p></div><p class="refs">对应比利时第{E(s["articles"])}条 · <a href="{E(s["source"])}" target="_blank" rel="noopener noreferrer">核查来源 ↗</a></p></article>'
 p+='</div></section>'+map_panel(cities)
 p+='<section class="atlas-section" id="culture"><div class="section-heading"><span class="section-no">02</span><div><p class="eyebrow">CULTURAL MECHANISMS</p><h2>四个文化因素，一条因果链。</h2><p class="lede">处境不会制造真理，却影响人需要回答什么问题、怎样把答案传给下一代。</p></div></div><div class="culture-grid">'
 for i,c in enumerate(data['culture']):
  p+=f'<article class="culture-card tone-{i}"><span class="culture-icon">{icon(c["icon"])}</span><h3>{E(c["title"])}</h3><dl><dt>处境</dt><dd data-note-block="culture-{i}-cause">{E(c["cause"])}</dd><dt>作用机制</dt><dd data-note-block="culture-{i}-mechanism">{E(c["mechanism"])}</dd><dt>怎样读信条</dt><dd data-note-block="culture-{i}-reading">{E(c["reading"])}</dd></dl><p class="culture-memory">✦ {E(c["memory"])}</p></article>'
 p+='</div><div class="cause-flow"><div>'+icon('pin')+'<b>真实处境</b><small>语言、权力、教导需要</small></div><span>→</span><div>'+icon('scroll')+'<b>公开回答</b><small>按圣经说明所信</small></div><span>→</span><div>'+icon('people')+'<b>共同承担</b><small>教会接纳与教师认信</small></div><span>→</span><div>'+icon('book')+'<b>代代传递</b><small>讲台、家庭与学习</small></div></div></section>'
 p+='<section class="atlas-section" id="city-index"><h2>地理定位，不代替历史判断。</h2><div class="table-wrap" tabindex="0" role="region" aria-label="历史与现代城市对照"><table><thead><tr><th>城市</th><th>历史关联</th><th>现代位置</th><th>地图</th></tr></thead><tbody>'
 for c in cities:p+=f'<tr><th>{E(c["name"])}<small>{E(c["en"])}</small></th><td>{E(c["role"])}</td><td>{c["lat"]:.3f}°N · {c["lon"]:.3f}°E</td><td><button type="button" class="locate-scene" data-city="{c["id"]}">{icon("pin")} 定位</button></td></tr>'
 p+='</tbody></table></div><p class="refs">城市坐标为现代城市中心的近似定位，不把它们称作历史会议、投递事件或处决地点的精确坐标。</p></section><section class="atlas-section" id="atlas-sources"><h2>来源与阅读边界</h2><p>以下区分历史事实与原创解释；文化机制是帮助理解的分析，不能用地域标签决定每个人的信仰。</p><div class="resource-links">'
 for s in data['sources']:p+=f'<a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">{E(s["title"])} ↗</a>'
 p+='</div><p class="refs">地图引擎：Leaflet 1.9.4，本地随站保存；默认现代底图Esri，OpenStreetMap为备用。在线服务的覆盖与连通性取决于地区和网络，示意图不依赖在线图层。原文来源、版本及第36条差异见<a href="index.html#sources">总说明</a>。</p></section><footer><p>GTstudy · 历史地图馆 · v2.0.0 · 2026.10.24</p><a href="index.html">回到37条全景深读 ↗</a></footer></main></body></html>'
 return enhance_page(p,cities)
def build_readers(root,originals,head,topbar,anchor,cities):
 out=root/'dist';text_stats={}
 for doc in originals['documents']:
  key=doc['key'];p=head(doc['title']+' · 原文书房 · GTstudy')+topbar(True)+'<main id="main" class="reader-main"><div class="reader-intro" id="top"><p class="eyebrow">THE CONFESSIONAL LIBRARY</p><h1>原文书房</h1><p>安静地读，准确地记。每页只载入一份认信，保持原文、脚注与附经完整。</p></div><div class="reader-controls"><label>阅读文本 <select id="docSelect">'
  for d in originals['documents']:p+=f'<option value="{d["key"]}" {"selected" if d["key"]==key else ""}>{E(d["title"])}</option>'
  p+='</select></label><button type="button" id="readerMask" aria-pressed="false">遮盖正文 · 背诵</button><button type="button" id="readerCopy">复制当前全文</button><button type="button" id="readerSpeak">▷ 朗读当前全文</button><button type="button" id="readerStop">□ 停止</button><button type="button" id="readerPrint">打印干净版</button><span id="readerStatus" role="status"></span></div><p class="reader-version">原文不混入释义；彩色重点仅是个人阅读标记。选字可标记，右下角可回看。设备朗读不是原站录音。</p>'
  p+=f'<article class="document" id="doc-{key}" data-doc="{key}"><div class="document-header"><p class="eyebrow">CCI · BOOK OF PRAISE · 2015</p><h2>{E(doc["title"])}</h2><p>{anchor(doc["source"],"指定网站目录／原文")}</p></div>'
  if len(doc['sections'])>1:
   p+='<details class="reader-index"><summary>显示本文详细目录</summary><nav>'+''.join(f'<a href="#reader-{key}-{i}">{E(s["title"])}</a>' for i,s in enumerate(doc['sections'],1))+'</nav></details>'
  if key=='dort':p+='<p class="reader-version">包括59条正面教义与四组完整驳谬；指定版本缺载的独立结语不以其他译本补写。</p>'
  group=''
  for i,s in enumerate(doc['sections'],1):
   if s.get('group') and s['group']!=group:group=s['group'];p+=f'<h3 class="reader-group">{E(group)}</h3>'
   p+=f'<section class="reader-section" id="reader-{key}-{i}">'+(f'<h3>{E(s["title"])}</h3>' if len(doc['sections'])>1 else '')+f'<div class="reader-passage" tabindex="0" role="button" aria-label="{E(s["title"])}，背诵模式下按回车显示或遮盖正文"><div class="original-text" data-original="{key}-{i}">{s["html"]}</div><span class="mask-prompt" aria-hidden="true">点击或按回车揭开此节</span></div><a class="passage-source" href="{E(s["source"])}" target="_blank" rel="noopener noreferrer">来源 ↗</a></section>'
  p+='</article><footer><p>指定中文译文 ©《中国改革宗敬拜手册》出版委员会，2015。资料来源：ccifellowship.org。</p><p>v2.0.0 · 2026.10.24 · <a href="index.html#sources">版本与来源说明</a></p></footer></main>'
  payload={'key':key,'title':doc['title'],'sections':[{'title':s['title'],'text':s['text']} for s in doc['sections']]}
  p+='<script type="application/json" id="readerData">'+json.dumps(payload,ensure_ascii=False).replace('</',r'<\/')+'</script><script src="reader.js" defer></script></body></html>'
  p=enhance_page(p,cities)
  filename='reader.html' if key=='apostles' else 'reader-'+key+'.html'
  (out/filename).write_text(p,encoding='utf8',newline='\n');text_stats[key]=len(p.encode())
 return text_stats

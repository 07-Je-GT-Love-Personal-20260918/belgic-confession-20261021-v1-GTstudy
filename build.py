"""Build the complete static study edition. Python standard library only."""
from pathlib import Path
import json, html, hashlib

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
OUT.mkdir(exist_ok=True)
def load(p): return json.loads((ROOT/p).read_text(encoding='utf8'))
def e(s): return html.escape(str(s),quote=True)
originals=load('dist/originals.json')
docs={d['key']:d for d in originals['documents']}
overview=load('research/overview.json')
articles=load('research/articles-1-19.json')+load('research/articles-20-37.json')
articles.sort(key=lambda a:a['n'])
assert [a['n'] for a in articles]==list(range(1,38))
GROUPS=[(1,7,'认识神与祂的话','启示'),(8,13,'三一、创造与护理','三一'),(14,17,'堕落、拣选与应许','恩典'),(18,26,'中保、称义与新生命','基督'),(27,35,'教会、职分与圣礼','教会'),(36,37,'地上的秩序与终极盼望','盼望')]
def group(n): return next(g for g in GROUPS if g[0]<=n<=g[1])
NAV=[('overview','01','圣经全景'),('history','02','时间与现场'),('covenant','03','圣约主线'),('articles','04','37条深读'),('compare','05','三信条对照'),('creeds','06','三大普世信经'),('memory','07','记忆与自测'),('sources','08','来源与版本')]
def topbar(reader=False):
 return f'''<a class="skip" href="#main">跳到正文</a><header class="topbar"><a class="brand" href="index.html"><span class="brandmark">✦</span><span>GT<span class="brandlight">study</span><small>认信 · 理解 · 生活</small></span></a><div class="header-right"><span class="edition">BELGIC CONFESSION · 1561</span><button type="button" id="theme" aria-label="切换明暗主题">◐ <span>主题</span></button><button type="button" id="font" aria-label="调整正文字号">A<span>＋</span></button>{'<a class="button" href="index.html#articles">返回解读 ↗</a>' if reader else '<button type="button" id="tocToggle" aria-controls="toc" aria-expanded="true">☷ 目录</button>'}</div></header><div class="progress" aria-hidden="true"><i id="scrollProgress"></i></div>'''
def head(title):
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>{title}</title><meta name="description" content="从整本圣经读懂比利时信条37条：欧陆改革宗、圣约神学、时间线与地图、三项联合信条比较、六份认信原文与背诵。"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="app.js" defer></script></head><body>'''
def section(id,num,title,desc): return f'<section class="chapter" id="{id}"><div class="section-heading"><span class="section-no">{num}</span><div><p class="eyebrow">THE BELGIC CONFESSION / STUDY EDITION</p><h2>{title}</h2><p class="lede">{desc}</p></div></div>'
def anchor(url,label): return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗</a>'

toc='<aside id="toc" class="toc" aria-label="学习目录"><div class="toc-head"><p class="eyebrow">你的阅读地图</p><button id="tocClose" type="button" aria-label="关闭目录">×</button></div><p class="toc-title">比利时信条</p><p class="muted">37条 · 一条救恩主线</p><nav>'
for id,num,title in NAV:
 toc+=f'<a href="#{id}" class="nav-major"><span>{num}</span>{title}</a>'
 if id=='articles':
  toc+='<details><summary>展开37条详细目录</summary>'
  for a in articles: toc+=f'<a class="nav-article" href="#article-{a["n"]}">{a["n"]:02d} · {e(a["title"])}</a>'
  toc+='</details>'
toc+='</nav><a class="toc-reader" href="reader.html">▤ 六份认信 · 原文书房 ↗</a><p class="tiny">2026.10.22 · v1.0.0<br>欧陆改革宗学习版</p></aside><button class="toc-backdrop" id="tocBackdrop" aria-label="关闭目录"></button>'

hero='''<section class="hero" id="top"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> CONTINENTAL REFORMED · 欧陆改革宗</p><p class="hero-kicker">《比利时信条》全景深读</p><h1>在逼迫中，<br>承认<span>盼望。</span></h1><p class="hero-desc">从整本圣经的故事，走进37条认信。<br>看见三一神的恩典，读懂教会为何如此相信。</p><div class="hero-actions"><a class="button primary" href="#overview">开始全景阅读 <span>↓</span></a><a class="button ghost" href="reader.html?doc=belgic">阅读信条原文 ↗</a></div><div class="hero-meta"><span><b>37</b>条逐一解析</span><span><b>6</b>份认信全文</span><span><b>1</b>位救恩中保</span></div></div><figure class="hero-art"><svg viewBox="0 0 520 520" role="img" aria-label="原创教学插画：书卷、城楼与认信之光，并非历史手稿复原"><defs><linearGradient id="bookg" x2="1" y2="1"><stop stop-color="#234c43"/><stop offset="1" stop-color="#142f29"/></linearGradient><pattern id="grid" width="38" height="38" patternUnits="userSpaceOnUse"><path d="M38 0H0V38" fill="none" stroke="#b9ba9d" stroke-opacity=".18"/></pattern></defs><rect width="520" height="520" rx="180" fill="url(#grid)"/><circle cx="280" cy="236" r="175" fill="none" stroke="#aa8c50" stroke-opacity=".35"/><circle cx="280" cy="236" r="143" fill="none" stroke="#aa8c50" stroke-opacity=".2"/><path d="M110 357V238h25v-29h22v-37l15-18 15 18v37h23v29h32v119M340 357V210h22v-39h19v-58l13-18 13 18v58h19v39h24v147" fill="none" stroke="#908c70" stroke-width="1.4" opacity=".45"/><g transform="rotate(-9 260 275)"><rect x="135" y="118" width="256" height="344" rx="9" fill="#0b211c" opacity=".13" transform="translate(12 14)"/><path d="M135 131Q135 118 148 118H389V451H148Q135 451 135 438Z" fill="#d8c7a0"/><path d="M133 123Q133 111 147 111H387V439H147Q133 439 133 426Z" fill="url(#bookg)"/><path d="M151 111V439" stroke="#ac8b52" opacity=".6"/><rect x="170" y="141" width="188" height="263" rx="2" fill="none" stroke="#c1a56d" opacity=".65"/><path d="M261 172V212M245 187H277" stroke="#c1a56d" stroke-width="2"/><text x="265" y="248" text-anchor="middle" fill="#e8ddbd" font-size="18" letter-spacing="4">CONFESSIO</text><text x="265" y="280" text-anchor="middle" fill="#e8ddbd" font-size="27" letter-spacing="5">BELGICA</text><path d="M211 302H319" stroke="#c1a56d" opacity=".6"/><text x="265" y="342" text-anchor="middle" fill="#cbb884" font-family="Georgia,serif" font-size="23" letter-spacing="8">1561</text><text x="265" y="379" text-anchor="middle" fill="#cbb884" font-size="10" letter-spacing="3">WE BELIEVE &amp; CONFESS</text></g><circle cx="424" cy="380" r="42" fill="#ede6d4" stroke="#bba26e"/><text x="424" y="388" text-anchor="middle" font-family="Georgia,serif" font-size="25" fill="#6c5631">37</text><path class="art-spark" d="M102 130V154M90 142H114" stroke="#a58b50" stroke-width="2"/></svg><figcaption>原创教学插画 · 非历史手稿复原</figcaption></figure></section>'''

body=head('比利时信条37条全景深读 · GTstudy')+topbar()+toc+'<main id="main">'+hero
body+='<div class="reader-note"><span>✧ 阅读原则</span><p><strong>圣经是最高规范。</strong>以下深读为原创教学释义；金色原文区采用指定网站中文译文。经文章节仅作索引，请连同上下文阅读。保存的进度与笔记仅留在当前浏览器。</p></div>'
body+=section('overview','01','先看整本圣经，再读每一条。','把教义放回创造、堕落、应许、成全与新创造的完整故事。')
body+='<div class="overview-grid">'
for o in overview['overview']: body+=f'<article class="overview-card"><span class="card-icon">{o["icon"]}</span><h3>{e(o["title"])}</h3><p>{e(o["text"])}</p><p class="refs">▱ {e(o["refs"])}</p></article>'
body+='</div><div class="flow" aria-label="救赎历史流程图">'
for i,(t,s) in enumerate([('创造','神赐生命与使命'),('堕落','罪与死进入世界'),('应许','神主动寻找罪人'),('成全','基督受死并复活'),('招聚','圣灵藉道建立教会'),('新创造','复活、审判与同住')]): body+=f'<div><span>0{i+1}</span><strong>{t}</strong><small>{s}</small></div>'
body+='</div><div class="callout green"><h3>一句抓住核心</h3><p>三一神以祂可信的话显明自己，在基督里拯救失丧的人，藉圣灵招聚教会，使祂的子民在真实世界中敬虔生活，直到祂更新万有。</p></div></section>'
body+=section('history','02','一份信条，写在真实的压力之下。','不是抽象的教义清单，而是受逼迫教会向神、向统治者、向世界发出的公共见证。')
body+='<div class="history-intro"><article><h3>为什么写？</h3><p>16世纪的低地地区处于哈布斯堡统治之下，宗教认信与政治忠诚紧密交织。改革宗信徒受到镇压，也常被与叛乱或激进运动相混同。德布利的回答不是先主张一个不受约束的私人宗教空间，而是公开说明：我们所信是圣经的福音，所敬拜是古代教会承认的三一神；我们愿意履行公民责任，却不能把良心交给违背神话语的命令。</p><p>信条因而有双重方向：对外澄清指控，对内建立教会。第1—11条把改革宗接回大公信仰；第22—26条澄清救恩；第27—35条说明教会生活；第36—37条把地上的顺服放在天上的审判之下。</p></article><aside class="callout amber"><h3>地名先辨清</h3><p><strong>Belgic ≠ 现代比利时国家。</strong>它指向当时的低地地区，跨越今日荷兰、比利时及法国北部等现代边界。信条起初以法文写成，随后进入荷兰语世界；这是一份跨语言、跨城市传播的认信。</p><p>故事性描述以已核查史实为限；下列内容没有虚构德布利的现场对白或心理活动。</p></aside></div>'
body+='<div class="timeline">'
for t in overview['timeline']: body+=f'<article class="timeline-item"><div class="timeline-date">{e(t["year"])}</div><div><p class="eyebrow">⌖ {e(t["place"])}</p><h3>{e(t["title"])}</h3><p>{e(t["text"])}</p></div></article>'
body+='</div><p class="refs">历史依据：'+anchor('https://threeforms.org/introduction-to-the-creeds-and-confessions/','URCNA 官方介绍')+' · '+anchor('https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession','CCI 导言')+' · 详细来源见文末。</p>'
body+='<div class="map-layout"><div class="map-panel"><div class="map-caption"><span class="eyebrow">GEOGRAPHY OF CONFESSION</span><h3>跨越语言的认信网络</h3><p>经纬度定位示意 · 非1561年疆界图 · 连线不代表精确旅行路线</p></div><svg class="geo-map" viewBox="0 0 700 600" role="img" aria-labelledby="maptitle mapdesc"><title id="maptitle">改革宗认信相关的六座城市</title><desc id="mapdesc">图尔奈、瓦朗谢讷、安特卫普、多德雷赫特、海德堡、日内瓦按经纬度相对定位。非历史疆界图，城市详情也可通过下方按钮阅读。</desc><defs><pattern id="mapgrid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="currentColor" opacity=".12"/></pattern></defs><rect x="25" y="10" width="650" height="565" rx="12" fill="url(#mapgrid)"/><text x="38" y="40" class="map-small">北 N ↑</text><text x="580" y="560" class="map-small">东 E →</text>'
def xy(c): return (80+(c['lon']-2.5)*79,60+(52.3-c['lat'])*73)
body+='<defs><clipPath id="geoClip"><rect x="25" y="10" width="650" height="565" rx="12"/></clipPath></defs><g clip-path="url(#geoClip)" class="country-shapes">'
for feature in load('research/geography.json')['features']:
 geometry=feature['geometry']
 polygons=geometry['coordinates'] if geometry['type']=='MultiPolygon' else [geometry['coordinates']]
 for polygon in polygons:
  parts=[]
  for ring in polygon:
   pts=[xy({'lon':coord[0],'lat':coord[1]}) for coord in ring]
   parts.append('M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'Z')
  body+=f'<path d="{"".join(parts)}" fill-rule="evenodd"><title>{e(feature["name"])} · 现代参照轮廓</title></path>'
body+='</g><g class="country-labels"><text x="112" y="425">法国 · 现代参照</text><text x="450" y="125">德国</text><text x="298" y="70">荷兰</text><text x="287" y="215">比利时</text><text x="480" y="512">瑞士</text></g>'
citydict={c['id']:c for c in overview['cities']}
for aa,bb in [('geneva','tournai'),('tournai','valenciennes'),('tournai','antwerp'),('antwerp','dordrecht'),('heidelberg','dordrecht')]:
 x,y=xy(citydict[aa]);xx,yy=xy(citydict[bb]);body+=f'<path class="map-route" d="M{x},{y}L{xx},{yy}"/>'
offsets={'tournai':(-16,-18),'valenciennes':(16,26),'antwerp':(20,14),'dordrecht':(18,-15),'heidelberg':(-90,-18),'geneva':(18,12)}
for c in overview['cities']:
 x,y=xy(c);dx,dy=offsets[c['id']];body+=f'<circle cx="{x}" cy="{y}" r="7" class="map-point"/><text x="{x+dx}" y="{y+dy}" class="map-label">{e(c["name"])}</text><text x="{x+dx}" y="{y+dy+17}" class="map-small">{c["lat"]:.2f}°N · {c["lon"]:.2f}°E</text>'
body+='</svg><p class="refs">底图：Natural Earth 1:110m，公有领域。轮廓仅作现代地理参照。</p></div><div class="map-detail"><p class="eyebrow">选择城市 · 阅读真实背景</p><div class="city-buttons">'
for i,c in enumerate(overview['cities']): body+=f'<button class="city-btn {"active" if i==0 else ""}" type="button" data-city="{c["id"]}" aria-pressed="{"true" if i==0 else "false"}">{e(c["name"])}</button>'
body+='</div>'
for i,c in enumerate(overview['cities']): body+=f'<article class="city-detail" id="city-{c["id"]}" {"hidden" if i else ""}><p class="eyebrow">{e(c["en"])}</p><h3>{e(c["role"])}</h3><p>{e(c["text"])}</p><p class="refs">{c["lat"]}°N · {c["lon"]}°E</p></article>'
body+='<div class="culture"><h4>区域文化的三把钥匙</h4><p><b>语言：</b>法语南部与荷兰语北部的传播，需要翻译与共同教义。</p><p><b>城市：</b>商业、印刷与流亡者网络，加速文本与教师的跨境流动。</p><p><b>权力：</b>领地、君王与教会的关系，使认信同时面对良心和公共秩序。</p></div></div></div></section>'
body+=section('covenant','03','同一恩典，真实展开的历史。','圣约神学不是给信条另加一层密码，而是把它的教义重新接回神信实的应许。')
body+='<div class="table-wrap" tabindex="0" role="region" aria-label="圣约与信条对照表，可横向滚动"><table><thead><tr><th>历史阶段</th><th>应许与安排</th><th>怎样指向基督</th><th>信条关联与辨析</th></tr></thead><tbody>'
for c in overview['covenants']: body+=f'<tr><th>{e(c["name"])}<small>{e(c["ref"])}</small></th><td>{e(c["promise"])}</td><td>{e(c["christ"])}</td><td><b>第{e(c["articles"])}条</b><p>{e(c["caution"])}</p></td></tr>'
body+='</tbody></table></div><div class="two-col"><div class="callout green"><h3>约、拣选与教会：相关，却不能混为一词</h3><p>拣选显明救恩终极根源在神；圣约说明神以应许、命令和记号与百姓相交的历史施行；教会是基督藉道与灵招聚的群体。第16条不能取消第28条加入教会的责任，第34条也不能取代第22条的信心。外在领受记号与内在领受基督不可机械等同。</p></div><div class="callout rose"><h3>同宗传统，也有需要交代的差异</h3><p>CanRC、URCNA、Heritage Reformed与PRCA同属广义欧陆改革宗认信传统，但对圣约、应许向谁陈明、普遍恩惠等议题并非所有表述一致。本学习版以三项联合信条共有的教义为骨架，不把某一联会的全部解释提升为全体唯一标准。威斯敏斯特传统可作互证，不能取代本次指定认信。</p></div></div>'
body+='<div class="mindmap"><div class="mind-root">三一神的救赎恩典</div><div class="mind-branches"><div><b>根源 · 父的拣选</b><span>非因预见功劳<br>第16条</span></div><div><b>成就 · 子的中保</b><span>真神真人，代赎与代求<br>第18—26条</span></div><div><b>施行 · 灵与圣道</b><span>信心、更新与圣礼<br>第22—24、33—35条</span></div><div><b>群体 · 圣约生活</b><span>教会、家庭、公共责任<br>第27—36条</span></div><div><b>终局 · 更新万有</b><span>身体复活、公义显明<br>第37条</span></div></div></div></section>'
body+=section('articles','04','37条，从承认神到盼望再来。','每条依次看本质、因果、经文、圣约、历史、误区与应用。释义默认完整铺开；原文另设金色阅读区。')
body+='<div class="article-tools"><label class="search-label"><span>⌕</span><input type="search" id="articleSearch" placeholder="搜索37条：如 称义、婴洗、护理…" aria-label="搜索37条解读"></label><label>主题 <select id="groupFilter"><option value="">全部37条</option>'
for lo,hi,title,key in GROUPS:body+=f'<option value="{key}">{lo}—{hi} · {title}</option>'
body+='</select></label><button id="showOriginals" type="button">展开全部原文</button><button id="resetSearch" type="button">重置筛选</button></div><p id="searchCount" role="status" class="muted">显示全部37条</p><div class="group-links">'
for lo,hi,title,key in GROUPS: body+=f'<a href="#article-{lo}"><b>{lo:02d}—{hi:02d}</b> {title}</a>'
body+='</div><div id="articleList">'
fields=[('logic','因果与结构','◈'),('biblical','放回整本圣经','▱'),('covenant','圣约视角 · 解释联结','⌘'),('context','真实情境与写作针对','⌖'),('error','难点与误区','!'),('application','进入今天的生活','↗')]
for a in articles:
 n=a['n'];src=docs['belgic']['sections'][n-1];g=group(n)
 body+=f'<article class="article-card" id="article-{n}" data-n="{n}" data-group="{g[3]}"><header class="article-heading"><span class="article-number">{n:02d}</span><div><p class="eyebrow">{e(g[2])} · 原创教学释义</p><h3>{e(a["title"])}</h3></div><button class="mark-done" type="button" data-n="{n}" aria-pressed="false" aria-label="标记第{n}条已学">✓ 已学</button></header><div class="core"><span>本质核心</span><p>{e(a["core"])}</p></div><div class="article-grid">'
 for key,title,icon in fields: body+=f'<section class="analysis-field {key}"><h4><span>{icon}</span> {title}</h4><p>{e(a[key])}</p></section>'
 refs=a['refs'];refstr='；'.join(refs) if isinstance(refs,list) else refs
 related=a['related'];relatedstr='；'.join(related) if isinstance(related,list) else related
 body+=f'</div><div class="article-cross"><p><b>经文研读</b> {e(refstr)}</p><p><b>认信互证</b> {e(relatedstr)}</p></div><div class="memory-strip"><span>✧ 记忆钩子</span><strong>{e(a["memory"])}</strong></div><details class="original"><summary>▤ 展开第{n}条原文 · CCI中文译文</summary><div class="source-caption">{anchor(src["source"],"指定网站原文")}<span>正文、段号与脚注均独立于上方释义</span></div><div class="original-text" data-original="belgic-{n}">{src["html"]}</div></details><details class="notes"><summary>✎ 我的研读笔记 · 仅存本机</summary><label for="note-{n}">第{n}条：我理解了什么？还有什么问题？</label><textarea id="note-{n}" data-note="{n}" rows="3" placeholder="写下自己的理解与下一步查考…"></textarea></details></article>'
body+='</div><p id="noResults" hidden class="callout amber">没有匹配条目。请换一个关键词，或点“重置筛选”。</p></section>'
body+=section('compare','05','为什么是三份，而不是一份？','一份给出整体认信，一份把真理教进生活，一份在争论处守护恩典。它们相互补足，不构成三种福音。')
body+='''<div class="compare-trio"><article><span class="eyebrow">1561 · CONFESSION</span><h3>比利时信条</h3><b>我们信什么？</b><p>面对逼迫与误解，37条有次序地陈明神、启示、人、基督、救恩、教会与终局。</p><span class="chip">整体认信 · 公共见证</span></article><article><span class="eyebrow">1563 · CATECHISM</span><h3>海德堡要理问答</h3><b>这信仰怎样成为我的安慰？</b><p>以129问、52主日，把罪苦、救赎、感恩带进讲台、家庭与学校。</p><span class="chip">牧养教导 · 敬虔塑造</span></article><article><span class="eyebrow">1618—1619 · CANONS</span><h3>多特信经</h3><b>救恩为什么完全出于恩典？</b><p>围绕救恩论争议，五项教义分四个主体单元陈明，并逐项驳谬。</p><span class="chip">争议澄清 · 确据与坚忍</span></article></div><div class="table-wrap" tabindex="0" role="region" aria-label="三项联合信条深度比较"><table><thead><tr><th>比较角度</th><th>比利时信条</th><th>海德堡要理问答</th><th>多特信经</th></tr></thead><tbody>
<tr><th>触发的问题</th><td>信徒被指控为错误宗教与政治叛乱者；教会需要公开身份。</td><td>领地教会、学校和青年需要共同的福音教导。</td><td>抗辩派争议使拣选、救赎、归正与坚忍的教导受挑战。</td></tr>
<tr><th>文体与听众</th><td>我们相信的连续告白；面向教会与外部社会。</td><td>问与答；以你、我、我们塑造个人与共同体认信。</td><td>正面教义与驳谬；为教会判断争论提供边界。</td></tr>
<tr><th>救恩根源</th><td>第16条强调神在基督里的恩慈拣选。</td><td>第54问把被拣选的教会与圣子招聚相连。</td><td>第一项细分拣选、弃绝、确据及牧养处理。</td></tr>
<tr><th>称义与善行</th><td>第22—24条区分信心领受、基督的义与更新果子。</td><td>第60—64问说明白白称义，第86问说明善行的感恩目的。</td><td>第三／四项说明更新的根源；第五项说明神怎样保守信徒。</td></tr>
<tr><th>教会与圣礼</th><td>第27—35条有完整的教会、职分、纪律与圣礼论。</td><td>第54—55、65—85问用于教导与实际操练。</td><td>不是全面教会论；强调福音宣讲与蒙恩途径，不取代其他两份。</td></tr>
<tr><th>圣约关联</th><td>第17、25、34条是应许、成全与儿女记号的重要连接。</td><td>第74问清楚把婴孩与圣约、教会及应许联系。</td><td>第二项第8条涉及以基督的血成就新约；第一项第17条牧养敬虔父母。</td></tr>
<tr><th>若只剩这一份</th><td>有整体轮廓，却少了问答的渐进训练和多特对争论的细辨。</td><td>有深厚安慰，却少了同等篇幅的公共告白与争议裁断。</td><td>会把改革宗压缩成救恩五点，遗漏启示、三一、圣礼等整体。</td></tr>
</tbody></table></div><div class="callout green"><h3>三份文件为何能联合？</h3><p>联合不是把三份文字相加形成新启示，而是在同一圣经真理上共同签署、教导和接受检验。重复使关键福音在不同场景中再次发声；不同文体则让整体、个人和争论各得其所。合理比较不是强求每一份都回答所有问题，而是看它在当时被托付回答什么。</p></div><div class="two-col"><article class="callout amber"><h3>多特不等于五句口号</h3><p>TULIP是后来的英语记忆法，不是1618—1619年文件的原有顺序。多特第三、第四项合并，且包含驳谬。抗辩派也不能被简化成毫不承认罪与恩典；真正争点涉及拣选根据、救赎目的、恩典效力与坚忍。阅读须到具体条款。</p></article><article class="callout rose"><h3>与威斯敏斯特怎样互证？</h3><p>两传统共同承认三一、圣经权威、唯独因信称义、恩约与婴洗。威斯敏斯特信仰告白第7章更集中使用约的体系表达，第25—29章展开教会与圣礼；比利时则以不同结构承载相近真理。它们具有各自历史、用语和教会接纳范围，不可逐句视为同一文件。本页未混入其译文充当CCI原文。</p></article></div></section>'''
body+=section('creeds','06','三大普世信经，守护同一位救主。','三项联合信条承接大公教会的三一论与基督论。普世在此表达大公信仰的接续，不表示所有历史教会接纳程度完全相同。')
body+='''<div class="compare-trio"><article><span class="card-icon">Ⅰ</span><h3>使徒信经</h3><p>以父、子、灵为骨架，以基督降卑和升高为故事线。用于洗礼教导与教会共同宣认。</p><p class="refs">不是使徒集体亲笔；现行文本逐步形成。</p><a class="button" href="reader.html?doc=apostles">干净版 · 阅读与背诵 ↗</a></article><article><span class="card-icon">Ⅱ</span><h3>尼西亚信经</h3><p>说明子受生而非被造、与父同质，也承认圣灵的神性；捍卫能真正施救的主。</p><p class="refs">区分325、381与西方和子的后续历史。</p><a class="button" href="reader.html?doc=nicene">干净版 · 阅读与背诵 ↗</a></article><article><span class="card-icon">Ⅲ</span><h3>亚他那修信经</h3><p>本质不分，位格不混；基督一位而有神人二性。精密的用语服事正确的敬拜与救恩。</p><p class="refs">作者不详；CCI正文为42点，勿套用其他分节。</p><a class="button" href="reader.html?doc=athanasian">干净版 · 阅读与背诵 ↗</a></article></div><div class="two-col"><div class="callout green"><h3>为何古代的神学边界仍然重要？</h3><p>若子只是最高的受造物，我们并没有神亲自来救；若基督没有完整人性，祂就没有担当我们真实的人性；若把父子灵混成一个角色，就抹去父差子、子顺服、圣灵施行救恩的真实关系。三一与二性不是可略过的术语，而是福音之所以成立的根基。比利时第8—11、18—19条就在这条大公认信线上。</p></div><div class="callout amber"><h3>三个容易误读的句子</h3><p><b>降在阴间：</b>按海德堡第44问，从基督为我们承受可怕痛苦理解，勿凭此另造死后第二次受苦的故事。</p><p><b>从父和子而出：</b>本页忠实保留指定西方文本；不把西方后加的用语称作381年会议原句。</p><p><b>行善者得永生：</b>按比利时第22—24、37条看审判中显出的信心果子，不能改读成善行购买称义。</p></div></div></section>'''
body+=section('memory','07','先记住骨架，再长出细节。','记忆不是只背口号，而是能用自己的话说出：是什么、为什么、经文在哪里、怎样生活。')
body+='<div class="memory-overview"><div class="callout green"><h3>六站记忆路径</h3><p class="memory-large">启示 → 三一 → 恩典 → 基督 → 教会 → 盼望</p><p>1—7话语可靠；8—13神是谁、怎样掌管；14—17人失落、神寻找；18—26基督成就并赐新生命；27—35聚成教会、道与圣礼；36—37地上尽责、盼望审判。</p></div><div class="callout amber"><h3>1 · 3 · 7 · 14天复习</h3><p>第1天：读原文，说一句核心。第3天：遮住答案，回忆经文与误区。第7天：把相邻两条连起来讲。第14天：向别人解释一个实际问题，再回原文校正。以下进度只说明自己标记的学习情况，不代表掌握程度测验。</p><p><b id="learnedCount">0 / 37 条已标记</b></p><progress id="learnedProgress" value="0" max="37" aria-label="已学条目进度"></progress></div></div><div class="flashcard"><p class="eyebrow">ACTIVE RECALL · 37条回忆卡</p><p id="flashIndex" class="muted">第1条 / 共37条</p><h3 id="flashQuestion"></h3><div id="flashAnswer" hidden></div><div class="toolbar"><button type="button" id="flashPrev">← 上一条</button><button type="button" class="primary" id="flashReveal" aria-expanded="false">显示核心与记忆句</button><button type="button" id="flashNext">下一条 →</button><button type="button" id="flashRandom">⤨ 随机</button></div></div><div class="quiz-panel"><h3>理解自测 · 选择后看解释</h3><div id="quiz"></div></div><div class="callout green"><h3>把四组区别记清</h3><div class="distinctions"><p><b>本质／位格</b><br>神是什么／谁是神<br>一体三位：第8—11条</p><p><b>称义／成圣</b><br>法庭地位／生命更新<br>有区别、不分离：第22—24条</p><p><b>记号／实在</b><br>水饼酒／基督与祂的恩惠<br>相关、不混同：第33—35条</p><p><b>政权／基督国度</b><br>公共秩序／终极救恩主权<br>顺服有界限：第36—37条</p></div></div><div class="toolbar"><button type="button" id="exportNotes">↓ 导出学习笔记与进度</button><label class="button import-label">↑ 导入备份<input id="importNotes" type="file" accept="application/json,.json"></label><span id="saveStatus" role="status" class="muted"></span></div></section>'
body+=section('sources','08','每一次深读，都能回到来源。','文本、解释与历史各有来源层级。原文基线：2026年10月21日；本版发布：10月22日。已核查指定文本与相关主题资料，未穷尽全站。')
body+='''<div class="callout amber"><h3>版本与原文完整性的边界</h3><p>① 原文均来自ccifellowship.org《敬拜手册》中文译文：三大信经、比利时37条、海德堡129问、多特59条正面教义及四组驳谬。全部收在原文书房。多特的独立结语未见于指定版本，因此没有用其他译文补入。</p><p>② 用户提供的245页PDF与网页主体同属2015版体系，但并非每个字都相同；网页原文不由PDF排字覆盖。PDF仅作为参考输入，不将整本PDF上传发布。</p><p>③ 网站正文的用字、标点、段号、脚注保留；允许屏幕换行与段落布局变化。原站疑似排字不静默修正。亚他那修引言所述条号与正文实际42点不完全吻合，教学编号遵循实际正文。</p><p>④ 第36条的1905年删文说明是版本史的一部分，不是现代所有联会一致采用同一改文的证明。原文忠实保存，历史解释另列。</p><p>⑤ 232个原文单元与10月21日成功核验记录的摘要相符；本次批量访问全部连接超时，不能确认原站此刻有无后续改动。详见下面两份独立记录。</p><p>⑥ 本站的圣约联结、记忆句、图表、比较与问题均为原创教学内容，不能引作任何信条的逐字原文。</p><p><a href="source-report.html">查看155个来源、232个正文单元的基线与本次访问记录 ↗</a></p></div><div class="source-list">'''
for i,s in enumerate(overview['sources'],1): body+=f'<article><span>{i:02d}</span><div><h3>{anchor(s["url"],s["title"])}</h3><p>{e(s["use"])}</p></div></article>'
body+='</div><details class="extension"><summary>更多研究入口 · 按传统与用途选择</summary><p>下列为继续查考入口，并不表示已逐篇核读或赞同全部文章；教会和神学院资料须按具体作者、文体与证据审查。</p><div class="resource-links">'
for name,url in [('恩约教会','https://www.ccreformed.org/'),('改革宗初学者','https://www.reformedbeginner.net/'),('CanRC','https://canrc.org/'),('URCNA','https://www.urcna.org/'),('Heritage Reformed','https://heritagereformed.com/'),('PRCA','https://www.prca.org/'),('OPC · 长老会改革宗','https://opc.org/'),('Canadian Reformed Seminary','https://canadianreformedseminary.ca/'),('Westminster Seminary','https://www.wts.edu/'),('CRTS','https://crts.edu/')]: body+=anchor(url,name)
body+='</div></details></section><footer><div><span class="brandmark">✦</span><b> GTstudy · 比利时信条</b><p>让认信回到圣经，让理解进入生活。</p></div><div><p>belgic-confession-20261021-v1-GTstudy</p><p>v1.0.0 · 2026.10.22 · Asia/Taipei</p><a href="reader.html">六份认信原文书房 ↗</a></div></footer></main><a href="#top" class="backtop" aria-label="回到顶部">↑</a><script type="application/json" id="flashData">'+json.dumps([dict(n=a['n'],title=a['title'],core=a['core'],memory=a['memory']) for a in articles],ensure_ascii=False).replace('</','<\/')+'</script></body></html>'
(OUT/'index.html').write_text(body,encoding='utf8')

# All six complete documents are statically present, without remote dependencies.
reader=head('原文书房 · 六份认信 · GTstudy')+topbar(True)+'''<main id="main" class="reader-main"><div class="reader-intro"><p class="eyebrow">THE CONFESSIONAL LIBRARY</p><h1>原文书房</h1><p>安静地读，准确地记。三份普世信经与三项联合信条，均为指定网站中文译文。</p></div><div class="reader-controls"><label>阅读文本 <select id="docSelect">'''
for d in originals['documents']: reader+=f'<option value="{d["key"]}">{e(d["title"])}</option>'
reader+='''</select></label><button type="button" id="readerMask" aria-pressed="false">遮盖正文 · 背诵</button><button type="button" id="readerCopy">复制当前全文</button><button type="button" id="readerSpeak">▷ 朗读当前全文</button><button type="button" id="readerStop">□ 停止</button><button type="button" id="readerPrint">打印干净版</button><span id="readerStatus" role="status"></span></div><p class="reader-version">原文层：不混入本站释义、不自动繁简转换、不静默修订原站文字。遮盖后可点击或用键盘揭开单节。朗读使用设备语音，音色与可用性因设备而异。</p>'''
for d in originals['documents']:
 reader+=f'<article class="document" id="doc-{d["key"]}" data-doc="{d["key"]}"><div class="document-header"><p class="eyebrow">CCI · BOOK OF PRAISE · 2015</p><h2>{e(d["title"])}</h2><p>{anchor(d["source"],"指定网站目录／原文")}</p></div>'
 if len(d['sections'])>1:
  reader+='<details class="reader-index"><summary>显示本文详细目录</summary><nav>'
  for i,s in enumerate(d['sections'],1): reader+=f'<a href="#reader-{d["key"]}-{i}">{e(s["title"])}</a>'
  reader+='</nav></details>'
 if d['key']=='dort': reader+='<p class="reader-version">版本说明：包括全部59条正面教义和四组驳谬。指定版本未收独立结语；不以其他译本补写。</p>'
 currentgroup=''
 for i,s in enumerate(d['sections'],1):
  if s.get('group') and s['group']!=currentgroup:
   currentgroup=s['group'];reader+=f'<h3 class="reader-group">{e(currentgroup)}</h3>'
  reader+=f'<section class="reader-section" id="reader-{d["key"]}-{i}">'
  if len(d['sections'])>1: reader+=f'<h3>{e(s["title"])}</h3>'
  reader+=f'<div class="reader-passage" tabindex="0" role="button" aria-label="{e(s["title"])}，背诵模式下按回车显示或遮盖正文"><div class="original-text" data-original="{d["key"]}-{i}">{s["html"]}</div><span class="mask-prompt" aria-hidden="true">点击或按回车揭开此节</span></div><a class="passage-source" href="{e(s["source"])}" target="_blank" rel="noopener noreferrer">来源 ↗</a></section>'
 reader+='</article>'
reader+='<footer><p>指定中文译文 ©《中国改革宗敬拜手册》出版委员会，2015。资料来源：ccifellowship.org。</p><p>学习版 v1.0.0 · 2026.10.22 · <a href="index.html#sources">版本与来源说明</a></p></footer></main><script type="application/json" id="originalData">'+json.dumps(originals,ensure_ascii=False).replace('</','<\/')+'</script></body></html>'
(OUT/'reader.html').write_text(reader,encoding='utf8')
(OUT/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#204c40"/><text x="32" y="45" text-anchor="middle" fill="#e8dab5" font-size="43">✦</text></svg>',encoding='utf8')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.suffix in ('.html','.css','.js','.json','.svg') and p.name!='manifest.json'}
(OUT/'manifest.json').write_text(json.dumps({'version':'1.0.0','date':'2026-10-22','files':manifest},indent=2),encoding='utf8')
print(f'Built {len(articles)} commentary articles; {sum(len(d["sections"]) for d in originals["documents"])} original sections.')

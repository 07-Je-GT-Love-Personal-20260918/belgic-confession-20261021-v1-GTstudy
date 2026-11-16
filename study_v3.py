from study_v2 import E,icon,enhance_page

VERSION='3.0.0'
DATE='2026-11-14'

STEPS=[
 ('325 / 381','地中海东部','谁是救我们的主？','尼西亚与君士坦丁堡的教义争议推动教会澄清子与圣灵的神性。','同受敬拜，意味着同有神性。','cross'),
 ('1561','图尔奈','受逼迫，为何还要公开？','法语改革宗群体用可检验的告白，区分信仰归属与政治叛乱。','良心归神，公民责任仍在。','scroll'),
 ('1563','海德堡','会签署，也会教导吗？','普法尔茨的讲台、学校与家庭需要可以复习、可以问答的共同教材。','罪苦 → 救赎 → 感恩','book'),
 ('1566 / 1567','安特卫普与瓦朗谢讷','传播之后，谁来承担？','安特卫普修订接纳信条；德布利随后在瓦朗谢讷殉道。两事分属不同城市与年份。','教会承担见证，基督拥有终审。','press'),
 ('1618—1619','多德雷赫特','争议怎样得到教会回答？','多特大会处理救恩争议，并审订比利时信条；三项联合信条由此得到共同使用。','全面告白 · 牧养教导 · 争议澄清','people'),
]

ROWS=[
 ('初始任务','洗礼与教导：让人按父、子、灵的次序承认福音。','教会会议：排除把子归入受造界的读法，展开圣灵的地位。','拉丁西方的教义辨析：分别解释三一与道成肉身。'),
 ('三一的重心','三重认信结构把创造、救赎与教会生活连起来。','从创造与敬拜辨认子的神性；圣灵与父、子同受敬拜。','一个神性、三个位格；不能混淆位格，也不能分割本质。'),
 ('基督的重心','按降生、受难、复活、升天、再来追踪救赎事件。','说明降世救我们的那一位与父同质。','同一位子兼有完整神性和完整人性；二性不混乱，位格不分裂。'),
 ('教会与终局','圣徒相通、赦罪、身体复活与永生。','教会的四重特征、洗礼、复活与更新的世界。','普遍复活、审判与终局；行为显出信仰的实际果效。'),
 ('各自的限度','适合背诵，但没有展开永恒受生或二性联合的精细边界。','适合辨明神性，却未详细说明同一基督如何兼具二性。','辨析细密，不能替代简明的洗礼教导和救赎故事。'),
]




def story():
 p='<section id="story" class="atlas-section v3-story"><p class="eyebrow">ATLAS STUDIO · 五幕讲解</p><h2>从共同敬拜，到共同教导</h2><p>五幕是一条教义传承线，不是人物旅行路线。</p><div class="story-layout"><ol class="story-line">'
 for i,(year,city,title,history,memory,ico) in enumerate(STEPS,1):
  p+=f'<li><details {"open" if i==1 else ""} name="story-chapters" id="story-{i}"><summary>{icon(ico)}<b>{E(year)}</b> {E(city)}</summary><h3>{E(title)}</h3><p data-note-block="story-{i}">{E(history)}</p><strong>{E(memory)}</strong></details></li>'
 return p+'''</ol><figure class="story-screen"><video controls playsinline preload="none" poster="story-poster.webp" width="960" height="540" aria-label="五幕认信故事：无声字幕短片"><source src="confession-story.mp4" type="video/mp4"></video><figcaption>30秒无声图解 · 逐幕字幕已印入画面 · 左侧是可展开的文字稿</figcaption></figure></div></section>'''


def offline_map(cities):
 p='<div class="offline-atlas" aria-label="两张可离线阅读的地理示意图">'
 for ancient,title,water in [(False,'低地与莱茵河流域','北海'),(True,'意大利与博斯普鲁斯海峡','地中海')]:
  data=[c for c in cities if (c['group']=='ancient')==ancient]
  w,s,e,n=(6,36,34,46) if ancient else (0,45,10,54)
  labels={'tournai':(-10,-21,'end'),'valenciennes':(-8,26,'end'),'antwerp':(15,25,'start'),'dordrecht':(13,-13,'start'),'constantinople':(-15,-18,'end'),'nicaea':(12,26,'start'),'heidelberg':(-12,-15,'end')}
  svg=f'<svg viewBox="0 0 560 320" role="img" aria-label="{title}城市经纬度定位，非历史疆界"><rect width="560" height="320" rx="25" fill="var(--v3-sea)"/><path d="M55 65H515M55 130H515M55 195H515M55 260H515M105 45V280M220 45V280M335 45V280M450 45V280" stroke="currentColor" stroke-opacity=".13"/><text x="24" y="32" class="chart-caption">{water}区域 · 北 ↑</text>'
  for c in data:
   x=55+455*(c['lon']-w)/(e-w); y=45+220*(n-c['lat'])/(n-s); dx,dy,align=labels.get(c['id'],(0,24,'middle'))
   svg+=f'<g class="offline-pin"><circle cx="{x:.1f}" cy="{y:.1f}" r="13" opacity=".16"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5"/><text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{align}">{E(c["name"])}</text></g>'
  p+=f'<figure><h3>{title}</h3>{svg}</svg><figcaption>以经纬度定位；背景格线为示意，不绘制历史疆界。</figcaption></figure>'
 return p+'</div>'


def creed_page(head,topbar,cities,docs):
 keys=['apostles','nicene','athanasian']; labels=[next(d['title'] for d in docs if d['key']==k) for k in keys]
 p=head('三经对读 · GTstudy')+topbar(True)+'''<main id="main" class="atlas-main creed-lab"><section class="atlas-section" id="top"><p class="eyebrow">CREED STUDIO · 三经对读</p><h1>记故事，辨身份，守边界。</h1><p>三经共享同一信仰骨架：父创造，子成就救赎，圣灵施行救恩；神召聚教会，使死人复活。每一份信经回答的首要问题不同。</p><details class="reader-index"><summary>展开对读目录</summary><nav><a href="#clean">三经干净版</a><a href="#matrix">五维比较</a><a href="#theology">圣经与圣约</a><a href="#review">主动回忆</a></nav></details></section><section class="atlas-section" id="clean"><h2>选一份，直接读原文</h2><div class="creed-launch">'''
 for i,(k,label) in enumerate(zip(keys,labels)):
  p+=f'<a class="creed-tile tone-{i}" href="{"reader.html" if i==0 else "reader-"+k+".html"}">{icon(["book","cross","shield"][i])}<strong>{E(label)}</strong><span>干净版 · 遮盖背诵 ↗</span></a>'
 p+='</div></section><section class="atlas-section" id="matrix"><h2>一套信仰，三种教会任务</h2><div class="creed-matrix">'
 for i,(topic,*cells) in enumerate(ROWS):
  p+=f'<section><h3>{E(topic)}</h3><dl>'+''.join(f'<div class="tone-{j}"><dt>{E(labels[j])}</dt><dd data-note-block="creed-matrix-{i}-{j}">{E(c)}</dd></div>' for j,c in enumerate(cells))+'</dl></section>'
 p+='''</div><div class="callout amber"><h3>为什么三份都值得保留？</h3><p data-note-block="creed-purpose">只保留简明故事，可能说得出基督做了什么，却说不清祂是谁；只保留会议术语，容易丢掉洗礼教导的清楚脉络；只保留细密边界，又难以替代全会众容易共同背诵的语言。三份彼此补足，权威同样从属圣经。</p><p>325年与381年是不同历史节点；现存通行文本的接受史还涉及451年。CCI采用西方传统文本；关于圣灵发出的西方增语不应倒置为381年原句。亚他那修信经属于拉丁西方传统，作者不详，接纳范围不同于尼西亚信经。</p></div></section><section class="atlas-section" id="theology"><h2>从圣经到认信，再回到圣经</h2><div class="creed-launch"><article class="creed-tile tone-0"><b>01 · 圣经神学</b><p data-note-block="creed-bible">约1:1–18把创造与道成肉身系于同一位道；林前15:20–28把基督复活连到末后复活。认信的故事因此从创造走向新创造。</p></article><article class="creed-tile tone-1"><b>02 · 圣约神学</b><p data-note-block="creed-covenant">加3:16、29把应许的承受系于基督；来8把新约的应许系于中保。洗礼是所赐应许的记号与印证，不能把领受记号等同于自动重生。对读比利时第34条与海德堡第69–74问。</p></article><article class="creed-tile tone-2"><b>03 · 欧陆改革宗</b><p data-note-block="creed-reformed">比利时第8–11条接续三一认信，第18–19条说明道成肉身与二性联合；多特信经进一步澄清救恩如何出于神的恩典。教会以信条共同作证，仍须接受圣经检验。</p></article></div><p>亚他那修信经严肃对待所信的对象与审判。按比利时第22–24、37条合读：基督是称义的根据，信心领受基督，善行显出信心的果子。</p></section><section class="atlas-section" id="review"><h2>合上书，回答三句</h2><div class="story-line"><details><summary>哪一份最适合从救赎事件背起？</summary><p>使徒信经：从创造、降生到复活与永生。</p></details><details><summary>如果子是受造物，受损的是哪条信仰？</summary><p>尼西亚信经所守护的子与父同有神性；创造万有者不能被归进受造万有。</p></details><details><summary>为什么要区别「一位」和「二性」？</summary><p>亚他那修信经：行动与受苦者是同一位子；祂按人性受苦，神性不变成人性。</p></details></div><p class="refs">历史参考：<a href="https://threeforms.org/introduction-to-the-creeds-and-confessions/">URCNA 认信导言</a>。中文正文与附经只从原文书房引用；本页文字为学习释义。</p></section></main></body></html>'''
 return enhance_page(p,cities)

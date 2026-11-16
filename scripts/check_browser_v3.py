"""Browser acceptance: static learning flows and blocked map CDN fallback."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
with ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=root/'dist')) as server, sync_playwright() as pw:
 Thread(target=server.serve_forever,daemon=True).start()
 url=f'http://127.0.0.1:{server.server_port}/'
 browser=pw.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
 page=browser.new_page(reduced_motion='reduce'); errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
 measurements=[]
 def fits():
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),page.url
  bad=page.evaluate('''() => [...document.querySelectorAll('summary, .creed-tile, .story-screen, .mark-filters, .map-toolbar')].filter(e=>e.getClientRects().length && !e.closest('body:not(.toc-open) .toc')).filter(e=>{const r=e.getBoundingClientRect();return r.left< -1 || r.right>innerWidth+1 || e.scrollWidth>e.clientWidth+2}).map(e=>[e.textContent.trim().slice(0,30),e.getBoundingClientRect().left,e.getBoundingClientRect().right,e.scrollWidth,e.clientWidth])''');assert not bad,(page.url,bad)
 for w in [320,375,430,768,1024,1440]:
  page.set_viewport_size({'width':w,'height':860})
  for name in ['index.html','atlas.html','creeds.html','reader.html','reader-nicene.html','reader-athanasian.html']:
   page.goto(url+name,wait_until='load'); fits()
   if name=='index.html':
    for i in range(2):page.locator('#tocToggle').click();fits()
    passage=page.locator('#article-1 details summary').first;passage.click();fits();passage.click()
   if name=='atlas.html':
    for t in page.locator('.scene-tabs button').all():t.click();fits()
    for t in page.locator('.v3-story summary').all():t.click();fits()
    page.locator('#quickToggle').click();page.locator('#openMarks').click();fits();page.locator('#closeMarks').click()
   if name=='creeds.html':
    for t in page.locator('summary').all():t.click();fits();t.click()
   measurements.append({'width':w,'page':name,'fits':True})
 page.goto(url+'atlas.html');page.route('https://**/*',lambda route:route.abort())
 page.locator('#loadMap').click();page.locator('#retryMap').wait_for(state='visible',timeout=32000);fits()
 assert page.locator('.offline-atlas svg').count()==2
 page.locator('#stopMap').click();assert page.locator('#loadMap').is_visible()
 page.locator('video').evaluate('(v)=>{v.muted=true;return v.play()}'); page.wait_for_function("document.querySelector('video').currentTime>0.25");assert page.locator('video').evaluate('(v)=>v.duration')==30
 page.locator('video').evaluate('(v)=>v.pause()')
 page.goto(url+'creeds.html'); page.locator('[data-note-block=creed-purpose]').evaluate('''e=>{const r=document.createRange();r.setStart(e.firstChild,0);r.setEnd(e.firstChild,12);getSelection().removeAllRanges();getSelection().addRange(r)}''');page.locator('[data-mark-style=gold]').click();
 page.locator('#quickToggle').click();page.locator('#openMarks').click();page.get_by_text('编辑样式与我的理解').click();page.get_by_label('修改标记样式').select_option('dash');page.get_by_label('我的理解',exact=True).fill('历史、身份与边界');page.get_by_text('保存理解与样式').click();
 page.locator('#markSearch').fill('身份');assert page.locator('.saved-mark').count()==1
 page.reload();page.locator('#quickToggle').click();page.locator('#openMarks').click();assert page.locator('.mark-memo').inner_text()=='历史、身份与边界';assert page.locator('.saved-mark .style-dash').count()==1
 page.get_by_text('回到原处',exact=True).click();assert page.locator('.mark-located').count()==1
 assert not errors,errors
 page.goto(url+'atlas.html');page.screenshot(path=str(root/'qa/v3-atlas-desktop.png'))
 page.set_viewport_size({'width':375,'height':860});page.goto(url+'creeds.html#matrix');page.screenshot(path=str(root/'qa/v3-creeds-mobile.png'))
 report={'layouts':measurements,'interactions':['repeated disclosures','scene switching','blocked online tiles and local fallback','30s video playback','highlight edit, memo search, reload and return'],'page_errors':errors}
 (root/'qa/v3-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 browser.close();print(f'{len(measurements)} page/width combinations and interaction flows passed')

"""Public/local browser acceptance with exact commit and asset-byte verification."""
import argparse, hashlib, json, re, shutil, time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

p=argparse.ArgumentParser()
p.add_argument('--url',default='http://127.0.0.1:8080/')
p.add_argument('--out',default='build/qa-local')
p.add_argument('--commit',default='')
a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];http=[];screens=[];failed_requests=[]
def check(name,condition):
 checks.append({'name':name,'passed':bool(condition)})
 if not condition:raise AssertionError(name)
def filename(name):return 'index.html' if name=='home' else name+'.html'
def bust(url):return url+('&' if '?' in url else '?')+'qa='+str(time.time_ns())
def snap(page,name,full=False):
 page.screenshot(path=str(out/name),full_page=full,scale='css',animations='disabled');screens.append(name)
def visit(page,url):
 last=None
 for attempt in range(4):
  try:
   response=page.goto(bust(url),wait_until='networkidle',timeout=60000)
   status=response.status if response else 0
   http.append({'url':url,'status':status,'attempt':attempt+1})
   if status==200:return response
  except Exception as exc:last=str(exc)[:300]
  time.sleep(2*(attempt+1))
 raise AssertionError('Page unreachable after bounded retries: '+url+' '+str(last))
def slide(page,selector,value):
 page.locator(selector).evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}))}',str(value))

manifest={}
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=shutil.which('chromium') or None,headless=True)
 context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=2,reduced_motion='reduce',accept_downloads=True)
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('requestfailed',lambda req:failed_requests.append({'url':req.url,'failure':req.failure}))
 try:
  r=context.request.get(bust(urljoin(a.url,'release.json')),timeout=30000)
  check('Release manifest HTTP 200',r.status==200);manifest=r.json()
  expected=a.commit or manifest['source_commit']
  check('Exact source commit in manifest',manifest['source_commit']==expected)
  check('Eleven public pages',len(manifest['pages'])==11)
  check('Nine approved artworks',manifest['artworks']==9)
  for path,digest in manifest['files'].items():
   res=context.request.get(bust(urljoin(a.url,path)),timeout=30000)
   check('Published file HTTP 200: '+path,res.status==200)
   check('Published file exact SHA256: '+path,hashlib.sha256(res.body()).hexdigest()==digest)
  art=context.request.get(bust(urljoin(a.url,'assets/art/web-manifest.json'))).json()
  check('Nine native image records',len(art['records'])==9)
  check('No asset upscaling',all(not v['upscaled'] and v['web_size'][0]<=v['source_size'][0] and v['web_size'][1]<=v['source_size'][1] for v in art['records']))
  for name in manifest['pages']:
   for language in ['zh','en']:
    response=visit(page,urljoin(a.url,filename(name))+'?lang='+language)
    key=name+'/'+language
    check(key+' HTTP 200',response.status==200)
    check(key+' current build',page.evaluate('window.QURI_BUILD')==manifest['version'])
    check(key+' exact source commit',page.evaluate('window.QURI_SOURCE_COMMIT')==expected)
    check(key+' page identity',page.locator('body').get_attribute('data-page')==name)
    check(key+' language',page.locator('html').get_attribute('lang')==('en' if language=='en' else 'zh-CN'))
    check(key+' one visible h1',page.locator('h1:visible').count()==1)
    for width in [1440,768,390]:
     page.set_viewport_size({'width':width,'height':1000});page.wait_for_timeout(250)
     check(key+f' no overflow at {width}',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.set_viewport_size({'width':1440,'height':1000});page.wait_for_timeout(250)
    for i,img in enumerate(page.locator('#app > :not(#legacy-home) img').all()):
     if not img.is_visible():continue
     img.scroll_into_view_if_needed();img.evaluate('(e)=>e.loading="eager"')
     page.wait_for_function('(e)=>e.complete&&e.naturalWidth>0',arg=img.element_handle(),timeout=15000)
     check(key+f' native artwork {i}',img.evaluate('(e)=>e.naturalWidth>=800'))
     check(key+f' native dimensions not enlarged {i}',img.evaluate('(e)=>Math.max(e.clientWidth/e.naturalWidth,e.clientHeight/e.naturalHeight)<=1.04'))
     check(key+f' no old thumbnail {i}',not '/hero-atlantis.webp' in img.get_attribute('src'))
    links=page.locator('#app > :not(#legacy-home) a[href]').evaluate_all('(xs)=>xs.map(x=>x.href)')
    valid={filename(p) for p in manifest['pages']}
    check(key+' valid same-site page links',all(urlparse(u).path.split('/')[-1] in valid or urlparse(u).path.endswith('/') for u in links if urlparse(u).netloc==urlparse(a.url).netloc))
    if language=='en':
     visible=page.locator('body').inner_text().replace('中文','')
     check(key+' English UI has no leaked Chinese',not re.search(r'[\u3400-\u9fff]',visible))
    page.evaluate('scrollTo(0,0)');page.wait_for_timeout(150)
    snap(page,name+'-'+language+'-desktop.png')
    if language=='zh':
     page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(250);page.evaluate('scrollTo(0,0)')
     snap(page,name+'-zh-mobile.png')
     page.set_viewport_size({'width':1440,'height':1000})
  visit(page,urljoin(a.url,'explore.html?lang=zh'))
  check('24 concept cards',page.locator('#page-content .concept').count()==24)
  page.locator('#search').fill('entanglement');check('Bilingual concept search',page.locator('#page-content .concept').count()>0)
  page.locator('#page-content .concept').first.click();check('Concept dialog',page.locator('#entryDialog').is_visible())
  page.locator('#entryDialog [data-read]').click();check('Reading progress persisted',bool(page.evaluate('localStorage.getItem("quri-read-v1")')))
  page.locator('[data-action=close]').click();page.locator('#search').fill('')
  page.locator('#page-content [data-cat="information"]').click();check('Category filter',page.locator('#page-content .concept').count()==5)
  page.locator('#page-content [data-cat="all"]').click()
  with page.expect_download() as dl:page.locator('[data-action=export]').click()
  dl.value.save_as(str(out/'knowledge-map.svg'));check('SVG export',(out/'knowledge-map.svg').stat().st_size>1000)
  visit(page,urljoin(a.url,'journey.html?lang=zh'))
  page.locator('[data-path="spiritual"]').click();check('Learning route switches',page.locator('#steps .step').count()==8)
  check('Reading progress shared across pages','1 /' in page.locator('#progress').inner_text())
  visit(page,urljoin(a.url,'lab.html?lang=zh'))
  page.locator('[data-action=many]').click();check('Double slit sampling','200' in page.locator('#labValue').inner_text())
  page.locator('[data-lang=en]').click();check('Samples survive language switch','200' in page.locator('#labValue').inner_text())
  page.locator('#detector').check();check('Which-path behavior','V = 0.00' in page.locator('#labValue').inner_text() and page.locator('#visibility').is_disabled())
  page.locator('[data-lab=phase]').click();slide(page,'#phase',180);check('Destructive interference','0.00' in page.locator('#labValue').inner_text())
  page.locator('[data-lab=uncertainty]').click();slide(page,'#width',1);check('Uncertainty product','0.50' in page.locator('#labValue').inner_text())
  page.locator('[data-lab=bell]').click();slide(page,'#theta',45);check('Bell ideal maximum','2.828' in page.locator('#labValue').inner_text())
  page.locator('[data-action=pairs]').click();check('Pair samples','1,000' in page.locator('#pairStats').inner_text())
  check('Retina canvas backing resolution',page.locator('#experiment').evaluate('(e)=>e.width>=e.getBoundingClientRect().width*devicePixelRatio-1'))
  page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(400)
  check('Canvas redraw after resizing',page.locator('#experiment').evaluate('(e)=>e.width>=e.getBoundingClientRect().width*devicePixelRatio-1'))
  slide(page,'#theta',30)
  visit(page,urljoin(a.url,'about.html?lang=en'));visit(page,urljoin(a.url,'lab.html?lang=en'))
  check('Experiment parameters survive page navigation',page.locator('#theta').input_value()=='30')
  snap(page,'lab-en-mobile-full.png',True)
  visit(page,urljoin(a.url,'play.html?lang=en'))
  for i,answer in enumerate([0,1,1,0,1,0]):page.locator(f'[data-quiz="{i}"][data-choice="{answer}"]').click()
  check('Quiz scoring','6/6' in page.locator('.q-quiz-score').inner_text() and 'Correct 6' in page.locator('.q-quiz-score').inner_text())
  page.locator('[data-lang=zh]').click();check('Quiz answers survive language switch','6/6' in page.locator('.q-quiz-score').inner_text())
  visit(page,urljoin(a.url,'community.html?lang=en'))
  check('Local notebook truthfully labelled','not a public forum' in page.locator('#page-content').inner_text())
  note='My unsaved quantum draft — release verification.'
  page.locator('#notebook').fill(note);page.locator('[data-lang=zh]').click()
  check('Unsaved notebook survives language switch',page.locator('#notebook').input_value()==note)
  page.locator('[data-q=save-note]').click();visit(page,urljoin(a.url,'community.html?lang=en'))
  check('Saved notebook survives reload',page.locator('#notebook').input_value()==note)
  with page.expect_download() as dl:page.locator('[data-q=export-note]').click()
  dl.value.save_as(str(out/'notebook.txt'));check('Notebook export bytes',(out/'notebook.txt').read_text()==note)
  visit(page,urljoin(a.url,'sources.html?lang=en'));check('20 source entries',page.locator('#page-content .source').count()==20)
  page.goto(a.url+'?lang=en#sources',wait_until='domcontentloaded');page.wait_for_url('**/sources.html*',timeout=20000)
  check('Old deep link migrates','sources.html' in page.url)
  visit(page,urljoin(a.url,'index.html?lang=en'))
  page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(250)
  page.locator('[data-q=menu]').click();check('Mobile menu opens',page.locator('.q-mobile-menu').is_visible())
  page.keyboard.press('Escape');check('Escape closes mobile menu',not page.locator('.q-mobile-menu').is_visible())
  check('No JavaScript errors',not errors)
 finally:
  report={'release':manifest.get('version'),'source_commit':manifest.get('source_commit'),'base_url':a.url,
      'scope':'HTTP browser acceptance; exact public file SHA256 verification','passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),
      'checks':checks,'javascript_errors':errors,'http_attempts':http,'request_failures':failed_requests,'screenshots':screens,
      'widths':[1440,768,390],'device_scale_factor':2,'screenshot_scale':'css'}
  (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
  browser.close()
print(json.dumps({'release':manifest['version'],'passed':len(checks),'failed':0,'base_url':a.url,'source_commit':manifest['source_commit']}))

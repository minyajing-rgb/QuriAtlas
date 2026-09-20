"""Browser acceptance checks for every public QuriAtlas page and core interactions."""
import argparse,json,time,shutil
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

VERSION='0.6.0-atlantis-fullsite'
PAGES=['home','explore','lab','mind','stories','play','community','journey','sources','about','entanglement']
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8080/');p.add_argument('--out',default='build/qa-local');a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,condition):
 checks.append({'name':name,'passed':bool(condition)})
 if not condition:raise AssertionError(name)
def path(name):return 'index.html' if name=='home' else name+'.html'
def slide(selector,value):page.locator(selector).evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}))}',str(value))
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=shutil.which('chromium') or None,headless=True)
 context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce',accept_downloads=True)
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 try:
  for name in PAGES:
   for language in ['zh','en']:
    url=urljoin(a.url,path(name))+'?lang='+language+'&qa='+str(time.time_ns())
    response=page.goto(url,wait_until='networkidle',timeout=60000)
    check(name+'/'+language+' HTTPS/HTTP 200',response.status==200)
    check(name+'/'+language+' release',page.evaluate('window.QURI_BUILD')==VERSION)
    check(name+'/'+language+' page route',page.locator('body').get_attribute('data-page')==name)
    check(name+'/'+language+' language',page.locator('html').get_attribute('lang')==('en' if language=='en' else 'zh-CN'))
    check(name+'/'+language+' heading',page.locator('h1:visible').count()==1)
    for width in [1440,768,390]:
     page.set_viewport_size({'width':width,'height':1000});page.wait_for_timeout(180)
     check(name+'/'+language+f' layout {width}px',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.set_viewport_size({'width':1440,'height':1000})
    for img in page.locator('#app > :not(#legacy-home) img').all():
     if img.is_visible():
      img.scroll_into_view_if_needed();img.evaluate('(e)=>e.loading="eager"')
      page.wait_for_function('(e)=>e.complete && e.naturalWidth>0',arg=img.element_handle(),timeout=15000)
      check(name+'/'+language+' native art',img.evaluate('(e)=>e.naturalWidth>=800'))
    page.evaluate('scrollTo(0,0)');page.wait_for_timeout(200)
    if language=='zh':page.screenshot(path=str(out/(name+'-zh-desktop.png')),full_page=True)
    if name=='home' and language=='en':page.screenshot(path=str(out/'home-en-desktop.png'),full_page=False)
    check(name+'/'+language+' valid local HTML targets',page.evaluate(r'''()=>Array.from(document.querySelectorAll('#app > :not(#legacy-home) a[href]')).filter(a=>new URL(a.href).origin===location.origin && a.getAttribute('href').includes('.html')).every(a=>/^(index|explore|lab|mind|stories|play|community|journey|sources|about|entanglement)\.html/.test(a.getAttribute('href')))'''))
  page.goto(urljoin(a.url,'explore.html?lang=zh'),wait_until='networkidle')
  check('24 real concept cards',page.locator('#page-content .concept').count()==24)
  page.locator('#search').fill('entanglement');check('Bilingual search finds concepts',page.locator('#page-content .concept').count()>0)
  page.locator('#page-content .concept').first.click();check('Concept dialog opens',page.locator('#entryDialog').is_visible())
  page.locator('#entryDialog [data-read]').click();check('Reading saved',bool(page.evaluate('localStorage.getItem("quri-read-v1")')))
  page.locator('[data-action=close]').click();page.locator('#search').fill('')
  with page.expect_download() as dl:page.locator('[data-action=export]').click()
  dl.value.save_as(str(out/'knowledge-map.svg'));check('SVG export',Path(out/'knowledge-map.svg').stat().st_size>1000)
  page.goto(urljoin(a.url,'lab.html?lang=zh'),wait_until='networkidle')
  page.locator('[data-action=many]').click();check('Double slit 200 samples','200' in page.locator('#labValue').inner_text())
  page.locator('[data-lang=en]').click();check('Samples persist across languages','200' in page.locator('#labValue').inner_text())
  page.locator('#detector').check();check('Which path clears samples and removes visibility','V = 0.00' in page.locator('#labValue').inner_text() and page.locator('#visibility').is_disabled())
  page.locator('[data-lab=phase]').click();slide('#phase',180);check('Destructive interference','0.00' in page.locator('#labValue').inner_text())
  page.locator('[data-lab=uncertainty]').click();slide('#width',1);check('Gaussian uncertainty product','0.50' in page.locator('#labValue').inner_text())
  page.locator('[data-lab=bell]').click();slide('#theta',45);check('Bell ideal maximum','2.828' in page.locator('#labValue').inner_text())
  page.locator('[data-action=pairs]').click();check('Joint pair samples','1,000' in page.locator('#pairStats').inner_text())
  page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(out/'lab-en-mobile.png'),full_page=True)
  page.goto(urljoin(a.url,'play.html?lang=en'),wait_until='networkidle')
  for i,answer in enumerate([0,1,1,0,1,0]):page.locator(f'[data-quiz="{i}"][data-choice="{answer}"]').click()
  check('Quiz completes accurately','6/6' in page.locator('.q-quiz-score').inner_text() and 'Correct 6' in page.locator('.q-quiz-score').inner_text())
  page.goto(urljoin(a.url,'community.html?lang=en'),wait_until='networkidle')
  page.locator('#notebook').fill('My quantum note — native art release QA.');page.locator('[data-q=save-note]').click();page.reload(wait_until='networkidle')
  check('Notebook persists',page.locator('#notebook').input_value().startswith('My quantum note'))
  with page.expect_download() as dl:page.locator('[data-q=export-note]').click()
  check('Notebook export',dl.value.suggested_filename=='QuriAtlas-notebook.txt')
  page.goto(urljoin(a.url,'sources.html?lang=en'),wait_until='networkidle');check('20 evidence entries',page.locator('#page-content .source').count()==20)
  page.goto(a.url+'?lang=en#sources',wait_until='domcontentloaded');page.wait_for_url('**/sources.html*',timeout=20000);check('Old deep links resolve','sources.html' in page.url)
  page.goto(urljoin(a.url,'index.html?lang=zh'),wait_until='networkidle');page.screenshot(path=str(out/'home-zh-mobile.png'),full_page=True)
  page.locator('[data-q=menu]').click();check('Mobile menu functional',page.locator('.q-mobile-menu').is_visible())
  check('No JavaScript runtime errors',not errors)
 finally:
  report={'release':VERSION,'base_url':a.url,'scope':'real HTTP browser acceptance','page_count':11,'languages':['zh','en'],'widths':[1440,768,390],'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'checks':checks,'javascript_errors':errors}
  (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
  browser.close()
print(json.dumps({'release':VERSION,'passed':len(checks),'base_url':a.url}))

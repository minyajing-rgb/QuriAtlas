"""QuriAtlas browser QA for the standalone GitHub Pages site."""
import argparse, json, re, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

p=argparse.ArgumentParser(); p.add_argument('--url',default='http://127.0.0.1:8080/'); p.add_argument('--out',default='build/qa'); a=p.parse_args()
out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
checks=[]; errors=[]
def check(name,ok):
    checks.append({'name':name,'passed':bool(ok)})
    assert ok,name
def cjk(s): return bool(re.search(r'[\u3400-\u9fff]',s))

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=shutil.which('chromium') or None)
    page=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce')
    page.on('pageerror',lambda e:errors.append(str(e)))
    r=page.goto(a.url,wait_until='networkidle')
    check('HTTP 200',r.status==200)
    check('Expected build',page.evaluate('window.QURI_BUILD')=='0.5.0-atlantis-home')
    check('Cinematic hero image loaded',page.locator('.hero-scene').evaluate('e=>e.complete && e.naturalWidth>=400'))
    check('Light Atlantis theme',page.evaluate("getComputedStyle(document.documentElement).colorScheme")=='light')
    check('24 concept cards',page.locator('.concept').count()==24)
    check('20 traceable sources',page.locator('.source').count()==20)
    check('Six portal cards',page.locator('.portal-card').count()==6)
    check('Three homepage showcase modules',page.locator('.landing-showcase > *').count()==3)
    page.screenshot(path=str(out/'desktop-zh.png'),full_page=False)
    page.locator('[data-lang=en]').click()
    check('English document mode',page.locator('html').get_attribute('lang')=='en')
    check('English page title',not cjk(page.title()))
    page.locator('[data-lab=slits]').click()
    page.locator('[data-action=many]').click()
    check('Double slit interaction', '200' in page.locator('#labValue').inner_text())
    page.locator('[data-lang=zh]').click()
    check('Lab state survives language switch','200' in page.locator('#labValue').inner_text())
    page.set_viewport_size({'width':390,'height':900}); page.wait_for_timeout(150)
    check('Mobile width',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    check('Mobile hero remains visual',page.locator('.hero').bounding_box()['height']>=700)
    page.screenshot(path=str(out/'mobile-zh.png'),full_page=False)
    check('No JS errors',not errors)
    browser.close()
report={'build':'0.5.0-atlantis-home','passed':len(checks),'checks':checks,'javascript_errors':errors,'url':a.url}
(out/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(checks),'url':a.url}))

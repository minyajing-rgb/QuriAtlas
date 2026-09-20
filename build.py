"""Build all public pages from the existing sourced corpus and the new visual shell."""
from pathlib import Path
import json, hashlib, shutil
ROOT=Path(__file__).resolve().parent
RELEASE='0.6.0-atlantis-fullsite'
PAGES=['home','explore','lab','mind','stories','play','community','journey','sources','about','entanglement']
manifest=json.loads((ROOT/'data/CURRENT.json').read_text())
data_path=(ROOT/'data'/manifest['dataset']).resolve()
if not data_path.is_relative_to((ROOT/'data').resolve()):raise ValueError('Unsafe corpus path')
data=json.loads(data_path.read_text())
en=json.loads((ROOT/'site/en.json').read_text())
assert set(en['entries'])=={e['id'] for e in data['entries']}
def pack(obj):return json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
css='\n'.join((ROOT/'site'/x).read_text() for x in ['style.css','mobile.css','release.css'])
js=(ROOT/'site/app.js').read_text()
# Improve contrast of the preserved teaching-model canvas for the light theme.
js=js.replace("purple='#bb9efb',gold='#e6bd80',cyan='#70d9e0',muted='#a9b5cf'","purple='#7657bc',gold='#ad7b30',cyan='#2983ac',muted='#5e7194'")
# Avoid loading the rejected low-resolution image even during the legacy engine boot.
js=js.replace('assets/hero-atlantis.webp','assets/art/home-crop.webp?v=6')
css=css.replace("url('assets/hero-atlantis.webp')","url('assets/art/home-crop.webp?v=6')")
extra=(ROOT/'site/release.js').read_text()
page_template='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#f7faff"><meta name="description" content="QuriAtlas: quantum physics through stories, original artwork, interactive models and evidence."><meta name="quri-build" content="'''+RELEASE+'''"><title>QuriAtlas｜量子漫游</title><style>'''+css+'''</style></head><body data-page="__PAGE__"><div id="app"></div><dialog id="entryDialog"></dialog><noscript>Enable JavaScript to explore the interactive atlas. 请启用 JavaScript 使用互动知识地图。</noscript><script id="atlas-data" type="application/json">'''+pack(data)+'''</script><script id="english-data" type="application/json">'''+pack(en)+'''</script><script>'''+js+'''</script><script>'''+extra+'''</script></body></html>'''
for p in PAGES:(ROOT/('index.html' if p=='home' else p+'.html')).write_text(page_template.replace('__PAGE__',p))
(ROOT/'release.json').write_text(json.dumps({'version':RELEASE,'pages':PAGES,'concepts':len(data['entries']),'sources':len(data['sources']),'artworks':9},indent=2))
(ROOT/'.nojekyll').touch()
# Only public site content is staged, never transfer URLs, scripts or internal research notes.
stage=ROOT/'build/public'
if stage.exists():shutil.rmtree(stage)
(stage/'assets/art').mkdir(parents=True)
for p in PAGES:shutil.copy2(ROOT/('index.html' if p=='home' else p+'.html'),stage)
for p in (ROOT/'assets/art').glob('*.webp'):shutil.copy2(p,stage/'assets/art'/p.name)
for name in ['CNAME','.nojekyll','release.json']:shutil.copy2(ROOT/name,stage/name)
print(json.dumps({'version':RELEASE,'pages':len(PAGES),'html_sha256':hashlib.sha256((stage/'index.html').read_bytes()).hexdigest()}))

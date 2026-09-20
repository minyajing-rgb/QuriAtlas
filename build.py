"""Build standalone QuriAtlas HTML from the canonical corpus and bilingual UI source."""
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'data/CURRENT.json').read_text(encoding='utf-8'))
data_path=(ROOT/'data'/manifest['dataset']).resolve()
if not data_path.is_relative_to((ROOT/'data').resolve()):
    raise ValueError('Corpus must remain inside data/')
data=json.loads(data_path.read_text(encoding='utf-8'))
en=json.loads((ROOT/'site/en.json').read_text(encoding='utf-8'))

assert {e['id'] for e in data['entries']}==set(en['entries'])
assert all(len(v)==4 for v in en['entries'].values())
for key in ('categories','bridges','timeline'):
    assert len(en[key])==len(data[key])
assert len(en['domains'])==len(data['expansion_plan']['domains'])

def pack(v):
    return json.dumps(v,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')

css=(ROOT/'site/style.css').read_text(encoding='utf-8')+(ROOT/'site/mobile.css').read_text(encoding='utf-8')
js=(ROOT/'site/app.js').read_text(encoding='utf-8')
page='''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#f7faff">
<title>QuriAtlas｜量子漫游 · Interactive Quantum Physics</title>
<meta name="description" content="Bilingual interactive quantum physics atlas with stories, experiments, evidence trails and a cinematic Atlantis-inspired visual world.">
<meta name="quri-build" content="0.5.0-atlantis-home">
<style>'''+css+'''</style></head><body>
<div id="app"></div><dialog id="entryDialog"></dialog>
<noscript>This interactive atlas requires JavaScript. 本互动知识地图需要启用 JavaScript。</noscript>
<script id="atlas-data" type="application/json">'''+pack(data)+'''</script>
<script id="english-data" type="application/json">'''+pack(en)+'''</script>
<script>'''+js+'''</script></body></html>'''

(ROOT/'index.html').write_text(page,encoding='utf-8')
print(json.dumps({'build':'0.5.0-atlantis-home','concepts':len(data['entries']),'sources':len(data['sources']),'bytes':len(page.encode()),'sha256':hashlib.sha256(page.encode()).hexdigest()}))

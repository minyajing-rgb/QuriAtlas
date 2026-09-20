"""Build and fingerprint the complete bilingual QuriAtlas static site."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess
from tools.prepare_web_art import prepare
ROOT = Path(__file__).resolve().parent
RELEASE = '0.6.1-atlantis-fullsite'
PAGES = ['home','explore','lab','mind','stories','play','community','journey','sources','about','entanglement']

def read(path): return (ROOT/path).read_text(encoding='utf-8')
def pack(obj): return json.dumps(obj, ensure_ascii=False, separators=(',',':')).replace('<','\\u003c')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = json.loads(read('data/CURRENT.json'))
    data_path = (ROOT/'data'/manifest['dataset']).resolve()
    if not data_path.is_relative_to((ROOT/'data').resolve()): raise ValueError('Unsafe corpus path')
    data = json.loads(data_path.read_text(encoding='utf-8')); en = json.loads(read('site/en.json'))
    assert set(en['entries']) == {e['id'] for e in data['entries']}
    assert all(len(v) == 4 for v in en['entries'].values())
    for key in ('categories','bridges','timeline'): assert len(en[key]) == len(data[key])
    assert len(en['domains']) == len(data['expansion_plan']['domains'])
    art = prepare()
    commit = os.environ.get('GITHUB_SHA')
    if not commit:
        try: commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
        except (OSError,subprocess.CalledProcessError): commit = 'local-preview'
    css = '\n'.join(read('site/'+x) for x in ['style.css','mobile.css','release.css','hardening.css'])
    js = read('site/app.js')
    js = js.replace("purple='#bb9efb',gold='#e6bd80',cyan='#70d9e0',muted='#a9b5cf'", "purple='#7657bc',gold='#ad7b30',cyan='#2983ac',muted='#5e7194'")
    # Match backing pixels to actual CSS width and device scale. No changes to model math.
    needle = 'c.setTransform(1.5,0,0,1.5,0,0);c.clearRect(0,0,820,340);'
    replacement = "const rs=Math.max(1,Math.min(4,(canvas.getBoundingClientRect().width||820)*(devicePixelRatio||1)/820));canvas.width=Math.ceil(820*rs);canvas.height=Math.ceil(340*rs);c.setTransform(rs,0,0,rs,0,0);c.clearRect(0,0,820,340);"
    if needle not in js: raise ValueError('Canvas integration point changed; review before publishing')
    js = js.replace(needle, replacement)
    js = js.replace('assets/hero-atlantis.webp','assets/art/home-web.webp?v=061')
    css = css.replace('assets/hero-atlantis.webp','assets/art/home-web.webp?v=061')
    extra = read('site/release.js')
    extra = re.sub(r"const RELEASE='[^']+';", "const RELEASE='"+RELEASE+"';", extra, count=1)
    # Use the reviewed crop for each content image; keep the large native scene for the homepage.
    for old in ('-crop.webp?v=6','-crop.webp?v=061'):
        js = js.replace(old,'-web.webp?v=061'); css = css.replace(old,'-web.webp?v=061'); extra = extra.replace(old,'-web.webp?v=061')
    extra = extra.replace('home-scene.webp?v=6','home-scene.webp?v=061')
    extra += '\n' + read('site/hardening.js')
    template = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#f7faff"><meta name="description" content="QuriAtlas: stories, native artwork, interactive quantum models and evidence."><meta name="quri-build" content="'+RELEASE+'"><meta name="quri-source-commit" content="'+commit+'"><title>QuriAtlas｜量子漫游</title><style>'+css+'</style></head><body data-page="__PAGE__"><div id="app"></div><dialog id="entryDialog"></dialog><noscript>Enable JavaScript to explore the interactive atlas. 请启用 JavaScript。</noscript><script id="atlas-data" type="application/json">'+pack(data)+'</script><script id="english-data" type="application/json">'+pack(en)+'</script><script>'+js+'</script><script>'+extra+'</script></body></html>'
    stage = ROOT/'build/public'
    if stage.exists(): shutil.rmtree(stage)
    (stage/'assets/art').mkdir(parents=True)
    for p in PAGES:
        name = 'index.html' if p=='home' else p+'.html'
        (ROOT/name).write_text(template.replace('__PAGE__',p), encoding='utf-8')
        shutil.copy2(ROOT/name,stage/name)
    names = [r['web_file'].split('/')[-1] for r in art['records']] + ['home-scene.webp','web-manifest.json']
    for name in names: shutil.copy2(ROOT/'assets/art'/name,stage/'assets/art'/name)
    shutil.copy2(ROOT/'CNAME', stage/'CNAME'); (stage/'.nojekyll').touch(); (ROOT/'.nojekyll').touch()
    # Pages consumes these provisioning files; upload-pages-artifact omits dotfiles.
    # Keep configuration intact, but fingerprint only resources the public site serves.
    deployment_metadata = {'CNAME', '.nojekyll'}
    release = {'version':RELEASE,'source_commit':commit,'pages':PAGES,'concepts':len(data['entries']),'sources':len(data['sources']),'artworks':9,
        'files':{str(f.relative_to(stage)):sha(f) for f in sorted(stage.rglob('*')) if f.is_file() and f.name not in deployment_metadata},
        'deployment_metadata':sorted(deployment_metadata),
        'scope':'Bilingual educational static site. Local notebook only; not a public forum.'}
    for p in (ROOT/'release.json',stage/'release.json'): p.write_text(json.dumps(release,indent=2),encoding='utf-8')
    print(json.dumps({'version':RELEASE,'source_commit':commit,'pages':len(PAGES),'artworks':9,'fingerprinted_files':len(release['files'])}))

if __name__ == '__main__': main()

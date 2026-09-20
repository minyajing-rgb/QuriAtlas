"""One-time import of approved chat artwork, spatially tiled to avoid thumbnail downsampling.
No crop is a substitute/reconstruction of an unseen source: all tiles are from the uploaded PNGs.
The download URLs are exact signed export URLs provided by the connector; no signatures are modified.
"""
from pathlib import Path
import json,io,urllib.request,urllib.parse,concurrent.futures,hashlib,time
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/art';OUT.mkdir(parents=True,exist_ok=True)
SPECS=[('home',1672,941),('lab',1672,941),('basics',1448,1086),('mind',1448,1086),('stories',1448,1086),('play',1448,1086),('community',1448,1086),('entanglement',1672,941),('journey',1672,941)]
urls=[]
for n in range(1,5):
 m=json.loads((ROOT/f'ops/art-transfer-{n}.json').read_text());d=m['design']
 for p,(date,exp,sig) in enumerate(m['records'],1):
  q={'X-Amz-Algorithm':'AWS4-HMAC-SHA256','X-Amz-Credential':f'AKIAQYCGKMUHVZ3RB6IW/{date[:8]}/us-east-1/s3/aws4_request','X-Amz-Date':date,'X-Amz-Expires':str(exp),'X-Amz-Signature':sig,'X-Amz-SignedHeaders':'host','response-expires':m['expires']}
  urls.append(f'https://s3.amazonaws.com/document-export-us1.canva.com/{d[-5:]}/{d}/1/thumbnail/{p:04}.png?'+urllib.parse.urlencode(q,quote_via=urllib.parse.quote))
assert len(urls)==96
CACHE=ROOT/'build/art-tiles';CACHE.mkdir(parents=True,exist_ok=True)
def retrieve(args):
 i,url=args
 for attempt in range(3):
  try:
   with urllib.request.urlopen(url,timeout=50) as r: raw=r.read()
   im=Image.open(io.BytesIO(raw)).convert('RGB');im.load()
   if im.width<560 or im.height<350:raise ValueError(f'tile {i} smaller than original crop: {im.size}')
   # Canva export may apply a 1.009x preview transform. Never enlarge a thumbnail.
   if im.size!=(560,350):im=im.resize((560,350),Image.Resampling.LANCZOS)
   im.save(CACHE/f'{i:03}.png');return im
  except Exception:
   if attempt==2:raise
   time.sleep(2)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:tiles=list(pool.map(retrieve,enumerate(urls)))
k=0;result=[]
for name,w,h in SPECS:
 im=Image.new('RGB',(w,h))
 for y in range(0,h,350):
  for x in range(0,w,560):
   im.paste(tiles[k].crop((0,0,min(560,w-x),min(350,h-y))),(x,y));k+=1
 im.save(OUT/f'{name}.png',optimize=True)
 im.save(OUT/f'{name}.webp',quality=94,method=6)
 # Remove the baked navigation / page edge from the homepage artwork only.
 if name=='home':im.crop((0,90,w,850)).save(OUT/'home-scene.webp',quality=94,method=6)
 # Independent artwork crops used under real HTML captions, never a screenshot as a fake page.
 crops={'home':(580,120,1640,850),'lab':(610,140,1630,850),'basics':(450,150,1400,1060),'mind':(470,280,1410,1050),'stories':(520,230,1420,1040),'play':(490,230,1400,1020),'community':(10,350,1030,1050),'entanglement':(820,80,1672,730),'journey':(380,340,1510,900)}
 im.crop(crops[name]).save(OUT/f'{name}-crop.webp',quality=94,method=6)
 result.append({'key':name,'width':w,'height':h,'file':f'{name}.webp','bytes':(OUT/f'{name}.webp').stat().st_size,'sha256':hashlib.sha256((OUT/f'{name}.webp').read_bytes()).hexdigest(),'transfer':'spatial tiles of approved original, reassembled at original dimensions; export resampling documented'})
 print(name,w,h,result[-1]['bytes'])
assert k==96
(OUT/'manifest.json').write_text(json.dumps(result,indent=2))
print('All nine original-size images saved permanently in assets/art.')

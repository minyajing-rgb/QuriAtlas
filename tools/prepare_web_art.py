"""Create native-resolution web crops; retain original artwork and never upscale."""
from pathlib import Path
from PIL import Image
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/art'
# Pixel coordinates reviewed against the nine approved originals. The left-hand
# painted headings/buttons are excluded from content-page art, not treated as UI.
CROPS = {
    'home': (610, 100, 1672, 850),
    'basics': (560, 170, 1448, 1060),
    'lab': (680, 210, 1672, 850),
    'mind': (570, 150, 1448, 1030),
    'stories': (605, 280, 1448, 1050),
    'play': (295, 330, 1448, 1055),
    'community': (320, 345, 1448, 1055),
    'entanglement': (665, 110, 1672, 880),
    'journey': (0, 340, 1672, 910),
}

def prepare():
    records = []
    for key, box in CROPS.items():
        src = ART / (key + '.png')
        if not src.exists():
            raise FileNotFoundError('Approved original missing: ' + str(src))
        with Image.open(src) as image:
            image = image.convert('RGB')
            if box[2] > image.width or box[3] > image.height:
                raise ValueError('Crop outside original: ' + key)
            crop = image.crop(box)
            dst = ART / (key + '-web.webp')
            crop.save(dst, 'WEBP', quality=94, method=6)
            records.append({'key': key, 'source': 'assets/art/' + src.name,
                'source_size': [image.width, image.height], 'crop_box': list(box),
                'web_file': 'assets/art/' + dst.name, 'web_size': list(crop.size),
                'upscaled': False, 'sha256': hashlib.sha256(dst.read_bytes()).hexdigest()})
    report = {'version': '0.6.1', 'method': 'Crop only, native pixels, WebP quality 94; no upscaling.',
        'original_artworks': 9, 'records': records,
        'note': 'Fictional scenes and decorative labels are not apparatus diagrams or UI controls.'}
    (ART / 'web-manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report

if __name__ == '__main__':
    print(json.dumps(prepare(), ensure_ascii=False))

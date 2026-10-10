from pathlib import Path
import hashlib, json, urllib.request
ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/'config/SGIT_CORE_FROZEN.json').read_text())
commit=cfg['frozen_repo']['commit']
base=f"https://raw.githubusercontent.com/miroslavsvitek/SGIT-Hodge-Curl-Conscious-Visual-Detection/{commit}/supplementary/"
out=ROOT/'frozen_assets'; out.mkdir(exist_ok=True)

def gitblob(b): return hashlib.sha1(f"blob {len(b)}\0".encode()+b).hexdigest()
for name,expected in cfg['frozen_assets'].items():
    url=base+name
    print('FETCH',url)
    with urllib.request.urlopen(url,timeout=120) as r: b=r.read()
    if isinstance(expected,dict):
        if hashlib.sha256(b).hexdigest()!=expected['sha256']: raise SystemExit(f'SHA256 mismatch: {name}')
        if gitblob(b)!=expected['git_blob']: raise SystemExit(f'git-blob mismatch: {name}')
    else:
        if gitblob(b)!=expected: raise SystemExit(f'git-blob mismatch: {name}')
    (out/name).write_bytes(b)
print('FROZEN_ASSETS_PASS')

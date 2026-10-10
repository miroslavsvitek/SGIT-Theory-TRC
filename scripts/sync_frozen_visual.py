"""Download exact upstream original visual scripts and frozen geometry; verify each Git blob SHA-1.
Requires internet only when executing this script on user's local Windows computer.
Does not modify user originals or participant data.
"""
import hashlib,json,urllib.request,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
UPSTREAM='miroslavsvitek/SGIT-Hodge-Curl-Conscious-Visual-Detection'
COMMIT='f0ffc52cf0003bdba2e90ca53712375beda6709d'
FILES={
'frozen_analysis/discovery/HGFT_X2_FROZEN_CONFIG_1_0.json':'c9d4aaf0987875754a3901e1361e0268aae4a691',
'frozen_analysis/discovery/HGFT_X2_FROZEN_PROTOCOL.md':'0c93f3918241a0d20c63be7f38a1bc90b42b13ba',
'frozen_analysis/discovery/hgft_x2_math.py':'10a324e42d294d57f4d723e9352074aaa64b5ddf',
'frozen_analysis/discovery/sgit_hgft_x2.py':'5cd2842e36b8cbc8440ad58b01e630d64c66bddc',
'frozen_analysis/replication/E18_R0_LITERAL_REPLICATION_CONFIG_1_0.json':'e97b004598c93b0e4049bd4069a66da011ef589c',
'frozen_analysis/replication/E18_R0_LITERAL_REPLICATION_PROTOCOL_LOCK.md':'b70a353807bbd4eab9663aa5b995c585466acd5',
'frozen_analysis/replication/E18_R2B_CHANNEL_SELECTION_AMENDMENT.md':'689c55c71a9e2e02b79afbfce7ec59e23c56e6f5',
'frozen_analysis/replication/E18_R2B_CHANNEL_SELECTION_AMENDMENT_1_0.json':'4b676ce42ccbc63a37e7b54f68d491dc54eb4c5',
'frozen_analysis/replication/sgit_e18_r2_final.py':'2cb4599f3eb8aaedd4e0a234deb476c2c5458867',
'supplementary/S1_nominal_montage_coordinates.csv':'fb812e2d51daee8262d4e98dfc3e15e68b8c70c4',
'supplementary/S2_frozen_edges.csv':'db9ed87891ab6e1739cd9fe246269f5c89877003',
'supplementary/S3_frozen_triangles.csv':'d5b67f0610720095870186f6a4c5f4e534dcb9de',
'supplementary/S4_frozen_curl_basis_222x12.csv':'362e6b23e30fb8d054702541d30768b6b1d8d86e',
'supplementary/S5_frozen_gradient_basis_222x12.csv':'193b289cc3037420e6e6d7626ad7e5971dd3f7af',
'supplementary/S6_frozen_mode_ranks.csv':'f528b2a4026dd667faee71127c174bc0ef95c94f',
'supplementary/S7_frozen_hodge_complex_exact.npz':'ec549f94a8cfedfa93f0831afd00817fcf89d5de',
}
def sha_git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\x00'+data).hexdigest()
def sync():
    records=[]
    for path,expected in FILES.items():
        dest=ROOT/'upstream_visual'/path
        if dest.exists() and sha_git_blob(dest.read_bytes())==expected:
            status='VERIFIED_EXISTING'
        else:
            url=f'https://raw.githubusercontent.com/{UPSTREAM}/{COMMIT}/{path}'
            try:
                with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'SGIT-frozen-reproduction'}),timeout=35) as res: data=res.read()
                got=sha_git_blob(data)
                if got!=expected: raise RuntimeError(f'SHA mismatch {path}: {got} != {expected}')
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(data)
                status='VERIFIED_DOWNLOADED'
            except Exception as exc:
                status='FAILED: '+str(exc)
        records.append({'path':path,'expected_git_blob_sha1':expected,'status':status})
        print(status,path,flush=True)
    out=ROOT/'audit_output';out.mkdir(exist_ok=True)
    (out/'upstream_sync.json').write_text(json.dumps({'upstream':UPSTREAM,'commit':COMMIT,'files':records},indent=2),encoding='utf-8')
    if any('FAILED' in r['status'] for r in records):raise SystemExit('Missing upstream files: see audit_output/upstream_sync.json')
    print('All',len(records),'original upstream assets verified against Git SHA-1')
if __name__=='__main__': sync()

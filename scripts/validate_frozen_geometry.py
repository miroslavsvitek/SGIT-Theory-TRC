"""Validate original frozen Hodge geometry using exact upstream CSVs. No fabricated assets."""
import numpy as np,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from sgit.core import incidence
folder=ROOT/'upstream_visual'/'supplementary'
for name in ['S2_frozen_edges.csv','S3_frozen_triangles.csv','S4_frozen_curl_basis_222x12.csv','S5_frozen_gradient_basis_222x12.csv']:
    if not (folder/name).exists():raise SystemExit(f'Missing {name}; first run python scripts/sync_frozen_visual.py')
def csv_numeric(file, columns, fields):
    import csv
    with file.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        missing=[x for x in fields if x not in reader.fieldnames]
        if missing: raise ValueError(f'Missing {missing} in {file}')
        a=np.array([[float(row[field]) for field in fields] for row in reader],float)
    if a.ndim != 2 or a.shape[1] != columns: raise ValueError(f'Unexpected {file} shape {a.shape}')
    return a
edges=csv_numeric(folder/'S2_frozen_edges.csv',2,['i_1based','j_1based']).astype(int)-1
tris=csv_numeric(folder/'S3_frozen_triangles.csv',3,['i_1based','j_1based','k_1based']).astype(int)-1
if edges.shape!=(222,2) or tris.shape!=(216,3):raise ValueError(f'Bad graph sizes {edges.shape} {tris.shape}')
b1,b2=incidence(64,edges,tris)
assert np.linalg.matrix_rank(b1)==63
assert np.linalg.matrix_rank(b2)==153
assert not np.any(b1@b2)
for kind,file in [('C','S4_frozen_curl_basis_222x12.csv'),('G','S5_frozen_gradient_basis_222x12.csv')]:
    a=csv_numeric(folder/file,12,[('curl' if kind=='C' else 'grad')+'_mode_'+str(i) for i in range(1,13)])
    assert a.shape==(222,12), (kind,a.shape)
    assert np.allclose(a.T@a,np.eye(12),atol=1e-5),kind
    if kind=='C':assert np.allclose(b1@a,0,atol=1e-5),kind
    else:assert np.allclose(b2.T@a,0,atol=1e-5),kind
print('PASS: 222 edges, 216 triangles, topology, 12x CURL and GRAD orthonormal bases')

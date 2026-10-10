from pathlib import Path
import json, hashlib, zipfile
ROOT=Path(__file__).resolve().parents[1]
# core config
cfg=json.loads((ROOT/'config/SGIT_CORE_FROZEN.json').read_text())
assert cfg['nodes']==64 and cfg['edges']==222 and cfg['triangles']==216
assert cfg['rank_B1']+cfg['rank_B2']+cfg['harmonic_dim']==222
assert len(cfg['curl_rank_indices_zero_based'])==12
assert len(cfg['grad_rank_indices_zero_based'])==12
# exact no-report transport
T=json.loads((ROOT/'config/MONTAGE60_TEMPLATE_TRANSPORT_R4.json').read_text())
assert T['quality']['PASS'] and len(T['matrix_64x96'])==64 and len(T['matrix_64x96'][0])==96
# result existence/status
expected={
 'G2A_no_report_RESULT.json':'G2A_SWS_REPORT_INDEPENDENCE_NOT_SUPPORTED',
 'G2B0_sensitivity_RESULT.json':'SENSITIVITY_NOT_SUPPORTIVE',
 'G2B1_causal_RESULT.json':'NOT_EVALUABLE_TOO_FEW'}
for f,status in expected.items():
    d=json.loads((ROOT/'results'/f).read_text())
    assert d['status']==status,(f,d['status'])
print('REPOSITORY_METADATA_PASS')

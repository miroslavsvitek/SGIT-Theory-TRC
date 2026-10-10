from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[1]
def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def close(x,y): assert math.isclose(x,y,rel_tol=0,abs_tol=1e-10),(x,y)
def main():
 sws=load('historical_v1_4/results/G2A_no_report_RESULT.json')
 assert sws['N']==16
 assert sws['status']=='G2A_SWS_REPORT_INDEPENDENCE_NOT_SUPPORTED'
 close(sws['median_DeltaPP_SWS'],0.13959292483407815)
 close(sws['p_SWS'],0.0107421875)
 close(sws['p_control'],0.072998046875)
 atlas=load('results/transport_atlas3/TRANSPORT_ATLAS3_RESULT.json')
 assert atlas['evidence_status']=='DEV_MECHANISM_DISSECTION_NOT_INDEPENDENT_REPLICATION'
 assert atlas['scientific_status']=='DISTRIBUTED_6D_TRANSPORT'
 assert all(v['support_tier']=='NO_SUPPORT' for v in atlas['branches'].values())
 assert all(abs(v)<1e-10 for v in atlas['FULL6_continuity']['errors'].values())
 g2b0=load('historical_v1_4/results/G2B0_sensitivity_RESULT.json')
 assert g2b0['status']=='SENSITIVITY_NOT_SUPPORTIVE'
 print('PASS: source JSON evidence checks; NOT a raw-data reanalysis')
if __name__=='__main__':main()

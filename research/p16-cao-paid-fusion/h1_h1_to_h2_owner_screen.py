#!/usr/bin/env python3
"""Identify exact one-FULL-call H1+H1 -> H2 native-fusion obligations.

Reads Cao's frozen 21449-event P16 word; classifies rank-one paid
neighbors by physical register ownership. Screens the precise full
18-call arithmetic improvement at kappa=0.0030220. Does not confer
free multi-register tensors or prove an admissible physical call.
"""
from collections import Counter
from decimal import Decimal,localcontext
from hashlib import sha256
from pathlib import Path
import gzip,json,sys
HERE=Path(__file__).resolve().parent
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE.parents[2]
W=ROOT/'research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz'
pin=json.loads((ROOT/'research/kappa-round3-warp-20261022/ACTUAL-WORD-FREEZE.json').read_text())
raw=gzip.decompress(W.read_bytes())
assert sha256(raw).hexdigest()==pin['canonical_payload_sha256']
data=json.loads(raw)
cert=json.loads((ROOT/'research/kappa-round6-compiler-tightening-20261022/ARITHMETIC.json').read_text())
assert cert['kappa']=='15108879/5000000000'
P=Counter({int(k):v for k,v in cert['paid'].items()})
T=Counter({int(k):v for k,v in cert['targets'].items()})
assert sum(P.values())==64404 and sum(T.values())==10928
assert P[1]>36 and P[2]>0
changed=P.copy();changed[1]-=36;changed[2]+=18
assert sum(P.values())-sum(changed.values())==18
assert sum(r*v for r,v in P.items())==sum(r*v for r,v in changed.items())
with localcontext() as ctx:
    ctx.prec=65
    t=Decimal(1)-Decimal('.0030220')
    moment=lambda pp:sum(Decimal(r)**t*v for r,v in T.items())-sum(Decimal(r)**t*v for r,v in pp.items())
    original,proposed=moment(P),moment(changed)
    assert original<0<proposed
    gain=proposed-original
analysis={}
for orientation,word in data['programs'].items():
    assert sum(e[0]=='climb' for e in word)==3290
    assert sum(e[0]=='center' for e in word)==8
    one=[(i,e) for i,e in enumerate(word) if e[0]=='climb' and e[5]==1]
    assert len(one)==2201
    adjacent=[(a,b) for a,b in zip(one,one[1:]) if b[0]==a[0]+1]
    same=[(a,b) for a,b in adjacent if a[1][2]==b[1][2]]
    distinct=[(a,b) for a,b in adjacent if a[1][2]!=b[1][2]]
    assert len(adjacent)==len(same)+len(distinct)
    examples=[{'left_index':a[0],'right_index':b[0],
               'left_register':a[1][2],'right_register':b[1][2],
               'left_frame_pair':a[1][3:5],'right_frame_pair':b[1][3:5],
               'joint_operator_admitted':False} for a,b in distinct[:12]]
    analysis[orientation]={
        'native_event_count':len(word),
        'rank1_jobs':len(one),
        'adjacent_rank1_pairs':len(adjacent),
        'adjacent_same_L_register':len(same),
        'adjacent_distinct_L_register':len(distinct),
        'source_exact_candidate_examples':examples,
        'direct_one_field_rank2_fusion_witnesses':0}
assert analysis['forward']['adjacent_same_L_register']==0
assert analysis['backward']['adjacent_same_L_register']==0
receipt={'status':'PASS_EXACT_H1_FUSION_PHYSICAL_OWNERSHIP_SCREEN',
    'source_sha':'20bb93cd990d2ff683e4d0fc56b87a42cd5d3296',
    'native_word_sha256':pin['canonical_payload_sha256'],
    'goal_kappa':'0.0030220',
    'whole_paid_rank_delta':{'H1':-36,'H2':18},
    'whole_paid_jobs_before':64404,
    'whole_paid_jobs_counterfactual':64404-18,
    'productive_outputs':10928,
    'rank_surplus':752,
    'baseline_moment_at_goal':str(original),
    'counterfactual_moment_at_goal':str(proposed),
    'hypothetical_exact_gain':str(gain),
    'physical_ownership_still_open':True,
    'physical_fusion_admitted':False,
    'new_kappa_proved':False,
    'native_orientations':analysis}
(HERE/'H1_FUSION_OWNER_SCREEN_RECEIPT.json').write_text(
    json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print(receipt['status'],'desired_gain',gain)
for d,v in analysis.items():
    print(d,'H1',v['rank1_jobs'],
          'adjacent_pairs',v['adjacent_rank1_pairs'],
          'same_register',v['adjacent_same_L_register'],
          'different_register',v['adjacent_distinct_L_register'])
print('COUNTERFACTUAL_MOMENT',proposed,'PHYSICAL_ADMISSION_OPEN')

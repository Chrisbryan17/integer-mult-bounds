#!/usr/bin/env python3
"""Audit all 16 prefix/suffix allocations against Cao's frozen P16 invoice.

The screen uses the exact source formula from query-thinned-controllers
controller.py inventories(): for each prefix length a and b=15-a, two
224-copy diagonal targets of rank 1+8(j+1), and idle 224-copy jobs
of rank 8(j+1), j=1..length. This is an invoice comparison, not
a construction or factorization proof for unselected allocations.
"""
from collections import Counter
from decimal import Decimal,localcontext
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE.parents[2]
native=json.loads((ROOT/'research/kappa-round3-warp-20261022/NATIVE-VALIDATION.json').read_text())
cert=json.loads((ROOT/'research/kappa-round6-compiler-tightening-20261022/ARITHMETIC.json').read_text())
assert native['status']=='PASS_JOINT_HELPER_MAPS_NATIVE_BOTH_632_INTERPRETERS'
assert cert['kappa']=='15108879/5000000000'
H=Counter({int(k):v for k,v in native['helpers'].items()})
P=Counter({int(k):v for k,v in native['paid'].items()})
assert H==Counter({4:28,7:7,8:47,9:326})
assert P==Counter({1:2201,2:412,3:510,4:127,5:40,8:8})
def hist(a):
    assert 0<=a<=15
    t=Counter({k:18*v for k,v in H.items()})
    p=Counter({k:18*v for k,v in P.items()});p[1]+=15*112
    t[145]+=224
    for length in (a,15-a):
        for j in range(1,length+1):
            t[1+8*(j+1)]+=224
            p[8*(j+1)]+=224
    return +t,+p
baselineT,baselineP=hist(7)
assert baselineT==Counter({int(k):v for k,v in cert['targets'].items()})
assert baselineP==Counter({int(k):v for k,v in cert['paid'].items()})
with localcontext() as ctx:
    ctx.prec=70
    kappa=Decimal(15108879)/Decimal(5000000000)
    theta=1-kappa
    def moment(t,p):
        return sum(Decimal(r)**theta*n for r,n in t.items())-sum(Decimal(r)**theta*n for r,n in p.items())
    baseline=moment(baselineT,baselineP)
    assert baseline>0
    rows=[]
    for a in range(16):
        t,p=hist(a)
        assert sum(t.values())==10928 and sum(p.values())==64404
        assert sum(r*v for r,v in t.items())-sum(r*v for r,v in p.items())==752
        score=moment(t,p)
        rows.append({'prefix':a,'suffix':15-a,'moment':str(score),'delta_from_a7':str(score-baseline),
                     'is_construction_verified':a==7})
    assert rows[7]['moment']==rows[8]['moment']
    assert all(Decimal(row['moment'])<baseline for row in rows if row['prefix'] not in (7,8))
    assert all(Decimal(rows[i]['moment'])>Decimal(rows[i-1]['moment']) for i in range(1,8))
    assert all(Decimal(rows[i]['moment'])<Decimal(rows[i-1]['moment']) for i in range(9,16))
report={'status':'PASS_16_SPLITS_EXACT_SOURCE_HISTOGRAM',
        'model':'Frozen P16 p=16, 18 LOCAL, 15 QUERY_SHEAR, a+b=15, source diagonal and idle counts',
        'source_native_sha':native['actual_word_canonical_sha256'],
        'selected_kappa':'15108879/5000000000',
        'selected_prefix':7,'symmetric_equivalent_prefix':8,
        'unique_best_histo_pairs':[[7,8],[8,7]],
        'baseline_controller_factorization_reused':True,
        'alternate_factorizations_or_physical_execution_not_proved':True,
        'controller_redesign_beats_Cao':False,
        'new_kappa_proved':False,'rows':rows}
(HERE/'CONTROLLER_16_SPLIT_RECEIPT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(report['status'],'selected_margin',rows[7]['moment'])
print('ALL_OTHER_SPLITS_STRICTLY_WORSE; a=8 HISTOGRAM TIED BUT NEW FACTORIZATION NOT ADMITTED')

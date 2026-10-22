#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent high-precision numerical regression, NOT the exact proof engine."""
from decimal import Decimal as D,localcontext
from collections import Counter
import json
from pathlib import Path
H={4:28,7:7,8:47,9:326}
P={1:2237,2:388,3:494,4:147,5:36,8:8}
def moment(hist,k):
    t=D(1)-k
    return sum(D(v)*((t*D(r).ln()).exp()) for r,v in hist.items())
def score(p,a,k):
    tgt=Counter({r:v*(p+2) for r,v in H.items()})
    paid=Counter({r:v*(p+2) for r,v in P.items()})
    tgt[8*p+17]+=224
    paid[1]+=112*(p-1)
    for arm in (a,p-1-a):
        for j in range(1,arm+1):
            tgt[8*j+9]+=224
            paid[8*j+8]+=224
    return moment(tgt,k)-moment(paid,k)
def verify():
    with localcontext() as ctx:
        ctx.prec=65
        k=D('0.0030201659770156204897')
        x={p:score(p,(p-1)//2,k) for p in range(2,101)}
        assert x[16]>x[15] and x[16]>x[17]
        assert all(x[16]>x[p] for p in x if p!=16)
        assert abs(x[16])<D('0.000000001')
        v={p:score(p,(p-1)//2,D('0.006')) for p in range(2,101)}
        assert max(v,key=v.get)==2
        assert all(val<0 for val in v.values())
        for p in range(2,40):
            vals=[score(p,a,k) for a in range(p)]
            assert max(vals)==vals[(p-1)//2]
        return {'status':'PASS_NUMERICAL_CROSS_CHECK_NOT_THEOREM',
                'decimal_precision':65,'pairs_tested':99,
                'p16_margin_near_root':str(x[16]),
                'p16_minus_p15':str(x[16]-x[15]),
                'p17_minus_p16':str(x[17]-x[16]),
                'p2_margin_at_0_006':str(v[2]),'new_kappa':False}
if __name__=='__main__':
    x=verify()
    Path(__file__).with_name('CONTROLLER_FAMILY_NUMERIC_CHECK.json').write_text(json.dumps(x,indent=2)+'\n')
    print('PASS_INDEPENDENT_65DIGIT_PAIR_SPLIT_REGRESSION')

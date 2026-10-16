#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent positive-Mercator exact fixed-point/Taylor historical P104
moment enclosure. This DOES NOT check the 448-ADD borrowed-dirty invoice.
"""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
C=json.loads((ROOT/'SELECTED_HISTORICAL_MOMENT_SNAPSHOT.json').read_text())
m=int(C['m']);replicas=int(C['replicas']);calls=9*replicas
assert m==73 and calls==144
p={int(k):int(v) for k,v in C['complex_profile'].items()}
p[8]-=8*calls;p[7]+=8*calls
for rank in (1,1,1,5,1,1,4,1,1):p[rank]-=8*calls
p[48]-=8*9*replicas
assert sum(k*v for k,v in p.items())==m*13312-5248
assert all(v>=0 for v in p.values())
b=F(C['selected_complex_b']); W=13312
# ln(m/r)=sum_{k>=1} z^k/k; z=(m-r)/m lies in [0,1).
# All enclosure decisions use exact integer arithmetic; not floats.
S=10**48;N=2800;K=11

def mercator(r):
    assert 0<r<m
    n=m-r; d=m
    lo=hi=0
    powerlo=powerhi=S
    for k in range(1,N+1):
        powerlo=(powerlo*n)//d
        powerhi=(powerhi*n+d-1)//d
        lo+=powerlo//k
        hi+=(powerhi+k-1)//k
    # Rigorous tail bound z^(N+1)/((N+1)*(1-z)).
    tail=F(powerhi*n,(N+1)*r)
    cap=tail.numerator//tail.denominator+int(tail.numerator%tail.denominator!=0)
    return F(lo,S),F(hi+cap,S)

def exp_pair(a,bound):
    assert F(0)<=a<=bound<F(1,10)
    def partial(x):
        total=term=F(1)
        for k in range(1,K+1):
            term=term*x/k
            total+=term
        return total,term*x/F(K+1)
    lo,_=partial(a)
    hi,nextterm=partial(bound)
    return lo,hi+nextterm/(1-bound/F(K+2))

sum_lo=sum_hi=F(0)
for rank,count in sorted(p.items()):
    if not count:continue
    l,h=mercator(rank)
    el,eh=exp_pair(b*l,b*h)
    sum_lo+=count*rank*el
    sum_hi+=count*rank*eh
lo=sum_lo/F(m*W);hi=sum_hi/F(m*W)
assert hi-lo<F(1,10**20)
cases={}
for delta in (0,1,2):
    a=lo+F(delta*calls,m*W)-1
    z=hi+F(delta*calls,m*W)-1
    assert z<0 if delta<2 else a>0
    cases[str(delta)]='negative' if delta<2 else 'positive'
assert F(1915,1000)<(1-hi)*m*W/calls
assert (1-lo)*m*W/calls<F(1917,1000)
result={
 'status':'PASS_EXACT_HISTORICAL_MOMENT_ONLY',
 'method':'positive Mercator log with fixed-point outward integer interval, exp Taylor bound',
 'terms':{'mercator':N,'exp':K},'denominator':str(S),
 'conditions':cases,'headroom_rank_units':{'lower':'1.915','upper':'1.917'},
 'moment_interval_width_lt':'1e-20','borrowed_dirty_448_ADD_word_check':False,
 'full_recursive_invoice':False,'new_kappa':False
}
(ROOT/'P104_MERCATOR_MOMENT_RECEIPT.json').write_text(
    json.dumps(result,sort_keys=True,indent=2)+'\n')
print('PASS_P104_INDEPENDENT_EXACT_MERCATOR historical_only '
      '0_EXTRA_NEG 1_EXTRA_NEG 2_EXTRA_POS '
      'borrowed_word_complete_invoice_OPEN')

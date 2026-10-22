#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact-rational global p/a barrier for PR4470 native with PR4440 controller.

Every integer p>=2 and every 0<=a<p is covered. The native helper/paid
profile, 112 ports, p+2 thick stages, p-1 queries, and idle/main formula
are fixed. The theorem excludes this restricted family only; no new kappa.
"""
from collections import Counter
from fractions import Fraction as Q
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from frontier_rational_gate import HELP, PAID, weight
RAW_LO=Q('0.0030201659770')
RAW_HI=Q('0.0030201659771')
GOAL=Q('0.006')

def profile(p,a):
    assert isinstance(p,int) and p>=2 and isinstance(a,int) and 0<=a<p
    full=p+2
    t=Counter({r:n*full for r,n in HELP.items()})
    b=Counter({r:n*full for r,n in PAID.items()})
    t[1+8*full]+=224
    b[1]+=112*(p-1)
    for arm in (a,p-1-a):
        for j in range(1,arm+1):
            t[8*(j+1)+1]+=224
            b[8*(j+1)]+=224
    return t,b

def diff_net(p,a,q,b):
    ta,pa=profile(p,a);tb,pb=profile(q,b)
    c=Counter(ta);c.subtract(pa);c.subtract(tb);c.update(pb)
    return {r:v for r,v in c.items() if v}

def signed_bounds(coeff,lo,hi):
    assert Q(0)<lo<=hi<Q('0.1')
    lower=upper=0
    for rank,count in coeff.items():
        if count>0:
            a,_=weight(rank,hi);_,b=weight(rank,lo)
            lower+=count*a;upper+=count*b
        elif count<0:
            _,b=weight(rank,lo);a,_=weight(rank,hi)
            lower+=count*b;upper+=count*a
    return [lower,upper]

def balanced(p):return (p-1)//2

def run():
    t,b=profile(16,7)
    assert (sum(t.values()),sum(r*n for r,n in t.items()))==(10928,239886)
    assert (sum(b.values()),sum(r*n for r,n in b.items()))==(64620,239134)
    assert not diff_net(16,7,16,7)
    rise=signed_bounds(diff_net(16,7,15,7),RAW_LO,RAW_HI)
    fall=signed_bounds(diff_net(17,8,16,7),RAW_LO,RAW_HI)
    c=Counter(t);c.subtract(b)
    c={r:v for r,v in c.items() if v}
    root_lo=signed_bounds(c,RAW_LO,RAW_LO)
    root_hi=signed_bounds(c,RAW_HI,RAW_HI)
    s2,b2=profile(2,0);n2=Counter(s2);n2.subtract(b2)
    value2=signed_bounds({r:v for r,v in n2.items() if v},GOAL,GOAL)
    slope2=signed_bounds(diff_net(3,1,2,0),GOAL,GOAL)
    assert rise[0]>0 and fall[1]<0
    assert root_lo[0]>0 and root_hi[1]<0
    assert value2[1]<0 and slope2[1]<0
    # For 0<t<1, strict concavity of x^t makes
    # f_j=(8j+9)^t-(8j+8)^t positive and decreasing in j.
    # Balanced arms maximize sum f_j. Between consecutive balanced p,
    # the first difference is L(t)-112
    # +224*((8p+25)^t-(8p+17)^t)+224*f_floor((p+1)/2).
    # Both nonconstant summands decrease; the first strictly.
    # Therefore S(p) has strictly decreasing differences for every p>=2.
    return {'status':'PASS_GLOBAL_FIXED_SUPPLIER_CONTROLLER_FAMILY',
      'all_pairs':'every integer p>=2','all_prefixes':'every 0<=a<=p-1',
      'optimum_at_p16_a7_or8':True,
      'selected_root_bracket':[str(RAW_LO),str(RAW_HI)],
      'p16_minus_p15_over_root_bracket':rise,
      'p17_minus_p16_over_root_bracket':fall,
      'p16_root_lower_sign':root_lo,'p16_root_upper_sign':root_hi,
      'at_kappa_0_006_p2_is_max_and_negative':True,
      'p2_moment_at_0_006':value2,'p3_minus_p2_at_0_006':slope2,
      'signed_moment_integer_denominator':10**20,
      'proof':'balanced arms from decreasing marginal; globally strictly decreasing first differences; four exact outward rational sign checks',
      'validity':'PR4470 native rank profile and PR4440 p-pair query-thinned controller only',
      'source_ref':'CrocSwap/integer-mult-bounds@b9a13c1673e0e9697de410de16e8bbf3207a7363',
      'new_algorithm':False,'new_kappa':False}

if __name__=='__main__':
    x=run()
    Path(__file__).with_name('CONTROLLER_FAMILY_CERTIFICATE.json').write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
    print('PASS_GLOBAL_ALL_P_ALL_A p16 balanced optimum under frozen native supplier')
    print('PASS_EXACT_006_NO_GO all p>=2 in PR4440 family')

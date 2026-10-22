#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fail-closed exact moment test for the smallest useful P16 rank exchange.

One *hypothetical whole-controller occurrence* changes an existing rank-4
productive field to rank 5 AND a rank-8 paid child to rank 9.
Both total rank masses increase by one, preserving rank surplus.
This is NOT a legitimate circuit until both operators are shown equivalent
for arbitrary inputs with physical source/owner/phase and tape tariffs.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from decimal import Decimal,localcontext
from pathlib import Path
import json

HELP={4:28,7:7,8:47,9:326}
PAID_LOCAL={1:2237,2:388,3:494,4:147,5:36,8:8}
MAIN={145:224,73:224,**{r:448 for r in (17,25,33,41,49,57,65)}}
IDLE={72:224,**{r:448 for r in (16,24,32,40,48,56,64)}}
TARGET_KAPPA=Q('0.00302017')
SCALE=10**22
def hist(*sections):
 c=Counter()
 for part in sections:c.update(part)
 return +c
def weighted(base,factor):return {r:v*factor for r,v in base.items()}
def count(h):return sum(h.values()),sum(k*v for k,v in h.items())
def log_bounds(n,terms=34):
 if n==1:return Q(0),Q(0)
 e=n.bit_length()-1;u=Q(n,2**e)
 def logu(x):
  z=(x-1)/(x+1);p=z;total=Q(0)
  for k in range(terms):
   total+=2*p/(2*k+1);p*=z*z
  return total,total+2*p/((2*terms+1)*(1-z*z))
 a,b=logu(Q(2));c,d=logu(u)
 return e*a+c,e*b+d
def expminus(x,n):
 v=Q(1);s=v
 for k in range(1,n+1):v*=-x/k;s+=v
 return s
@lru_cache(None)
def weight(rank,k):
 if rank==1:return SCALE,SCALE
 la,lb=log_bounds(rank)
 xa,xb=k*la,k*lb
 assert Q(0)<xa<=xb<Q(1)
 low=rank*expminus(xb,35)*SCALE
 high=rank*expminus(xa,36)*SCALE
 return low.numerator//low.denominator, -(-high.numerator//high.denominator)
def interval(t,p,k):
 low=hi=0
 for r,n in t.items():
  if n:
   a,b=weight(r,k);low+=n*a;hi+=n*b
 for r,n in p.items():
  if n:
   a,b=weight(r,k);low-=n*b;hi-=n*a
 return {'lower_scaled':low,'upper_scaled':hi,'scale':SCALE,
         'lower_decimal':str(Decimal(low)/SCALE),
         'upper_decimal':str(Decimal(hi)/SCALE)}
def run():
 t=hist(MAIN,weighted(HELP,18))
 p=hist(IDLE,weighted(PAID_LOCAL,18),{1:1680})
 assert count(t)==(10928,239886)
 assert count(p)==(64620,239134)
 bad=interval(t,p,TARGET_KAPPA)
 assert bad['upper_scaled']<0
 T=t.copy();P=p.copy()
 T[4]-=1;T[5]+=1
 P[8]-=1;P[9]+=1
 assert T[4]>=0 and P[8]>=0
 assert count(T)==(10928,239887)
 assert count(P)==(64620,239135)
 assert count(T)[1]-count(P)[1]==752
 good=interval(T,P,TARGET_KAPPA)
 assert good['lower_scaled']>0
 # Independent high-precision Decimal evaluation of each histogram.
 with localcontext() as ctx:
  ctx.prec=70
  x=Decimal(TARGET_KAPPA.numerator)/Decimal(TARGET_KAPPA.denominator)
  alpha=1-x
  score=lambda a,b: sum(Decimal(r)**alpha*n for r,n in a.items())-sum(Decimal(r)**alpha*n for r,n in b.items())
  original=score(t,p);altered=score(T,P)
  gain=(Decimal(5)**alpha-Decimal(4)**alpha)-(Decimal(9)**alpha-Decimal(8)**alpha)
  assert original<0<altered
  assert abs((altered-original)-gain)<Decimal('1e-58')
  independent={'baseline_deficit':str(-original),
               'balanced_exchange_moment_gain':str(gain),
               'hypothetical_margin_at_target':str(altered)}
 # Incumbent local geometry has 8 rank-eight centre children per full call;
 # 28 productive rank-four helpers, 18 full-call uses.
 # Those counts ensure the screened ranks EXIST; NOT feasibility of the
 # simultaneous operator-preserving exchange.
 assert PAID_LOCAL[8]==8 and HELP[4]==28
 assert TARGET_KAPPA>Q('0.0030201659771')
 result={'schema':'p16-target-00302017-neutral-rank-exchange-screen/1',
  'status':'PASS_EXACT_RATIONAL_SCREEN_ONLY',
  'source':'CrocSwap/integer-mult-bounds@b9a13c1673e0e9697de410de16e8bbf3207a7363',
  'selected_kappa':'0.00302015','pending_open_kappa':'0.00302016597',
  'requested_kappa':'0.00302017',
  'baseline_moment':bad,'counterfactual_moment':good,
  'independent_decimal_70digit_check':independent,
  'target_changes':{'rank4_productive':-1,'rank5_productive':1},
  'paid_changes':{'rank8_child':-1,'rank9_child':1},
  'whole_controller_productive_fields':10928,'whole_controller_paid_jobs':64620,
  'rank_surplus_before_and_after':752,
  'candidate_native_positive_operator_admitted':False,
  'candidate_global_phase_and_both_orientations':'UNPROVED',
  'productive_ownership_source_and_tape':'UNPROVED',
  'uniform_all_size_and_BIT_outer':'UNPROVED',
  'new_kappa_proved':False,
  'interpretation':'One paid rank8->9 and productive rank4->5 exchange could cross 0.00302017 while preserving counts and rank surplus, but no physical operator witness exists.'}
 pth=Path(__file__).with_name('RANK_EXCHANGE_SCREEN_RESULT.json')
 pth.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print('PASS_P16_00302017_EXACT_MOMENT_SCREEN')
 print('BASELINE_DEFICIT',independent['baseline_deficit'])
 print('PAIRED_EXCHANGE_GAIN',independent['balanced_exchange_moment_gain'])
 print('HYPOTHETICAL_MARGIN',independent['hypothetical_margin_at_target'])
 print('NATIVE_ADMISSION_OPEN, NEW_KAPPA_FALSE')
 return result
if __name__=='__main__':run()

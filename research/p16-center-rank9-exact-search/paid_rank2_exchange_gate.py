#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact-rational screen, not admission, for paid F2+F2 -> F1+F3."""
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'p16-k00302017-rank-exchange'))
from rank_exchange_screen import (hist,weighted,HELP,PAID_LOCAL,MAIN,IDLE,interval,TARGET_KAPPA)
T=hist(MAIN,weighted(HELP,18))
P=hist(IDLE,weighted(PAID_LOCAL,18),{1:1680})
assert (sum(P.values()),sum(r*n for r,n in P.items()))==(64620,239134)
old=interval(T,P,TARGET_KAPPA)
p=P.copy();p[2]-=2;p[1]+=1;p[3]+=1
assert (sum(p.values()),sum(r*n for r,n in p.items()))==(64620,239134)
new=interval(T,p,TARGET_KAPPA)
assert old['upper_scaled']<0<new['lower_scaled']
report={'status':'PASS_EXACT_MOMENT_ONLY','kappa':'0.00302017',
 'paid_exchange':{'F1':1,'F2':-2,'F3':1},
 'rank_mass_preserved':True,'productive_outputs_unchanged':True,
 'old_moment':old,'new_moment':new,
 'physical_operator':'UNCONSTRUCTED','new_kappa':False}
(HERE/'PAID_RANK2_EXCHANGE_RECEIPT.json').write_text(
 json.dumps(report,sort_keys=True,indent=2)+'\n')
print('PASS_EXACT_F2_PAIR_SCREEN_AND_PHYSICAL_UNCONSTRUCTED')

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact restricted no-go: extending a rank-4 helper exit alone cannot
improve the native target-minus-paid moment in the monotone frame compiler.

If the previous endpoint is reached by a last native rank-r positive
transport with r<=4, a one-dimensional terminal extension charges rank
r->r+1, while productive rank increases 4->5. Strict concavity of x^t,
0<t<1, makes gain nonpositive; any newly created F1 is even costlier.
This does not forbid coupled centre/helper transformations.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from rank_exchange_screen import weight,SCALE,TARGET_KAPPA
def interval_diff(a,b,c,d):
 # (w(a)-w(b))-(w(c)-w(d)), outward interval.
 al,au=weight(a,TARGET_KAPPA);bl,bu=weight(b,TARGET_KAPPA)
 cl,cu=weight(c,TARGET_KAPPA);dl,du=weight(d,TARGET_KAPPA)
 return [al-bu-cu+dl,au-bl-cl+du]
def run():
 cases={}
 for r in range(0,5):
  if r==0:
   # newly created rank-one Fourier child, paid +1.
   reward_lower,reward_upper=weight(5,TARGET_KAPPA)
   base_lower,base_upper=weight(4,TARGET_KAPPA)
   low,hi=reward_lower-base_upper-SCALE,reward_upper-base_lower-SCALE
  else:low,hi=interval_diff(5,4,r+1,r)
  if r==4:assert low<=0<=hi
  else:assert hi<0,(r,low,hi)
  cases[str(r)]={'scaled_lower':low,'scaled_upper':hi,
    'description':'existing terminal F-r increased to F-(r+1)' if r else 'new terminal F1'}
 assert len(cases)==5
 out={'status':'PASS_RESTRICTED_MONOTONE_EXIT_NO_GO',
   'κ_test':'0.00302017','productive_rank':'4→5',
   'terminal_native_paid_rank_range':'0..4',
   'moment_delta_upper_nonpositive_all':True,
   'strictly_negative_unless_original_last_child_rank4':True,
   'scope':'Only one helper terminal enlargement in the existing monotone chart chronology, with no global rewrites or centre interactions',
   'new_kappa_proved':False,'cases':cases}
 (P/'TERMINAL_EXTENSION_NO_GO.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print('PASS_TERMINAL_ONLY_HELPER_R4_TO_R5_NO_KAPPA')
 return out
if __name__=='__main__':run()

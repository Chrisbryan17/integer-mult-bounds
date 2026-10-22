#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact PR4470 full 32x32 Laurent miter for postponing 8 tail idle jobs.
Physical weighted ADD and output mask charges remain OPEN.
"""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p16_coupled_query_miter import original,replay,Z,mono,add,shift
def virtual(events,corrupt=False):
 n=32
 rows=[[({Z:1} if i==j else {}) for j in range(n)] for i in range(n)]
 tags=[[0]*33 for _ in range(n)]
 last=max(i for i,e in enumerate(events) if e[0]=='LOCAL')
 deferred=[];weighted=[]
 for i,e in enumerate(events):
  k=e[0]
  if k=='IDLE':
   _,pair,stages=e
   if i>last:
    deferred.append(i)
    for r in (2*pair,2*pair+1):
     for s in stages:tags[r][s]+=1
   else:
    d=mono(stages=stages)
    for r in (2*pair,2*pair+1):rows[r]=[shift(p,d) for p in rows[r]]
  elif k=='ADD':
   _,dst,src,sgn=e
   delta=tuple([0]+[a-b for a,b in zip(tags[src],tags[dst])])
   if any(delta):weighted.append(i)
   rows[dst]=[add(a,shift(b,delta,sgn)) for a,b in zip(rows[dst],rows[src])]
  elif k in ('LOCAL','QUERY_SHEAR'):
   _,stage,pair,back=e
   x,y=(2*pair+1,2*pair) if back else (2*pair,2*pair+1)
   assert not any(tags[x]) and not any(tags[y]),'Native conjugation is NOT free'
   term=mono(1 if back else -1)
   rows[y]=[add(a,shift(b,term,-1 if back else 1)) for a,b in zip(rows[y],rows[x])]
   if k=='LOCAL':
    d=mono(stages=[stage])
    for r in (x,y):rows[r]=[shift(p,d) for p in rows[r]]
  elif k=='SIGNED_SWAP':
   _,a,b=e
   rows[a],rows[b]=rows[b],[shift(p,Z,-1) for p in rows[a]]
   tags[a],tags[b]=tags[b],tags[a]
  else:raise AssertionError(e)
 terminal=[i for i,t in enumerate(tags) if any(t)]
 if corrupt:terminal=terminal[1:]
 for i in terminal:rows[i]=[shift(p,tuple([0]+tags[i])) for p in rows[i]]
 return rows,deferred,weighted,tags
def run():
 events=original()
 reference=replay(events)
 new,deferred,weighted,tags=virtual(events)
 assert new==reference and len(deferred)==8 and len(weighted)==18
 assert virtual(events,True)[0]!=reference
 assert sum(bool(any(t)) for t in tags)==16
 paid_original=8*sum(len(events[i][2]) for i in deferred)
 terminal_proxy=8*sum(sum(t) for t in tags)
 assert (paid_original,terminal_proxy)==(352,704)
 result={'status':'PASS_EXACT_32x32_LAURENT_TAIL',
 'deferred_IDLES':8,'new_weighted_ADDs':18,'remaining_terminal_monomial_masks':16,
 'original_shared_IDLE_rank_mass_per_port':352,
 'independent_terminal_mask_rank_mass_proxy_per_port':704,
 'native_opaque_gate_tag_conflicts':0,'matrix_coefficients_exact':1024,
 'terminal_mask_mutation':'REJECTED',
 'source_owner_and_boundary_fusion_cost':'UNPRICED',
 'claim':'Deferral is algebraically exact, but does not erase determinant; naive per-output materialization doubles the rank-mass proxy.',
 'new_kappa':False}
 (P/'TAIL_IDLE_FULL_MITER.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print('PASS_P16_TAIL_IDLE_DEFER 8_IDLE 18_WEIGHTED_ADD 16_FINAL_MASK 352_to_704_proxy')
 return result
if __name__=='__main__':run()

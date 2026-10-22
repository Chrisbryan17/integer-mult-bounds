#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact P16 right-tail Laurent stage-major batch and determinant no-go.

The formal b=2 shared-stage price makes the P16 0.006 moment positive,
but would UNDERPAY the Laurent determinant. The existing physical supplier
does not admit an independent four-field shift for one old rank-8 child.
"""
from pathlib import Path
from collections import defaultdict
import sys,json
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p16_coupled_query_miter import original,replay
from frontier_rational_gate import profiles,moment_interval
def stage_major(source,capacity):
 last=max(i for i,e in enumerate(source) if e[0]=='LOCAL')
 pos=[i for i,e in enumerate(source) if e[0]=='IDLE' and i>last]
 assert len(pos)==8 and pos==list(range(pos[0],pos[0]+8))
 masks={source[i][1]:source[i][2] for i in pos}
 by_stage=defaultdict(list)
 for pair,stages in masks.items():
  for stage in stages:by_stage[stage].append(pair)
 assert sorted(len(v) for v in by_stage.values())==[1,2,3,4,5,6,7,8,8]
 macros=[]
 for stage,pairs in sorted(by_stage.items()):
  pairs=sorted(pairs)
  for j in range(0,len(pairs),capacity):
   macros.append(['BATCH_STAGE',stage,pairs[j:j+capacity]])
 # Only the expansion into ORIGINAL, PAID, one-pair IDLE gates is admitted.
 expanded=[['IDLE',pair,[m[1]]] for m in macros for pair in m[2]]
 rewritten=source[:pos[0]]+expanded+source[pos[-1]+1:]
 assert replay(source)==replay(rewritten)
 return masks,by_stage,macros
def run():
 source=original();target,paid=profiles()
 report={}
 for capacity in (1,2,3,4,8):
  masks,stages,macros=stage_major(source,capacity)
  count=len(macros)
  oldmass=sum(8*len(v) for v in masks.values())
  assert oldmass==352
  actual_exponent=sum(2*len(v) for v in stages.values())
  proposed_exponent=2*count
  assert actual_exponent==88
  p=paid.copy()
  for stage_list in masks.values():
   r=8*len(stage_list)
   p[r]-=112;assert p[r]>=0
  p[8]+=112*count
  moment=moment_interval(target,p,'0.006')
  report[str(capacity)]={'formal_batch_count':count,
    'real_existing_rank8_single_pair_lowerings':44,
    'required_Laurent_determinant_degree':actual_exponent,
    'hypothetical_paid_determinant_degree':proposed_exponent,
    'unpaid_determinant_degree':actual_exponent-proposed_exponent,
    'real_single_pair_rank_mass':oldmass,
    'hypothetical_rank8_mass':8*count,
    'kappa_0_006_counterfactual_moment_only':moment,
    'real_physical_batch_child_admitted':False}
 assert report['1']['kappa_0_006_counterfactual_moment_only']['negative']
 assert report['2']['kappa_0_006_counterfactual_moment_only']['positive']
 assert report['2']['formal_batch_count']==24
 assert report['2']['unpaid_determinant_degree']==40
 result={'status':'PASS_EXACT_STAGE_MAJOR_OPERATOR_WITH_DETERMINANT_REJECTION',
   'source_event_sha256':'624305383d5e7e1687e01356d5e41ff4ee3d4f06b3cab71cf9a65ea22fc8dd52',
   'tail_IDLES':8,'distinct_stage_axes':9,
   'stage_multiplicities':[1,2,3,4,5,6,7,8,8],
   'batch_screens':report,
   'interpretation':'A new two-pair rank8 native shift needs z^4 determinant per stage, whereas existing one-pair rank8 shift carries z^2. All independent input ports must be preserved and paid.',
   'physical_owner_tape_productive_credit':'OPEN',
   'actual_new_kappa':False}
 (P/'P16_STAGE_MAJOR_BATCH_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print('PASS_P16_STAGE_MAJOR_EXACT_AND_DET_NO_GO W2_24_calls 40_UNPAID_DETERMINANT no_kappa')
 return result
if __name__=='__main__':run()

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact integral typed-numerator P104 side correction I-G/2.
After all 104 sources enter the zero chart, add twice each matching source
to its target numerator. Negate the eight aggregate carriers during core,
restore them afterwards. No fractional ops or additional CLEAN scratch.
Owner/caller precision and global supplier remain OPEN.
"""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
W=json.loads((P/'P104_INPLACE_DYADIC_WORD.json').read_text())
B=json.loads((P/'P104_INPLACE_SOURCE_WORD.json').read_text())
O=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
zero=O['frames'].index([])
ev=W['events']
sources=[i for i,e in enumerate(ev) if e[0]=='source_to_zero']
assert sources==list(range(sources[0],sources[0]+104))
after_sources=sources[-1]+1
identity=[['add','Y'+str(t),'S'+str(t),1,zero]
          for t in range(104) for duplicate in range(2)]
pivots=B['pivots'];enter=[];leave=[]
for i,p in enumerate(pivots):
    name='S'+str(p)
    moves=[(j,e) for j,e in enumerate(ev)
           if e[0]=='transport' and e[1]==name]
    incoming=[(j,e) for j,e in moves
              if e[2]==zero and len(O['frames'][e[3]])==1]
    outgoing=[(j,e) for j,e in moves
              if e[3]==zero and len(O['frames'][e[2]])==1]
    assert len(incoming)==len(outgoing)==1
    enter.append(incoming[0]);leave.append(outgoing[0])
i0=max(j for j,e in enter)+1
i1=min(j for j,e in leave)
assert after_sources<i0<i1
minus=[['sign','S'+str(p),-1,enter[i][1][3]]
       for i,p in enumerate(pivots)]
unminus=[['sign','S'+str(p),-1,leave[i][1][2]]
         for i,p in enumerate(pivots)]
events=[]
for at,e in enumerate(ev):
    if at==after_sources:events+=identity
    if at==i0:events+=minus
    if at==i1:events+=unminus
    events.append(e)
assert len(events)==len(ev)+224
assert sum(e[0]=='add' for e in events)==1510
assert sum(e[0]=='sign' for e in events)==26
assert sum(e[0]=='transport' for e in events)==772
assert not any(e[0] in ('scale','allocate_zero','erase_zero') for e in events)
out={'schema':'p104-typed-inplace-side-I-minus-G-over-2/1',
 'source_word_sha256':W['source_word_sha256'],
 'numerator_map':'Ynum_out=Ynum_in+(2I-G)*S',
 'decoded_semantics':'Yout=Yin+(I-G/2)*S',
 'target_denominator':2,
 'identity_adds':208,'aggregate_negations':16,
 'signed_ADD':1510,'signed_NEG':26,'fractional_native_scalers':0,
 'clean_aggregate_registers':0,'dirty_helpers_preserved':8,
 'early_Y_owner_requirement':104,
 'positive_native_child_calls':980,'child_rank_mass':1720,
 'caller_encoded_boundary':'OPEN','precision_bit_tape':'OPEN',
 'global_owner_and_selected_supplier':'OPEN',
 'all_size':'OPEN','new_kappa':False,'events':events}
(P/'P104_INPLACE_SIDE_WORD.json').write_text(
 json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
print('PASS_P104_TYPED_I_MINUS_G_HALF_WORD ADD=1510 SIGN=26'
      ' half_native=0 clean_new=0 child_calls=980 rank_mass=1720')

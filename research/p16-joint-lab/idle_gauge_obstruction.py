#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact structural gauge-tag obstruction screen of PR4470 P16 physical events.
No stage/owner work assumed free. Not a full Laurent/native equivalence proof.
"""
from collections import Counter
from pathlib import Path
import hashlib,json
events=[['LOCAL',0,0,False],['LOCAL',1,0,True],['IDLE',1,[0,1]]]
for i in range(1,16):
    events.extend([
        ['ADD',2*i-2,2*i,1],['ADD',2*i+1,2*i-1,-1],
        ['QUERY_SHEAR',2*i,i-1,False],
        ['ADD',2*i-2,2*i,-1],['ADD',2*i+1,2*i-1,1],
        ['LOCAL',2*i+1,i,True]
    ])
    if i<=6:
        events.append(['IDLE',i+1,[0,1]+list(range(3,2*i+2,2))])
events.append(['LOCAL',32,15,False])
for j in range(7,15):
    events.append(['IDLE',j,list(range(2*j+3,32,2))+[32]])
for i in range(15,0,-1):
    events.extend([['ADD',2*i,2*i-2,1],['ADD',2*i-1,2*i+1,-1]])
for i in range(16):events.append(['SIGNED_SWAP',2*i,2*i+1])
assert len(events)==154
assert dict(Counter(e[0] for e in events))=={
    'LOCAL':18,'IDLE':15,'ADD':90,'QUERY_SHEAR':15,'SIGNED_SWAP':16}
source_serialized=json.dumps(events,separators=(',',':'))
assert hashlib.sha256(source_serialized.encode()).hexdigest()==(
 '624305383d5e7e1687e01356d5e41ff4ee3d4f06b3cab71cf9a65ea22fc8dd52')
# Above digest independently checked against physical_events from upstream
# CrocSwap/integer-mult-bounds@b9a13c1 CONTROLLER.json, git blob
# 49a2f0675819f9deeea27ed77be2c2b6ff2e87e5.
tags=[[0]*33 for _ in range(32)]
weighted=[];native=[];queries=[]
for k,e in enumerate(events):
    typ=e[0]
    if typ=='IDLE':
        for r in (2*e[1],2*e[1]+1):
            for stage in e[2]:tags[r][stage]+=1
    elif typ=='ADD':
        dst,src=e[1:3]
        diff=[a-b for a,b in zip(tags[src],tags[dst])]
        if any(diff):weighted.append([k,dst,src,sum(bool(v) for v in diff)])
    elif typ=='QUERY_SHEAR':
        pair=e[2]
        if tags[2*pair]!=tags[2*pair+1]:queries.append([k,pair])
    elif typ=='LOCAL':
        pair=e[2]
        if any(tags[2*pair]) or any(tags[2*pair+1]):
            native.append([k,pair])
    elif typ=='SIGNED_SWAP':
        a,b=e[1:3];tags[a],tags[b]=tags[b],tags[a]
    else:raise AssertionError(e)
assert len(weighted)==62
assert len(native)==7
assert len(queries)==0
assert sum(bool(any(t)) for t in tags)==28
assert sum(sum(v!=0 for v in t) for t in tags)==158
result={
 'status':'PASS_EXACT_PR4470_SKELETON_GAUGE_DIAGNOSTIC',
 'source_repo':'CrocSwap/integer-mult-bounds',
 'source_ref':'b9a13c1673e0e9697de410de16e8bbf3207a7363',
 'controller_git_blob':'49a2f0675819f9deeea27ed77be2c2b6ff2e87e5',
 'physical_events_sha256':hashlib.sha256(source_serialized.encode()).hexdigest(),
 'physical_events':154,'idle_operations':15,
 'unit_ADDs':90,'ADDs_needing_nonunit_Laurent_weight':len(weighted),
 'native_gate_pending_tag_obligations':len(native),
 'query_tag_mismatches':len(queries),
 'terminal_tagged_registers':28,'terminal_nonzero_stage_tags':158,
 'witness_weighted_ADDs':weighted,'witness_opaque_native_gates':native,
 'proof':'For value R_i=z^{tag_i} B_i, a logical unit ADD R_d+=R_s requires B_d+=z^(tag_s-tag_d) B_s. An IDLE increments tags but does not cancel weighted ADD, native conjugation or terminal output charges.',
 'interpretation':'Naive free Laurent-tag IDLE erasure not admitted; alternative lifting/physical fusion remains open.',
 'selected_kappa':'0.00302015','new_kappa':False}
Path(__file__).with_name('IDLE_GAUGE_OBSTRUCTION.json').write_text(
 json.dumps(result,indent=2,sort_keys=True)+'\n')
print('PASS_PR4470_GAUGE_SKELETON 154_EVENTS 62_NONUNIT_ADD'
      ' 7_OPAQUE_NATIVE 28_TAGGED_OUTPUTS no_kappa')

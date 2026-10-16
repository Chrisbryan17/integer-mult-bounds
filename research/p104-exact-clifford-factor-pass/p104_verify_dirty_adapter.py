#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent arbitrary-dirty P104 trace interpreter and no-free-reset controls."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent
W=json.loads((ROOT/'P104_BORROWED_DIRTY_WORD.json').read_text())
SOURCE=ROOT/'p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json'
if not SOURCE.exists():
    SOURCE=ROOT/'p104_native_e8_gate/evidence/NATIVE_CHART_WORD.json'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39'
O=json.loads(SOURCE.read_text())
assert len(O['events'])==1064
assert len(W['events'])==1204
assert W['pre_reads']==156 and W['dirty_helpers']==8 and W['output_early_live']==100
assert W['counts']['zero_initializations']==0
assert W['counts']['rank_mass']==1496 and W['counts']['transport_occurrences']==756
assert W['counts']['adds']==448 and W['counts']['distinct_transports']==514
pre=W['events'][:156]
assert all(e[0]=='add' and e[1].startswith('Y') and e[2].startswith('H')
           and tuple(W['frames'][e[4]])==() for e in pre)

def canonical_event(e, word):
    if e[0]=='transport':
        return ('transport',e[1],tuple(word['frames'][e[2]]),
                tuple(word['frames'][e[3]]),e[4])
    if e[0]=='add':
        return ('add',e[1],e[2],e[3],tuple(word['frames'][e[4]]))
    raise AssertionError(e)

new=[canonical_event(e,W) for e in W['events'][156:]]
old=[canonical_event(e,O) for e in O['events'] if e[0] not in ('zero','erase')]
assert new==old
def recipe_map(w):
    return {(tuple(w['frames'][r['old']]),tuple(w['frames'][r['new']])):
            r['gates'] for r in w['transports']}
assert recipe_map(W)==recipe_map(O)
assert len(recipe_map(W))==514

H=sorted({e[2] for e in pre})
assert len(H)==8
inputs={f'X{i}':{i:1} for i in range(8)}
inputs.update({f'Y{t}':{8+t:1} for t in range(104)})
inputs.update({name:{112+i:1} for i,name in enumerate(H)})
frames={k:() for k in inputs}
for i in range(8):
    first=next(e for e in O['events'] if e[0]=='transport' and e[1]==f'X{i}')
    frames[f'X{i}']=tuple(O['frames'][first[2]])

def apply(data, event, check_frames=False):
    if event[0]!='add':return
    _,dst,src,sgn,_=event
    assert sgn in (-1,1)
    for j,x in data[src].items():
        data[dst][j]=data[dst].get(j,0)+sgn*x
        if data[dst][j]==0:del data[dst][j]

actual={k:v.copy() for k,v in inputs.items()}
for e in W['events']:
    if e[0]=='transport':
        _,name,a,b,rank=e
        assert frames[name]==tuple(W['frames'][a])
        assert abs(len(W['frames'][a])-len(W['frames'][b]))==rank
        frames[name]=tuple(W['frames'][b])
    else:
        assert e[0]=='add'
        assert frames[e[1]]==frames[e[2]]==tuple(W['frames'][e[4]])
        apply(actual,e)
reference={f'X{i}':{i:1} for i in range(8)}
reference.update({f'Y{t}':{8+t:1} for t in range(104)})
reference.update({name:{} for name in H})
for e in O['events']:
    if e[0]=='add':apply(reference,e)
for t in range(104):
    y=f'Y{t}'
    assert actual[y]==reference[y],(y,actual[y],reference[y])
    assert all(j<112 for j in actual[y])
    last=next(e for e in reversed(O['events'])
              if e[0]=='transport' and e[1]==y)
    assert frames[y]==tuple(O['frames'][last[3]])
for i in range(8):assert actual[f'X{i}']=={i:1}
for i,name in enumerate(H):
    assert actual[name]=={112+i:1} and frames[name]==()

# Independent omission control: one omitted pre-read must contaminate an output.
bad={k:v.copy() for k,v in inputs.items()}
for index,e in enumerate(W['events']):
    if index!=0 and e[0]=='add':apply(bad,e)
assert bad['Y0']!=reference['Y0']
assert any(j>=112 for j in bad['Y0'])
print('PASS_P104_DIRTY_BORROW_INDEPENDENT pre_adds=156 all_outputs=104 '
      'arbitrary_dirt=8 restored=8 original_transports_identical=756 '
      'original_rank_mass_identical=1496 zero_reset=0 '
      'negative_control=REJECTED no_new_kappa')

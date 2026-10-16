#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent exact integer 216-input, 104x104 Gram typed-numerator proof.
No division/rounding, clean init, hidden X scratch or uncharged cancellation.
This checks finite algebra, NOT caller's global dyadic interface admission.
"""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p104_native_e8_gate.scripts import native_chart_emitter as E
W=json.loads((P/'P104_INPLACE_DYADIC_WORD.json').read_text())
O=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
ev=W['events'];frames=O['frames']
H=sorted({e[2] for e in ev if e[0]=='add' and e[2].startswith('H')})
S=['S%d'%j for j in range(104)]
Y=['Y%d'%j for j in range(104)]
names=S+Y+H;idx={r:i for i,r in enumerate(names)}
assert len(names)==216 and len(H)==8
assert sum(e[0]=='add' for e in ev)==1298
assert not any(e[0] in ('scale','allocate_zero','erase_zero') for e in ev)
def replay(skip=-1):
    data={r:{idx[r]:1} for r in names}
    chart={r:() for r in Y+H};entered=set();returned=set()
    for at,e in enumerate(ev):
        if at==skip:continue
        k=e[0]
        if k=='source_to_zero':
            _,r,root,n=e
            assert r in S and r not in entered
            assert root==E.E8.live[int(r[1:])] and n==1
            entered.add(r);chart[r]=()
        elif k=='source_from_zero':
            _,r,root,n=e
            assert r in entered and r not in returned and chart[r]==()
            assert root==E.E8.live[int(r[1:])] and n==1
            returned.add(r);chart[r]=('intrinsic',root)
        elif k=='transport':
            _,r,a,b,n=e
            assert chart[r]==tuple(frames[a])
            assert abs(len(frames[a])-len(frames[b]))==n>0
            assert E.subset(frames[a],frames[b]) or E.subset(frames[b],frames[a])
            chart[r]=tuple(frames[b])
        elif k=='sign':
            _,r,n,f=e
            assert n==-1 and chart[r]==tuple(frames[f])
            data[r]={i:-v for i,v in data[r].items()}
        elif k=='add':
            _,dst,src,n,f=e
            assert n in (-1,1) and chart[dst]==chart[src]==tuple(frames[f])
            for i,v in list(data[src].items()):
                data[dst][i]=data[dst].get(i,0)+n*v
                if not data[dst][i]:del data[dst][i]
        else:raise AssertionError(('illegal integral primitive',e))
    assert entered==returned==set(S)
    return data

forward=replay();L=E.E8.live
assert all(forward[r]=={idx[r]:1} for r in S+H)
nonzero=0
for t in range(104):
    expected={104+t:1}
    for s in range(104):
        v=E.E8.IP[L[t]][L[s]]
        if v:expected[s]=v;nonzero+=1
    assert forward[Y[t]]==expected
# Inverse transpose for the INTEGER numerator shear (not G/2).
D={r:{idx[r]:1} for r in names}
for t in range(104):
    for s in range(104):
        v=E.E8.IP[L[t]][L[s]]
        if v:D[S[s]][104+t]=-v
for i in range(216):
    for j in range(216):
        assert sum(forward[r].get(i,0)*D[r].get(j,0) for r in names)==int(i==j)
first=next(i for i,e in enumerate(ev) if e[0]=='add'
           and e[1] in S and e[2] in S)
try:wrong=replay(skip=first)
except AssertionError:pass
else:assert wrong!=forward
# An odd Gram coefficient rules out interpreting the output as an unencoded
# Z-valued G/2 result with zero precision/denominator work.
odd=next((t,s) for t in range(104) for s in range(104)
         if abs(E.E8.IP[L[t]][L[s]])==1)
assert forward[Y[odd[0]]].get(odd[1]) in (-1,1)
receipt={'status':'PASS_TYPED_INTEGER_EXACT',
 'formal_independent_inputs':216,'sources_restored':104,'dirty_H_restored':8,
 'full_104x104_entries':10816,'integer_dual_entries':46656,
 'strict_no_fractional_primitive':True,'strict_no_new_clean_registers':True,
 'scalar_ADD':1298,'sign':12,'source_mutation_rejected':True,
 'odd_denominator2_witness':list(odd),'native_owners':'OPEN',
 'caller_denominator2_and_rounding':'OPEN','all_size':'OPEN','new_kappa':False}
(P/'P104_TYPED_INTEGER_RECEIPT.json').write_text(
 json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print('PASS_P104_TYPED_DYADIC_INTEGER_104X104 inputs=216 coef=10816'
      ' inverse_transpose=46656 native_half=0 clean_X=0'
      ' denominator2_caller=OPEN')

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Producer-independent exact 216-input, 104x104 Gram-half, inverse-transpose
and symbolic physical-chart replay for borrowed SOURCE registers. No κ claim.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,collections,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p104_native_e8_gate.scripts import native_chart_emitter as E
W=json.loads((P/'P104_INPLACE_SOURCE_WORD.json').read_text())
O=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
frames=O['frames'];events=W['events']
H=sorted({e[2] for e in events if e[0]=='add' and e[2].startswith('H')})
assert len(H)==8
S=['S'+str(i) for i in range(104)]
Y=['Y'+str(i) for i in range(104)]
names=S+Y+H;idx={x:i for i,x in enumerate(names)}
assert len(names)==216 and len(set(names))==216
assert collections.Counter(e[0] for e in events)=={
 'add':1302,'transport':772,'source_to_zero':104,
 'source_from_zero':104,'scale':16,'sign':10}
assert not any(e[0] in ('allocate_zero','erase_zero') for e in events)

def replay(skip=-1,wrong_half=False,wrong_sign=False):
    rows={name:{idx[name]:Q(1)} for name in names}
    chart={name:() for name in Y+H}
    entered=set();exited=set()
    first_sign=next(i for i,e in enumerate(events) if e[0]=='sign')
    for at,e in enumerate(events):
        if at==skip:continue
        typ=e[0]
        if typ=='source_to_zero':
            _,role,root,r=e
            assert role in S and root==E.E8.live[int(role[1:])] and r==1
            assert role not in entered;entered.add(role);chart[role]=()
        elif typ=='source_from_zero':
            _,role,root,r=e
            assert role in entered and role not in exited and r==1
            assert chart[role]==() and root==E.E8.live[int(role[1:])]
            exited.add(role);chart[role]=('intrinsic',root)
        elif typ=='transport':
            _,role,a,b,r=e
            assert role in chart and chart[role]==tuple(frames[a])
            assert r==abs(len(frames[a])-len(frames[b]))>0
            assert E.subset(frames[a],frames[b]) or E.subset(frames[b],frames[a])
            chart[role]=tuple(frames[b])
        elif typ=='scale':
            _,role,n,d,f=e
            assert role in S and chart[role]==tuple(frames[f])
            assert (n,d) in ((1,2),(2,1))
            z=Q(n,d) if not (wrong_half and n==1) else Q(1)
            rows[role]={k:v*z for k,v in rows[role].items()}
        elif typ=='sign':
            _,role,sgn,f=e
            assert role in S and chart[role]==tuple(frames[f]) and sgn==-1
            if not (wrong_sign and at==first_sign):
                rows[role]={k:-v for k,v in rows[role].items()}
        elif typ=='add':
            _,dst,src,sgn,f=e
            assert sgn in (-1,1)
            assert chart[dst]==chart[src]==tuple(frames[f])
            for k,v in list(rows[src].items()):
                rows[dst][k]=rows[dst].get(k,Q())+sgn*v
                if not rows[dst][k]:del rows[dst][k]
        else:raise AssertionError(e)
    assert entered==exited==set(S)
    return rows

actual=replay()
L=E.E8.live
assert all(actual[s]=={idx[s]:Q(1)} for s in S)
assert all(actual[h]=={idx[h]:Q(1)} for h in H)
for t,r in enumerate(L):
    expected={idx[Y[t]]:Q(1)}
    for j,s in enumerate(L):
        x=E.E8.IP[r][s]
        if x:expected[idx[S[j]]]=Q(x,2)
    assert actual[Y[t]]==expected
# Formal ordinary inverse-transpose of the entire 216-variable shear.
D={name:{idx[name]:Q(1)} for name in names}
for t,r in enumerate(L):
    for j,s in enumerate(L):
        x=E.E8.IP[r][s]
        if x:D[S[j]][idx[Y[t]]]=-Q(x,2)
for i in range(216):
    for j in range(216):
        assert sum(actual[k].get(i,Q())*D[k].get(j,Q()) for k in names)==int(i==j)

pre=next(i for i,e in enumerate(events) if e[0]=='add' and e[1] in S and e[2] in S)
post=max(i for i,e in enumerate(events) if e[0]=='add' and e[1] in S and e[2] in S)
for kwargs in ({'skip':pre},{'skip':post},{'wrong_half':True},{'wrong_sign':True}):
    try:mutated=replay(**kwargs)
    except AssertionError:continue
    assert mutated!=actual,('accepted negative control',kwargs)
B=W['B_8x104'];U=W['U_8x104'];bp=W['Bp_8x8'];inv=W['Bp_inverse'];p=W['pivots']
assert len(set(p))==8 and all(sum(bp[i][j]*inv[j][k] for j in range(8))==int(i==k)
                              for i in range(8) for k in range(8))
assert all(sum(bp[i][j]*U[j][s] for j in range(8))==B[i][s]
           for i in range(8) for s in range(104))
report={'status':'PASS_FINITE_INPLACE_SOURCE',
 'independent_formal_inputs':216,'source_preserved':104,'target_outputs':104,
 'dirty_helpers_restored':8,'new_clean_aggregate_scratch':0,
 'gram_entries_checked':10816,'logical_inverse_transpose_entries_checked':46656,
 'scalar_ADD':1302,'scalar_SIGN':10,'fractional_scale':16,
 'conditional_rank_mass':1720,
 'negative_controls_rejected':4,
 'source_owner_price':'OPEN','scalar_halving':'OPEN','new_kappa':False}
(P/'P104_INPLACE_SOURCE_INDEPENDENT_RECEIPT.json').write_text(
 json.dumps(report,sort_keys=True,indent=2)+'\n')
print('PASS_P104_INPLACE_104X104_GRAM_HALF inputs=216 coef=10816'
      ' dual=46656 clean=0 ADD=1302 SIGN=10'
      ' mutants=4 source_owner_price_OPEN')

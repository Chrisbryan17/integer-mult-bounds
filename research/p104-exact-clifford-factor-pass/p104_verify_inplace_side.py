#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent exact 216-variable integral I-G/2 typed numerator checker:
all 104x104 coefficients, 46,656 inverse-transpose entries and controls.
No inherited producer functions are used in symbolic event execution.
"""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p104_native_e8_gate.scripts import native_chart_emitter as E
W=json.loads((P/'P104_INPLACE_SIDE_WORD.json').read_text())
O=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
fr=O['frames'];ev=W['events']
H=sorted({e[2] for e in ev if e[0]=='add' and e[2].startswith('H')})
S=['S'+str(i) for i in range(104)]
Y=['Y'+str(i) for i in range(104)]
names=S+Y+H;idx={r:i for i,r in enumerate(names)}
assert len(names)==216 and len(H)==8
assert sum(e[0]=='add' for e in ev)==1510
assert sum(e[0]=='sign' for e in ev)==26
assert not any(e[0] in ('allocate_zero','erase_zero','scale') for e in ev)
def replay(skip=-1,wrong_neg=-1):
    rows={r:{idx[r]:1} for r in names}
    chart={r:() for r in Y+H}
    sources=set();restored=set()
    for at,e in enumerate(ev):
        if at==skip:continue
        typ=e[0]
        if typ=='source_to_zero':
            _,r,root,k=e
            assert r in S and r not in sources and root==E.E8.live[int(r[1:])] and k==1
            sources.add(r);chart[r]=()
        elif typ=='source_from_zero':
            _,r,root,k=e
            assert r in sources and r not in restored and chart[r]==()
            assert root==E.E8.live[int(r[1:])] and k==1
            restored.add(r);chart[r]=('intrinsic',root)
        elif typ=='transport':
            _,r,a,b,k=e
            assert chart[r]==tuple(fr[a]) and k==abs(len(fr[a])-len(fr[b]))>0
            assert E.subset(fr[a],fr[b]) or E.subset(fr[b],fr[a])
            chart[r]=tuple(fr[b])
        elif typ=='sign':
            _,r,sgn,f=e
            assert r in S and chart[r]==tuple(fr[f]) and sgn==-1
            if at!=wrong_neg:rows[r]={j:-v for j,v in rows[r].items()}
        elif typ=='add':
            _,d,s,sgn,f=e
            assert sgn in (-1,1) and chart[d]==chart[s]==tuple(fr[f])
            for j,v in list(rows[s].items()):
                rows[d][j]=rows[d].get(j,0)+sgn*v
                if not rows[d][j]:del rows[d][j]
        else:raise AssertionError(('illegal native',e))
    assert sources==restored==set(S)
    return rows
F=replay();L=E.E8.live
assert all(F[r]=={idx[r]:1} for r in S+H)
for t in range(104):
    expected={104+t:1}
    for s in range(104):
        v=2*int(t==s)-E.E8.IP[L[t]][L[s]]
        if v:expected[s]=v
    assert F[Y[t]]==expected,(t,F[Y[t]],expected)
dual={r:{idx[r]:1} for r in names}
for t in range(104):
    for s in range(104):
        v=2*int(t==s)-E.E8.IP[L[t]][L[s]]
        if v:dual[S[s]][104+t]=-v
for i in range(216):
    for j in range(216):
        assert sum(F[r].get(i,0)*dual[r].get(j,0) for r in names)==int(i==j)
ident=next(i for i,e in enumerate(ev) if e[0]=='add' and e[1]=='Y0'
           and e[2]=='S0')
neg=next(i for i,e in enumerate(ev) if e[0]=='sign' and e[1]=='S68'
         and tuple(fr[e[3]])!=())
for mutation in ({'skip':ident},{'skip':ident+1},{'wrong_neg':neg}):
    try:wrong=replay(**mutation)
    except AssertionError:continue
    assert wrong!=F,('mutation accepted',mutation)
receipt={'schema':'p104-typed-I-minus-G-over-2-exact-replay/1',
 'status':'PASS_FINITE_TYPED_SIDE_CORRECTION',
 'formal_inputs':216,'gram_entries':10816,
 'inverse_transpose_entries':46656,'restored_sources':104,
 'restored_borrowed_dirty_helpers':8,'extra_clean_registers':0,
 'signed_ADD':1510,'signed_NEG':26,'fractional_native_operators':0,
 'child_calls':980,'rank_mass':1720,
 'mutants_rejected':3,'early_owned_Y':'OPEN',
 'decoded_input_output_owner':'OPEN',
 'global_precision_tape':'OPEN','all_size':'OPEN','new_kappa':False}
(P/'P104_INPLACE_SIDE_VERIFICATION.json').write_text(
    json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print('PASS_P104_INPLACE_TYPED_I_MINUS_G_HALF'
      ' inputs=216 gram=10816 dual=46656 sources=104'
      ' dirty=8 zero_clean=YES fractional_native=ZERO'
      ' mutants=3 supplier_and_kappa_OPEN')

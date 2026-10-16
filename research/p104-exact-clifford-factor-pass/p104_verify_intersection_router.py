#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent 216-input scalar/frame replay and 1,238-rank lower-bound audit.
Does not import or trust the intersection router.
"""
from pathlib import Path
import json,sys,collections
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'p104_native_e8_gate/scripts'))
import native_chart_emitter as E
O=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())

def span(f):
    t={0}
    for x in f:t|={x^v for v in tuple(t)}
    return t

def dist(A,B):
    a,b=span(A),span(B)
    return a.bit_length()-1 if False else ((len(a).bit_length()-1)
           +(len(b).bit_length()-1)-2*((len(a&b)).bit_length()-1))

def check(label,source):
    old=json.loads((P/source).read_text())
    new=json.loads((P/f'P104_INTERSECTION_{label}.json').read_text())
    before=old['events'];after=new['events']
    fr=[tuple(x) for x in new['frames']]
    assert fr[:len(O['frames'])]==[tuple(x) for x in O['frames']]
    assert [e for e in before if e[0]!='transport']==[e for e in after if e[0]!='transport']
    H=sorted({r for e in before if e[0]=='add' for r in e[1:3] if r.startswith('H')})
    S=[f'S{i}' for i in range(104)];Y=[f'Y{i}' for i in range(104)]
    names=S+Y+H;idx={r:i for i,r in enumerate(names)}
    assert len(names)==216 and len(H)==8
    zero=next(i for i,f in enumerate(fr) if not f)
    state={r:zero for r in Y+H}
    data={r:{idx[r]:1} for r in names}
    seen=set();left=set();rank=0;transports=0
    for e in after:
        k=e[0]
        if k=='source_to_zero':
            assert e[1] in S and e[1] not in state
            state[e[1]]=zero;seen.add(e[1])
        elif k=='source_from_zero':
            assert e[1] in seen and e[1] not in left and state[e[1]]==zero
            state[e[1]]='intrinsic';left.add(e[1])
        elif k=='transport':
            _,r,a,b,c=e
            assert state[r]==a and a!=b
            assert span(fr[a])<=span(fr[b]) or span(fr[b])<=span(fr[a])
            assert c==abs(len(fr[a])-len(fr[b]))>0
            state[r]=b;rank+=c;transports+=1
        elif k=='add':
            _,dst,src,sign,f=e
            assert sign in (-1,1) and state[dst]==state[src]==f
            for j,v in list(data[src].items()):
                data[dst][j]=data[dst].get(j,0)+sign*v
                if not data[dst][j]:del data[dst][j]
        elif k=='sign':
            assert e[2]==-1 and state[e[1]]==e[3]
            data[e[1]]={j:-v for j,v in data[e[1]].items()}
        else:raise AssertionError(e)
    assert seen==left==set(S)
    assert all(data[r]=={idx[r]:1} for r in S+H)
    for t,rt in enumerate(E.E8.live):
        want={104+t:1}
        for s,rs in enumerate(E.E8.live):
            v=E.E8.IP[rt][rs]
            if label!='G':v=2*int(t==s)-v
            if v:want[s]=v
        assert data[Y[t]]==want
    final={r:zero for r in Y+H}
    for e in before:
        if e[0]=='source_to_zero':final[e[1]]=zero
        elif e[0]=='transport':final[e[1]]=e[3]
        elif e[0]=='source_from_zero':final[e[1]]='intrinsic'
    assert state==final
    anchor={r:[zero] for r in Y+H}
    for e in before:
        k=e[0]
        if k=='source_to_zero':anchor[e[1]]=[zero]
        elif k=='source_from_zero':anchor[e[1]].append(zero)
        elif k=='add':anchor[e[1]].append(e[4]);anchor[e[2]].append(e[4])
        elif k=='sign':anchor[e[1]].append(e[3])
    for h in H:anchor[h].append(zero)
    for y in Y:anchor[y].append(final[y])
    lower=sum(dist(fr[a],fr[b]) for seq in anchor.values()
              for a,b in zip(seq,seq[1:]))
    assert rank==lower==1238
    assert transports==(687 if label=='G' else 703)
    return {'scope':'independent finite fixed-anchor model','status':'PASS',
            'full_104x104_coefficients':10816,'independent_input_columns':216,
            'all_sources_restored':104,'dirty_helpers_restored':8,
            'unchanged_scalar_events':True,
            'native_calls_plus_source_ports':transports+208,
            'total_native_rank_mass_including_source':rank+208,
            'fixed_anchor_lower_bound':lower,
            'source_host_owner':'OPEN','all_size':'OPEN','new_kappa':False}

if __name__=='__main__':
    res={}
    options={'G':('P104_INPLACE_DYADIC_WORD.json','P104_INPLACE_DYADIC_TARGET_WORD.json'),
             'I_minus_G_half':('P104_INPLACE_SIDE_WORD.json','P104_INPLACE_SIDE_I_MINUS_G_HALF_WORD.json')}
    for label,candidates in options.items():
        source=next(x for x in candidates if (P/x).exists())
        res[label]=check(label,source)
        print('PASS_INDEPENDENT_INTERSECTION',label,res[label]['fixed_anchor_lower_bound'])
    (P/'P104_INTERSECTION_INDEPENDENT_RECEIPT.json').write_text(
        json.dumps(res,sort_keys=True,indent=2)+'\n')

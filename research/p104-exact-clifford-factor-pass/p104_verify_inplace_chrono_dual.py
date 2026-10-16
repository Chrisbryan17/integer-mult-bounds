#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independently replay both chronological 216-input P104 inverse-transposes,
including Delta frame, source entry/exit, scalar negation and all 104x104 rows.
Wrong ADD sign and reversing event order are rejected.
"""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p104_native_e8_gate.scripts import native_chart_emitter as E
D=json.loads((P/'P104_INPLACE_CHRONOLOGICAL_DUAL_WORDS.json').read_text())
O=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
frames=O['frames'];live=E.E8.live
for name,part in D['programs'].items():
    ev=part['events']
    H=sorted({x for e in ev if e[0]=='add' for x in e[1:3] if x.startswith('H')})
    S=['S'+str(i) for i in range(104)]
    Y=['Y'+str(i) for i in range(104)]
    regs=S+Y+H;index={x:i for i,x in enumerate(regs)}
    assert len(regs)==216 and len(H)==8
    def run(word):
        data={x:{index[x]:1} for x in regs}
        chart={x:() for x in Y+H}
        entered=set();returned=set()
        for at,e in enumerate(word):
            typ=e[0]
            if typ=='add':
                _,dest,src,sign,fr=e
                assert sign in (-1,1) and chart[dest]==chart[src]==tuple(frames[fr])
                for i,v in list(data[src].items()):
                    data[dest][i]=data[dest].get(i,0)+sign*v
                    if not data[dest][i]:del data[dest][i]
            elif typ=='sign':
                _,reg,sign,fr=e
                assert sign==-1 and chart[reg]==tuple(frames[fr])
                data[reg]={i:-v for i,v in data[reg].items()}
            elif typ=='delta_transport':
                _,reg,a,b,rank=e
                assert chart[reg]==tuple(frames[a])
                assert rank==abs(len(frames[a])-len(frames[b]))>0
                assert E.subset(frames[a],frames[b]) or E.subset(frames[b],frames[a])
                chart[reg]=tuple(frames[b])
            elif typ=='delta_source_to_zero':
                _,reg,root,rank=e
                assert reg in S and reg not in entered
                assert root==live[int(reg[1:])] and rank==1
                entered.add(reg);chart[reg]=()
            elif typ=='delta_source_from_zero':
                _,reg,root,rank=e
                assert reg in entered and reg not in returned and chart[reg]==()
                assert root==live[int(reg[1:])] and rank==1
                returned.add(reg);chart[reg]=('conjugate-intrinsic',root)
            else:raise AssertionError(('unknown dual event',e))
        assert entered==returned==set(S)
        return data
    rows=run(ev)
    assert all(rows[r]=={index[r]:1} for r in Y+H)
    for s in range(104):
        expected={s:1}
        for t in range(104):
            c=E.E8.IP[live[t]][live[s]]
            if name=='I_minus_G_half':c=2*int(t==s)-c
            if c:expected[104+t]=-c
        assert rows[S[s]]==expected,(name,s)
    j=next(i for i,e in enumerate(ev) if e[0]=='add')
    bad=[e.copy() for e in ev];bad[j][3]*=-1
    try:changed=run(bad)
    except AssertionError:pass
    else:assert changed!=rows
    try:changed=run(list(reversed(ev)))
    except AssertionError:pass
    else:assert changed!=rows
    print('PASS_P104_INPLACE_CHRONOLOGICAL_DUAL',name,
          'formal=216 dual_matrix_entries=46656'
          ' bad_sign=REJECTED reversed_chronology=REJECTED')
receipt={'schema':'p104-full-inplace-source-dual-event-proof/1',
 'status':'PASS_FINITE_CHRONOLOGICAL_DELTA',
 'checked_programs':['G','I_minus_G_half'],
 'formal_variables_each':216,'matrix_entries_each':46656,
 'native_children_each':980,'rank_mass_each':1720,
 'conjugate_Gamma_endpoint_callers':'OPEN',
 'global_source_owner_and_host':'OPEN',
 'all_size_and_moments':'OPEN','new_kappa':False}
(P/'P104_INPLACE_CHRONOLOGICAL_DUAL_RECEIPT.json').write_text(
    json.dumps(receipt,sort_keys=True,indent=2)+'\n')

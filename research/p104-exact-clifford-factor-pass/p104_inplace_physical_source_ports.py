#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent exact-512-column physical source-port native admission test.
The 104 intrinsic C(q) ports each enter and exit by ONE positive F1 child.
Source authority, tape, own/host and scaling remain independently unpriced.
"""
from pathlib import Path
import hashlib,json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p104_physical_e8_isometry import physical
from p104_native_e8_gate.scripts import native_chart_emitter as E
import p104_verify_rank_r_all_columns as V
from p104_rank_r_native_recipes import normalize,gates_of
W=json.loads((P/'P104_INPLACE_SOURCE_WORD.json').read_text())
assert W['source_word_sha256']=='a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39'
assert sum(e[0]=='source_to_zero' for e in W['events'])==104
assert sum(e[0]=='source_from_zero' for e in W['events'])==104
def chart(q):
    span=[q]
    for i in range(9):
        v=1<<i
        if E.rank(span+[v])==len(span)+1:span.append(v)
        if len(span)==9:break
    assert E.rank(span)==9
    G=E.transpose(span)
    assert E.transpose(G)==tuple(span)
    return G,E.inverse(G)
records=[]
for s,root in enumerate(E.E8.live):
    q=physical(E.LABELS[root])
    G,Gi=chart(q)
    core=[['C',1,1]]
    prefix=[['P',Gi]]
    last=[['P',G]]
    entrance=prefix+core+last+[['X',q]]
    exit=prefix+core+last
    assert V.identical([['C',q,-1]],entrance),('entrance',s)
    assert V.identical([['C',q,1]],exit),('exit',s)
    lm=normalize(prefix);right_in=normalize(last+[['X',q]])
    right_out=normalize(last)
    assert V.identical(gates_of(lm)+core+gates_of(right_in),[['C',q,-1]])
    assert V.identical(gates_of(lm)+core+gates_of(right_out),[['C',q,1]])
    records.append({'port':s,'physical_root_line':q,'entrance':[lm,right_in],
                    'exit':[lm,right_out],'child_rank':1})
assert len(records)==104
payload={'schema':'p104-inplace-physical-port-bridge/1',
 'source_word_sha256':W['source_word_sha256'],
 'source_entry_ports':104,'source_exit_ports':104,
 'positive_rank1_source_children':208,
 'all_208_exact_512_column_operators':True,
 'core_rank_r_children':756,
 'eight_pivot_zero_line_bridges':16,
 'total_positive_rank_r_children':980,
 'total_child_rank_mass':1720,
 'clean_aggregate_scratch':0,
 'full_source_owner':'OPEN','halving_precision':'OPEN',
 'recursive_invoice_and_all_size':'OPEN','new_kappa':False,
 'source_records':records}
(P/'P104_INPLACE_PHYSICAL_SOURCE_PORTS.json').write_text(
    json.dumps(payload,indent=2,sort_keys=True)+'\n')
print('PASS_P104_INPLACE_208_PHYSICAL_PORT_CHILDREN source_ports=104'
      ' rank1=208 columns_each=512 total_children=980 rank_mass=1720'
      ' source_ownership_OPEN')

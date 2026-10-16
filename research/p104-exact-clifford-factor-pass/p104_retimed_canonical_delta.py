#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""All 104 canonical-to-Delta intrinsic E8 port bridges are X monomials.
Their paid address movement/owner lifetimes are NOT zero.
"""
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
from p104_physical_e8_isometry import physical
from p104_native_e8_gate.scripts import native_chart_emitter as E
from p104_routed_native_audit import equal_exact
from p104_verify_rank_r_all_columns import identical
roots=[physical(E.LABELS[x]) for x in E.E8.live]
assert len(set(roots))==104
records=[]
for i,q in enumerate(roots):
    src=[['C',q,+1]]
    src_delta=[['C',q,-1]]
    src_change=[['X',q]]
    target=[['C',q,-1]]+[['C',1<<k,+1] for k in range(9)]
    target_delta=[['C',q,+1]]+[['C',1<<k,-1] for k in range(9)]
    target_change=[['X',511^q]]
    equal_exact(src_delta+src_change,src)
    equal_exact(target_delta+target_change,target)
    if i in (0,22,52,103):
        assert identical(src_delta+src_change,src)
        assert identical(target_delta+target_change,target)
    records.append({'port':i,'physical_q':q,'source_X_offset':q,
                    'target_X_offset':511^q})
result={'schema':'p104-retimed-canonical-delta-intrinsic-ports/1',
        'status':'PASS_FINITE_EXACT_CLIFFORD',
        'source_and_target_port_pairs':104,
        'rank_zero_X_address_offsets':208,
        'added_recursive_Fourier_children':0,
        'exact_Pauli_and_10_column_ports':104,
        'full_512_column_sample_ports':[0,22,52,103],
        'physical_address_host_tape_price':'OPEN',
        'selected_recursive_invoice':'OPEN','new_kappa':False,
        'ports':records}
(P/'P104_RETIMED_CANONICAL_DELTA_BRIDGES.json').write_text(
 json.dumps(result,sort_keys=True,indent=2)+'\n')
print('PASS_P104_CANONICAL_DELTA_SOURCE_TARGET source=104 target=104 rank_zero=208')

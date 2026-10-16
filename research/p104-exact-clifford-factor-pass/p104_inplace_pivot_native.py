#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""All 16 zero <-> genuine physical-E8 root-line pivot source bridges:
one positive F1 per leg, exact global phase on all 512 operator columns.
"""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p104_physical_e8_isometry import physical
from p104_native_e8_gate.scripts import native_chart_emitter as E
from p104_minimal_symplectic import factor
from p104_exact_native_factor import correction
from p104_rank_r_native_recipes import lower
import p104_verify_rank_r_all_columns as V
W=json.loads((P/'P104_INPLACE_SOURCE_WORD.json').read_text())
roots=[pair[0] for pair in E.E8.chosen[1]]
records=[]
for i,root in enumerate(roots):
    q=physical(E.LABELS[root])
    original=E.gamma((q,))
    for direction,gates in (('in',original),('out',E.adjoint(original))):
        gates=[list(g) for g in gates]
        candidate,r=factor([tuple(g) for g in gates])
        assert r==1
        fix,_=correction(gates,candidate)
        rec={'old':0,'new':1,'rank':r,'occurrences':1,
             'gates':[list(g) for g in candidate+fix]}
        new=lower(rec)
        assert sum(g[0]=='C' for g in new['gates'])==1
        assert all(g[2]==1 for g in new['gates'] if g[0]=='C')
        assert V.identical(gates,new['gates']),(i,direction)
        records.append({'source':'S'+str(W['pivots'][i]),
                        'physical_root_line':q,'direction':direction,
                        'rank1':1,'monomial_L':new['left_monomial'],
                        'monomial_R':new['right_monomial']})
assert len(records)==16
result={'status':'PASS_EXACT_PHYSICAL_E8_PIVOT_NATIVE',
 'genuine_E8_root_line_pairs':8,'transport_recipe_count':16,
 'exact_complex_columns_per_recipe':512,'positive_rank1_children':16,
 'total_full_forward_rank_r_children':980,'total_rank_mass':1720,
 'early_target_owner_and_host':'OPEN',
 'typed_caller_and_bit_precision':'OPEN',
 'complete_recursive_invoice':'OPEN','all_size':'OPEN','new_kappa':False,
 'pivot_children':records}
(P/'P104_INPLACE_PIVOT_NATIVE.json').write_text(
    json.dumps(result,indent=2,sort_keys=True)+'\n')
print('PASS_P104_16_PIVOT_PHYSICAL_NATIVE_512_COLUMNS'
      ' source_ports=104 source_legs=208 pivot_legs=16'
      ' original_core_children=756 combined=980 rank_mass=1720')

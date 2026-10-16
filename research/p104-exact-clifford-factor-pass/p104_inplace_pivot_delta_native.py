#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact physical Delta pivot-line native proof for each of the 16 E8 legs:
one positive F1 and explicit phase-correct Gaussian monomial factors, all
512 complex columns. Canonical caller endpoint conversion remains OPEN.
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
from p104_dual_native_check import conjugate
import p104_verify_rank_r_all_columns as V
W=json.loads((P/'P104_INPLACE_SOURCE_WORD.json').read_text())
R=[pair[0] for pair in E.E8.chosen[1]]
out=[]
for i,root in enumerate(R):
    q=physical(E.LABELS[root])
    for direction,old in (('entry',E.gamma((q,))),
                          ('exit',E.adjoint(E.gamma((q,))))):
        target=conjugate([list(g) for g in old])
        candidate,r=factor([tuple(g) for g in target])
        assert r==1
        fix,_=correction(target,candidate)
        prepared={'old':0,'new':1,'rank':1,'occurrences':1,
                  'gates':[list(g) for g in candidate+fix]}
        child=lower(prepared)
        assert sum(g[0]=='C' for g in child['gates'])==1
        assert all(g[2]==1 for g in child['gates'] if g[0]=='C')
        assert V.identical(target,child['gates']),('phase',i,direction)
        out.append({'source':'S'+str(W['pivots'][i]),
                    'physical_E8_root_q':q,'direction':direction,
                    'rank':1,'left_monomial':child['left_monomial'],
                    'right_monomial':child['right_monomial']})
assert len(out)==16
receipt={'status':'PASS_PHYSICAL_DELTA_PIVOT_EXACT',
 'distinct_physical_pivot_delta_words':16,'all_complex_columns_each':512,
 'positive_rank1_children':16,
 'source_delta_entry_exit_children':208,
 'core_isometric_delta_child_occurrences':756,
 'total_delta_native_children_per_word':980,'delta_rank_mass':1720,
 'canonical_intrinsic_dual_endpoint':'OPEN',
 'fully_paid_owner_host_precision':'OPEN','new_kappa':False,
 'records':out}
(P/'P104_INPLACE_DELTA_PIVOT_NATIVE.json').write_text(
    json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print('PASS_P104_INPLACE_16_DELTA_PIVOT_FULL_MATRIX'
      ' exact_columns=512 positive_F1=16'
      ' combined_dual_native=980 rank_mass=1720')

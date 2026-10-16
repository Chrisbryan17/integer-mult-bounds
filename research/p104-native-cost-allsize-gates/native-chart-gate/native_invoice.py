#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Actual E8-labelled same-trace comparison; NOT a selected recursive invoice."""
import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('native',P/'native_chart_emitter.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a=m.build(0)['counts'];b=m.build(1909)['counts']
assert (a['rank_mass'],a['addition_events'],a['raw_C_gate_occurrences'])==(2224,416,5696)
assert (b['rank_mass'],b['addition_events'],b['raw_C_gate_occurrences'])==(1496,292,4160)
report={'schema':'p104-nine-axis-raw-clifford-comparator/1',
 'scope':'literal canonical chart words for a fixed E8 decoder and fixed home-return itinerary; zero initialization is assumed available and unpriced',
 'unmixed':a,'single_sign_8_helper':b,
 'differences':{k:b[k]-a[k] for k in ('rank_mass','addition_events','raw_C_gate_occurrences')},
 'critical_missing':['clean helper provisioning and lifetime hosting','source/query access and inverse-transpose','address monomials and phase compiler runtime','rank-difference-child native factorization','recursive children and selected price engines','all-size compiler and analytic/rounding proof'],
 'new_kappa':False}
(P/'evidence').mkdir(parents=True,exist_ok=True)
(P/'evidence'/'NATIVE_INVOICE.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS_RAW_CLIFFORD_INVOICE unmixed_C=%d mixed_C=%d saved_C=%d extra_clean_helpers=%d selected_kappa_UNCHANGED'%(a['raw_C_gate_occurrences'],b['raw_C_gate_occurrences'],a['raw_C_gate_occurrences']-b['raw_C_gate_occurrences'],b['helpers_zero_initialized']))

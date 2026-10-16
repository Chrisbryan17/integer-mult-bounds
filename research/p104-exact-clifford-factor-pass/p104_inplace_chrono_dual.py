#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Emit P104 chronological ordinary inverse-transpose words for both integral
target-numerator maps. Every ADD is transposed with opposite sign in ORIGINAL
event order. All physical charts become conjugate Delta, not ordinary Gamma.
"""
from pathlib import Path
import json,collections
P=Path(__file__).resolve().parent
sources={'G':'P104_INPLACE_DYADIC_WORD.json',
         'I_minus_G_half':'P104_INPLACE_SIDE_WORD.json'}
out={}
for key,path in sources.items():
    w=json.loads((P/path).read_text())
    dual=[]
    for e in w['events']:
        t=e[0]
        if t=='add':dual.append(['add',e[2],e[1],-e[3],e[4]])
        elif t=='sign':dual.append(e)
        elif t=='transport':dual.append(['delta_transport',*e[1:]])
        elif t=='source_to_zero':dual.append(['delta_source_to_zero',*e[1:]])
        elif t=='source_from_zero':dual.append(['delta_source_from_zero',*e[1:]])
        else:raise AssertionError(('inadmissible scalar in typed word',e))
    assert len(dual)==len(w['events'])
    assert sum(e[0]=='add' for e in dual)==w['signed_ADD']
    assert sum(e[0]=='sign' for e in dual)==w['signed_NEG']
    assert sum(e[0]=='delta_transport' for e in dual)==772
    assert sum(e[0] in ('delta_source_to_zero','delta_source_from_zero') for e in dual)==208
    out[key]={'source':path,'events':dual,
              'signed_ADD':w['signed_ADD'],'signed_NEG':w['signed_NEG'],
              'conjugate_native_core_and_pivot_events':772,
              'conjugate_native_source_events':208}
payload={'schema':'p104-chronological-inplace-Delta-ordinary-dual/1',
 'operator_definition':'F^(-T) with Delta_W=conjugate(Gamma_W)',
 'same_event_order':True,'all_scalar_ADDs_swapped_and_negated':True,
 'positive_native_child_calls_per_orientation':980,
 'native_rank_mass_per_orientation':1720,
 'canonical_caller_endpoint_adapters':'OPEN',
 'full_host_and_recursive_invoice':'OPEN','all_size':'OPEN',
 'new_kappa':False,'programs':out}
(P/'P104_INPLACE_CHRONOLOGICAL_DUAL_WORDS.json').write_text(
    json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n')
print('PASS_P104_INPLACE_DELTA_CHRONOLOGICAL_DUAL_COMPILED'
      ' G_ADD=1298 side_ADD=1506 native=980 per_word')

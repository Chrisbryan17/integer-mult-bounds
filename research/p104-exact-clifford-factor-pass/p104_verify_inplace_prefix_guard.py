#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact per-register/all-prefix L1 coefficient growth of P104 typed integer
Gram/2 and I-G/2 words. This is a *finite scalar* guard only, not a global
Gaussian phase, physical address, rounding, tape or all-size resource bound.
"""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
words={'Gram_half':'P104_INPLACE_DYADIC_WORD.json',
       'I_minus_Gram_half':'P104_INPLACE_SIDE_WORD.json'}
report={}
for name,path in words.items():
    W=json.loads((P/path).read_text())
    ev=W['events']
    H=sorted({e[2] for e in ev if e[0]=='add' and e[2].startswith('H')})
    roles=['S%d'%j for j in range(104)]+['Y%d'%j for j in range(104)]+H
    assert len(roles)==216
    data={role:{j:1} for j,role in enumerate(roles)}
    peaks={'source':(1,-1,''),'target':(1,-1,''),'helper':(1,-1,'')}
    abs_coef=(1,-1,'')
    for k,e in enumerate(ev):
        typ=e[0]
        if typ=='add':
            _,dst,src,sign,_=e
            for i,v in list(data[src].items()):
                data[dst][i]=data[dst].get(i,0)+sign*v
                if not data[dst][i]:del data[dst][i]
        elif typ=='sign':
            _,role,sign,_=e
            assert sign==-1
            data[role]={i:-v for i,v in data[role].items()}
        elif typ in ('transport','source_to_zero','source_from_zero'):pass
        else:raise AssertionError(('not integral operator',e))
        for role in roles:
            row=data[role];l1=sum(abs(x) for x in row.values())
            group='source' if role[0]=='S' else 'target' if role[0]=='Y' else 'helper'
            if l1>peaks[group][0]:peaks[group]=(l1,k,role)
            coef=max((abs(x) for x in row.values()),default=0)
            if coef>abs_coef[0]:abs_coef=(coef,k,role)
    maximum=max(p[0] for p in peaks.values())
    guard=(maximum-1).bit_length()
    assert (maximum,guard)==((105,7) if name=='Gram_half' else (103,7))
    assert abs_coef[0]==3
    report[name]={
      'all_prefix_events_checked':len(ev),
      'formal_scalar_input_variables':216,
      'maximum_absolute_l1_row_sum':maximum,
      'guard_bits_for_equal_magnitude_input_bound':guard,
      'maximum_absolute_single_input_coefficient':abs_coef[0],
      'locations':{k:{'l1':v[0],'event':v[1],'register':v[2]}
                   for k,v in peaks.items()}}
assert report['Gram_half']['locations']['source']['l1']==98
assert report['I_minus_Gram_half']['locations']['source']['l1']==98
output={'schema':'p104-inplace-exact-all-prefix-finite-scalar-growth/1',
 'status':'PASS_FINITE_PREFIX',
 'type_domain':'Z scalar numerator; p input magnitude bits +7 magnitude guard',
 'results':report,'global_analytic_precision_rounding':'OPEN',
 'physical_address_and_host_tape':'OPEN','all_size':'OPEN','new_kappa':False}
(P/'P104_INPLACE_PREFIX_GUARD.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
print('PASS_P104_EXACT_7_BIT_PREFIX_GUARD'
      ' Gram_half_l1=105 I_minus_G_half_l1=103'
      ' source_peak=98 single_coefficient_peak=3'
      ' global_precision_and_all_size_OPEN')

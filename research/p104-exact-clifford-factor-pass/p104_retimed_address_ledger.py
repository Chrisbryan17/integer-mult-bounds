#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Explicit, independently verified reversible GL(9,2) address-program counts.
CNOT equivalents, CZ and phase operations are NOT free and NOT recursively
priced native children. This ledger intentionally excludes unadmitted hosting.
"""
from pathlib import Path
import json,collections
P=Path(__file__).resolve().parent
cache={}
def lower(rows):
    A=list(rows);word=[]
    for col in range(9):
        pivot=next(i for i in range(col,9) if (A[i]>>col)&1)
        if pivot!=col:
            A[col],A[pivot]=A[pivot],A[col]
            word.append(('SWAP',col,pivot))
        for i in range(9):
            if i!=col and (A[i]>>col)&1:
                A[i]^=A[col];word.append(('CNOT',i,col))
    assert A==[1<<i for i in range(9)]
    return list(reversed(word))
def apply(word,x):
    for kind,i,j in word:
        if kind=='CNOT':
            if (x>>j)&1:x^=1<<i
        elif ((x>>i)^(x>>j))&1:
            x^=(1<<i)|(1<<j)
    return x
results={}
for mode in ('G','I_minus_G_half'):
    for orient in ('forward','dual'):
        file=('P104_ROUTED_NATIVE_' if orient=='forward' else 'P104_RETIMED_DELTA_NATIVE_')+mode+'.json'
        data=json.loads((P/file).read_text())
        items=data['recipes'] if orient=='forward' else data['records']
        names=('left_monomial','right_monomial') if orient=='forward' else ('left','right')
        totals=collections.Counter();max_CNOT=0
        for record in items:
            n=record['occurrences'] if orient=='forward' else record['count']
            for key in names:
                m=record[key];G=tuple(m['matrix_rows'])
                if G not in cache:
                    gates=lower(G)
                    for x in range(512):
                        y=sum((((G[i]&x).bit_count())&1)<<i for i in range(9))
                        assert apply(gates,x)==y
                    cache[G]=gates
                gates=cache[G]
                cnot=sum(k=='CNOT' for k,i,j in gates)
                swaps=sum(k=='SWAP' for k,i,j in gates)
                max_CNOT=max(max_CNOT,cnot+3*swaps)
                totals['monomial_records']+=n
                totals['logical_CNOT_equivalent']+=n*(cnot+3*swaps)
                totals['SWAP_explicit']+=n*swaps
                totals['linear_Z4_coefficients']+=n*sum(bool(v) for v in m['linear_Z4'])
                totals['quadratic_CZ_cross_terms']+=n*sum((row>>(i+1)).bit_count()
                                             for i,row in enumerate(m['quadratic_rows']))
                totals['nonzero_X_offsets']+=n*bool(m['offset'])
                totals['X_offset_bit_count']+=n*m['offset'].bit_count()
                totals['nonzero_global_PH']+=n*bool(m['phase'])
        assert max_CNOT<=96
        assert totals['monomial_records']==2*(687 if mode=='G' else 703)
        results[mode+'__'+orient]={'totals':dict(sorted(totals.items())),
            'maximum_CNOT_equivalent_per_GL9':max_CNOT}
        print('PASS_P104_MONOMIAL_LOWERING',mode,orient,
              totals['logical_CNOT_equivalent'],flush=True)
result={'schema':'p104-retimed-reversible-address-subledger/1',
 'status':'PASS_EXACT_LOGICAL_ADDRESS_CIRCUITS',
 'distinct_GL9_matrices_independently_checked_all_512_addresses':len(cache),
 'scope':'internal transport monomials only, excludes 208 native source-port children and target rank-zero adapters',
 'CNOT_upper_bound_per_GL9':96,
 'array_RAM_traffic_model':'each tensor-factor CNOT costs at most 512^lambda complex-cell accesses; one diagonal or nonzero X record costs <=2*512^lambda accesses; lambda factor for CNOT',
 'physical_tape_head_and_host_cost':'OPEN',
 'complete_recursive_invoice':'OPEN','selected_moment':'OPEN',
 'all_size':'OPEN','new_kappa':False,'programs':results}
(P/'P104_RETIMED_MONOMIAL_ADDRESS_LEDGER.json').write_text(
 json.dumps(result,sort_keys=True,indent=2)+'\n')

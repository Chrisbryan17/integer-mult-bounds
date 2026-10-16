#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Occurrence-weighted positive native-child, monomial and signed-scalar
subledger. This does NOT price recursive hosting, source or precision.
"""
from pathlib import Path
import collections,json
P=Path(__file__).resolve().parent
w=json.loads((P/'P104_RANK_R_NATIVE_RECIPES.json').read_text())
d=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
S='a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39'
assert w['source_word_sha256']==d['source_pin']==S
counts=collections.Counter();ranks=collections.Counter();addr=collections.Counter()
for t in w['transports']:
    n=t['occurrences'];rank=t['rank']
    counts['transport_occurrences']+=n
    counts['one_rank_r_child']+=n;ranks[rank]+=n
    for role in ('left_monomial','right_monomial'):
        m=t[role];G=m['matrix_rows'];Q=m['quadratic_rows']
        a=m['linear_Z4'];b=m['offset'];p=m['phase']
        assert len(G)==len(Q)==len(a)==9
        assert len({sum(((G[i]>>j)&1)<<i for i in range(9))
                    for j in range(9)})==9
        assert all(((Q[i]>>j)&1)==((Q[j]>>i)&1)
                   for i in range(9) for j in range(9))
        assert all(((Q[i]>>i)&1)==(a[i]&1) for i in range(9))
        counts['monomial_records']+=n
        counts['nonidentity_G']+=n*int(G!=[1<<i for i in range(9)])
        counts['out_of_place_linear_form_xors']+=n*sum(
            max(0,x.bit_count()-1) for x in G)
        counts['nonzero_X_offsets']+=n*bool(b)
        counts['X_offset_popcount']+=n*b.bit_count()
        counts['nonzero_global_PH']+=n*bool(p)
        counts['global_phase_exponent_mod4_sum']+=n*p
        counts['nonzero_linear_Z4_coeffs']+=n*sum(x!=0 for x in a)
        counts['quadratic_cross_terms']+=n*sum(
            (Q[i]>>(i+1)).bit_count() for i in range(9))
        addr[b.bit_count()]+=n
    counts['affine_coset_X_corrections_before_fusion']+=n*t['affine_X_corrections']
    counts['negative_C_axis_corrections_before_fusion']+=n*t['negative_C_absorbed_into_X']
assert counts['transport_occurrences']==counts['one_rank_r_child']==756
assert sum(rank*v for rank,v in ranks.items())==1496
assert counts['monomial_records']==1512
adds=collections.Counter(len(d['frames'][e[4]]) for e in d['events']
                         if e[0]=='add')
assert dict(sorted(adds.items()))=={0:156,1:76,2:88,3:48,4:44,5:24,6:12}
report={
 'schema':'p104-borrowed-dirty-native-literal-subledger/1',
 'source_word_sha256':S,'positive_rank_r_histogram':dict(sorted(ranks.items())),
 'positive_rank_r_mass':sum(k*v for k,v in ranks.items()),
 'addition_rank_histogram':dict(sorted(adds.items())),
 'counts':dict(sorted(counts.items())),
 'X_offset_popcount_histogram':{str(k):v for k,v in sorted(addr.items())},
 'not_a_recursive_invoice':[
   'monomial prices unknown; XOR form counts not an in-place address bill',
   'source access/mutation, 100 early Y owners, eight preserved dirty helpers',
   'paid host/idle/tape/precision/physical endpoint inverse transpose',
   'optimized selected #1094 comparator, moments/outer/bit H1-H5/rounding'],
 'new_kappa':False,'physical_supplier_admitted':False}
(P/'P104_RANK_R_LITERAL_LEDGER.json').write_text(
    json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS_P104_RANK_R_NATIVE_LITERAL_LEDGER',dict(sorted(counts.items())),
      'rank_hist',dict(sorted(ranks.items())),
      'ADD_hist',dict(sorted(adds.items())),flush=True)

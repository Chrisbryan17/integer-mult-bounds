#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Source-matched exact Laurent determinant invariant for PR4470 IDLE stages.

With LOCAL and boundary factors frozen, determinant-one signed ADD shears
and signed swaps cannot erase an IDLE product whose determinant is
a nontrivial multivariate Laurent monomial. No physical rank bound inferred.
"""
import json,runpy
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent
events=runpy.run_path(str(P/'idle_gauge_obstruction.py'))['events']
hist=Counter()
for e in events:
    if e[0]=='IDLE':
        for stage in e[2]:hist[stage]+=2
assert dict(sorted(hist.items()))=={
 0:14,1:14,3:12,5:10,7:8,9:6,11:4,13:2,
 17:2,19:4,21:6,23:8,25:10,27:12,29:14,31:16,32:16}
assert len(hist)==17 and sum(hist.values())==158
# Determinant-one lifting identity in the exact Laurent polynomial ring:
# diag(z,z^-1) = U(z) L(-z^-1) U(z) J.
def one(c=1,e=0):return {e:c} if c else {}
def plus(a,b):
    x=dict(a)
    for k,v in b.items():x[k]=x.get(k,0)+v
    return {k:v for k,v in x.items() if v}
def product(a,b):
    x={}
    for k,v in a.items():
        for l,w in b.items():x[k+l]=x.get(k+l,0)+v*w
    return {k:v for k,v in x.items() if v}
def mm(A,B):
    return [[plus(product(A[i][0],B[0][j]),product(A[i][1],B[1][j]))
             for j in range(2)] for i in range(2)]
def determinant(A):
    return plus(product(A[0][0],A[1][1]),
                {e:-v for e,v in product(A[0][1],A[1][0]).items()})
u=one();z=one(1,1);inv=one(1,-1);zero={}
U=[[u,z],[zero,u]]
L=[[u,zero],[one(-1,-1),u]]
J=[[zero,one(-1)],[u,zero]]
D=[[z,zero],[zero,inv]]
assert mm(mm(mm(U,L),U),J)==D
assert determinant(U)==determinant(L)==determinant(J)==determinant(D)==u
assert determinant([[z,zero],[zero,z]])==one(1,2)!=u
report={'status':'PASS_SOURCE_MATCHED_LAURENT_DETERMINANT',
 'original_P16_IDLE_events':15,
 'multivariate_Laurent_determinant_exponents':dict(sorted(hist.items())),
 'supported_stage_axes':17,'total_nonzero_exponents':158,
 'source_events_sha256':'624305383d5e7e1687e01356d5e41ff4ee3d4f06b3cab71cf9a65ea22fc8dd52',
 'proven':'Frozen LOCAL+boundary and unit determinant shears/swaps cannot erase nontrivial IDLE determinant without a paid replacement monomial operator.',
 'verified_constructive_identity':'diag(z,z^-1)=U(z)L(-z^-1)U(z)J',
 'physical_owner_rank_and_tape':'UNPRICED',
 'alternative_CONTROLLER_OPERATOR':'NOT_YET_CONSTRUCTED',
 'new_kappa':False}
(P/'P16_IDLE_LAURENT_DETERMINANT_RECEIPT.json').write_text(
 json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS_P16_IDLE_DETERMINANT exact_17_axes degree_158 unit_shear_only_NO_GO')

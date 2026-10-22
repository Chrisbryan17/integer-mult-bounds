#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact W2 independent-input query rank barrier, anchored to PR4470 window.

Restricts cheap operations to q-free invertible integer shears/permutations.
One rank-one q-oracle cannot realize two independent rank-one q-updates.
Exhaustive shortest four-register signed shear sandwich: four ADDs.
Not a bound on enlarged native or nonlinear batched architectures.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json,random
P=Path(__file__).resolve().parent
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(A,B):
 n=len(A);return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def sh(n,d,s,sign):
 M=eye(n);assert d!=s and sign in (-1,1);M[d][s]=sign;return M
def inverse(word,n):
 A=eye(n)
 for d,s,c in word:A=mm(sh(n,d,s,c),A)
 AI=eye(n)
 for d,s,c in reversed(word):AI=mm(sh(n,d,s,-c),AI)
 assert mm(A,AI)==eye(n)
 return A,AI
def qmatrix(n,pairs):
 A=[[0]*n for _ in range(n)]
 for i in pairs:A[2*i+1][2*i]=1
 return A
def factor(word,n,pairs):
 A,AI=inverse(word,n)
 return mm(mm(AI,qmatrix(n,pairs)),A)
def rank(M):
 A=[[Fraction(x) for x in row] for row in M]
 n=len(A);r=0
 for j in range(len(A[0])):
  p=next((i for i in range(r,n) if A[i][j]),None)
  if p is None:continue
  A[r],A[p]=A[p],A[r];v=A[r][j];A[r]=[x/v for x in A[r]]
  for i in range(n):
   if i!=r and A[i][j]:
    v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[r])]
  r+=1
  if r==n:break
 return r
word=[(0,2,1),(3,1,-1)]
Q=factor(word,4,[0])
assert Q==[[0,0,0,0],[1,0,1,0],[0,0,0,0],[1,0,1,0]]
assert rank(Q)==1
options=[(i,j,c) for i in range(4) for j in range(4) if i!=j for c in (-1,1)]
counts={}
for k in range(3):
 counts[k]=sum(factor(w,4,[0])==Q for w in product(options,repeat=k))
assert counts=={0:0,1:0,2:2}
# Because the q-free constant term must remain the identity, a query
# sandwich A^-1 (I+qE) A with two signed pre-ADDs needs the two inverse
# post-ADDs. Thus minimum 4 for this single-query window alphabet.
Q2=[[0]*8 for _ in range(8)]
for offset in (0,4):
 for i in range(4):
  for j in range(4):Q2[offset+i][offset+j]=Q[i][j]
assert rank(Q2)==2
twice=word+[(a+4,b+4,c) for a,b,c in word]
assert factor(twice,8,[0,2])==Q2
rng=random.Random(20261022)
for j in range(100):
 cross=[(rng.randrange(4),rng.randrange(4,8),rng.choice((-1,1))) for _ in range(6)]
 A,AI=inverse(cross,8)
 assert rank(mm(mm(A,Q2),AI))==2
report={'status':'PASS_W2_RANK_LOWER_BOUND',
 'source':'PR4470 five-event unit shear/QUERY window',
 'W1_exact_q_update_rank':1,'W2_exact_q_update_rank':2,
 'minimum_W2_rank1_queries_under_q_free_GL8':2,
 'W1_exhaustive_pre_shear_lengths_0_to_2':counts,
 'minimum_original_W1_signed_ADDs_with_one_query':4,
 'arbitrary_cross_instance_GL8_mutations_checked':100,
 'condition':'Only rank-one q-dependent query primitive, all remaining gates q-independent invertible and cleanly restored; no free q-dependent ADD.',
 'unadmitted_multisite_query':'OPEN','improved_kappa':False}
(P/'W2_RANK_QUERY_NO_GO.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS_P16_W2_QUERY_RANK_BARRIER rank2_needs_2_oracles; W1_length2_search=2')

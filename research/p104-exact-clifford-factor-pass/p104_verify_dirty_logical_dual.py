#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent exact-integer *logical* inverse-transpose check for all 120
formal P104 inputs. Physical canonical Clifford endpoints remain OPEN.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
word=json.loads((ROOT/'P104_BORROWED_DIRTY_WORD.json').read_text())
N=120
H=sorted({e[2] for e in word['events']
          if e[0]=='add' and e[2].startswith('H')})
assert len(H)==8
names=[f'X{i}' for i in range(8)]+[f'Y{i}' for i in range(104)]+H
idx={name:i for i,name in enumerate(names)}
adds=[e for e in word['events'] if e[0]=='add']
assert len(adds)==448

def execute(rows,ops):
    for d,s,sgn in ops:
        a,b=rows[d],rows[s]
        for k,v in b.items():
            a[k]=a.get(k,0)+sgn*v
            if not a[k]:del a[k]
    return rows

I=[{i:1} for i in range(N)]
ops=[(idx[e[1]],idx[e[2]],e[3]) for e in adds]
F=execute([r.copy() for r in I],ops)
C={}
for t in range(104):
    j=8+t
    assert F[j].get(j)==1
    assert all((k<8 or k==j) for k in F[j])
    C[t]={k:v for k,v in F[j].items() if k<8}
for i in list(range(8))+list(range(112,120)):assert F[i]==I[i]
ideal=[r.copy() for r in I]
for t,row in C.items():
    for i,v in row.items():ideal[i][8+t]=-v
# (AB)^(-T)=A^(-T)B^(-T), so dual elementary ADDs stay in the
# original chronological order, with source/target swapped and sign negated.
dual_ops=[(s,d,-sgn) for d,s,sgn in ops]
D=execute([r.copy() for r in I],dual_ops)
assert D==ideal
for a in range(N):
    for b in range(N):
        total=sum(F[k].get(a,0)*D[k].get(b,0) for k in range(N))
        assert total==int(a==b),(a,b,total)
err=dual_ops.copy()
err[0]=(err[0][0],err[0][1],-err[0][2])
assert execute([r.copy() for r in I],err)!=ideal
print('PASS_P104_BORROWED_DIRTY_LOGICAL_DUAL columns=120 '
      'forward_ADD=448 transpose_inverse_ADD=448 '
      'Ftranspose_times_D=I exact_integer=YES '
      'wrong_sign_REJECTED physical_endpoints_OPEN full_recursive_invoice_OPEN')

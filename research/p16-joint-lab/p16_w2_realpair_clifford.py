#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""One rank-r complex Clifford F_r computes TWO independent REAL transforms.

F_r = product_j (I+i X_(1<<j))/sqrt(2), j=0..r-1.
F_r F_r^T = i^r X_(2^r-1) exactly, global phase included.
For real x,y, w=F_r(x+i*y), recover:
 Fx=(w+i^r X_mask conjugate(w))/2,
 Fy=(w-i^r X_mask conjugate(w))/(2i).
This is not valid for TWO arbitrary complex inputs and does NOT establish a
new P16 whole-supplier cost, physical owners, output credit or kappa.
"""
from collections import defaultdict
from pathlib import Path
import json,random
P=Path(__file__).resolve().parent
def add(a,b):return a[0]+b[0],a[1]+b[1]
def irot(a,p):
 for _ in range(p%4):a=(-a[1],a[0])
 return a
def F(values,r):
 out={k:v for k,v in values.items() if v!=(0,0)}
 for j in range(r):
  nxt=defaultdict(lambda:(0,0))
  for k,v in out.items():
   nxt[k]=add(nxt[k],v)
   nxt[k^(1<<j)]=add(nxt[k^(1<<j)],irot(v,1))
  out={k:v for k,v in nxt.items() if v!=(0,0)}
 return out
def recover(w,r):
 mask=(1<<r)-1;x={};y={}
 for k in set(w)|{k^mask for k in w}:
  a=w.get(k,(0,0));c=w.get(k^mask,(0,0))
  b=irot((c[0],-c[1]),r)
  s=add(a,b);d=(a[0]-b[0],a[1]-b[1])
  assert s[0]%2==s[1]%2==d[0]%2==d[1]%2==0
  xx=(s[0]//2,s[1]//2);yy=(d[1]//2,-d[0]//2)
  if xx!=(0,0):x[k]=xx
  if yy!=(0,0):y[k]=yy
 return x,y
def verify(x,y,r):
 inp={k:(v,0) for k,v in x.items()}
 for k,v in y.items():inp[k]=add(inp.get(k,(0,0)),(0,v))
 a,b=recover(F(inp,r),r)
 assert a==F({k:(v,0) for k,v in x.items()},r)
 assert b==F({k:(v,0) for k,v in y.items()},r)
def run():
 rng=random.Random(20261022)
 for r in range(1,10):
  for k in range(512):
   verify({k:1},{},r);verify({},{k:1},r)
  for _ in range(64):
   x={rng.randrange(512):rng.choice((-11,-7,-3,1,5,9)) for j in range(5)}
   y={rng.randrange(512):rng.choice((-11,-7,-3,1,5,9)) for j in range(5)}
   verify(x,y,r)
 # Two arbitrary COMPLEX input registers cannot be injected into one.
 # (x,y)->x+i*y has a nontrivial complex-linear kernel:
 # (x,y) and (x+i*delta,y-delta) have the identical packed input.
 x=(3,4);y=(5,6);delta=(2,-7)
 newx=add(x,irot(delta,1));newy=(y[0]-delta[0],y[1]-delta[1])
 assert add(x,irot(y,1))==add(newx,irot(newy,1))
 assert (x,y)!=(newx,newy)
 receipt={'status':'PASS_EXACT_W2_REALPAIR_FOURIER',
 'ranks':[1,2,3,4,5,6,7,8,9],'basis_columns_per_rank':1024,
 'random_real_input_pairs_per_rank':64,
 'total_exact_basis_columns':9216,'total_random_pairs':576,
 'exact_global_phase':'i^r','exact_division_by_two':'CHECKED_IN_GAUSSIAN_NUMERATORS',
 'source_domain':'two independent REAL arrays',
 'cannot_replace_two_arbitrary_complex_inputs':True,
 'complex_input_collision':'EXHIBITED',
 'old_native_complex_F_r_calls':2,'new_calls_for_two_real_inputs':1,
 'recovery_price':'conjugation, X_mask address permutation, i^r phase, two Gaussian adds and exact division by 2',
 'whole_recursive_supplier_and_bit_transfer':'OPEN',
 'selected_kappa':'0.00302015','new_kappa':False}
 (P/'P16_REALPAIR_CLIFFORD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
 print('PASS_P16_W2_REALPAIR_CLIFFORD 9216_basis_columns 576_random r=1..9 complex_inputs_NO_GO')
if __name__=='__main__':run()

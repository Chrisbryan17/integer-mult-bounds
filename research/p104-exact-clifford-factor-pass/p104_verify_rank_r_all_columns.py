#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent exact Gaussian 512-column verifier for all 514 positive-rank-r
Clifford recipes, with native X offsets and global phase included.
"""
from pathlib import Path
import json,hashlib,collections,time
import numpy as np
ROOT=Path(__file__).resolve().parent;M=512;N=9
S='a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39'
WORD=ROOT/'p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json'
if not WORD.exists():WORD=ROOT/'p104_native_e8_gate/evidence/NATIVE_CHART_WORD.json'
orig=json.loads(WORD.read_text())
assert hashlib.sha256(WORD.read_bytes()).hexdigest()==S
factor=json.loads((ROOT/'P104_RANK_R_NATIVE_RECIPES.json').read_text())
assert factor['source_word_sha256']==S
orig_recipes={(t['old'],t['new']):t['gates'] for t in orig['transports']}
assert len(orig_recipes)==len(factor['transports'])==514
bits=np.array([(x>>j)&1 for x in range(M) for j in range(N)],dtype=np.int8).reshape(M,N)
indices=np.arange(M,dtype=np.int64)
cache={}
def perm(rows):
    key=('P',tuple(rows))
    if key not in cache:
        dest=np.zeros(M,dtype=np.int64)
        for i in range(N):
            v=sum((bits[:,j] for j in range(N) if (rows[i]>>j)&1),
                  start=np.zeros(M,dtype=np.int64))%2
            dest|=v<<i
        cache[key]=dest
    return cache[key]
def diag(Q,alpha):
    key=('D',tuple(Q),tuple(alpha))
    if key not in cache:
        phase=np.zeros(M,dtype=np.int64)
        for i in range(N):
            phase+=int(alpha[i])*bits[:,i]
            for j in range(i+1,N):
                if (Q[i]>>j)&1:phase+=2*bits[:,i]*bits[:,j]
        cache[key]=np.asarray(phase%4,dtype=np.uint8)
    return cache[key]

def matrix(gates):
    r=np.eye(M,dtype=np.int64);im=np.zeros((M,M),dtype=np.int64);power=0
    for g in gates:
        typ=g[0]
        if typ in ('P','X'):
            dest=perm(g[1]) if typ=='P' else (indices^g[1])
            nr=np.empty_like(r);ni=np.empty_like(im)
            nr[dest],ni[dest]=r,im
            r,im=nr,ni
        elif typ=='D':
            phase=diag(g[1],g[2]);nr=r.copy();ni=im.copy()
            one=(phase==1);two=(phase==2);three=(phase==3)
            nr[one],ni[one]=-im[one],r[one]
            nr[two],ni[two]=-r[two],-im[two]
            nr[three],ni[three]=im[three],-r[three]
            r,im=nr,ni
        elif typ=='PH':
            p=g[1]%4
            if p==1:r,im=-im,r
            if p==2:r,im=-r,-im
            if p==3:r,im=im,-r
        elif typ=='C':
            q,sign=g[1:]
            assert 0<q<M and sign in (-1,1)
            ix=indices^q
            if sign==1:
                nr=r-im+r[ix]+im[ix]
                ni=r+im-r[ix]+im[ix]
            else:
                nr=r+im+r[ix]-im[ix]
                ni=im-r+r[ix]+im[ix]
            r,im=nr,ni;power+=1
        else:raise AssertionError(('unknown gate',g))
    return r,im,power

def identical(a,b):
    ra,ia,ka=matrix(a);rb,ib,kb=matrix(b)
    return np.array_equal(ra<<kb,rb<<ka) and np.array_equal(ia<<kb,ib<<ka)

t0=time.monotonic();root_counts=collections.Counter()
for j,t in enumerate(factor['transports']):
    key=(t['old'],t['new']);orig_word=orig_recipes[key]
    gates=t['gates'];r=t['rank']
    assert sum(g[0]=='C' for g in gates)==r
    assert all(g[2]==1 for g in gates if g[0]=='C')
    assert identical(orig_word,gates),(j,key)
    n=t['occurrences']
    root_counts['rank_mass']+=n*r
    root_counts['rank_children']+=n
assert (root_counts['rank_mass'],root_counts['rank_children'])==(1496,756)

# Detect wrong phase, signed-Fourier direction and monomial X offset.
first=factor['transports'][0]
changed=[list(g) for g in first['gates']]
changed[-1][1]=(changed[-1][1]+1)%4
assert not identical(orig_recipes[first['old'],first['new']],changed)
changed=[list(g) for g in first['gates']]
ci=next(i for i,g in enumerate(changed) if g[0]=='C')
changed[ci][2]*=-1
assert not identical(orig_recipes[first['old'],first['new']],changed)
changed=[list(g) for g in first['gates']]
xi=next(i for i,g in enumerate(changed) if g[0]=='X')
changed[xi][1]^=1
assert not identical(orig_recipes[first['old'],first['new']],changed)
for q in (1,81,511):
    assert identical([['C',q,1],['C',q,1]],[['X',q]])
    assert identical([['C',q,-1]],[['C',q,1],['X',q]])
report={'status':'PASS_EXACT_ALL_COLUMNS','source_word_sha256':S,
        'recipes':514,'basis_columns':512,'child_calls':756,'rank_mass':1496,
        'monomial_sides_per_call':2,'positive_native_children':True,
        'global_phase_control':'REJECTED','signed_C_control':'REJECTED',
        'X_offset_control':'REJECTED','actual_recursive_supplier_admitted':False,
        'full_recursive_invoice':False,'new_kappa':False}
(ROOT/'P104_RANK_R_512_COLUMN_RECEIPT.json').write_text(
    json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS_P104_POSITIVE_RANK_R_512_COLUMNS exact_phase=YES recipes=514 '
      'columns=512 paid_child_calls=756 rank_mass=1496 '
      'X_PHASE_AND_SIGN_CONTROLS_REJECTED elapsed=%.2fs' % (time.monotonic()-t0))

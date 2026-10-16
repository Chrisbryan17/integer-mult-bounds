#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact-phase P104 one-positive-F_r Clifford child lowering with selected
monomial (D,P,X,PH) record schema. Source/owner/host/tape costs still OPEN.
"""
from pathlib import Path
import json, hashlib, collections
ROOT=Path(__file__).resolve().parent
SOURCE='a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39'
M=512;N=9

def parity(x):return x.bit_count()&1
def apply_matrix(rows,x):
    return sum(parity(z&x)<<i for i,z in enumerate(rows))
def phase_diagonal(Q,alpha,x):
    result=sum(alpha[i] for i in range(N) if x>>i&1)
    for i in range(N):
        if x>>i&1:
            result += 2*sum((Q[i]>>j)&1 for j in range(i+1,N) if x>>j&1)
    return result%4
def monomial_apply(gates,x):
    p=0
    for g in gates:
        k=g[0]
        if k=='P':x=apply_matrix(g[1],x)
        elif k=='D':p=(p+phase_diagonal(g[1],g[2],x))%4
        elif k=='X':x ^= g[1]
        elif k=='PH':p=(p+g[1])%4
        else:raise AssertionError(('not monomial',g))
    return x,p

def normalize(gates):
    values=[monomial_apply(gates,j) for j in range(M)]
    b,p0=values[0]
    cols=[values[1<<i][0]^b for i in range(N)]
    G=[sum(((cols[j]>>i)&1)<<j for j in range(N)) for i in range(N)]
    alpha=[(values[1<<i][1]-p0)%4 for i in range(N)]
    Q=[(alpha[i]&1)<<i for i in range(N)]
    for i in range(N):
        for j in range(i+1,N):
            mix=(values[(1<<i)|(1<<j)][1]-values[1<<i][1]-values[1<<j][1]+p0)%4
            assert mix in (0,2),(i,j,mix)
            Q[i]|=(mix//2)<<j
            Q[j]|=(mix//2)<<i
    record={'quadratic_rows':Q,'linear_Z4':alpha,'matrix_rows':G,
            'offset':b,'phase':p0}
    assert all(((Q[i]>>j)&1)==((Q[j]>>i)&1) for i in range(N) for j in range(N))
    assert all((alpha[i]&1)==((Q[i]>>i)&1) for i in range(N))
    assert len({apply_matrix(G,x) for x in range(M)})==M
    assert all((apply_matrix(G,x)^b,(phase_diagonal(Q,alpha,x)+p0)%4)==values[x]
               for x in range(M)),('monomial normal form',record)
    return record

def gates_of(rec):
    return [['D',rec['quadratic_rows'],rec['linear_Z4']],
            ['P',rec['matrix_rows']],['X',rec['offset']],['PH',rec['phase']]]

def lower(original):
    word=original['gates'];r=original['rank']
    begin=next(i for i,g in enumerate(word) if g[0]=='C')
    original_core=word[begin:begin+r]
    assert all(g[0]=='C' and g[1]==1<<i and g[2] in (-1,1)
               for i,g in enumerate(original_core))
    neg=sum(g[1] for g in original_core if g[2]==-1)
    prefix=word[:begin]
    suffix=[];after=word[begin+r:];j=0;affine=0
    while j<len(after):
        g=after[j]
        if g[0]!='C':
            suffix.append(g);j+=1
        else:
            assert j+1<len(after) and after[j+1]==g and g[2]==1
            # Exact identity C(q,+)^2=X(q), including global phase.
            suffix.append(['X',g[1]]);affine+=1;j+=2
    assert affine in (0,1)
    assert all(g[0]!='C' for g in prefix+suffix)
    first=normalize(prefix)
    final=normalize(([['X',neg]] if neg else []) +suffix)
    child=[['C',1<<i,1] for i in range(r)]
    new=gates_of(first)+child+gates_of(final)
    return {'old':original['old'],'new':original['new'],'rank':r,
        'occurrences':original['occurrences'],
        'left_monomial':first,'native_positive_child':r,
        'right_monomial':final,
        'negative_C_absorbed_into_X':neg.bit_count(),
        'affine_X_corrections':affine,
        'gates':new}

def run():
    old=json.loads((ROOT/'P104_MINIMAL_C_CANDIDATES.json').read_text())
    assert old['source_word_sha256']==SOURCE
    rows=[lower(t) for t in old['transports']]
    assert len(rows)==514
    counts=collections.Counter()
    for r in rows:
        n=r['occurrences'];counts['transports']+=n
        counts['rank_mass']+=n*r['rank']
        counts['positive_native_rank_r_children']+=n
        counts['affine_X_occurrences']+=n*r['affine_X_corrections']
        counts['core_sign_X_axis_mass']+=n*r['negative_C_absorbed_into_X']
        counts['recorded_monomial_sides']+=2*n
    assert counts['transports']==756 and counts['rank_mass']==1496
    assert counts['positive_native_rank_r_children']==756
    assert counts['affine_X_occurrences']==168
    receipt={'schema':'p104-one-native-positive-child-per-transport/1',
      'scope':'exact canonical chart operator, paid address/source/owner/precision OPEN',
      'selected_supplier_admitted':False,'new_kappa':False,
      'source_word_sha256':SOURCE,'counts':dict(counts), 'transports':rows}
    p=ROOT/'P104_RANK_R_NATIVE_RECIPES.json'
    p.write_text(json.dumps(receipt,sort_keys=True,separators=(',',':'))+'\n')
    print('PASS_P104_POSITIVE_RANK_R_CONSTRUCTION distinct=514 '
          'moves=756 rank_mass=1496 affine_X_occurrences=168 '
          'all_monomial_normal_forms_512_addresses=YES '
          'exact_phase_checker_NEXT',flush=True)

if __name__=='__main__':run()

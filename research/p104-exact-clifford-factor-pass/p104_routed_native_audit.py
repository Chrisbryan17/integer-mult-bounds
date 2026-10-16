#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact physical E8 Clifford compilation of optimally retimed P104 words.
Checks all distinct recipes with 18 generator images and 10 exact Gaussian
input columns (global phase included). No paid source/owner admission.
"""
from pathlib import Path
import sys,json,collections,hashlib
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
sys.path.insert(0,str(P/'p104_native_e8_gate/scripts'))
import native_chart_emitter as E
from p104_physical_e8_isometry import physical
from p104_minimal_symplectic import factor,symp
from p104_exact_native_factor import correction
from p104_rank_r_native_recipes import lower

def state(gates,source):
    work={source:(1,0)};power=0
    def rot(a,b,p):return [(a,b),(-b,a),(-a,-b),(b,-a)][p%4]
    for gate in gates:
        nxt={};kind=gate[0]
        if kind=='C':
            q,sgn=gate[1:]
            for x,(a,b) in work.items():
                for y,u,v in ((x,a-sgn*b,b+sgn*a),
                              (x^q,a+sgn*b,b-sgn*a)):
                    c,d=nxt.get(y,(0,0));nxt[y]=(c+u,d+v)
            power+=1
        else:
            for x,(a,b) in work.items():
                if kind=='P':
                    x=sum(((row&x).bit_count()&1)<<i for i,row in enumerate(gate[1]))
                elif kind=='X':x^=gate[1]
                elif kind=='D':
                    Q,alpha=gate[1:]
                    p=sum(alpha[i] for i in range(9) if x>>i&1)
                    for i in range(9):
                        if x>>i&1:
                            p+=2*sum((Q[i]>>j)&1 for j in range(i+1,9) if x>>j&1)
                    a,b=rot(a,b,p)
                elif kind=='PH':a,b=rot(a,b,gate[1])
                else:raise AssertionError(gate)
                c,d=nxt.get(x,(0,0));nxt[x]=(c+a,d+b)
        work={x:pair for x,pair in nxt.items() if pair!=(0,0)}
    return work,power

def exact(a,b):
    ap=[g for g in a if g[0]!='X'];bp=[g for g in b if g[0]!='X']
    for i in range(9):
        assert symp(ap,1<<i,0)==symp(bp,1<<i,0)
        assert symp(ap,0,1<<i)==symp(bp,0,1<<i)
    for x in [0]+[1<<i for i in range(9)]:
        A,ka=state(a,x);B,kb=state(b,x)
        assert {i:(v<<kb,w<<kb) for i,(v,w) in A.items()}=={
            i:(v<<ka,w<<ka) for i,(v,w) in B.items()}

def compile_word(label):
    W=json.loads((P/f'P104_INTERSECTION_{label}.json').read_text())
    frames=[tuple(physical(x) for x in fr) for fr in W['frames']]
    occ=collections.Counter((e[2],e[3]) for e in W['events'] if e[0]=='transport')
    records=[];profile=collections.Counter()
    for j,((a,b),n) in enumerate(sorted(occ.items())):
        source=[tuple(g) for g in E.transport(frames[a],frames[b])]
        word,r=factor(source)
        fix,_=correction(source,word)
        candidate=lower({'old':a,'new':b,'rank':r,
                         'occurrences':n,
                         'gates':[list(g) for g in list(word)+fix]})
        assert r==abs(len(frames[a])-len(frames[b]))
        assert sum(g[0]=='C' for g in candidate['gates'])==r
        assert all(g[2]==1 for g in candidate['gates'] if g[0]=='C')
        exact(source,candidate['gates'])
        if j==0:
            for fault in ('phase','sign','offset'):
                broken=[list(g) for g in candidate['gates']]
                k=next(i for i,g in enumerate(broken)
                      if g[0]=={'phase':'PH','sign':'C','offset':'X'}[fault])
                if fault=='phase':broken[k][1]=(broken[k][1]+1)%4
                if fault=='sign':broken[k][2]*=-1
                if fault=='offset':broken[k][1]^=1
                try:exact(source,broken)
                except AssertionError:pass
                else:raise AssertionError('accepted mutation '+fault)
        profile[r]+=n
        records.append({'old':a,'new':b,'rank':r,'occurrences':n,
                        'left_monomial':candidate['left_monomial'],
                        'right_monomial':candidate['right_monomial']})
    assert sum(profile.values())==W['new_counts']['transports']
    assert sum(k*v for k,v in profile.items())==1238
    report={'status':'PASS_FINITE_PHYSICAL_CLIFFORD',
      'scope':'18 signed Pauli basis actions and 10 exact Gaussian columns per recipe',
      'source_word_sha256':W['source_word_sha256'],
      'distinct_native_recipes':len(records),'positive_native_calls':sum(profile.values()),
      'rank_histogram':dict(sorted(profile.items())),'internal_rank_mass':1238,
      'source_port_children':208,'combined_rank_mass':1446,
      'phase_mutation':'REJECTED','sign_mutation':'REJECTED',
      'offset_mutation':'REJECTED','owner_host_tape':'OPEN',
      'selected_recursive_invoice':'OPEN','new_kappa':False,
      'recipes':records}
    (P/f'P104_ROUTED_NATIVE_{label}.json').write_text(
        json.dumps(report,sort_keys=True,separators=(',',':'))+'\n')
    print('PASS_ROUTED_E8_CLIFFORD',label,len(records),sum(profile.values()),1238,flush=True)

if __name__=='__main__':
    for label in ('G','I_minus_G_half'):compile_word(label)

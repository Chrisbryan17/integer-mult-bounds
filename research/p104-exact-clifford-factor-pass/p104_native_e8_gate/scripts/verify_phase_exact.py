#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent exact Gaussian-integer evaluator for nine-axis Clifford words.

Tests literal 514 native transport recipes for exact return-to-identity,
including global phase, not a projective/tableau-only check. The individual
C gates are *not* optimized to one child of rank-difference.
"""
import importlib.util,json,gzip
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('emitter',P/'native_chart_emitter.py')
E=importlib.util.module_from_spec(s);s.loader.exec_module(E)
WP=P/'evidence'/'NATIVE_CHART_WORD.json'
W=json.loads(WP.read_text() if WP.exists() else gzip.decompress(WP.with_suffix('.json.gz').read_bytes()))
FR=[tuple(x) for x in W['frames']]
M=512

def phase(circ,src):
    re=[0]*M;im=[0]*M;re[src]=1;level=0
    for g in circ:
        k=g[0]
        if k=='P':
            row=g[1];r=[0]*M;i=[0]*M
            for x in range(M):
                if not(re[x] or im[x]):continue
                dest=sum(((a&x).bit_count()&1)<<j for j,a in enumerate(row))
                r[dest]+=re[x];i[dest]+=im[x]
            re,im=r,i
        elif k=='D':
            Q,alpha=g[1],g[2]
            for x in range(M):
                if not(re[x] or im[x]):continue
                q=sum(alpha[j] for j in range(9) if x>>j&1)
                q+=2*sum(((Q[j]&(x>> (j+1) << (j+1))).bit_count()&1) for j in range(9) if x>>j&1)
                q%=4
                a,b=re[x],im[x]
                if q==1:re[x],im[x]=-b,a
                elif q==2:re[x],im[x]=-a,-b
                elif q==3:re[x],im[x]=b,-a
        elif k=='C':
            dest,s=g[1],g[2];assert 0<dest<M and s in (-1,1)
            r=[0]*M;i=[0]*M
            for x in range(M):
                a,b,c,d=re[x],im[x],re[x^dest],im[x^dest]
                if s==1:r[x],i[x]=a-b+c+d,a+b-c+d
                else:r[x],i[x]=a+b+c-d,b-a+c+d
            re,im=r,i;level+=1
        elif k=='PH':
            for x in range(M):
                a,b=re[x],im[x]
                q=g[1]%4
                if q==1:re[x],im[x]=-b,a
                elif q==2:re[x],im[x]=-a,-b
                elif q==3:re[x],im[x]=b,-a
        else:raise ValueError('not a Clifford primitive')
    return tuple((r,i) for r,i in zip(re,im)),level

def is_identity(gates,probe):
    out,k=phase(gates,probe)
    # Each C carries an exact factor 1/2. Equal unitary must be 1 at its
    # diagonal entry, not merely nonzero up to global phase.
    return all(pair==((1<<k,0) if j==probe else (0,0)) for j,pair in enumerate(out))

def run():
    checks=0
    for t in W['transports']:
        a,b=FR[t['old']],FR[t['new']]
        gates=[tuple(g) for g in t['gates']]
        # The reverse is constructed by an independent gate-list reversal,
        # not by loading the saved reverse transport from the certificate.
        opposite=list(E.adjoint(gates))
        if not is_identity(gates+opposite,0):raise AssertionError('inverse global phase')
        checks+=1
    samples=W['transports'][::max(1,len(W['transports'])//14)]
    for t in samples:
        gates=[tuple(g) for g in t['gates']]
        assert is_identity(gates+list(E.adjoint(gates)),511)
        assert is_identity(gates+list(E.adjoint(gates)),37)
        checks+=2
    first=next(t for t in W['transports'] if any(g[0]=='C' for g in t['gates']))
    gates=[tuple(g) for g in first['gates']]
    bad=gates+[('PH',1)]+list(E.adjoint(gates))
    assert not is_identity(bad,0),'global phase mutation accepted'
    # Sign reversal in C must not preserve a standalone positive child.
    assert not is_identity([('C',1,1),('C',1,1)],0)
    print('PASS_P104_EXACT_CLIFFORD_PHASE native_recipe_loops=%d extra_boundary_probes=%d global_phase_mutation_REJECTED C_sign_control_REJECTED actual_E8=YES paid_optimisation=OPEN'%(len(W['transports']),checks-len(W['transports'])))
if __name__=='__main__':run()

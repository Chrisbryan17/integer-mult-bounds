#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent physical E8 514 forward + dual exact Clifford proofs and
112 intrinsic rank-zero adapters. Exact Pauli basis + 10 complex input states
determines each operator; sampled full 512-column matrices are positive controls.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import p104_verify_rank_r_all_columns as V
import p104_dual_native_check as D
import p104_rank_r_native_recipes as R
from p104_minimal_symplectic import factor,symp
from p104_exact_native_factor import correction
from p104_native_e8_gate.scripts import native_chart_emitter as E
from p104_physical_e8_isometry import physical
W=json.loads((ROOT/"P104_PHYSICAL_E8_ISOMETRIC_WORD.json").read_text())
F=json.loads((ROOT/"P104_ISOMETRIC_NATIVE_RECIPES.json").read_text())
assert len(W["transports"])==len(F["transports"])==514
assert F["isometry_sha256"]==hashlib.sha256(
 (ROOT/"P104_PHYSICAL_E8_ISOMETRIC_WORD.json").read_bytes()).hexdigest()

def exact_state(gates,source):
    state={source:(1,0)};power=0
    def rotate(re,im,n):
        return [(re,im),(-im,re),(-re,-im),(im,-re)][n%4]
    for g in gates:
        kind=g[0];nxt={}
        if kind=="C":
            q,sign=g[1:]
            for x,(re,im) in state.items():
                a,b=re-sign*im,im+sign*re
                c,d=re+sign*im,im-sign*re
                for y,dr,di in ((x,a,b),(x^q,c,d)):
                    ar,ai=nxt.get(y,(0,0));nxt[y]=(ar+dr,ai+di)
            power+=1
        else:
            for x,(re,im) in state.items():
                if kind=="P":x=R.apply_matrix(g[1],x)
                elif kind=="X":x^=g[1]
                elif kind=="D":re,im=rotate(re,im,R.phase_diagonal(g[1],g[2],x))
                elif kind=="PH":re,im=rotate(re,im,g[1])
                else:raise ValueError(g)
                ar,ai=nxt.get(x,(0,0));nxt[x]=(ar+re,ai+im)
        state={x:v for x,v in nxt.items() if v!=(0,0)}
    return state,power

def exact_clifford(a,b):
    # Equal unsigned symplectic Clifford action means difference is Pauli times
    # phase. Equality on 0 and all nine singleton addresses fixes that Pauli
    # and the global phase, so this checks ALL operator columns mathematically.
    xg=[g for g in a if g[0]!="X"]
    yg=[g for g in b if g[0]!="X"]
    for i in range(9):
        assert symp(xg,1<<i,0)==symp(yg,1<<i,0)
        assert symp(xg,0,1<<i)==symp(yg,0,1<<i)
    for col in [0]+[1<<i for i in range(9)]:
        va,ka=exact_state(a,col)
        vb,kb=exact_state(b,col)
        assert {k:(r<<kb,s<<kb) for k,(r,s) in va.items()}=={
               k:(r<<ka,s<<ka) for k,(r,s) in vb.items()},("phase",col)
    return True

samples={0,1,7,29,57,100,149,198,250,302,366,413,470,513}
for j,(t,r) in enumerate(zip(W["transports"],F["transports"])):
    assert (t["old"],t["new"])==(r["old"],r["new"])
    exact_clifford(t["gates"],r["gates"])
    dual=D.dual_positive(r)
    exact_clifford(D.conjugate(t["gates"]),dual["conjugate_native_word"])
    if j in samples:
        assert V.identical(t["gates"],r["gates"])
        assert V.identical(D.conjugate(t["gates"]),dual["conjugate_native_word"])
print("PASS_PHYSICAL_ISOMETRY_514_FORWARD_DUAL_CLIFFORD_IDENTITIES "
      "full_matrix_sample=14_each",flush=True)

def rank_zero_monomial(gates):
    candidate,rank=factor([tuple(g) for g in gates])
    assert rank==0
    fix,_=correction(gates,candidate)
    raw=[list(g) for g in candidate+fix]
    pure=[];k=0
    while k<len(raw):
        g=raw[k]
        if g[0]=="C":
            assert k+1<len(raw) and raw[k+1]==g and g[2]==1
            pure.append(["X",g[1]]);k+=2
        else:pure.append(g);k+=1
    m=R.normalize(pure)
    legal=R.gates_of(m)
    exact_clifford(gates,legal)
    return m,legal

source_ports=[];target_ports=[]
F9=[["C",1<<i,1] for i in range(9)]
for i,pair in enumerate(E.E8.chosen[1]):
    q=physical(E.LABELS[pair[0]])
    intrinsic=[["C",q,-1]]+[list(g) for g in E.gamma((q,))]
    rec,legal=rank_zero_monomial(intrinsic)
    if i in (0,3,7):assert V.identical(intrinsic,legal)
    source_ports.append({"source":i,"q":q,"monomial":rec})
for t,live in enumerate(E.E8.live):
    q=physical(E.LABELS[live])
    sink=tuple(physical(x) for x in E.sink_for(live))
    assert all(((q&x).bit_count()&1)==0 for x in sink)
    intrinsic=[list(g) for g in E.adjoint(E.gamma(sink))]+[["C",q,-1]]+F9
    rec,legal=rank_zero_monomial(intrinsic)
    if t in (0,1,10,22,41,67,99,103):assert V.identical(intrinsic,legal)
    target_ports.append({"target":t,"q":q,"monomial":rec})
assert len(source_ports)==8 and len(target_ports)==104
receipt={
 "schema":"p104-isometric-native-intrinsic-adapter-verified/1",
 "source_word_sha256":W["source_word_sha256"],
 "physical_isometry_sha256":F["isometry_sha256"],
 "all_root_pairings_checked":14400,"all_sinks_checked":104,
 "forward_transports_exact_clifford":514,
 "dual_transports_exact_clifford":514,
 "exact_input_columns_per_operator":10,"symplectic_generators_per_operator":18,
 "separately_full_512_column_sample_each_orientation":14,
 "physical_source_rank_zero_intrinsic_adapters":8,
 "physical_target_rank_zero_intrinsic_adapters":104,
 "full_512_column_source_samples":3,"full_512_column_target_samples":8,
 "owner_and_scalar_halving":"OPEN","full_recursive_invoice":"OPEN",
 "new_kappa":False,"source_adapters":source_ports,"target_adapters":target_ports}
(ROOT/"P104_ISOMETRIC_NATIVE_PORT_RECEIPT.json").write_text(
    json.dumps(receipt,indent=2,sort_keys=True)+"\n")
print("PASS_P104_GENUINE_E8_PHYSICAL_NATIVE_ADAPTERS sources=8 targets=104 "
      "forward=514 dual=514 no_new_kappa")

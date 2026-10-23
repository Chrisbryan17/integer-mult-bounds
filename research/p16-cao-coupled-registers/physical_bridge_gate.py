#!/usr/bin/env python3
"""Cao #4610: exact phase/dual-native integration of one four-XOR GL9 bridge.

A source-pinned admissible local gauge, but NOT a new or cheaper multiplication
supplier: paid recursive profile and the old conditional kappa are unchanged.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import argparse,gzip,hashlib,json,sys

PIN="cfcd36b40326d7a5815e1db5313444379b3fb756b27d5201c561574c085cc0dd"
PROFILE={1:2201,2:412,3:510,4:127,5:40,8:8}

def span(b):
    s={0}
    for x in b:s|={y^x for y in tuple(s)}
    return s

def run(root):
    src=root/"research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz"
    raw=gzip.decompress(src.read_bytes())
    assert hashlib.sha256(raw).hexdigest()==PIN
    original=json.loads(raw);c=deepcopy(original["canonical"])
    u,v=211,238
    a,ell=16,75
    G=[(1<<i)^(a if ((ell>>i)&1) else 0) for i in range(9)]
    linear=lambda x:__import__('functools').reduce(
        int.__xor__,(G[i] for i in range(9) if (x>>i)&1),0)
    assert all(linear(linear(x))==x for x in range(512))
    assert {linear(x) for x in span(c["frames"][u])}==span(c["frames"][v])
    gates=[(i,j) for i in range(9) if ell>>i&1 for j in range(9) if a>>j&1]
    assert len(gates)==4
    for x in range(512):
        y=x
        for i,j in gates:
            if y>>i&1:y^=1<<j
        assert y==linear(x)
    c["warps"].append({"op":73,"G_columns":G,"from_frame":u,"to_frame":v})
    sys.path.insert(0,str(root/"research/warp-interface-20261022"))
    import warp_merge as W
    F=W.F
    compiled={};details={}
    for d,old in original["programs"].items():
        raw=[deepcopy(x) for x in old if x[0]!="climb"]
        matches=[(i,e) for i,e in enumerate(raw)
                 if e[0]=="scalar" and e[2]==u and e[1][0]=="add"
                 and e[1][1][0]==e[1][2][0]=="L"]
        assert len(matches)==2
        i,event=matches[0]
        dest,source=event[1][1:3]
        new=[["warp",dest,73,u,v],["warp",source,73,u,v],
             ["scalar",deepcopy(event[1]),v],
             ["warp",dest,-73,v,u],["warp",source,-73,v,u]]
        p=W.synthesize(c,raw[:i]+new+raw[i+1:])
        def tariff(program):
            count=Counter(e[5] for e in program if e[0]=="climb")
            count.update(e[4] for e in program if e[0]=="center")
            return +count
        assert tariff(p)==tariff(old)==PROFILE
        assert len(p)==len(old)+4
        compiled[d]=p;details[d]={"raw_event_index":i,"new_events":len(p)}
    V=F.load(root/"research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py","bridge_source_rows")
    X=F.load(root/"research/kappa-rebuild/complex/native_extensions.py","bridge_source_native")
    for d,p in compiled.items():
        backward=d=="backward"
        env=deepcopy(c);env["R"]=408;env["local_profile"]=PROFILE
        rows,receipt=X.literal_replay(V,env,p,backward)
        assert all(rows["L",i]==V.expected(("L",i),[],backward,False) for i in range(632))
        independent=V.replay(p,env,[],backward,False)
        assert independent["all_scalar_frames_checked"] and not independent["mismatch_examples"]
        assert independent["paid_profile"]==receipt["paid_profile"]
        assert receipt["arbitrary_owned_C0_cleared"]
        assert receipt["real_scalar_allowance"]==(158168 if backward else 158120)
        details[d].update(two_632_column_interpreters=True,
                          scalar_allowance=receipt["real_scalar_allowance"],
                          owned_C0_cleared=True)
    ce=F.load(root/"research/t74-native-fast/vendor/native/new/code/borrow/vendor/clifford/clifford_exact.py","bridge_phase_ce")
    P=F.load(root/"research/kappa-function-composition/complex/prune_native.py","bridge_phase_P")
    gm=ce.transpose(tuple(G),9);tr=ce.transpose(ce.inv(gm,9),9)
    quadratic=tuple((1<<i)^sum(ce.parity(x&b)<<j for j,b in enumerate(tr))
                    for i,x in enumerate(tr))
    K=ce.perm(9,gm).then(ce.diag(9,quadratic))
    assert K.then(K).tab==ce.identity(9)
    assert K.then(K).zero_state()==K.adjoint().then(K).zero_state()
    fu=ce.canonical_frame(9,c["frames"][u]);fv=ce.canonical_frame(9,c["frames"][v])
    A=fu.adjoint().then(K).then(fv)
    B=fv.adjoint().then(K.adjoint()).then(fu)
    assert A.then(B).tab==ce.identity(9)
    assert A.then(B).zero_state()==fu.adjoint().then(fu).zero_state()
    checked=0
    for d in ("forward","backward"):
        for sign,physical in ((1,A),(-1,B)):
            actual=P.conjugate(ce,physical) if d=="backward" else physical
            evidence=X.N.lower_exact(P,ce,actual)
            assert evidence["rank"]==0 and evidence["right"] is None
            reconstructed=P.monomial(ce,evidence["left"],9)
            assert reconstructed.tab==actual.tab
            assert reconstructed.zero_state()==actual.zero_state()
            checked+=1
    bad=deepcopy(compiled["forward"])
    mutated=False
    for e in bad:
        if e[0]=="scalar" and e[2]==v and e[1][0]=="add":
            e[1][3]+=1;mutated=True;break
    assert mutated
    rejected=False
    try:
        badenv=deepcopy(c);badenv["local_profile"]=PROFILE;badenv["R"]=408
        rows,_=X.literal_replay(V,badenv,bad,False)
        rejected=any(rows["L",i]!=V.expected(("L",i),[],False,False) for i in range(632))
    except (ValueError,AssertionError):rejected=True
    assert rejected
    return {"status":"PASS_FULL_DUAL_NATIVE_AND_EXACT_PHASE_RANK_NEUTRAL_GAUGE",
        "canonical_sha256":PIN,"source_commit":"20bb93cd990d2ff683e4d0fc56b87a42cd5d3296",
        "registers":details,"source_frame":u,"target_frame":v,
        "new_operator":73,"G_columns":G,"four_controlled_xor_gates":gates,
        "all_512_G_points_checked":True,"exact_signed_clifford_phase_checks":checked,
        "new_clifford_self_inverse":True,"bad_scalar_mutation_rejected":True,
        "paid_profile_unchanged":PROFILE,"native_paid_jobs":3298,
        "whole_controller_paid_jobs":64404,"new_kappa_proved":False,
        "new_warp_execution_cost_is_not_zero_assumed":True,
        "full_uniform_native_supplier_not_accepted":True}

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    result=run(args.source)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(result["status"])

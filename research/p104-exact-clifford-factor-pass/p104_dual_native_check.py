#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact conjugate-Delta Clifford transport: one positive rank-r native child.
Finite physical inverse-transpose transport only; endpoint owner admission OPEN.
"""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import p104_rank_r_native_recipes as R
S="a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39"
source=ROOT/"p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json"
if not source.exists():source=ROOT/"p104_native_e8_gate/evidence/NATIVE_CHART_WORD.json"
assert hashlib.sha256(source.read_bytes()).hexdigest()==S
original=json.loads(source.read_text())
pos=json.loads((ROOT/"P104_RANK_R_NATIVE_RECIPES.json").read_text())
assert len(original["transports"])==len(pos["transports"])==514

def conjugate(gates):
    out=[]
    for gate in gates:
        g=list(gate)
        if g[0]=="D":g[2]=[(-a)%4 for a in g[2]]
        elif g[0]=="PH":g[1]=(-g[1])%4
        elif g[0]=="C":g[2]=-g[2]
        assert g[0] in ("D","PH","C","P","X")
        out.append(g)
    return out

def dual_positive(rec):
    # Exact C(q,-) = C(q,+) X(q), including global phase.
    rank=rec["rank"];mask=(1<<rank)-1
    cg=conjugate(rec["gates"])
    k=next(i for i,g in enumerate(cg) if g[0]=="C")
    assert all(g[0]=="C" and g[1]==(1<<j) and g[2]==-1
               for j,g in enumerate(cg[k:k+rank]))
    assert all(g[0]!="C" for g in cg[:k]+cg[k+rank:])
    left=R.normalize(cg[:k])
    right=R.normalize([["X",mask]]+cg[k+rank:])
    gates=R.gates_of(left)+[["C",1<<j,+1] for j in range(rank)]+R.gates_of(right)
    return {"old":rec["old"],"new":rec["new"],"rank":rank,
            "occurrences":rec["occurrences"],"left":left,"right":right,
            "conjugate_native_word":gates}

def run():
    rows=[dual_positive(t) for t in pos["transports"]]
    assert len(rows)==514 and sum(t["occurrences"] for t in rows)==756
    assert sum(t["rank"]*t["occurrences"] for t in rows)==1496
    out={"schema":"p104-delta-physical-transpose-native/1",
         "source_sha256":S,
         "contract":"Delta_W=conjugate(Gamma_W); no free canonical endpoint adapter",
         "source_rank_r_sha256":hashlib.sha256(
             (ROOT/"P104_RANK_R_NATIVE_RECIPES.json").read_bytes()).hexdigest(),
         "distinct_transports":514,"occurrences":756,"rank_mass":1496,
         "source_owner_and_rounding_open":True,"new_kappa":False,
         "transports":rows}
    (ROOT/"P104_DUAL_NATIVE_RECIPES.json").write_text(
        json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
    print("PASS_DUAL_POSITIVE_RECIPE_CONSTRUCTION recipes=514 occurrences=756 rank_mass=1496")
if __name__=="__main__":run()

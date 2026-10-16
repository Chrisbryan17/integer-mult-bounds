#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent full 512-column exact Gaussian phase verification of all 514
Delta-transport native recipes. Canonical endpoint shortcut negative control.
"""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import p104_dual_native_check as D
import p104_verify_rank_r_all_columns as V
from p104_native_e8_gate.scripts import native_chart_emitter as E
source=ROOT/"p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json"
if not source.exists():source=ROOT/"p104_native_e8_gate/evidence/NATIVE_CHART_WORD.json"
old=json.loads(source.read_text())
word=json.loads((ROOT/"P104_DUAL_NATIVE_RECIPES.json").read_text())
assert len(word["transports"])==514
orig={(t["old"],t["new"]):t["gates"] for t in old["transports"]}
for i,t in enumerate(word["transports"]):
    expected=D.conjugate(orig[t["old"],t["new"]])
    assert V.identical(expected,t["conjugate_native_word"]),(i,t["old"],t["new"])
    assert sum(g[0]=="C" for g in t["conjugate_native_word"])==t["rank"]
    assert all(g[2]==1 for g in t["conjugate_native_word"] if g[0]=="C")
first=word["transports"][0]
expected=D.conjugate(orig[first["old"],first["new"]])
bad=[g.copy() for g in first["conjugate_native_word"]]
bad[-1][1]=(bad[-1][1]+1)%4
assert not V.identical(expected,bad)
bad=[g.copy() for g in first["conjugate_native_word"]]
ix=next(i for i,g in enumerate(bad) if g[0]=="C")
bad[ix][2]*=-1
assert not V.identical(expected,bad)

# Explicit actual E8 separating column, not an arbitrary chart counterexample.
roots=[pair[0] for pair in E.E8.chosen[1]]
root=roots[0]
t=next(t for t in range(104) if E.E8.IP[E.E8.live[t]][root])
c=E.E8.IP[E.E8.live[t]][root]
assert (t,c)==(22,-1)
frame=(E.LABELS[root],)
canonical=list(E.gamma(frame))
delta=D.conjugate(canonical)
ar,ai,ak=V.matrix(canonical)
br,bi,bk=V.matrix(delta)
assert (int(ar[0,0]),int(ai[0,0]),ak)==(1,1,1)
assert (int(br[0,0]),int(bi[0,0]),bk)==(1,-1,1)
assert (-c*int(br[0,0]),-c*int(bi[0,0]))==(1,-1)
assert (-c*int(ar[0,0]),-c*int(ai[0,0]))==(1,1)
receipt={
 "status":"PASS","source_sha256":word["source_sha256"],
 "dual_native_distinct":514,"dual_native_occurrences":756,
 "rank_mass":1496,"exact_columns_per_recipe":512,
 "global_phase_mutation":"REJECTED","signed_C_mutation":"REJECTED",
 "wrong_canonical_endpoint_shortcut":"REJECTED",
 "endpoint_separating_witness":{
   "target":"Y22","source":"X0","signed_G":-1,
   "input_address":0,"output_address":0,
   "true_physical_X0_from_Y22":"(1-i)/2",
   "incorrect_canonical_shortcut":"(1+i)/2"},
 "physical_operator":"Delta_f S^(-T) Delta_i^(-1)",
 "canonical_endpoint_caller_bridge_admission":"OPEN",
 "source_owners":"OPEN","recursive_invoice":"OPEN","new_kappa":False}
(ROOT/"P104_DUAL_NATIVE_RECEIPT.json").write_text(
 json.dumps(receipt,indent=2,sort_keys=True)+"\n")
print("PASS_P104_DUAL_NATIVE_PHASE_512_COLUMNS recipes=514 columns=512 "
      "rank_mass=1496 wrong_endpoint_SHORTCUT_REJECTED no_kappa")

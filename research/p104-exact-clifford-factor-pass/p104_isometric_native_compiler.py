#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Recompile authentic physically isometric E8 Gamma chart transports:
one positive native F_r child with exact signed Gaussian phase.
"""
from pathlib import Path
import json,collections,hashlib,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from p104_minimal_symplectic import factor
from p104_exact_native_factor import correction
from p104_rank_r_native_recipes import lower
w=json.loads((ROOT/"P104_PHYSICAL_E8_ISOMETRIC_WORD.json").read_text())
assert len(w["transports"])==514
occ=collections.Counter((e[2],e[3]) for e in w["events"] if e[0]=="transport")
assert sum(occ.values())==756
records=[]
for t in w["transports"]:
    source=[tuple(g) for g in t["gates"]]
    candidate,r=factor(source)
    fix,_=correction(source,candidate)
    native=list(candidate)+fix
    assert r==abs(len(w["frames"][t["old"]])-len(w["frames"][t["new"]]))
    rec={"old":t["old"],"new":t["new"],"rank":r,
         "occurrences":occ[t["old"],t["new"]],
         "gates":[list(g) for g in native]}
    legal=lower(rec)
    assert sum(g[0]=="C" for g in legal["gates"])==r
    records.append(legal)
assert len(records)==514
assert sum(t["occurrences"] for t in records)==756
assert sum(t["rank"]*t["occurrences"] for t in records)==1496
out={
 "schema":"p104-genuine-e8-orthonormal-isometric-positive-F-r/1",
 "isometry_sha256":hashlib.sha256(
   (ROOT/"P104_PHYSICAL_E8_ISOMETRIC_WORD.json").read_bytes()).hexdigest(),
 "original_word_sha256":w["source_word_sha256"],
 "physical_labels_required":True,
 "distinct":514,"occurrences":756,"rank_mass":1496,
 "legal_early_source_and_scaling":"OPEN",
 "whole_supplier_and_all_size":"OPEN","new_kappa":False,
 "transports":records}
(ROOT/"P104_ISOMETRIC_NATIVE_RECIPES.json").write_text(
 json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
print("PASS_P104_ISOMETRIC_NATIVE_COMPILER recipes=514 "
      "native_children=756 rank_mass=1496 phase_oracle_NEXT")

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact 156-read source/early-owner manifest and two-side literal invoice.
Owner allocation, source legality and precision are explicitly fail-closed.
"""
from pathlib import Path
import json,collections,hashlib
ROOT=Path(__file__).resolve().parent
src=ROOT/"p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json"
if not src.exists():src=ROOT/"p104_native_e8_gate/evidence/NATIVE_CHART_WORD.json"
old=json.loads(src.read_text())
word=json.loads((ROOT/"P104_BORROWED_DIRTY_WORD.json").read_text())
forward=json.loads((ROOT/"P104_RANK_R_NATIVE_RECIPES.json").read_text())
dual=json.loads((ROOT/"P104_DUAL_NATIVE_RECIPES.json").read_text())
assert word["source_pin"]==forward["source_word_sha256"]==dual["source_sha256"]
assert sum(e[0]=="add" for e in word["events"])==448
original_first={}
for k,e in enumerate(old["events"]):
    regs=[e[1]] if e[0]=="transport" else [e[1],e[2]] if e[0]=="add" else []
    for reg in regs:original_first.setdefault(reg,k)
early=[];targets=set()
for k,e in enumerate(word["events"][:156]):
    assert e[0]=="add" and e[1].startswith("Y") and e[2].startswith("H")
    _,y,h,sgn,frame=e
    assert sgn in (-1,1) and word["frames"][frame]==[]
    targets.add(y)
    early.append({
      "event":k,"target":y,"source":h,"signed_add_coefficient":sgn,
      "chart_rank":0,"target_owner":"UNASSIGNED","source_owner":"UNASSIGNED",
      "early_target_mutation_authorized":False,
      "source_host_available":False,"paid_ADD_count":1,
      "original_first_target_event":original_first[y],
      "added_event_distance_not_a_time_measure":156+original_first[y]-k})
assert len(early)==156 and len(targets)==100
assert all(e["added_event_distance_not_a_time_measure"]>0 for e in early)
assert [e for e in word["events"] if e[0]=="transport"]==[
       e for e in old["events"] if e[0]=="transport"]
assert len(forward["transports"])==len(dual["transports"])==514

def count_native(data,fields):
    rank=collections.Counter();mon=collections.Counter()
    for item in data["transports"]:
        n=item["occurrences"]
        rank[item["rank"]]+=n
        for field in fields:
            m=item[field]
            mon["records"]+=n
            mon["nonzero_X_offset"]+=n*bool(m["offset"])
            mon["offset_bits"]+=n*m["offset"].bit_count()
            mon["nonzero_global_phase"]+=n*bool(m["phase"])
            mon["linear_Z4_terms"]+=n*sum(a!=0 for a in m["linear_Z4"])
            mon["quadratic_cross_terms"]+=n*sum(
                (m["quadratic_rows"][i]>>(i+1)).bit_count() for i in range(9))
            mon["out_of_place_linear_form_xors_not_real_host_bill"]+=n*sum(
                max(0,row.bit_count()-1) for row in m["matrix_rows"])
    assert rank=={1:320,2:272,3:72,4:56,5:24,6:12}
    assert mon["records"]==1512
    return {"child_profile":dict(sorted(rank.items())),
            "child_calls":sum(rank.values()),
            "rank_mass":sum(k*v for k,v in rank.items()),
            "scalar_ADDs":448,"monomial_sides":dict(sorted(mon.items()))}
a=count_native(forward,("left_monomial","right_monomial"))
b=count_native(dual,("left","right"))
assert a["child_calls"]==b["child_calls"]==756
assert a["rank_mass"]==b["rank_mass"]==1496
result={
 "schema":"p104-dirty-forward-delta-dual-required-owner-screen/1",
 "source_sha256":word["source_pin"],"forward":a,"conjugate_delta_dual":b,
 "if_both_orientations_required":{"native_child_calls":1512,
   "child_rank_mass":2992,"signed_ADDs":896,"monomial_side_records":3024},
 "required_pre_reads":156,"distinct_early_output_owners":100,
 "additional_event_distance_first_early_read_not_runtime":sum(
     max(e["added_event_distance_not_a_time_measure"] for e in early
         if e["target"]==target) for target in targets),
 "required_read_manifest":early,
 "unpriced":["source permissions, 100 early Y owners, eight dirty H owners",
             "16 exact fractional source scales for G/2 normalization",
             "native address/phase data movement","host/idle/tape/precision",
             "canonical endpoint/physical reverse contract",
             "actual selected #1094 optimized comparator, moments, all-size proof"],
 "source_owner_admission":"OPEN_FAIL_CLOSED","new_kappa":False}
(ROOT/"P104_FORWARD_DUAL_SOURCE_GATE.json").write_text(
    json.dumps(result,sort_keys=True,indent=2)+"\n")
print("PASS_P104_FORWARD_DUAL_SOURCE_GATE pre_reads=156 early_targets=100 "
      "forward_child=756 dual_child=756 pair_rank_mass=2992 "
      "owner_access_NOT_ADMITTED")

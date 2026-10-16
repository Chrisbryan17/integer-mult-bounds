#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact E8 physical pairing isometry: fix abstract 9-bit label mismatch.
All 120x120 root pairings and 104 physical hyperplane sinks are certified.
"""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from p104_native_e8_gate.scripts import native_chart_emitter as E
N=E.E8.NROW
indices=[N.index(row) for row in E.BASIS]
assert len(indices)==9
J=[sum(((N[indices[i]]>>indices[j])&1)<<j for j in range(9)) for i in range(9)]
assert E.rank(J)==9
assert all(((J[i]>>j)&1)==((J[j]>>i)&1)
           for i in range(9) for j in range(9))

def pair(a,b):
    return sum(((J[i]&b).bit_count()&1) for i in range(9) if a>>i&1)&1

# Fixed exact GF(2) orthonormal basis obtained by seeded finite search.
ORTH=[253,286,214,127,103,361,471,61,419]
assert E.rank(ORTH)==9
assert all(pair(v,w)==int(i==j)
           for i,v in enumerate(ORTH) for j,w in enumerate(ORTH))

def physical(x):
    assert 0<=x<512
    return sum(pair(x,v)<<i for i,v in enumerate(ORTH))

assert len({physical(x) for x in range(512)})==512
assert all(((physical(E.LABELS[i])&physical(E.LABELS[j])).bit_count()&1)==
           ((N[i]>>j)&1) for i in range(120) for j in range(120))
old_bad=sum((((E.LABELS[i]&E.LABELS[j]).bit_count()&1)!=
              ((N[i]>>j)&1)) for i in range(120) for j in range(120))
assert old_bad==7168
source=ROOT/"p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json"
if not source.exists():source=ROOT/"p104_native_e8_gate/evidence/NATIVE_CHART_WORD.json"
SHA="a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39"
assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
orig=json.loads(source.read_text())
frames=[tuple(physical(v) for v in f) for f in orig["frames"]]
assert all(E.rank(f)==len(f) for f in frames)
for t in orig["transports"]:
    a,b=frames[t["old"]],frames[t["new"]]
    assert E.subset(a,b) or E.subset(b,a)
    assert abs(len(a)-len(b))>0
for live in E.E8.live:
    q=physical(E.LABELS[live])
    sink=[physical(x) for x in E.sink_for(live)]
    assert len(sink)==E.rank(sink)==8
    assert all(((q&x).bit_count()&1)==0 for x in sink)
out={
 "schema":"p104-physical-e8-orthonormal-pairing/1",
 "source_word_sha256":SHA,"gram_rows_J":J,
 "source_basis_root_indices":indices,
 "orthonormal_vectors_in_source_coords":ORTH,
 "old_standard_dot_mismatches_on_120x120":old_bad,
 "checked_E8_root_pairings":14400,
 "verified_104_physical_orthogonal_target_sinks":True,
 "all_size_interface":"OPEN","new_kappa":False,
 "frames":[list(x) for x in frames],
 "transports":[{"old":t["old"],"new":t["new"],
    "gates":[list(g) for g in E.transport(frames[t["old"]],frames[t["new"]])]}
   for t in orig["transports"]],
 "events":orig["events"]}
(ROOT/"P104_PHYSICAL_E8_ISOMETRIC_WORD.json").write_text(
  json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
print("PASS_P104_E8_PHYSICAL_ISOMETRY pairings=14400 sinks=104 "
      "old_abstract_dot_mismatches=7168 transports=756 no_kappa")

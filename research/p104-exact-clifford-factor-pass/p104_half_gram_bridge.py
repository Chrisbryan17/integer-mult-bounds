#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Source-normalization bridge G -> G/2: eight explicit half-scalings before
mixing and eight inverse double-scalings after cleanup. A finite rational
construction, NOT an admitted integer/native scaling primitive.
"""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
source=ROOT/"P104_BORROWED_DIRTY_WORD.json"
old=json.loads(source.read_text())
assert old["source_pin"]=="a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39"
assert all(x[0]=="add" for x in old["events"][:156])
assert all(x[0] not in ("zero","erase","scale") for x in old["events"])
original=old["events"];root_frames={}
for i in range(8):
    name=f"X{i}"
    transports=[e for e in original if e[0]=="transport" and e[1]==name]
    assert transports
    start,end=transports[0][2],transports[-1][3]
    assert old["frames"][start]==old["frames"][end]
    assert len(old["frames"][start])==1
    root_frames[name]=start
start_scales=[["scale",f"X{i}",1,2,root_frames[f"X{i}"]] for i in range(8)]
end_scales=[["scale",f"X{i}",2,1,root_frames[f"X{i}"]] for i in range(8)]
word=old.copy()
word["schema"]="p104-borrowed-dirty-half-gram-rational/1"
word["source_original_sha256"]=hashlib.sha256(source.read_bytes()).hexdigest()
word["scope"]="finite G/2 algebra; fractional primitive, precision and hosting unresolved"
word["events"]=original[:156]+start_scales+original[156:]+end_scales
word["normalization"]={
 "target":"selected P104 low rank G/2 channel",
 "nonzero_entries":416,"source_half_scalings":8,"source_restore_double_scalings":8,
 "requires_invertible_two":True,"cost_and_precision":"UNPRICED",
 "original_X_preserved":True,"borrowed_H_preserved":True}
word["counts"]={**old["counts"],"scale_events":16,"scale_half_events":8,
                "scale_double_events":8,"events":len(word["events"])}
assert len(word["events"])==1220
assert sum(e[0]=="transport" for e in word["events"])==756
assert sum(e[0]=="add" for e in word["events"])==448
assert sum(e[0]=="scale" for e in word["events"])==16
(ROOT/"P104_HALF_GRAM_RATIONAL_WORD.json").write_text(
    json.dumps(word,indent=2,sort_keys=True)+"\n")
print("PASS_P104_HALF_GRAM_BRIDGE_COMPILED source_half=8 "
      "source_double=8 ADD=448 transports=756 events=1220 "
      "precision_and_scale_price_OPEN")

#!/usr/bin/env python3
"""Bound the first next scalar contact after all 108 original Cao GL9 bridge seeds.

Source-specific first-touch census, not an arbitrary-depth no-go theorem.
"""
import argparse,gzip,hashlib,json,sys
from collections import Counter
from pathlib import Path

PIN="cfcd36b40326d7a5815edb5313444379b3fb756b27d5201c561574c085cc0dd"

def run(root,prior):
    payload=gzip.decompress((root/"research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz").read_bytes())
    assert hashlib.sha256(payload).hexdigest()==PIN
    w=json.loads(payload);source=json.loads(prior.read_text())
    sys.path.insert(0,str(root/"research/warp-interface-20261022"))
    import warp_merge as W
    result={}
    for direction in ("forward","backward"):
        events=w["programs"][direction];dims=Counter();witness=[]
        for seed in source["orientations"][direction]["actual_rejections"]:
            if seed["obstruction"]!="incomparable_same_rank":continue
            role=seed["blocked_role"]
            first=next(((i,e) for i,e in enumerate(events[seed["end"]+1:],seed["end"]+1)
                        if role in W.roles(e)),None)
            assert first is not None
            i,e=first
            assert e[0]=="scalar"
            dim=len(w["canonical"]["frames"][e[2]])
            dims[dim]+=1
            witness.append({"original_window":[seed["start"],seed["end"]],
                            "role":role,"next_scalar_index":i,"next_scalar_rank":dim})
        result[direction]={"count":len(witness),"next_scalar_rank_histogram":dict(dims),
                           "first_examples":witness[:4]}
    assert result["forward"]["next_scalar_rank_histogram"]=={4:6}
    assert result["backward"]["next_scalar_rank_histogram"]=={8:102}
    return {"status":"PASS_108_NATIVE_GL9_SEEDS_NO_IMMEDIATE_RANK9_SCALAR",
            "frozen_native_sha256":PIN,"evidence":result,"new_kappa_proved":False,
            "scope":"First subsequent scalar of same blocked sibling register only; no global scalar-DAG exclusion."}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--prior",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    r=run(a.source,a.prior)
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(r["status"],r["evidence"]["forward"]["count"],r["evidence"]["backward"]["count"])

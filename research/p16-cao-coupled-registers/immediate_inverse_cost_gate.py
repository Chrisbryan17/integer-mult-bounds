#!/usr/bin/env python3
"""Certify Fourier-rank-two direct identity repair for all 108 Cao GL9 pairs.

This excludes only immediate undo with the original next-scalar chart unchanged,
not coordinated later scalar rewrites.
"""
import argparse,gzip,hashlib,json,sys
from collections import Counter
from decimal import Decimal,localcontext
from pathlib import Path
PIN="cfcd36b40326d7a5815e1db5313444379b3fb756b27d5201c561574c085cc0dd"

def run(root,bridge_file):
    blob=gzip.decompress((root/"research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz").read_bytes())
    assert hashlib.sha256(blob).hexdigest()==PIN
    C=json.loads(blob)["canonical"]
    rows=json.loads(bridge_file.read_text())["bridges"]
    assert len(rows)==108
    sys.path.insert(0,str(root/"research/warp-interface-20261022"))
    from warp_merge import F
    ce=F.load(root/"research/t74-native-fast/vendor/native/new/code/borrow/vendor/clifford/clifford_exact.py","immediate_ce")
    P=F.load(root/"research/kappa-function-composition/complex/prune_native.py","immediate_p")
    X=F.load(root/"research/kappa-rebuild/complex/native_extensions.py","immediate_x")
    cache={};dims=Counter()
    def frame(i):
        if i not in cache:cache[i]=ce.canonical_frame(9,C["frames"][i])
        return cache[i]
    for row in rows:
        x=row.get("from_frame");y=row.get("to_frame")
        d=len(C["frames"][x]);assert d==len(C["frames"][y])
        physical=frame(x).adjoint().then(frame(y))
        for orientation in ("forward","backward"):
            actual=P.conjugate(ce,physical) if orientation=="backward" else physical
            rec=X.N.lower_exact(P,ce,actual)
            assert rec["rank"]==2
        dims[d]+=1
    assert dims==Counter({8:102,4:6})
    with localcontext() as ctx:
        ctx.prec=70;t=Decimal(1)-Decimal("0.0030217758")
        saving=4-2*Decimal(2)**t
        direct_repair=Decimal(2)**t
        net=saving-direct_repair
        assert saving>0>net
    return {"status":"PASS_108_EXACT_RANK2_IMMEDIATE_IDENTITY_REPAIR_FLOOR",
            "native_pin":PIN,"cases":108,"dimension_histogram":dict(dims),
            "dual_direction_exact_Fourier_rank":2,
            "local_optimistic_saving":str(saving),
            "one_direct_repair_cost":str(direct_repair),
            "net_local_gain":str(net),
            "new_kappa_proved":False,
            "scope":"Fixed-next-scalar direct frame conversion only; no global rewrite no-go."}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--source",type=Path,required=True)
    p.add_argument("--bridges",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();r=run(a.source,a.bridges)
    a.out.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n")
    print(r["status"],r["net_local_gain"])

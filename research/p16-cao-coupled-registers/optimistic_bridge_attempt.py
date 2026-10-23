#!/usr/bin/env python3
"""Attempt a priced Cao H1/H1 merger using one single-register GL9 bridge.

The full cost histogram improves in each native direction, but literal
arbitrary-input replay rejects the changed operator. NO new kappa is admitted.
"""
import argparse,gzip,hashlib,json,sys
from pathlib import Path
from collections import Counter
from copy import deepcopy
from decimal import Decimal,localcontext

PIN="cfcd36b40326d7a5815e1db5313444379b3fb756b27d5201c561574c085cc0dd"
BASE={1:2201,2:412,3:510,4:127,5:40,8:8}

def run(root):
    raw=gzip.decompress((root/"research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest()==PIN
    word=json.loads(raw);c=deepcopy(word["canonical"])
    a,ell=16,75
    G=[(1<<i)^(a if ((ell>>i)&1) else 0) for i in range(9)]
    c["warps"].append({"op":73,"G_columns":G,"from_frame":211,"to_frame":238})
    sys.path.insert(0,str(root/"research/warp-interface-20261022"))
    import warp_merge as W
    F=W.F
    V=F.load(root/"research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py","opt_gauge_rows")
    X=F.load(root/"research/kappa-rebuild/complex/native_extensions.py","opt_gauge_literal")
    out={}
    for direction,original in word["programs"].items():
        indexes={};p=[]
        for i,e in enumerate(original):
            if e[0]!="climb":
                indexes[i]=len(p);p.append(deepcopy(e))
        for full in (15051,15052):
            i=indexes[full]
            assert p[i][0]=="scalar" and p[i][2]==1130
            p[i][2]=211
        p.insert(indexes[15052]+1,["warp",["L",631],73,211,238])
        new=W.synthesize(c,p)
        paid=Counter(e[5] for e in new if e[0]=="climb")
        paid.update(e[4] for e in new if e[0]=="center")
        assert paid==Counter({1:2197,2:414,3:510,4:127,5:40,8:8})
        with localcontext() as ctx:
            ctx.prec=60;t=Decimal(1)-Decimal("0.0030217758")
            gain=sum(Decimal(k)**t*(BASE.get(k,0)-paid.get(k,0))
                     for k in set(BASE)|set(paid))
        assert gain>0
        native=deepcopy(c);native["R"]=408;native["local_profile"]=dict(paid)
        matches=False
        try:
            rows,rec=X.literal_replay(V,native,new,direction=="backward")
            matches=all(rows["L",i]==V.expected(("L",i),[],direction=="backward",False)
                        for i in range(632))
        except (ValueError,AssertionError):
            matches=False
        assert not matches,"Unexpected accepted positive native candidate"
        out[direction]={"paid_profile":dict(paid),"moment_gain_arithmetic_only":str(gain),
                         "semantics_632_passed":matches}
    return {"status":"PASS_POSITIVE_INVOICE_REJECTED_BY_NATIVE_OPERATOR",
            "source_sha256":PIN,"directional_evidence":out,"new_kappa_proved":False}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--source",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args();rec=run(args.source)
    args.out.write_text(json.dumps(rec,sort_keys=True,indent=2)+"\n")
    print(rec["status"])

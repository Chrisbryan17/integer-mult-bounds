#!/usr/bin/env python3
"""Source-exact Cao P16 adjacent H1+H1 fusion geometry and no-free-monomial gate.
Reads frozen witness and whole invoice. Does NOT claim admissible H2 physical call.
"""
from collections import Counter
from decimal import Decimal, localcontext
from hashlib import sha256
from pathlib import Path
import argparse, gzip, json

PIN = "cfcd36b40326d7a5815e1db5313444379b3fb756b27d5201c561574c085cc0dd"

def need(cond, why):
    if not cond:
        raise AssertionError(why)

def span(basis):
    s = {0}
    for x in basis:
        s |= {v ^ x for v in tuple(s)}
    return frozenset(s)

def run(root):
    n = root / "research/kappa-round3-warp-20261022"
    freeze = json.loads((n / "ACTUAL-WORD-FREEZE.json").read_text())
    payload = gzip.decompress((n / "ACTUAL-WORD.json.gz").read_bytes())
    need(sha256(payload).hexdigest() == PIN == freeze["canonical_payload_sha256"], "Frozen payload integrity")
    native = json.loads(payload)
    frames = native["canonical"]["frames"]
    spans = [span(x) for x in frames]
    need(all(len(x) == (1 << len(frames[i])) for i, x in enumerate(spans)), "All GF2 frame bases independent")
    census, matches = {}, {}
    for direction, word in native["programs"].items():
        need(Counter(e[0] for e in word) == dict(phase=10,warp=240,scalar=17453,climb=3290,center=8,adapter=448), "Source event inventory")
        h1 = [(i,e) for i,e in enumerate(word) if e[0] == "climb" and e[5] == 1]
        need(len(h1) == 2201, "Source H1 inventory")
        adjacent = [(a,b) for a,b in zip(h1,h1[1:]) if b[0] == a[0] + 1]
        need(len(adjacent) == 671, "Adjacent source H1 count")
        rows = []
        for (i,a),(j,b) in adjacent:
            need(a[2] != b[2] and a[4] == b[4], "Separate registers, identical destination")
            u,w,v = spans[a[3]],spans[b[3]],spans[a[4]]
            need(u < v and w < v and 2*len(u) == len(v) == 2*len(w), "Strict rank-one GF2 intervals")
            equal = (u == w)
            intersect_dim = len(frames[a[4]]) - (1 if equal else 2)
            need(len(u & w) == 1 << intersect_dim, "Correct GF2 hyperplane intersection")
            rows.append(dict(index=i, registers=[a[2],b[2]], source_frames=[a[3],b[3]],
                        target_frame=a[4],target_dim=len(frames[a[4]]),
                        source_hyperplanes_equal=equal,
                        intersection_dim=intersect_dim,
                        roles=["main" if a[2] < 224 else "helper",
                               "main" if b[2] < 224 else "helper"]))
        census[direction] = dict(h1_count=len(h1),adjacent=len(rows),
            common_destination=len(rows),
            distinct_source_hyperplanes=sum(not x["source_hyperplanes_equal"] for x in rows),
            equal_source_hyperplanes=sum(x["source_hyperplanes_equal"] for x in rows),
            destination_dimensions=dict(sorted(Counter(x["target_dim"] for x in rows).items())),
            register_roles=dict(sorted(Counter("-".join(x["roles"]) for x in rows).items())))
        matches[direction] = rows
    forward,backward = matches["forward"],matches["backward"]
    need([x["index"] for x in forward] == [x["index"] for x in backward], "Forward/dual event indices")
    need(all(set(x["registers"]) == set(y["registers"]) and
             x["target_frame"] == y["target_frame"] and
             x["source_hyperplanes_equal"] == y["source_hyperplanes_equal"]
             for x,y in zip(forward,backward)), "Forward/dual exact pair correspondence")
    # Row support count survives all monomial input/output permutations and
    # nonzero lane scalings. An independent-register direct sum has 2
    # nonzeros/row, while a four-lane Walsh H2 has 4. This excludes ONLY
    # an uncharged monomial-only cross-register packing interface.
    h1sum=[[1,1,0,0],[1,-1,0,0],[0,0,1,1],[0,0,1,-1]]
    h2=[[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]
    support=lambda m:[sum(v!=0 for v in row) for row in m]
    need(support(h1sum)==[2]*4 and support(h2)==[4]*4, "Four-lane monomial obstruction")
    c=json.loads((root/"research/kappa-round6-compiler-tightening-20261022/ARITHMETIC.json").read_text())
    need(c["kappa"] == "15108879/5000000000", "Published κ pin")
    t=Counter({int(k):v for k,v in c["targets"].items()})
    p=Counter({int(k):v for k,v in c["paid"].items()})
    need(sum(t.values())==10928 and sum(p.values())==64404, "Complete controller invoice")
    proposed=p.copy()
    proposed[1]-=36
    proposed[2]+=18
    need(sum(r*v for r,v in p.items())==sum(r*v for r,v in proposed.items()), "Rank mass")
    with localcontext() as ctx:
        ctx.prec=65
        power=1-Decimal("0.0030220")
        margin=lambda paid:sum(Decimal(r)**power*v for r,v in t.items())-sum(Decimal(r)**power*v for r,v in paid.items())
        before=margin(p);after=margin(proposed)
    need(before < 0 < after, "Positive arithmetic-only hypothetical margin")
    shortlisted=sorted(forward,key=lambda x:(x["target_dim"],0 if x["roles"]==["helper","helper"] else 1,x["index"]))[:24]
    return dict(status="PASS_SOURCE_EXACT_FUSION_GEOMETRY_ONLY",
        source_revision="20bb93cd990d2ff683e4d0fc56b87a42cd5d3296",
        source_sha256=PIN,orientations=census, dual_pair_correspondence=True,
        monomial_only_gate=dict(unpacked_row_support=support(h1sum),
            H2_row_support=support(h2),
            scope="Only the direct-sum two-register model, allowing monomial input/output changes; nonmonomial packing and owner transfer remain open."),
        hypothetical_18_fusions=dict(target_kappa="0.0030220",
            paid_before=sum(p.values()),paid_after=sum(proposed.values()),
            margin_before=str(before),margin_after=str(after),gain=str(after-before)),
        shortlist=shortlisted, physical_fusion_admitted=False,new_kappa_proved=False)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    r=run(args.source)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(r["status"],r["orientations"]["forward"],
          "kappa_0030220_hypothetical_margin",r["hypothetical_18_fusions"]["margin_after"])

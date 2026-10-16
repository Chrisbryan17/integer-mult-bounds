#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent Fraction-exact selected G/2 120-column forward+logical-dual
checker. Scaling operations are required but not proven native/legal/cheap.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,copy,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from p104_native_e8_gate.scripts import native_chart_emitter as E
w=json.loads((ROOT/"P104_HALF_GRAM_RATIONAL_WORD.json").read_text())
assert w["normalization"]["nonzero_entries"]==416
assert len(w["events"])==1220
helpers=sorted({e[2] for e in w["events"] if e[0]=="add" and e[2].startswith("H")})
assert len(helpers)==8
names=[f"X{i}" for i in range(8)]+[f"Y{i}" for i in range(104)]+helpers
idx={s:i for i,s in enumerate(names)}
N=len(names)
assert N==120

def replay(events,dual=False):
    rows=[{i:Q(1)} for i in range(N)]
    frames={}
    for e in events:
        typ=e[0]
        if typ=="transport":
            _,name,a,b,r=e
            assert abs(len(w["frames"][a])-len(w["frames"][b]))==r
            frames.setdefault(name,a)
            assert frames[name]==a
            frames[name]=b
        elif typ=="scale":
            _,name,num,den,fr=e
            assert num>0 and den>0 and len(w["frames"][fr])==1
            frames.setdefault(name,fr)
            assert frames[name]==fr
            s=Q(num,den) if not dual else Q(den,num)
            rows[idx[name]]={k:s*v for k,v in rows[idx[name]].items()}
        elif typ=="add":
            _,dst,src,sgn,fr=e
            frames.setdefault(dst,fr);frames.setdefault(src,fr)
            assert frames[dst]==frames[src]==fr
            i,j=idx[dst],idx[src]
            if dual:i,j,sgn=j,i,-sgn
            for k,v in list(rows[j].items()):
                rows[i][k]=rows[i].get(k,Q(0))+sgn*v
                if not rows[i][k]:del rows[i][k]
        else:raise AssertionError(e)
    return rows

forward=replay(w["events"])
roots=[p[0] for p in E.E8.chosen[1]]
assert all(forward[i]=={i:Q(1)} for i in range(8))
assert all(forward[112+j]=={112+j:Q(1)} for j in range(8))
count=0
for t,target in enumerate(E.E8.live):
    want={8+t:Q(1)}
    for i,root in enumerate(roots):
        c=E.E8.IP[target][root]
        if c:
            assert c in (-1,1)
            want[i]=Q(c,2)
            count+=1
    assert forward[8+t]==want,(t,forward[8+t],want)
assert count==416
assert any(v.denominator==2 for row in forward[8:112] for v in row.values())
dual=replay(w["events"],dual=True)
for a in range(N):
    for b in range(N):
        val=sum((forward[k].get(a,Q(0))*dual[k].get(b,Q(0))
                 for k in range(N)),Q(0))
        assert val==int(a==b),(a,b,val)
for i,root in enumerate(roots):
    for t,target in enumerate(E.E8.live):
        assert dual[i].get(8+t,Q(0))==-Q(E.E8.IP[target][root],2)
bad=copy.deepcopy(w["events"])
k=next(i for i,e in enumerate(bad) if e[0]=="scale")
bad[k][2:4]=[1,1]
assert replay(bad)!=forward
bad=copy.deepcopy(w["events"])
k=max(i for i,e in enumerate(bad) if e[0]=="scale")
bad[k][2:4]=[1,1]
assert replay(bad)[idx["X7"]]!={7:Q(1)}
receipt={
 "status":"PASS_FINITE_RATIONAL",
 "source":"reviewed research/p104-native-channel/PROOF.md G/2 contract",
 "nonzero_half_coefficients":416,
 "half_scalings":8,"double_restore_scalings":8,
 "all_120_formal_columns":True,"all_14400_inverse_transpose_entries":True,
 "scaler_legal_native_implementation":"OPEN","scalar_scaling_cost":"UNKNOWN",
 "finite_integer_only_signed_ADD_cannot_generate_half":True,
 "selected_supplier_admitted":False,"complete_recursion":False,"new_kappa":False}
(ROOT/"P104_HALF_GRAM_RATIONAL_RECEIPT.json").write_text(
 json.dumps(receipt,indent=2,sort_keys=True)+"\n")
print("PASS_P104_HALF_GRAM_RATIONAL_FORWARD_AND_DUAL input_columns=120 "
      "nonzero_signed_halves=416 scales=16 sources_and_dirt_restored=YES "
      "G_versus_G_OVER_TWO_REJECTED missing_scale_REJECTED "
      "physical_scaler_owner_precision_OPEN")

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reproduce an exact forward 632-column rank-nine centre mutation of #4470.
This is a WORSE-cost candidate: it is not an improved integer multiplier.
"""
from collections import Counter
from copy import deepcopy
from decimal import Decimal,localcontext
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
SOURCE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE.parents[2]
sys.path.insert(0,str(SOURCE/'research/joint-helper-lattice'))
import native_joint as J

def rebuild(c,program):
    state=c['start'][:];out=[]
    def climb(r,f):
        old=state[r]
        if old==f:return
        assert J.F.span(c['frames'][old])<J.F.span(c['frames'][f])
        out.append(['climb','retimed',r,old,f,
                    len(c['frames'][f])-len(c['frames'][old])])
        state[r]=f
    for e in program:
        if e[0]=='climb':continue
        if e[0]=='scalar':
            g=e[1];roles=g[1:3] if g[0] in ('add','copy') else g[1:2]
            for role in roles:
                if role[0]=='L':climb(role[1],e[2])
        elif e[0]=='warp':
            climb(e[1][1],e[3]);state[e[1][1]]=e[4]
        out.append(e)
    for r,f in enumerate(c['final']):climb(r,f)
    return out

def paid(word):
    return Counter(e[-1] for e in word if e[0] in ('climb','center'))

def run():
    c,p,_,_,_=J.construct()
    assert len(p['forward'])==len(p['backward'])==21461
    assert all(rebuild(c,p[d])==p[d] for d in ('forward','backward'))
    old=p['forward'];q=deepcopy(old)
    idx=next(i for i,e in enumerate(q) if e[0]=='center')
    centre=q[idx];assert centre==['center',0,254,0,8]
    clear,copy=q[idx-2:idx]
    assert clear[1][0]=='clear' and copy[1][0]=='copy'
    source=copy[1][2][1];assert source==92
    earlier=next(i for i in range(idx-3,-1,-1)
                 if q[i][0]=='scalar' and q[i][1][0]=='add'
                 and ['L',source] in q[i][1][1:3])
    assert earlier==11216 and q[earlier][2]==254
    for e in (clear,copy,q[earlier]):e[2]=1
    centre[2]=1;centre[4]=9
    new=rebuild(c,q)
    V=J.F.load(SOURCE/'research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py','r9_literal_rows')
    X=J.F.load(SOURCE/'research/kappa-rebuild/complex/native_extensions.py','r9_literal_native')
    rows,receipt=X.literal_replay(V,c,new,False)
    assert all(rows['L',r]==V.expected(('L',r),[],False,False) for r in range(632))
    before,after=paid(old),paid(new)
    assert dict(before)=={1:2237,2:388,3:494,4:147,5:36,8:8}
    assert dict(after)=={1:2236,2:388,3:494,4:146,5:37,8:7,9:1}
    with localcontext() as ctx:
        ctx.prec=65
        t=Decimal(1)-Decimal('0.00302017')
        gain=sum(Decimal(r)**t*(before[r]-after[r])
                 for r in set(before)|set(after))
        assert gain<Decimal('-.98')
    report={'status':'PASS_632_FORWARD_BUT_WORSE_MOMENT',
      'source_sha':'b9a13c1673e0e9697de410de16e8bbf3207a7363',
      'mutated_contacts':[earlier,idx-2,idx-1,idx],
      'all_632_forward_columns_passed':True,
      'ordinary_dual':'NOT_VERIFIED','absolute_clifford_phase':'NOT_VERIFIED',
      'original_profile':dict(sorted(before.items())),
      'new_profile':dict(sorted(after.items())),
      'forward_cost_saving_at_target_kappa':str(gain),
      'productive_helper_rank_gain':0,'new_kappa':False}
    (HERE/'CENTRE9_FORWARD_EXACT_RECEIPT.json').write_text(
        json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(report['status'],'gain',gain)
    return report

if __name__=='__main__':run()

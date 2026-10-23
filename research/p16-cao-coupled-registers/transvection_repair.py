#!/usr/bin/env python3
"""Build exact four-controlled-XOR, involutive GL(9,2) chart bridges for Cao P16.

This is an algebraic address-space candidate, NOT an operator-preserving
native insertion or a paid recursive H1+H1->H2 fusion.
"""
import argparse,gzip,hashlib,json
from pathlib import Path
from collections import Counter

PIN='cfcd36b40326d7a5815e1db5313444379b3fb756b27d5201c561574c085cc0dd'
def span(basis):
    s={0}
    for v in basis:s|={x^v for x in tuple(s)}
    return s
def parity(x):return x.bit_count()%2
def transvection(x,a,ell):return x^(a if parity(x&ell) else 0)

def solve(U,V):
    H=U&V;k=len(U).bit_length()-1
    assert len(U)==len(V)==1<<k and len(H)==1<<(k-1)
    u=min(U-H);v=min(V-H)
    choices=[]
    for ell in range(1,512):
        if parity(u&ell)!=1 or parity(v&ell)!=1:continue
        if any(parity(h&ell) for h in H):continue
        for h in H:
            a=u^v^h
            assert a!=0 and parity(a&ell)==0
            choices.append((a.bit_count()+ell.bit_count(),a.bit_count(),ell.bit_count(),a,ell))
    assert choices
    _,_,_,a,ell=min(choices)
    cols=[transvection(1<<j,a,ell) for j in range(9)]
    assert all(transvection(transvection(x,a,ell),a,ell)==x for x in range(512))
    assert {transvection(x,a,ell) for x in U}==V
    assert len({transvection(x,a,ell) for x in range(512)})==512
    assert not (a&ell) and a.bit_count()*ell.bit_count()==4
    gates=[(controller,target) for controller in range(9) if (ell>>controller)&1
           for target in range(9) if (a>>target)&1]
    assert len(gates)==4 and all(controller!=target for controller,target in gates)
    for x in range(512):
        y=x
        for controller,target in gates:
            if (y>>controller)&1:y^=(1<<target)
        assert y==transvection(x,a,ell)
    return dict(a=a,ell=ell,G_columns=cols,G_inverse_columns=cols,
                coordinate_cost_score=a.bit_count()+ell.bit_count(),
                wt_a=a.bit_count(),wt_ell=ell.bit_count(),self_inverse=True,
                controlled_xor_gates=gates,exact_gate_count=4,exact_512=True)

def run(root,prior):
    gz=root/'research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz'
    b=gzip.decompress(gz.read_bytes())
    assert hashlib.sha256(b).hexdigest()==PIN
    frames=json.loads(b)['canonical']['frames']
    spaces=[span(f) for f in frames]
    bundle=json.loads(prior.read_text())
    bridges=[];rank_drops=[]
    for row in bundle['bridges']:
        oldframe=row.get('from_frame',row.get('old_frame'))
        newframe=row.get('to_frame',row.get('required_frame'))
        da=row.get('from_dim',row.get('source_dim'))
        db=row.get('to_dim',row.get('target_dim'))
        if da!=db:
            assert da>db
            rank_drops.append((row['direction'],da,db))
        else:
            U=spaces[oldframe];V=spaces[newframe]
            tr=solve(U,V)
            assert tr['G_columns']==tr['G_inverse_columns']
            if 'source_event_start' in row:
                loc=[row['source_event_start'],row['source_event_end']]
                primary=row['desired_role'];sibling=row['blocked_role']
            else:
                loc=row['source_event_range']
                primary=row['primary_role'];sibling=row['sibling_role']
            bridges.append(dict(direction=row['direction'],source_event_range=loc,
                                primary_role=primary,sibling_role=sibling,
                                from_frame=oldframe,to_frame=newframe,
                                from_dim=da,to_dim=db,**tr))
    assert len(bridges)==108 and len(rank_drops)==47
    counts=Counter((r['from_dim'],r['exact_gate_count']) for r in bridges)
    assert counts==Counter({(8,4):102,(4,4):6})
    return dict(status='PASS_108_EXACT_FOUR_CNOT_GL9_CHART_REPAIRS',
                frozen_native_sha256=PIN,
                bridge_count=len(bridges),rank_drop_count=len(rank_drops),
                four_gate_distribution={f'dimension{d}':v for (d,g),v in sorted(counts.items())},
                bridges=bridges,
                unchanged_native_operator_proved=False,
                physical_recursive_cost_paid=False,
                phase_admitted=False,new_kappa_proved=False)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--prior',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    a=p.parse_args()
    r=run(a.source,a.prior)
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(r['status'],r['four_gate_distribution'])

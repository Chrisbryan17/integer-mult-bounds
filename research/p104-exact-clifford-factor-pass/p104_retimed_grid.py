#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""All-prefix logical coefficient and physical-frame certificate, forward/Delta dual.

For tensor payload depth lambda >= 1, an exact local implementation is on
2^-(f+15lambda) Z[i], *conditional on the retained exact Clifford gates*.
This is not a complete recursive multiplication/host/tape/all-size theorem.
"""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p104_native_e8_gate.scripts import native_chart_emitter as E
rows_out={}
for mode in ('G','I_minus_G_half'):
    W=json.loads((P/f'P104_INTERSECTION_{mode}.json').read_text())
    frames=W['frames'];events=W['events']
    zero=next(i for i,f in enumerate(frames) if not f)
    H=sorted({r for e in events if e[0]=='add' for r in e[1:3] if r.startswith('H')})
    S=[f'S{i}' for i in range(104)];Y=[f'Y{i}' for i in range(104)]
    roles=S+Y+H
    assert len(roles)==216 and len(H)==8
    assert max(map(len,frames))==8
    largest_child=max(e[4] for e in events if e[0]=='transport')
    assert largest_child==6
    for orient in ('forward','ordinary_inverse_transpose'):
        row={r:{r:1} for r in roles}
        init={r:1 if r in S else 0 for r in roles}
        chart={r:'intrinsic' if r in S else zero for r in roles}
        dimension={r:init[r] for r in roles}
        peak={'row_l1':1,'scalar_coefficient':1,'termwise_grid_slope':0}
        where={}
        def inspect(r,event):
            a=row[r]
            vals={'row_l1':sum(abs(v) for v in a.values()),
                  'scalar_coefficient':max((abs(v) for v in a.values()),default=0),
                  'termwise_grid_slope':max((dimension[r]+init[s] for s in a),default=0)}
            for name,v in vals.items():
                if v>peak[name]:peak[name]=v;where[name]=[event,r]
        for r in roles:inspect(r,-1)
        entered=set();exited=set()
        for j,e in enumerate(events):
            typ=e[0]
            if typ=='source_to_zero':
                r=e[1]
                assert r in S and r not in entered and dimension[r]==1
                chart[r]=zero;dimension[r]=0;entered.add(r);inspect(r,j)
            elif typ=='source_from_zero':
                r=e[1]
                assert r in entered and r not in exited and chart[r]==zero
                chart[r]='intrinsic';dimension[r]=1;exited.add(r);inspect(r,j)
            elif typ=='transport':
                _,r,a,b,n=e
                assert chart[r]==a and n==abs(len(frames[a])-len(frames[b]))>0
                chart[r]=b;dimension[r]=len(frames[b]);inspect(r,j)
            elif typ=='add':
                _,dst,src,sgn,frame=e
                assert chart[dst]==chart[src]==frame and sgn in (-1,1)
                if orient=='ordinary_inverse_transpose':dst,src,sgn=src,dst,-sgn
                for s,v in list(row[src].items()):
                    row[dst][s]=row[dst].get(s,0)+sgn*v
                    if row[dst][s]==0:del row[dst][s]
                inspect(dst,j)
            elif typ=='sign':
                _,r,sgn,f=e
                assert sgn==-1 and chart[r]==f
                row[r]={s:-v for s,v in row[r].items()};inspect(r,j)
            else:raise AssertionError(e)
        assert entered==exited==set(S)
        assert all(dimension[r]==(1 if r in S else 8 if r in Y else 0) for r in roles)
        goal={'G':(105,135),'I_minus_G_half':(103,127)}[mode]
        assert peak['row_l1']==goal[orient!='forward']
        assert peak['termwise_grid_slope']<=9
        assert peak['scalar_coefficient']<=4
        assert all(row[h]=={h:1} for h in H)
        live=E.E8.live
        if orient=='forward':
            assert all(row[s]=={s:1} for s in S)
            for t,root in enumerate(live):
                expect={Y[t]:1}
                for j,other in enumerate(live):
                    g=E.E8.IP[root][other]
                    if mode!='G':g=2*int(t==j)-g
                    if g:expect[S[j]]=g
                assert row[Y[t]]==expect,(mode,orient,t)
        else:
            assert all(row[y]=={y:1} for y in Y)
            for j,other in enumerate(live):
                expect={S[j]:1}
                for t,root in enumerate(live):
                    g=E.E8.IP[root][other]
                    if mode!='G':g=2*int(t==j)-g
                    if g:expect[Y[t]]=-g
                assert row[S[j]]==expect,(mode,orient,j)
        rows_out[mode+'__'+orient]={'peaks':peak,'where':where,
          'max_native_rank':6,
          'sufficient_atomic_fraction_bits_per_tensor_layer':9,
          'sufficient_internal_fraction_bits_per_tensor_layer':15,
          'sufficient_scalar_guard_bits':(peak['row_l1']-1).bit_length(),
          'physical_source_rank_initial':1,
          'all_other_initial_ranks':0}
        print('PASS_P104_RETIMED_GRID',mode,orient,peak,flush=True)
result={'schema':'p104-retimed-uniform-tensor-local-grid/1',
 'status':'PASS_CONDITIONAL_LOCAL_TENSOR_GRID',
 'source_word_sha256':W['source_original_word_sha256'],
 'scope':'all integer lambda >=1 tensor lifts of the pinned physical Clifford word; scalar operator NOT tensor powered',
 'input':'real and imaginary components in 2^-f Z, abs <= H',
 'exact_internal_grid':'2^-(f+15*lambda) Z[i]',
 'encoded_target_decode':'additional denominator-two type bit, if decoded',
 'stored_component_magnitude_less_than':'H*2^(ceil((9lambda+1)/2)+8)',
 'butterfly_temporary_magnitude_less_than':'H*2^(ceil((9lambda+1)/2)+10)',
 'rounding_to_certified_grid':'identity for exact ideal native operations',
 'source_owner_host_tape_primitive_cost':'OPEN',
 'precision_under_approximate_recursive_children':'OPEN',
 'complete_integer_multiplication_all_sizes':'OPEN',
 'new_kappa':False,'programs':rows_out}
(P/'P104_RETIMED_TENSOR_GRID_CERT.json').write_text(
 json.dumps(result,sort_keys=True,indent=2)+'\n')

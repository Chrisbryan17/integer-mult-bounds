#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fail-closed 216-role chronological P104 owner/transport boundary:
the necessary schedule is NOT a valid selected physical owner allocation.
"""
from pathlib import Path
import collections,json
P=Path(__file__).resolve().parent
O=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
frames=O['frames']
reports={}
for mode,path in [('G','P104_INPLACE_DYADIC_WORD.json'),
                  ('I_minus_G_half','P104_INPLACE_SIDE_WORD.json')]:
    w=json.loads((P/path).read_text());ev=w['events']
    H=sorted({r for e in ev if e[0]=='add' for r in e[1:3]
              if r.startswith('H')})
    roles=['S%d'%j for j in range(104)]+['Y%d'%j for j in range(104)]+H
    assert len(H)==8 and len(roles)==216
    rec={r:{'first':None,'last':None,'reads':0,'writes':0,
            'ascents':0,'descents':0,'rank_mass':0,
            'owner':'UNASSIGNED'} for r in roles}
    orientation=collections.Counter();early=set()
    for idx,e in enumerate(ev):
        typ=e[0]
        if typ=='add':
            _,dst,src,sign,fr=e
            assert sign in (-1,1) and 0<=fr<len(frames)
            touched=[dst,src]
            rec[dst]['writes']+=1;rec[src]['reads']+=1
            if idx<156:early.add(dst)
        elif typ=='sign':
            touched=[e[1]];rec[e[1]]['writes']+=1
        elif typ=='transport':
            _,r,a,b,rank=e
            n0,n1=len(frames[a]),len(frames[b])
            assert rank==abs(n1-n0)>0
            touched=[r];rec[r]['rank_mass']+=rank
            v='ascent' if n1>n0 else 'descent'
            rec[r]['ascents' if n1>n0 else 'descents']+=1
            orientation[v]+=1;orientation[v+'_rank_mass']+=rank
        elif typ in ('source_to_zero','source_from_zero'):
            _,r,root,rank=e
            assert rank==1 and r.startswith('S')
            touched=[r]
            v='source_descent' if typ=='source_to_zero' else 'source_ascent'
            orientation[v]+=1;orientation[v+'_rank_mass']+=1
        else:raise AssertionError(e)
        for r in touched:
            if rec[r]['first'] is None:rec[r]['first']=idx
            rec[r]['last']=idx
    assert len(early)==100
    assert all(x['first'] is not None and x['last'] is not None
               for x in rec.values())
    assert orientation=={
      'source_descent':104,'source_descent_rank_mass':104,
      'source_ascent':104,'source_ascent_rank_mass':104,
      'ascent':568,'ascent_rank_mass':1172,
      'descent':204,'descent_rank_mass':340}
    reports[mode]={
      'distinct_required_logical_fields':216,
      'sources':104,'targets':104,'dirty_helpers':8,
      'new_clean_aggregate_fields':0,
      'early_borrow_compensation_Y':100,
      'physical_rank_decreasing_events':308,
      'physical_rank_decreasing_mass':444,
      'physical_rank_increasing_events':672,
      'physical_rank_increasing_mass':1276,
      'all_native_children':980,'native_rank_mass':1720,
      'source_and_owner_authority':'OPEN',
      'nonmonotone_selected_hosting':'OPEN',
      'source_target_ownership_records':rec}
out={'schema':'p104-inplace-owner-necessary-boundary/1',
 'status':'PASS_FINITE_INVENTORY_NOT_ADMITTED_HOST',
 'programs':reports,'all_size':'OPEN','new_kappa':False}
(P/'P104_INPLACE_OWNER_BOUNDARY.json').write_text(
 json.dumps(out,sort_keys=True,indent=2)+'\n')
print('PASS_P104_216_OWNER_ROLES'
      ' rank_decreasing_moves=308 decreasing_rank_mass=444'
      ' nonmonotone_selected_host_NOT_ADMITTED')

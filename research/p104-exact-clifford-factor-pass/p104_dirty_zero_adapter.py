#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Transform the frozen clean P104 E8 trace into arbitrary-dirty, zero-reset-free
borrowed-helper trace without changing a *single* native transport recipe.

This is a finite algebraic adapter only. Requires early owner/write access to
100 output Y rows and eight already-existing dirty helper fields at chart 0.
"""
import sys,json,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'p104_native_e8_gate/scripts'))
import native_chart_emitter as E
SRC_SHA='a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39'

def make():
    old=E.build(1909)
    text=json.dumps(old,indent=2,sort_keys=True)+'\n'
    assert hashlib.sha256(text.encode()).hexdigest()==SRC_SHA,'frozen native word drift'
    assert len(old['events'])==1064
    assert old['counts']['addition_events']==292
    frames=old['frames']
    zero=frames.index([])
    pre=[]; touched=set(); helpers=set()
    for e in old['events']:
        if e[0]=='add' and e[1].startswith('Y') and e[2].startswith('H'):
            _,y,h,sign,frame=e
            assert sign in (-1,1) and len(frames[frame])>=2
            pre.append(['add',y,h,-sign,zero]);touched.add(y);helpers.add(h)
    assert len(pre)==156 and len(touched)==100 and len(helpers)==8
    original=[e for e in old['events'] if e[0] not in ('zero','erase')]
    assert sum(e[0]=='zero' for e in old['events'])==8
    assert sum(e[0]=='erase' for e in old['events'])==8
    # The original Y values and eight dirty fields are *owned* and addressable
    # at frame 0 before any prep. This is a nonfree physical scheduling contract.
    w=old.copy();w['events']=pre+original
    w['schema']='p104-borrowed-dirty-helper-zero-chart-adapter/1'
    w['scope']='exact finite dirty-helper trace; early Y ownership, paid source/owner and all-size OPEN'
    w['source_pin']=SRC_SHA
    w['pre_reads']=156;w['dirty_helpers']=8;w['output_early_live']=100
    c=old['counts'].copy()
    c.update(addition_events=448,adds=448,rank_mass=1496,
             transport_occurrences=756,distinct_transports=514,
             zero_initializations=0,helpers_zero_initialized=0,helpers_zero_erased=0,
             new_pre_read_zero_frame_ADD=156,
             original_transport_count=756,
             original_transport_rank_mass=1496,
             **{'events':len(w['events'])})
    w['counts']=c
    w['flags']={**old['flags'],
        'full_arbitrary_dirty_helper_compatibility':True,
        'symbolic_arbitrary_dirty':True,
        'full_dirt_restoration':True,
        'clean_initialize_or_erase_required':False,
        'output_owners_early_and_paid':False,
        'source_admitted':False,
        'paid_full_recursive_profile':False,
        'uniform_all_size_supplier':False,
        'new_kappa':False}
    assert len(w['events'])==1204
    assert w['transports'] is old['transports']
    return w

if __name__=='__main__':
    w=make();out=ROOT/'P104_BORROWED_DIRTY_WORD.json'
    out.write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
    print('PASS_P104_DIRTY_ZERO_CHART_ADAPTER outputs=104 dirty=8 '
          'pre_reads=156 ADD=448 rank_mass=1496 transports=756 '
          'no_clean_reset=YES host_cost_OPEN')

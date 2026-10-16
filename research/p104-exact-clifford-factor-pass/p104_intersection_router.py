#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Minimum-rank nested E8 chart routing under fixed per-register scalar anchors.
No owner/host or all-size admission; selected kappa unchanged.
"""
from pathlib import Path
import collections,json
P=Path(__file__).resolve().parent
CONFIG={'G':next(x for x in ('P104_INPLACE_DYADIC_WORD.json','P104_INPLACE_DYADIC_TARGET_WORD.json') if (P/x).exists()),
        'I_minus_G_half':next(x for x in ('P104_INPLACE_SIDE_WORD.json','P104_INPLACE_SIDE_I_MINUS_G_HALF_WORD.json') if (P/x).exists())}
O=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
BASE=[tuple(x) for x in O['frames']]

def closure(basis):
    t={0}
    for v in basis:t|={v^x for x in tuple(t)}
    return t

def intersection(a,b):
    common=closure(a)&closure(b)
    out=[];seen={0}
    for x in sorted(common):
        if x not in seen:
            out.append(x);seen|={x^v for v in tuple(seen)}
    assert seen==common
    return tuple(out)

def distance(a,b):
    return len(a)+len(b)-2*len(intersection(a,b))

def run(filename):
    old=json.loads((P/filename).read_text());original=old['events']
    frames=list(BASE);index={f:i for i,f in enumerate(frames)}
    zero=index[()];helpers=sorted({v for e in original if e[0]=='add'
                                    for v in e[1:3] if v.startswith('H')})
    assert len(helpers)==8
    state={f'Y{t}':zero for t in range(104)}
    state.update({h:zero for h in helpers})
    out=[];stats=collections.Counter();by_role=collections.defaultdict(collections.Counter)
    def move(role,destination):
        if state[role]==destination:return
        a,b=frames[state[role]],frames[destination]
        joint=intersection(a,b)
        if closure(joint) in (closure(a),closure(b)):
            route=[destination]
        else:
            if joint not in index:
                index[joint]=len(frames);frames.append(joint)
            route=[index[joint],destination]
        for target in route:
            p=state[role];A,B=frames[p],frames[target]
            assert closure(A)<=closure(B) or closure(B)<=closure(A)
            r=abs(len(A)-len(B));assert r>0
            out.append(['transport',role,p,target,r]);state[role]=target
            stats['transports']+=1;stats['rank_mass']+=r
            by_role[role[0]]['transports']+=1;by_role[role[0]]['rank_mass']+=r
            if len(A)>len(B):
                stats['descents']+=1;stats['descent_rank_mass']+=r
                by_role[role[0]]['descents']+=1;by_role[role[0]]['descent_rank_mass']+=r
    for e in original:
        k=e[0]
        if k=='transport':continue
        if k=='source_to_zero':
            assert e[1] not in state
            state[e[1]]=zero;out.append(e)
        elif k=='source_from_zero':
            move(e[1],zero);out.append(e);state[e[1]]='intrinsic'
        elif k=='add':
            _,dest,src,s,f=e
            move(src,f);move(dest,f);out.append(e)
        elif k=='sign':
            move(e[1],e[3]);out.append(e)
        else:raise AssertionError(e)
    final={f'Y{t}':zero for t in range(104)}
    final.update({h:zero for h in helpers})
    for e in original:
        if e[0]=='source_to_zero':final[e[1]]=zero
        elif e[0]=='transport':final[e[1]]=e[3]
        elif e[0]=='source_from_zero':final[e[1]]='intrinsic'
    for h in helpers:move(h,zero)
    for t in range(104):move('Y'+str(t),final['Y'+str(t)])
    assert state==final
    assert [e for e in out if e[0]!='transport']==[e for e in original if e[0]!='transport']
    prior=collections.Counter()
    for e in original:
        if e[0]=='transport':
            prior['transports']+=1;prior['rank_mass']+=e[4]
            if len(BASE[e[2]])>len(BASE[e[3]]):
                prior['descents']+=1;prior['descent_rank_mass']+=e[4]
    anchors={f'Y{t}':[zero] for t in range(104)}
    anchors.update({h:[zero] for h in helpers})
    for e in original:
        if e[0]=='source_to_zero':anchors[e[1]]=[zero]
        elif e[0]=='add':
            anchors[e[1]].append(e[4]);anchors[e[2]].append(e[4])
        elif e[0]=='sign':anchors[e[1]].append(e[3])
        elif e[0]=='source_from_zero':anchors[e[1]].append(zero)
    for h in helpers:anchors[h].append(zero)
    for t in range(104):anchors['Y'+str(t)].append(final['Y'+str(t)])
    lower=sum(distance(BASE[a],BASE[b]) for seq in anchors.values()
              for a,b in zip(seq,seq[1:]))
    assert lower==stats['rank_mass']==1238
    assert (prior['transports'],prior['rank_mass'])==(772,1512)
    assert stats['transports'] in (687,703)
    stats['source_port_entrances']=104;stats['source_port_exits']=104
    stats['full_native_children']=stats['transports']+208
    stats['full_native_rank_mass']=stats['rank_mass']+208
    stats['new_intersection_frames']=len(frames)-len(BASE)
    return {'schema':'p104-fixed-anchor-intersection-rank/1',
            'status':'finite exact fixed-anchor rank minimum; hosting NOT admitted',
            'source_word_sha256':O['source_pin'],
            'original_counts':dict(prior),'new_counts':dict(stats),
            'lower_bound_rank_mass_fixed_anchors':lower,
            'savings_rank_mass':prior['rank_mass']-lower,
            'per_register_family':{k:dict(v) for k,v in by_role.items()},
            'owner_host_idle_tape_precision':'OPEN',
            'selected_comparator':'OPEN','all_size':'OPEN','new_kappa':False,
            'frames':[list(f) for f in frames],'events':out}

if __name__=='__main__':
    for key,name in CONFIG.items():
        r=run(name)
        (P/f'P104_INTERSECTION_{key}.json').write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
        print('PASS_INTERSECTION_ROUTING',key,'rank',r['new_counts']['rank_mass'],
              'children',r['new_counts']['transports'],
              'decreasing',r['new_counts']['descents'])

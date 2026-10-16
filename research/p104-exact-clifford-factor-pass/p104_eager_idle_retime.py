#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Owner-idle proxy: schedule each shortest-path descent immediately after
its preceding scalar/source anchor; delay ascent until the next anchor.
Same native children, same scalar order; not a paid host/idle invoice.
"""
from pathlib import Path
import collections,json
P=Path(__file__).resolve().parent

def retime(label):
    w=json.loads((P/f'P104_INTERSECTION_{label}.json').read_text())
    original=w['events'];fr=w['frames']
    anchors=[e for e in original if e[0]!='transport'];n=len(anchors)
    next_touch={};next_for=[None]*len(original);cursor=n
    for i in range(len(original)-1,-1,-1):
        e=original[i]
        if e[0]=='transport':
            next_for[i]=next_touch.get(e[1],n)
        else:
            cursor-=1
            for r in (e[1],e[2]) if e[0]=='add' else (e[1],):
                next_touch[r]=cursor
    assert cursor==0
    pre=collections.defaultdict(list);post=collections.defaultdict(list)
    last={};position=-1
    for i,e in enumerate(original):
        if e[0]!='transport':
            position+=1
            for r in (e[1],e[2]) if e[0]=='add' else (e[1],):
                last[r]=position
        elif len(fr[e[2]])>len(fr[e[3]]):
            post[last.get(e[1],-1)].append(e)
        else:pre[next_for[i]].append(e)
    result=list(post[-1])
    for k,a in enumerate(anchors):result+=pre[k]+[a]+post[k]
    result+=pre[n]
    assert len(result)==len(original)
    def occupancy(events):
        empty=next(i for i,f in enumerate(fr) if not f)
        helpers=sorted({r for e in events if e[0]=='add'
                        for r in e[1:3] if r.startswith('H')})
        chart={f'Y{i}':empty for i in range(104)}
        chart.update({h:empty for h in helpers})
        total=helper_total=peak=anchors_seen=0
        for e in events:
            k=e[0]
            if k=='transport':
                assert chart[e[1]]==e[2]
                chart[e[1]]=e[3]
            elif k=='source_to_zero':chart[e[1]]=empty
            elif k=='source_from_zero':
                assert chart[e[1]]==empty
                chart[e[1]]='intrinsic'
            elif k=='add':
                assert chart[e[1]]==chart[e[2]]==e[4]
            elif k=='sign':assert chart[e[1]]==e[3]
            else:raise AssertionError(e)
            if k!='transport':
                width=lambda v:1 if v=='intrinsic' else len(fr[v])
                occupied=sum(width(chart.get('S'+str(i),'intrinsic')) for i in range(104))
                occupied+=sum(width(chart['Y'+str(i)]) for i in range(104))
                hwidth=sum(width(chart[h]) for h in helpers)
                occupied+=hwidth
                total+=occupied;helper_total+=hwidth;peak=max(peak,occupied)
                anchors_seen+=1
        return {'milestones':anchors_seen,'rank_dimension_area_proxy':total,
                'helper_rank_dimension_area_proxy':helper_total,
                'peak_chart_dimension_sum_proxy':peak}
    before=occupancy(original);after=occupancy(result)
    assert before['milestones']==after['milestones']
    assert after['rank_dimension_area_proxy']<before['rank_dimension_area_proxy']
    assert after['peak_chart_dimension_sum_proxy']<=before['peak_chart_dimension_sum_proxy']
    out={**w,'status':'PASS_EAGER_ASCENT_LATE_DESCENT_EARLY',
         'events':result,'scheduling':'descent at preceding anchor; ascent at next anchor',
         'idle_proxy_before':before,'idle_proxy_after':after,
         'physical_owner_and_paid_idle':'OPEN','new_kappa':False}
    (P/f'P104_INTERSECTION_EAGER_{label}.json').write_text(
        json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('PASS_P104_EAGER_IDLE_PROXY',label,before,after)

if __name__=='__main__':
    for label in ('G','I_minus_G_half'):retime(label)

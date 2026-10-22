#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact GF(2) single/adjacent-two-contact P16 paid-rank screening.

Pinned source: #4470 b9a13c1673e0e9697de410de16e8bbf3207a7363.
No free C0 owner changes and no invented output credit. A moment-only
candidate does not establish exact physical phase, tape, or κ.
"""
from pathlib import Path
from collections import Counter
import json,math,sys
P=Path(__file__).resolve().parent
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else P.parents[2]
sys.path.insert(0,str(ROOT/'research/joint-helper-lattice'))
import native_joint as J

def roles(e):
    if e[0]!='scalar':return []
    g=e[1]
    values=g[1:3] if g[0] in ('add','copy') else g[1:2]
    return list(dict.fromkeys(x[1] for x in values if x[0]=='L'))

def has_owned(e):
    if e[0]!='scalar':return False
    g=e[1]
    values=g[1:3] if g[0] in ('add','copy') else g[1:2]
    return any(x[0]=='C' for x in values)

def compute():
    c,programs,_,_,_=J.construct();W=programs['forward']
    frames=c['frames']
    span=[frozenset(J.F.span(f)) for f in frames]
    dim=[len(s).bit_length()-1 for s in span]
    assert all(len(s)==2**d for s,d in zip(span,dim))
    left={};right={};previous={};following={}
    last=c['start'][:];last_contact={}
    for j,e in enumerate(W):
        if e[0]=='warp':
            last[e[1][1]]=e[4];last_contact[e[1][1]]=None
        if e[0]=='scalar':
            rs=roles(e)
            if rs:
                left[j]=[(r,last[r]) for r in rs]
                for r in rs:
                    previous[j,r]=last_contact.get(r)
                    last[r]=e[2];last_contact[r]=j
    last=c['final'][:];last_contact={}
    for j in range(len(W)-1,-1,-1):
        e=W[j]
        if e[0]=='warp':
            last[e[1][1]]=e[3];last_contact[e[1][1]]=None
        if e[0]=='scalar':
            rs=roles(e)
            if rs:
                right[j]=[(r,last[r]) for r in rs]
                for r in rs:
                    following[j,r]=last_contact.get(r)
                    last[r]=e[2];last_contact[r]=j
    def join(parts):
        basis=[v for f in parts for v in f]
        return frozenset(J.F.span(basis))
    def costs(pre,nxt,d):
        return sum(((d-(len(a).bit_length()-1))**t if d>len(a).bit_length()-1 else 0)
                   +(((len(b).bit_length()-1)-d)**t if len(b).bit_length()-1>d else 0)
                   for (_,a),(_,b) in zip(pre,nxt))
    t=1-.00302017
    opts={};single=[]
    for j,pre in left.items():
        nex=right[j];old=span[W[j][2]]
        a=join([frames[x] for _,x in pre])
        b=frozenset.intersection(*(span[x] for _,x in nex))
        assert a<=old<=b
        normalized_before=[(r,span[x]) for r,x in pre]
        normalized_after=[(r,span[x]) for r,x in nex]
        do=dim[W[j][2]]
        for new in {a,b}:
            if new==old:continue
            dn=len(new).bit_length()-1
            delta=costs(normalized_before,normalized_after,do)-costs(normalized_before,normalized_after,dn)
            assert delta<=1e-9,('unexpected single gain',j,delta)
            entry={'event':j,'new_span':new,'delta':delta,'owned':has_owned(W[j])}
            opts.setdefault(j,[]).append(entry);single.append(entry)
    assert len(single)==611 and sum(abs(e['delta'])<1e-10 for e in single)==239
    improved=[]
    attempts=0
    for entry in single:
        i=entry['event'];s=entry['new_span']
        neighbors={k for r in roles(W[i]) for k in
                   (previous.get((i,r)),following.get((i,r)))
                   if k is not None and k in left}
        for j in neighbors:
            before=[(r,s if previous.get((j,r))==i else span[x]) for r,x in left[j]]
            after=[(r,s if following.get((j,r))==i else span[x]) for r,x in right[j]]
            low=join([list(x) for _,x in before])
            high=frozenset.intersection(*(x for _,x in after))
            if not low<=high:continue
            old=span[W[j][2]]
            assert low<=old<=high
            oldcost=costs(before,after,dim[W[j][2]])
            for candidate in {low,high}:
                if candidate==old:continue
                rank=len(candidate).bit_length()-1
                gain=entry['delta']+oldcost-costs(before,after,rank)
                attempts+=1
                if gain>1e-10:
                    improved.append({'first':i,'second':j,'native_gain':gain,
                                     'first_frame':list(entry['new_span']),
                                     'second_frame':list(candidate),
                                     'owned_contact':entry['owned'] or has_owned(W[j]),
                                     'first_rank':len(s).bit_length()-1,
                                     'second_rank':rank})
    improved.sort(key=lambda r:-r['native_gain'])
    admissible=[x for x in improved if not x['owned_contact']]
    report={'schema':'p16-pr4470-contact-pair-exact-f2-span/1',
      'status':'PASS_GF2_EXACT_SEARCH_NOT_OPERATOR_ADMISSION',
      'source_sha':'b9a13c1673e0e9697de410de16e8bbf3207a7363',
      'native_events_each_orientation':len(W),
      'all_frames_verified_binary_subspaces':len(span),
      'single_endpoint_candidates':len(single),
      'single_improving_candidates':0,
      'single_equal_cost_candidates':sum(abs(x['delta'])<1e-10 for x in single),
      'two_contact_combination_attempts':attempts,
      'two_contact_improving_including_owned':len(improved),
      'two_contact_improving_ignoring_owned_workspace':len(admissible),
      'top_improvements':[dict(x,first_frame_rank=x['first_rank'],
                          second_frame_rank=x['second_rank'])
                          for x in improved[:12]],
      'candidate_native_phase':'UNPROVED',
      'conditional_kappa_target':'0.00302017',
      'new_kappa':False}
    (P/'CONTACT_PAIR_EXACT_GF2_RECEIPT.json').write_text(
        json.dumps(report,sort_keys=True,indent=2)+'\n')
    print('PASS_PR4470_GF2_CLOSED_SPAN_SINGLE',len(single),
          'PAIR',attempts,'POSITIVE',len(improved),
          'WITHOUT_OWNED_C0',len(admissible))
    return report

if __name__=='__main__':compute()

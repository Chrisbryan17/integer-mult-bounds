#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Physical Delta inverse-transpose transport: all retimed 104-port P104 words.
Finite exact Clifford, not an admitted selected supplier or a new kappa.
"""
from pathlib import Path
import json, collections, hashlib, sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from p104_physical_e8_isometry import physical
from p104_native_e8_gate.scripts import native_chart_emitter as E
from p104_rank_r_native_recipes import gates_of
from p104_dual_native_check import conjugate,dual_positive
from p104_routed_native_audit import equal_exact

def run(mode):
    src=P/f'P104_INTERSECTION_{mode}.json'
    forward=P/f'P104_ROUTED_NATIVE_{mode}.json'
    word=json.loads(src.read_text()); compiled=json.loads(forward.read_text())
    frames=[tuple(physical(v) for v in f) for f in word['frames']]
    actual=collections.Counter((e[2],e[3]) for e in word['events'] if e[0]=='transport')
    records=[];hist=collections.Counter()
    for j,rec in enumerate(compiled['recipes']):
        a,b,r,n=rec['old'],rec['new'],rec['rank'],rec['occurrences']
        assert actual[a,b]==n and abs(len(frames[a])-len(frames[b]))==r
        signed=gates_of(rec['left_monomial'])+[
            ['C',1<<i,1] for i in range(r)]+gates_of(rec['right_monomial'])
        got=dual_positive({'old':a,'new':b,'rank':r,
                           'occurrences':n,'gates':signed})
        exact=conjugate([list(g) for g in E.transport(frames[a],frames[b])])
        equal_exact(exact,got['conjugate_native_word'])
        assert sum(g[0]=='C' for g in got['conjugate_native_word'])==r
        assert all(g[2]==1 for g in got['conjugate_native_word'] if g[0]=='C')
        if j==0:
            for k in ('PH','C','X'):
                bad=[list(g) for g in got['conjugate_native_word']]
                at=next(i for i,g in enumerate(bad) if g[0]==k)
                if k=='PH':bad[at][1]=(bad[at][1]+1)%4
                elif k=='C':bad[at][2]*=-1
                else:bad[at][1]^=1
                try:equal_exact(exact,bad)
                except AssertionError:pass
                else:raise AssertionError('accepted '+k+' corruption')
        hist[r]+=n
        records.append({'old':a,'new':b,'rank':r,'count':n,
                        'left':got['left'],'right':got['right']})
    expected=(485,687) if mode=='G' else (493,703)
    assert (len(records),sum(hist.values()))==expected
    assert sum(r*n for r,n in hist.items())==1238
    report={'schema':'p104-retimed-delta-native/1','status':'PASS_FINITE',
            'mode':mode,'source_word_sha256':word['source_original_word_sha256'],
            'forward_recipes_sha256':hashlib.sha256(forward.read_bytes()).hexdigest(),
            'recipes':len(records),'conjugate_native_children':sum(hist.values()),
            'source_port_rank_one_children':208,
            'total_positive_children':sum(hist.values())+208,
            'internal_rank_mass':1238,'total_rank_mass':1446,
            'rank_hist':dict(sorted(hist.items())),
            'global_phase_sign_offset_controls':'REJECTED',
            'source_owner_host_tape':'OPEN','selected_moment':'OPEN',
            'all_size':'OPEN','new_kappa':False,'records':records}
    (P/f'P104_RETIMED_DELTA_NATIVE_{mode}.json').write_text(
        json.dumps(report,sort_keys=True,separators=(',',':'))+'\n')
    print('PASS_P104_RETIMED_DELTA',mode,len(records),sum(hist.values()),1238,flush=True)
if __name__=='__main__':
    for mode in ('G','I_minus_G_half'):run(mode)

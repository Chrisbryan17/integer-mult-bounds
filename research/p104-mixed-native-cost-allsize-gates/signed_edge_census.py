#!/usr/bin/env python3
"""Full E8 P104 signed-edge asymmetry verification, exact integer arithmetic.
Depends on merged #968 source. No native/all-size/kappa claim.
"""
import importlib.util
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'research'/'complex-frame-pair-decoders'/'verify.py'
spec=importlib.util.spec_from_file_location('complex_p104',SOURCE)
src=importlib.util.module_from_spec(spec);spec.loader.exec_module(src)
IP=src.IP
F0=tuple(src.FRAME0)
frames=src.frames_in(src.P112)
assert len(frames)==1260
hist=Counter();frame_types=Counter();decoders=0;checks=0
for F1 in frames:
    solutions=src.frame_pair_solutions(F0,F1)
    frame_types[len(solutions)]+=1
    assert len(solutions) in (0,8)
    live=sorted(set(range(120))-set(F0)-set(F1))
    assert len(live)==104
    for pairs in solutions:
        a=[p[0] for p in pairs]
        assert all((IP[a[i]][pairs[j][1]] in (-1,1)) if i==j
                   else (IP[a[i]][pairs[j][1]]==0)
                   for i in range(8) for j in range(8))
        rows=[tuple(IP[t][u] for u in a) for t in live]
        supports=[sum(1<<i for i,c in enumerate(row) if c) for row in rows]
        support_set=set(supports)
        assert len(support_set)==104
        E=[(i,j) for i in range(8) for j in range(i+1,8)
           if (1<<i)|(1<<j) in support_set]
        assert len(E)==12
        graph={i:set() for i in range(8)}
        for i,j in E:graph[i].add(j);graph[j].add(i)
        assert all(len(graph[i])==3 for i in range(8))
        antipode={}
        for i in range(8):
            dist={i:0};queue=[i]
            for u in queue:
                for v in graph[u]:
                    if v not in dist:
                        dist[v]=dist[u]+1;queue.append(v)
            opposite=[v for v in range(8) if dist[v]==3]
            assert len(opposite)==1
            antipode[i]=opposite[0]
        for i,j in E:
            same=[];opposite=[]
            for row,S in zip(rows,supports):
                if row[i] and row[j]:
                    (same if row[i]==row[j] else opposite).append(S)
            lengths=(len(same),len(opposite))
            assert sorted(lengths)==[1,27],(decoders,i,j,lengths)
            exceptional=same if len(same)==1 else opposite
            assert exceptional==[255^((1<<antipode[i])|(1<<antipode[j]))]
            hist[lengths]+=1;checks+=28
        decoders+=1
assert frame_types==Counter({8:896,0:364})
assert decoders==7168 and checks==2408448
assert hist==Counter({(27,1):53760,(1,27):32256}),hist
print('PASS_E8_SINGLE_SIGN_27_1 decoders=7168 edges=86016 reads=2408448 minority_at_antipodal_complement=YES no_kappa')

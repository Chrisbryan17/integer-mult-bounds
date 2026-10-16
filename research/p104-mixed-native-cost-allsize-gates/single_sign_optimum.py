#!/usr/bin/env python3
"""Finite independent P104 single-sign mixer-bank optimiser; no native/kappa claim."""
from functools import lru_cache
from itertools import combinations

EDGES=tuple((i,j) for i,j in combinations(range(8),2) if (i^j).bit_count()==1)
assert len(EDGES)==12

def tree(mask):
    vertices=[i for i in range(8) if mask>>i&1]
    n=len(vertices)
    if not 2<=n<=5:return False
    links={i:{j for j in vertices if j!=i and (i^j).bit_count()==1} for i in vertices}
    if sum(map(len,links.values()))//2!=n-1:return False
    seen={vertices[0]}; pending=[vertices[0]]
    while pending:
        for j in links[pending.pop()]-seen:
            seen.add(j);pending.append(j)
    return len(seen)==n

F=[m for m in range(1,255) if tree(m if m.bit_count()<=5 else 255^m)]
assert len(F)==104
assert {m for m in F if m.bit_count()==6} == {
    255^((1<<a)|(1<<b)) for a,b in EDGES
}
BLOCK=[sum(1<<k for k,(u,v) in enumerate(EDGES) if a in (u,v) or b in (u,v))
       for a,b in EDGES]

@lru_cache(None)
def width(mask):
    if not mask:return 0
    bit=mask&-mask;j=bit.bit_length()-1
    return max(width(mask^bit),1+width(mask&~BLOCK[j]))

# A physical decoder has one exceptional opposite-sign read of edge (a,b).
# The exceptional support is the complement of the ANTIPODAL edge,
# not the complement of (a,b). This finite sign lemma needs its separate
# root-census replay; the optimiser conditions on it.
ALLOWED=[]
for s in F:
    mask=0
    for j,(a,b) in enumerate(EDGES):
        opposite=(1<<(a^7))|(1<<(b^7))
        if (s>>a&1) and (s>>b&1) and s!=(255^opposite):
            mask|=1<<j
    ALLOWED.append(mask)

def invoice(bank):
    q=bank.bit_count()
    # Exactly one signed rank-two helper per bank edge, including
    # original-source climbs and returns, helper build and zero-restore.
    rank=832+12*q;adds=4*q;add_mass=8*q
    for s,m in zip(F,ALLOWED):
        n=s.bit_count();p=width(bank&m)
        # Original singles first, then the disjoint rank-two mixed reads.
        rank+=n*(n-1)-2*p*(n-p)
        adds+=n-p
        add_mass+=n*(n+1)//2-p*(n-p)
    return rank,adds,add_mass,q

costs=[invoice(b) for b in range(1<<12)]
assert costs[0]==(2224,416,1112,0)
best_rank=min(v[0] for v in costs)
best_mass=min(v[0]+v[2] for v in costs)
winners=[b for b,v in enumerate(costs) if v[0]+v[2]==best_mass]
assert best_rank==1496
assert costs[4095]==(1504,288,776,12)
assert len(winners)==6
assert all(costs[b]==(1496,292,764,8) for b in winners)
assert winners==[1781,1995,2526,2995,3437,3646]
print('PASS_SINGLE_SIGN_BANK banks=4096 helpers=8 adds=292 frame_rank=1496 add_rank=764 winners=6 native=UNPROVEN kappa=UNCHANGED')

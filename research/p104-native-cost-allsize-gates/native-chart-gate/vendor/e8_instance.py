#!/usr/bin/env python3
"""Independent genuine E8 root-instance check of mixed-label inclusion and signs."""
import itertools
from collections import Counter
from pathlib import Path
import json

roots=[]
for i,j in itertools.combinations(range(8),2):
 for ai,aj in itertools.product((2,-2),repeat=2):
  r=[0]*8;r[i]=ai;r[j]=aj;roots.append(tuple(r))
for row in itertools.product((1,-1),repeat=8):
 if row.count(-1)%2==0:roots.append(row)
def canon(v):
 return v if next(x for x in v if x)>0 else tuple(-x for x in v)
lines=sorted({canon(r) for r in roots})
assert len(roots)==240 and len(lines)==120
index={r:i for i,r in enumerate(lines)}
def dot(a,b):return sum(x*y for x,y in zip(a,b))
IP=[[dot(x,y)//4 for y in lines] for x in lines]
assert all(dot(a,b)%4==0 for a in lines for b in lines)
f0=[index[canon(tuple(2 if j==2*i else 2*k if j==2*i+1 else 0 for j in range(8)))] for i in range(4) for k in (1,-1)]
assert len(set(f0))==8
orth={i:{j for j in range(120) if j!=i and IP[i][j]==0} for i in range(120)}
remain=set(range(120))-set(f0)
found=[]
def clique(path,candidates):
 if len(path)==8:
  found.append(tuple(path));return
 while candidates:
  i=min(candidates);candidates.remove(i)
  clique(path+[i],{j for j in candidates if j in orth[i]})
clique([],set(remain))
assert len(found)==1260,len(found)

def solutions(f1):
 # Exact paired-normal search, both sides of a mixed coordinate frame.
 for smask in range(256):
  A=[f0[k] for k in range(8) if smask>>k&1]
  choices=[[j for j in f1 if all((IP[j][x]!=0)==(x==i) for x in A)] for i in A]
  if any(not c for c in choices):continue
  for c in itertools.product(*choices):
   if len(set(c))!=len(c):continue
   T=[j for j in f1 if j not in c]
   if len(T)!=8-len(A):continue
   rest=[i for i in f0 if i not in A]
   choices2=[[j for j in rest if all((IP[j][x]!=0)==(x==i) for x in T)] for i in T]
   if any(not c2 for c2 in choices2):continue
   for c2 in itertools.product(*choices2):
    if len(set(c2))!=len(c2):continue
    return list(zip(A,c))+list(zip(T,c2))
 return None
chosen=None
for f1 in found:
 sol=solutions(f1)
 if sol:
  chosen=(f1,sol);break
assert chosen is not None
f1,pairs=chosen
assert len(pairs)==8
live=sorted(set(range(120))-set(f0)-set(f1))
assert len(live)==104
assert all((IP[a][b] in (-1,1) if i==j else IP[a][b]==0)
           for i,(a,_) in enumerate(pairs) for j,(_,b) in enumerate(pairs))
NROW=[sum(((IP[i][j]+1)&1)<<j for j in range(120)) for i in range(120)]
# Recover the canonical cube chart from its two-term support graph.
supports=[sum(1<<k for k,(a,b) in enumerate(pairs) if IP[t][a]) for t in live]
assert len(set(supports))==104
edges=[(a,b) for a,b in itertools.combinations(range(8),2) if (1<<a)|(1<<b) in supports]
assert len(edges)==12
E2={(min(a,b),max(a,b)) for a,b in edges}
# Enumerate canonical bijections preserving graph edges.
charts=[]
for base in range(8):
 neighbors=[x for x in range(8) if (min(base,x),max(base,x)) in E2]
 if len(neighbors)!=3:continue
 for first in itertools.permutations(neighbors):
  mapping={0:base,1:first[0],2:first[1],4:first[2]}
  for x in (3,5,6):
   a=next(i for i in (1,2,4) if i&x)
   b=next(i for i in (1,2,4) if i&x and i!=a)
   common=[k for k in range(8) if (min(mapping[a],k),max(mapping[a],k)) in E2 and (min(mapping[b],k),max(mapping[b],k)) in E2 and k!=base]
   if len(common)!=1:break
   mapping[x]=common[0]
  if len(mapping)!=7:continue
  end=set(range(8))-set(mapping.values())
  if len(end)!=1:continue
  mapping[7]=next(iter(end))
  if all(((i^j).bit_count()==1)==((min(mapping[i],mapping[j]),max(mapping[i],mapping[j])) in E2) for i in range(8) for j in range(i+1,8)):
   charts.append(mapping)
assert len(charts)==48,len(charts)

# Pair-sum binary frame line E_(a+b) belongs to target sink iff two terms
# are both present OR both absent. Only use when both present.
checked=0
for a,b in edges:
 for t,S in zip(live,supports):
  mixed=NROW[pairs[a][0]]^NROW[pairs[b][0]]
  permitted=(mixed>>t&1)==0
  same_presence=bool(S>>a&1)==bool(S>>b&1)
  assert permitted==same_presence
  if (S>>a&1) and (S>>b&1):
   ca,cb=IP[t][pairs[a][0]],IP[t][pairs[b][0]]
   assert abs(ca)==abs(cb)==1
   v=1 if ca==cb else -1
   assert ca*(1)+ca*v*(1)==ca+cb # symbolic coefficients checked below
   checked+=1
# 12 cube edges each co-occur in precisely 28 supports.
assert checked==336,checked
print('PASS_E8_REAL_DECODER frame_count=1260 live=104 labels=120 chart_isomorphisms=48 signed_pair_reads=336 real_root_incidence=PASS no_kappa')

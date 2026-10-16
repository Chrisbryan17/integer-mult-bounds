#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reversibly reuse eight existing P104 source ports as E8 aggregate carriers.
Finite algebra ONLY: 100 early Y owners, 16 half/double operations, physical
source/host access, reverse-word and full all-size supplier remain unadmitted.
"""
from pathlib import Path
import json,sys
from fractions import Fraction
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
import p104_complete_gram_channel_stdlib as base

B=base.B
old=base.old
ROOTS=base.L
PIVOTS=[68,52,101,90,88,55,98,102]
Bp=[[B[i][s] for s in PIVOTS] for i in range(8)]
I,det=base.inverse_exact(Bp)
assert det in (-1,1) and all(x.denominator==1 for row in I for x in row)
U=[[sum(I[i][j]*B[j][s] for j in range(8)) for s in range(104)]
   for i in range(8)]
assert all(U[i][PIVOTS[j]]==int(i==j)
           for i in range(8) for j in range(8))
assert all(x.denominator==1 for row in U for x in row)
zero=base.empty
frames=base.frames

# Signed unit elementary operations reducing Bp to I.
A=[[int(x) for x in row] for row in Bp]
ops=[]
def step(kind,i,j=-1,s=0):
    if kind=='add':
        assert i!=j and s in (-1,1)
        A[i]=[a+s*b for a,b in zip(A[i],A[j])]
    elif kind=='neg':A[i]=[-a for a in A[i]]
    elif kind=='swap':A[i],A[j]=A[j],A[i]
    else:raise AssertionError(kind)
    ops.append((kind,i,j,s))
def addmany(i,j,x):
    for _ in range(abs(x)):
        step('add',i,j,1 if x>0 else -1)
for k in range(8):
    if not A[k][k]:
        step('swap',k,next(j for j in range(k+1,8) if A[j][k]))
    for j in range(k+1,8):
        n=0
        while A[j][k]:
            n+=1;assert n<50
            p,v=A[k][k],A[j][k]
            q=(abs(v)//abs(p))*(1 if p*v>0 else -1)
            if q:addmany(j,k,-q)
            if A[j][k]:step('swap',j,k)
    assert abs(A[k][k])==1
    if A[k][k]<0:step('neg',k)
for k in reversed(range(8)):
    for j in range(k):
        if A[j][k]:addmany(j,k,-A[j][k])
assert A==[[int(i==j) for j in range(8)] for i in range(8)]

def translate(op,undo=False):
    kind,i,j,s=op
    a='S'+str(PIVOTS[i]);b='S'+str(PIVOTS[j]) if j>=0 else ''
    if kind=='add':return [['add',a,b,-s if undo else s,zero]]
    if kind=='neg':return [['sign',a,-1,zero]]
    # This four-event swap is exact, paid and requires no temporary.
    if kind=='swap':
        return [['add',a,b,1,zero],['add',b,a,-1,zero],
                ['add',a,b,1,zero],['sign',b,-1,zero]]
    raise AssertionError(kind)
basis=[e for op in reversed(ops) for e in translate(op,True)]
unbasis=[e for op in ops for e in translate(op)]
outside=[s for s in range(104) if s not in PIVOTS]
prep=[['add','S'+str(PIVOTS[i]),'S'+str(s),
       1 if U[i][s]>0 else -1,zero]
      for s in outside for i in range(8)
      for unused in range(abs(int(U[i][s])))]
unprep=[['add',e[1],e[2],-e[3],zero] for e in reversed(prep)]
assert len(prep)==394
prefix=old['events'][:156]
body=old['events'][156:]
def remap(e):
    e=list(e)
    for j in ((1,2) if e[0]=='add' else (1,) if e[0]=='transport' else ()):
        if isinstance(e[j],str) and e[j].startswith('X'):
            e[j]='S'+str(PIVOTS[int(e[j][1:])])
    return e
body=[remap(e) for e in body]
line=base.line
events=(prefix+
    [['source_to_zero','S'+str(s),ROOTS[s],1] for s in range(104)]+
    prep+basis+
    [['transport','S'+str(PIVOTS[i]),zero,line[i],1] for i in range(8)]+
    [['scale','S'+str(PIVOTS[i]),1,2,line[i]] for i in range(8)]+
    body+
    [['scale','S'+str(PIVOTS[i]),2,1,line[i]] for i in range(8)]+
    [['transport','S'+str(PIVOTS[i]),line[i],zero,1] for i in range(8)]+
    unbasis+unprep+
    [['source_from_zero','S'+str(s),ROOTS[s],1] for s in range(104)])
def count(t):return sum(e[0]==t for e in events)
assert (count('transport'),count('scale'),count('add'),count('sign'))==(772,16,1302,10)
assert count('allocate_zero')==count('erase_zero')==0
out={
 'schema':'p104-source-unimodular-inplace/1',
 'source_word_sha256':old['source_pin'],'pivots':PIVOTS,
 'B_8x104':[[int(x) for x in row] for row in B],
 'Bp_8x8':[[int(x) for x in row] for row in Bp],
 'Bp_inverse':[[int(x) for x in row] for row in I],
 'U_8x104':[[int(x) for x in row] for row in U],
 'basis_unit_ADD':sum(e[0]=='add' for e in basis),
 'basis_SIGN':sum(e[0]=='sign' for e in basis),
 'prep_unit_ADD':len(prep),'signed_ADD':1302,'signed_NEG':10,
 'fractional_scalers':16,'new_clean_aggregate_registers':0,
 'borrowed_dirty_helpers':8,'early_Y_owners':100,
 'native_core_transports':756,'pivot_line_bridges':16,
 'physical_source_bridges':208,'conditional_rank_mass':1720,
 'real_owner_host_scaler':'OPEN','selected_moment':'OPEN',
 'uniform_all_size':'OPEN','new_kappa':False,'events':events}
(P/'P104_INPLACE_SOURCE_WORD.json').write_text(
    json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
print('PASS_P104_INPLACE_UNIMODULAR det=%d prep=394 ADD=1302 SIGN=10'
      ' clean_extra=0 conditional_rank_mass=1720 no_kappa' % det)

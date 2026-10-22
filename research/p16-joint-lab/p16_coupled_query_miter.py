#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact source-pinned PR4470 32x32 and W=2 64x64 Laurent miter.
Coupled query is a FORMAL four-port primitive, not physically admitted.
"""
from collections import Counter
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
def original():
 e=[['LOCAL',0,0,False],['LOCAL',1,0,True],['IDLE',1,[0,1]]]
 for i in range(1,16):
  e.extend([['ADD',2*i-2,2*i,1],['ADD',2*i+1,2*i-1,-1],['QUERY_SHEAR',2*i,i-1,False],['ADD',2*i-2,2*i,-1],['ADD',2*i+1,2*i-1,1],['LOCAL',2*i+1,i,True]])
  if i<=6:e.append(['IDLE',i+1,[0,1]+list(range(3,2*i+2,2))])
 e.append(['LOCAL',32,15,False])
 for j in range(7,15):e.append(['IDLE',j,list(range(2*j+3,32,2))+[32]])
 for i in range(15,0,-1):e.extend([['ADD',2*i,2*i-2,1],['ADD',2*i-1,2*i+1,-1]])
 for i in range(16):e.append(['SIGNED_SWAP',2*i,2*i+1])
 assert len(e)==154
 assert hashlib.sha256(json.dumps(e,separators=(',',':')).encode()).hexdigest()=='624305383d5e7e1687e01356d5e41ff4ee3d4f06b3cab71cf9a65ea22fc8dd52'
 return e
def lower(events):
 out=[];i=0
 while i<len(events):
  if i+4<len(events) and [e[0] for e in events[i:i+5]]==['ADD','ADD','QUERY_SHEAR','ADD','ADD']:
   a,b,q,c,d=events[i:i+5]
   assert a[3]==1 and b[3]==-1 and c[3]==-1 and d[3]==1
   assert a[1:3]==c[1:3] and b[1:3]==d[1:3]
   assert 2*q[2]==a[1] and q[3] is False
   assert a[2]==b[1]-1 and b[2]==a[1]+1
   out.append(['COUPLED_QUERY',q[1],q[2],False,[2*q[2],a[2]],[2*q[2]+1,b[1]]]);i+=5
  else:out.append(events[i]);i+=1
 assert Counter(x[0] for x in out)=={'LOCAL':18,'IDLE':15,'ADD':30,'COUPLED_QUERY':15,'SIGNED_SWAP':16}
 return out
Z=(0,)*34
def mono(c=0,stages=()):
 x=[0]*34;x[0]=c
 for s in stages:x[s+1]+=1
 return tuple(x)
def add(a,b,sgn=1):
 v=dict(a)
 for k,n in b.items():
  m=v.get(k,0)+sgn*n
  if m:v[k]=m
  else:v.pop(k,None)
 return v
def shift(a,k,sgn=1):
 return {tuple(i+j for i,j in zip(ex,k)):sgn*n for ex,n in a.items()}
def offset(e,d):
 a=list(e);kind=a[0]
 if kind in ('LOCAL','QUERY_SHEAR'):a[2]+=d//2
 elif kind=='IDLE':a[1]+=d//2
 elif kind in ('ADD','SIGNED_SWAP'):a[1]+=d;a[2]+=d
 elif kind=='COUPLED_QUERY':
  a[2]+=d//2;a[4]=[x+d for x in a[4]];a[5]=[x+d for x in a[5]]
 return a
def replay(events,n=32):
 rows=[[({Z:1} if i==j else {}) for j in range(n)] for i in range(n)]
 for e in events:
  kind=e[0]
  if kind in ('LOCAL','QUERY_SHEAR'):
   _,stage,pair,back=e
   x,y=(2*pair+1,2*pair) if back else (2*pair,2*pair+1)
   term=mono(1 if back else -1)
   rows[y]=[add(a,shift(b,term,-1 if back else 1)) for a,b in zip(rows[y],rows[x])]
   if kind=='LOCAL':
    term=mono(stages=[stage])
    for r in (x,y):rows[r]=[shift(a,term) for a in rows[r]]
  elif kind=='COUPLED_QUERY':
   _,stage,pair,back,inputs,outputs=e
   assert not back
   old=[list(row) for row in rows];term=mono(-1)
   v=[add(old[inputs[0]][j],old[inputs[1]][j]) for j in range(n)]
   for dst in outputs:rows[dst]=[add(old[dst][j],shift(v[j],term)) for j in range(n)]
  elif kind=='ADD':
   _,dst,src,sgn=e
   rows[dst]=[add(a,b,sgn) for a,b in zip(rows[dst],rows[src])]
  elif kind=='IDLE':
   _,pair,stages=e;term=mono(stages=stages)
   for r in (2*pair,2*pair+1):rows[r]=[shift(a,term) for a in rows[r]]
  elif kind=='SIGNED_SWAP':
   _,a,b=e;rows[a],rows[b]=rows[b],[shift(x,Z,-1) for x in rows[a]]
  else:raise AssertionError(e)
 return rows
def run():
 events=original();candidate=lower(events)
 M=replay(events);N=replay(candidate)
 assert M==N
 trial=json.loads(json.dumps(candidate))
 next(e for e in trial if e[0]=='COUPLED_QUERY')[5][1]=0
 assert replay(trial)!=M
 a=events+[offset(e,32) for e in events]
 b=candidate+[offset(e,32) for e in candidate]
 W=replay(a,64)
 assert W==replay(b,64)
 assert all(not W[i][j] for i in range(32) for j in range(32,64))
 assert all(not W[i][j] for i in range(32,64) for j in range(32))
 receipt={'status':'PASS_EXACT_LAURENT_FULL_OPERATOR','source_sha256':'624305383d5e7e1687e01356d5e41ff4ee3d4f06b3cab71cf9a65ea22fc8dd52',
 'original_events':154,'candidate_events':len(candidate),'W1_full_entries':1024,'W2_full_entries':4096,
 'original_unit_ADD':90,'formal_macro_unit_ADD':30,'query_windows':15,
 'formal_new_coupled_queries':15,'source_shear_mutation':'REJECTED',
 'physical_native_coupled_query_admitted':False,'paid_query_rank_savings':0,
 'selected_kappa':'0.00302015','new_kappa':False}
 (P/'COUPLED_QUERY_FULL_MITER.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
 (P/'COUPLED_QUERY_FORMAL_WORD.json').write_text(json.dumps({'schema':'p16-formal-four-port/1','events':candidate,'physical_admission':False},sort_keys=True,separators=(',',':'))+'\n')
 print('PASS_P16_32_AND_64_LAURENT_MITER query_windows=15 unit_ADD_90_to_30 physical_cost_OPEN')
 return receipt
if __name__=='__main__':run()

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Separate event replay and adversarial tests of the emitted E8 Clifford word.

The physical scalar ADD in a shared chart and abstract zero allocation are
recorded, NOT priced/implemented as a complete source/phase supplier.
"""
from pathlib import Path
import importlib.util,json,copy,gzip
from collections import Counter
P=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
N=load('emitter',P/'native_chart_emitter.py')
E=N.E8
WP=P/'evidence'/'NATIVE_CHART_WORD.json'
WORD=json.loads(WP.read_text() if WP.exists() else gzip.decompress(WP.with_suffix('.json.gz').read_bytes()))
F=[tuple(row) for row in WORD['frames']]

def dim(fr):
    p={}
    for x in fr:
        while x:
            j=x.bit_length()-1
            if j not in p:p[j]=x;break
            x^=p[j]
    return len(p)

def admissible(a,b):
    return all(dim(tuple(b)+(v,))==len(b) for v in a)

def add(x,y,s):
    z=dict(x)
    for k,v in y.items():
        z[k]=z.get(k,0)+s*v
        if not z[k]:del z[k]
    return z

class Failure(Exception):pass

def check(w,dirty=False):
    frames=[tuple(f) for f in w['frames']]
    if not all(len(f)==dim(f)<=9 for f in frames):raise Failure('dependent frame')
    source_id=w['source_root_ids']
    states={f'X{i}':[(N.LABELS[a],),{i:1}] for i,a in enumerate(source_id)}
    count=Counter()
    lookup={(x['old'],x['new']):x for x in w['transports']}
    if len(lookup)!=len(w['transports']):raise Failure('duplicate recipes')
    for k,v in lookup.items():
        a,b=frames[k[0]],frames[k[1]]
        if not (admissible(a,b) or admissible(b,a)):raise Failure('non nested recipe')
        if v['gates']!=json.loads(json.dumps(N.transport(a,b))):raise Failure('bad phase or Clifford recipe')
    out={};initializations=[];erases=[]
    for e in w['events']:
        typ=e[0]
        if typ=='zero':
            _,r=e
            if r in states:raise Failure('duplicate initialization')
            seed={112:1} if (dirty and not initializations) else {}
            states[r]=[(),seed];initializations.append(r)
        elif typ=='transport':
            _,r,old,new,rank=e
            if not (0<=old<len(frames) and 0<=new<len(frames)):raise Failure('bad frame index')
            if r not in states:
                if not r.startswith('Y'):raise Failure('unallocated transport')
                states[r]=[(),{8+int(r[1:]):1}]
            if states[r][0]!=frames[old]:raise Failure('chronology')
            if not (admissible(frames[old],frames[new]) or admissible(frames[new],frames[old])):
                raise Failure('frame not comparable')
            if abs(len(frames[old])-len(frames[new]))!=rank or rank<=0:raise Failure('rank mismatch')
            if (old,new) not in lookup:raise Failure('missing recipe')
            states[r][0]=frames[new];count[rank]+=1
        elif typ=='add':
            _,dst,src,sign,f=e
            if dst not in states or src not in states:raise Failure('unallocated operand')
            if sign not in (-1,1) or states[dst][0]!=states[src][0] or states[dst][0]!=frames[f]:raise Failure('illegal add')
            states[dst][1]=add(states[dst][1],states[src][1],sign)
        elif typ=='erase':
            _,r=e
            if r not in states or states[r][0]!=():raise Failure('nonempty erase frame')
            if states[r][1] and not dirty:raise Failure('nonzero erase')
            erases.append(r)
        else:raise Failure('unknown event')
    if len(initializations)!=8 or len(erases)!=8 or set(erases)!=set(initializations):raise Failure('helper lifecycle')
    for i in range(8):
        if states[f'X{i}']!=[(N.LABELS[source_id[i]],),{i:1}]:raise Failure('modified source')
    errors=[]
    for t,port in enumerate(w['live']):
        ideal={8+t:1}
        for i,a in enumerate(source_id):
            if E.IP[port][a]:ideal[i]=E.IP[port][a]
        if states[f'Y{t}'][1]!=ideal:errors.append(t)
        if len(states[f'Y{t}'][0])!=8:raise Failure('bad output frame')
    if not dirty and errors:raise Failure('wrong signed outputs '+str(errors[:4]))
    if dirty and not errors:raise Failure('arbitrary-dirt false pass')
    if not dirty and any(states[x][1] for x in erases):raise Failure('helper not cleaned')
    if sum(k*v for k,v in count.items())!=w['counts']['rank_mass']:raise Failure('rank sum')
    if len([x for x in w['events'] if x[0]=='add'])!=w['counts']['addition_events']:raise Failure('ADD count')
    return dict(rank=sum(k*v for k,v in count.items()),errors=errors,controls=len(lookup),initializations=len(initializations),transports=sum(count.values()),all_zero_erasures=len(erases))

def reject(w,needle):
    try:check(w)
    except Failure as e:
        if needle and needle not in str(e):raise Failure('wrong rejection '+str(e))
        return True
    raise Failure('bad program falsely accepted')

def test():
    obj=copy.deepcopy(WORD);good=check(obj)
    assert good['rank']==1496 and good['controls']==514
    bad=copy.deepcopy(obj);i=next(i for i,x in enumerate(bad['events']) if x[0]=='add');bad['events'].pop(i)
    reject(bad,'')
    bad=copy.deepcopy(obj);i=next(i for i,x in enumerate(bad['events']) if x[0]=='add');bad['events'][i][3]*=-1
    reject(bad,'')
    bad=copy.deepcopy(obj);i=next(i for i,x in enumerate(bad['events']) if x[0]=='transport');bad['events'][i][4]+=1
    reject(bad,'rank mismatch')
    bad=copy.deepcopy(obj); gates=next(z['gates'] for z in bad['transports'] if any(g[0]=='C' for g in z['gates'])); gi=next(i for i,g in enumerate(gates) if g[0]=='C'); gates[gi][2]*=-1
    reject(bad,'bad phase')
    bad=copy.deepcopy(obj);i=next(i for i,x in enumerate(bad['events']) if x[0]=='zero');bad['events'].pop(i)
    reject(bad,'unallocated')
    dirty=check(WORD,True)
    assert len(dirty['errors'])>0
    print('PASS_NATIVE_CHART_INDEPENDENT_EVENT_REPLAY rank=%d transports=%d ADD=%d outputs=104 helper_lifecycle=8 mutation_controls=5 dirty_helper_contaminates=%d phase_recipes=514 native_recipe_cost_UNOPTIMIZED'%(good['rank'],good['transports'],WORD['counts']['addition_events'],len(dirty['errors'])))

if __name__=='__main__':test()

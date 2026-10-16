#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Emit a phase-specified but UNOPTIMIZED finite E8 signed-mixer trace.

Unlike previous toy support-mask traces, every frame uses the authentic 9D
E8 label space. The per-transfer gate word is an explicit composition of
canonical Clifford charts: Gamma_new * Gamma_old^-1.  This is NOT a supplier:
clean helper allocation, physical address movement, host resources, and its
unoptimized Clifford-child invoice are not certified affordable.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations
from pathlib import Path
import importlib.util, json, hashlib

HERE=Path(__file__).resolve().parent
VENDOR=HERE/'vendor'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
E8=load('p104_e8',VENDOR/'e8_instance.py')
# Representation of F2^9: chosen independent pairing rows as a coordinate basis.
BASIS=[]
for row in E8.NROW:
    trial=BASIS+[row]
    if len(BASIS)<9:
        piv={}
        for z in trial:
            while z:
                j=z.bit_length()-1
                if j not in piv:piv[j]=z;break
                z^=piv[j]
        if len(piv)>len(BASIS):BASIS.append(row)
assert len(BASIS)==9
PIV={}
for k,row in enumerate(BASIS):
    z=row; mask=1<<k
    while z:
        j=z.bit_length()-1
        if j not in PIV:PIV[j]=(z,mask);break
        z^=PIV[j][0];mask^=PIV[j][1]
assert len(PIV)==9

def coordinate(bits):
    coeff=0
    while bits:
        j=bits.bit_length()-1
        assert j in PIV, 'missing E8 label basis'
        z,v=PIV[j];bits^=z;coeff^=v
    return coeff

LABELS=[coordinate(x) for x in E8.NROW]
assert len(set(LABELS))==120

def rank(xs):
    piv={}
    for x in xs:
        while x:
            j=x.bit_length()-1
            if j not in piv:piv[j]=x;break
            x^=piv[j]
    return len(piv)

def contains(fr,x):return rank(tuple(fr)+(x,))==len(fr)
def subset(a,b):return all(contains(b,x) for x in a)

def sink_for(target):
    out=[]
    for j in range(120):
        if (E8.NROW[j]>>target)&1:continue
        z=LABELS[j]
        if not contains(out,z):out.append(z)
        if len(out)==8:break
    assert len(out)==8
    assert all((E8.NROW[j]>>target)&1==0 for j in range(120) if contains(out,LABELS[j]))
    return tuple(out)

# Exact finite Clifford operator syntax inherited from the published exact
# native checker: P(G), D(Q,alpha), signed C(q,+/-), and global PH(p).
N=9

def parity(x):return x.bit_count()&1

def transpose(rows):return tuple(sum(((rows[j]>>i)&1)<<j for j in range(N)) for i in range(N))

def inverse(rows):
    a=[x|(1<<(N+i)) for i,x in enumerate(rows)]
    for j in range(N):
        k=next((i for i in range(j,N) if (a[i]>>j)&1),None)
        assert k is not None
        a[j],a[k]=a[k],a[j]
        for i in range(N):
            if i!=j and (a[i]>>j)&1:a[i]^=a[j]
    return tuple(x>>N for x in a)

def adjoint(gates):
    out=[]
    for gate in reversed(gates):
        k=gate[0]
        if k=='P':out.append(('P',inverse(gate[1])))
        elif k=='D':out.append(('D',gate[1],tuple((-a)%4 for a in gate[2])))
        elif k=='C':out.append(('C',gate[1],-gate[2]))
        elif k=='PH':out.append(('PH',(-gate[1])%4))
        else:raise ValueError(k)
    return tuple(out)

def gamma(U):
    U=tuple(U); r=len(U)
    assert rank(U)==r and r<=9
    if r==0:return ()
    if r==9:return tuple(('C',1<<i,1) for i in range(9))
    ext=list(U)
    for j in range(9):
        if len(ext)==9:break
        if not contains(ext,1<<j):ext.append(1<<j)
    G=transpose(ext)
    Gi=inverse(G);Gt=transpose(Gi)
    Q=tuple((1<<i)^sum(parity(Gt[i]&Gt[j])<<j for j in range(9)) for i in range(9))
    alpha=tuple((Q[i]>>i)&1 for i in range(9))
    K=(('P',G),('D',Q,alpha))
    return adjoint(K)+tuple(('C',1<<i,1) for i in range(r))+K


def transport(a,b):
    assert subset(a,b) or subset(b,a), 'non-nested transport'
    return adjoint(gamma(a))+gamma(b)

class Reg:
    def __init__(self,name,frame,data):self.name=name;self.frame=frame;self.data=dict(data);self.home=frame

def combine(x,y,c):
    out=dict(x)
    for k,v in y.items():
        out[k]=out.get(k,0)+c*v
        if not out[k]:del out[k]
    return out

class Recorder:
    def __init__(self):
        self.event=[];self.frames={};self.frame_by_id=[];self.transports={};self.rank_mass=0;self.adds=0;self.raw_children=0;self.profile=Counter();self.initialized=0
    def frame_id(self,frame):
        if frame not in self.frames:
            self.frames[frame]=len(self.frame_by_id);self.frame_by_id.append(frame)
        return self.frames[frame]
    def move(self,r,frame):
        frame=tuple(frame)
        assert rank(frame)==len(frame)
        if r.frame==frame:return
        old=r.frame
        assert subset(old,frame) or subset(frame,old),(r.name,old,frame)
        amount=abs(len(old)-len(frame))
        self.rank_mass+=amount
        self.profile[amount]+=1
        oldid,newid=self.frame_id(old),self.frame_id(frame)
        k=(oldid,newid)
        if k not in self.transports:
            gates=transport(old,frame)
            assert sum(g[0]=='C' for g in gates)==len(old)+len(frame)
            self.transports[k]=[list(g) for g in gates]
        self.raw_children+=len(old)+len(frame)
        self.event.append(['transport',r.name,oldid,newid,amount])
        r.frame=frame
    def add(self,d,s,sign):
        assert d.frame==s.frame and sign in (-1,1)
        d.data=combine(d.data,s.data,sign)
        self.adds+=1
        self.event.append(['add',d.name,s.name,sign,self.frame_id(d.frame)])
    def init(self,r):
        assert r.frame==() and not r.data
        self.initialized+=1;self.event.append(['zero',r.name])
    def erase(self,r):
        assert r.frame==() and not r.data
        self.event.append(['erase',r.name])


def build(bank=1909):
    assert bank in (0,1909),'validated comparator or mixed bank only'
    F1,pairs=E8.chosen;live=E8.live
    roots=[p[0] for p in pairs]
    signatures=[E8.IP[t][a] for t in live for a in roots]
    rows=[tuple(E8.IP[t][a] for a in roots) for t in live]
    supports=[sum(1<<i for i,x in enumerate(coef) if x) for coef in rows]
    assert len(set(supports))==104
    edges=[(i,j) for i,j in combinations(range(8),2) if ((1<<i)|(1<<j)) in supports]
    assert len(edges)==12
    majors={}
    for a,b in edges:
        same=sum(1 for c in rows if c[a] and c[b] and c[a]==c[b])
        diff=sum(1 for c in rows if c[a] and c[b] and c[a]==-c[b])
        assert sorted((same,diff))==[1,27]
        majors[a,b]=1 if same>diff else -1
    # 1909 is the exact optimizer winner in this noncanonical E8 vertex order.
    selected=[(a,b) for k,(a,b) in enumerate(edges) if bank>>k&1]
    assert len(selected)==(8 if bank else 0)
    for i in range(8):assert rank([LABELS[roots[i]]])==1
    # Symbolic inputs X_i and arbitrary preexisting Y_t are independent.
    regs={f'X{i}':Reg(f'X{i}',(LABELS[roots[i]],),{i:1}) for i in range(8)}
    output=[];rec=Recorder()
    for a,b in selected:
        U=(LABELS[roots[a]],LABELS[roots[b]])
        assert rank(U)==2
        for i in (a,b):rec.move(regs[f'X{i}'],U)
        helper=Reg(f'H{a}_{b}',(),{});rec.init(helper);rec.move(helper,U)
        rec.add(helper,regs[f'X{a}'],1)
        rec.add(helper,regs[f'X{b}'],majors[a,b])
        helper.home=U;regs[helper.name]=helper
        for i in (a,b):rec.move(regs[f'X{i}'],regs[f'X{i}'].home)
    # Enumerate ALL disjoint subsets of the bank to make a deterministic
    # maximum matching, independently of prior optimizer.
    def match(choices):
        best=()
        for length in range(len(choices)+1):
            for subset_edges in combinations(choices,length):
                used=[x for pair in subset_edges for x in pair]
                if len(used)==len(set(used)) and length>len(best):best=subset_edges
        return best
    for t,(coeff,S) in enumerate(zip(rows,supports)):
        sink=sink_for(live[t]);need=[]
        allowed=[(a,b) for a,b in selected if coeff[a] and coeff[b] and coeff[a]*majors[a,b]==coeff[b]]
        chosen=match(allowed)
        covered={z for pair in chosen for z in pair}
        for i in range(8):
            if coeff[i] and i not in covered:need.append((f'X{i}',coeff[i]))
        for a,b in chosen:need.append((f'H{a}_{b}',coeff[a]))
        target=Reg(f'Y{t}',(),{8+t:1})  # no zero-target assumption
        fr=[]
        for key,sgn in need:
            source=regs[key]
            assert subset(source.home,sink)
            for v in source.home:
                if not contains(fr,v):fr.append(v)
            rec.move(target,fr)
            rec.move(source,fr)
            rec.add(target,source,sgn)
            rec.move(source,source.home)
        rec.move(target,sink)
        assert target.data==combine({8+t:1},{i:coeff[i] for i in range(8) if coeff[i]},1),(t,target.data,coeff)
        output.append(target)
    for a,b in selected:
        U=(LABELS[roots[a]],LABELS[roots[b]])
        for i in (a,b):rec.move(regs[f'X{i}'],U)
        helper=regs[f'H{a}_{b}']
        rec.add(helper,regs[f'X{a}'],-1)
        rec.add(helper,regs[f'X{b}'],-majors[a,b])
        rec.move(helper,());rec.erase(helper)
        for i in (a,b):rec.move(regs[f'X{i}'],regs[f'X{i}'].home)
    assert all(regs[f'X{i}'].data=={i:1} and regs[f'X{i}'].frame==regs[f'X{i}'].home for i in range(8))
    assert all(regs[f'H{a}_{b}'].data=={} and regs[f'H{a}_{b}'].frame==() for a,b in selected)
    expected=(1496,292) if bank==1909 else (2224,416)
    assert (rec.rank_mass,rec.adds)==expected,(rec.rank_mass,rec.adds,expected)
    # independently rescan event trace for the exact rank profile
    check=Counter(x[4] for x in rec.event if x[0]=='transport')
    assert check==rec.profile
    assert sum(k*v for k,v in check.items())==rec.rank_mass
    assert sum(1 for x in rec.event if x[0]=='add')==rec.adds
    assert rec.initialized==(8 if bank else 0)
    return dict(schema='p104-mixed-native-chart-emitter/1',scope='exact actual E8 9-bit charts; raw finite Clifford transport words; NOT priced rank-difference-child supplier',
        source_root_ids=roots,second_frame=F1,live=live,bank=bank,edges=selected,major_signs={f'{a},{b}':majors[a,b] for a,b in selected},
        basis_root_indices=[E8.NROW.index(b) for b in BASIS],
        frames=[list(f) for f in rec.frame_by_id],transports=[{'old':a,'new':b,'gates':gs} for (a,b),gs in sorted(rec.transports.items())],events=rec.event,
        counts=dict(outputs=len(output),roots=120,rank_mass=rec.rank_mass,addition_events=rec.adds,helpers_zero_initialized=rec.initialized,
            helpers_zero_erased=rec.initialized,native_chart_count=len(rec.frame_by_id),unique_native_transports=len(rec.transports),rank_child_histogram=dict(sorted(rec.profile.items())),
            raw_C_gate_occurrences=rec.raw_children,naive_clifford_overhead=rec.raw_children-rec.rank_mass),
        flags={'actual_E8_labels':True,'signed_104_outputs_exact':True,'output_dirty_preserved':True,'helpers_end_zero':True,
               'full_arbitrary_dirty_helper_compatibility':False,'native_rank_optimal_recipe':False,'paid_full_recursive_profile':False,
               'uniform_all_size_supplier':False,'new_kappa':False})

if __name__=='__main__':
    path=HERE/'evidence'/'NATIVE_CHART_WORD.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    result=build();path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS_E8_NATIVE_CHART_EMITTER outputs=%d rank_mass=%d ADD=%d zero_ancillas=%d literal_C=%d distinct_frames=%d distinct_transports=%d native_rank_cost_UNOPTIMIZED all_size_OPEN'%(result['counts']['outputs'],result['counts']['rank_mass'],result['counts']['addition_events'],result['counts']['helpers_zero_initialized'],result['counts']['raw_C_gate_occurrences'],result['counts']['native_chart_count'],result['counts']['unique_native_transports']))

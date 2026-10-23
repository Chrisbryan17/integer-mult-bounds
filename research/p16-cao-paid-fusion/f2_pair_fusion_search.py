#!/usr/bin/env python3
"""Cao P16: enumerate physically source-compatible F2,F2 -> F1,F3 contact rewrites.

Searches BOTH scalar-role neighbors and their GF(2) common-frame obligations.
A favorable local shape is a *screen* only. Rebuilds and proves both complete
632-column words for any globally favorable candidate. No hidden free moves.
"""
from collections import Counter
from copy import deepcopy
from decimal import Decimal, localcontext
from pathlib import Path
import gzip,json,sys
HERE=Path(__file__).resolve().parent
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE.parents[2]
sys.path.insert(0,str(ROOT/'research/warp-interface-20261022'))
import warp_merge as W
F=W.F
def read(path):return json.loads(gzip.decompress(path.read_bytes()))
def roles(e):
    if e[0]=='scalar':
        g=e[1];items=g[1:3] if g[0] in ('add','copy') else g[1:2]
        return tuple(dict.fromkeys(x[1] for x in items if x[0]=='L'))
    if e[0]=='warp':return (e[1][1],)
    return ()
def run():
    word=read(ROOT/'research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz')
    c=word['canonical'];orig=word['programs']
    raw={d:[deepcopy(e) for e in p if e[0]!='climb'] for d,p in orig.items()}
    a,b=raw['forward'],raw['backward']
    assert len(a)==len(b)
    direction_frame_mismatches=sum(
        u[0]!='scalar' or v[0]!='scalar' or u[2]!=v[2]
        for u,v in zip(a,b) if u[0]=='scalar' or v[0]=='scalar')
    # Native dual words need not share every old contact frame. Never
    # assume they do; only replay a candidate against both orientations.
    frames=c['frames'];spans=[frozenset(F.span(v)) for v in frames]
    dim=[len(s).bit_length()-1 for s in spans]
    before={};after={}
    state=c['start'][:]
    for i,e in enumerate(a):
        for r in roles(e):
            before[i,r]=state[r]
            if e[0]=='scalar':state[r]=e[2]
            else:state[r]=e[4]
    state=c['final'][:]
    for i in range(len(a)-1,-1,-1):
        e=a[i]
        for r in roles(e):
            after[i,r]=state[r]
            if e[0]=='scalar':state[r]=e[2]
            else:state[r]=e[3]
    with localcontext() as ctx:
        ctx.prec=48
        power=Decimal(1)-Decimal('0.0030217758')
        weight={i:Decimal(i)**power for i in range(10)}
        weight[0]=Decimal(0)
    checks=Counter();candidates=[]
    for i,e in enumerate(a):
        if e[0]!='scalar':continue
        rr=roles(e)
        if not rr:continue
        old=e[2]
        if not any(dim[old]-dim[before[i,r]]==2 and
                   dim[after[i,r]]-dim[old]==2 for r in rr):continue
        checks['F2_F2_role_contact']+=1
        pre=[spans[before[i,r]] for r in rr];post=[spans[after[i,r]] for r in rr]
        lo=set(pre[0])
        for x in pre[1:]:
            # exact union-span closure over GF(2)
            lo={u^v for u in lo for v in x}
        hi=set(post[0])
        for x in post[1:]:hi.intersection_update(x)
        if not lo<=hi or len(lo)>len(spans[old]):continue
        checks['valid_joint_interval']+=1
        oldcost=sum(weight[dim[old]-dim[before[i,r]]]+
                    weight[dim[after[i,r]]-dim[old]] for r in rr)
        seen=set()
        for v in sorted(hi-lo):
            alt=frozenset(set(lo)|{x^v for x in lo})
            if alt in seen or not alt<=hi:continue
            seen.add(alt)
            k=alt.bit_length() if False else len(alt).bit_length()-1
            if k!=dim[old]-1:continue
            checks['GF2_rank1_eligible']+=1
            newcost=sum(weight[k-dim[before[i,r]]]+
                        weight[dim[after[i,r]]-k] for r in rr)
            gain=oldcost-newcost
            if gain<=0:continue
            checks['positive_local_candidates']+=1
            candidates.append((gain,i,alt,rr))
    candidates.sort(key=lambda x:-x[0])
    report={'schema':'cao-p16-f2-pair-common-frame-search/1',
       'status':'PASS_SOURCE_EXACT_GF2_CONSTRAINT_SCREEN',
       'source':'20bb93cd990d2ff683e4d0fc56b87a42cd5d3296',
       'native_SHA':json.loads((ROOT/'research/kappa-round3-warp-20261022/ACTUAL-WORD-FREEZE.json').read_text())['canonical_payload_sha256'],
       'f2_f2_pure_rank_screen':dict(checks),
       'nonidentical_oriented_scalar_contact_labels':direction_frame_mismatches,
       'admitted_improvement':False,'claimed_new_kappa':False,'top':[]}
    # Candidate acceptance demands a full compile, both directions, and
    # actual moment improvement in the recompiled paid histogram.
    Fneed=F.need
    X=F.load(ROOT/'research/kappa-rebuild/complex/native_extensions.py','fusion_exact_literal')
    V=F.load(ROOT/'research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py','fusion_exact_rows')
    base_paid=Counter(e[-1] for e in orig['forward'] if e[0] in ('climb','center'))
    tested=0
    for gain,i,span,rr in candidates[:30]:
        trial=deepcopy(c)
        # independent GF2 basis of the requested span
        basis=[];generated={0}
        for v in sorted(span):
            if v not in generated:
                basis.append(v);generated|={x^v for x in tuple(generated)}
        assert len(generated)==len(span)
        lab=len(trial['frames']);trial['frames'].append(basis)
        modified={}
        try:
            for d in ('forward','backward'):
                rawcopy=deepcopy(raw[d]);assert rawcopy[i][0]=='scalar'
                rawcopy[i][2]=lab
                modified[d]=W.synthesize(trial,rawcopy)
            paid={d:Counter(e[-1] for e in modified[d] if e[0] in ('climb','center'))
                  for d in modified}
            assert paid['forward']==paid['backward']
            with localcontext() as ctx:
                ctx.prec=50;tt=Decimal(1)-Decimal('0.0030217758')
                fullgain=sum(Decimal(k)**tt*(base_paid[k]-paid['forward'][k])
                             for k in set(base_paid)|set(paid['forward']))
            record={'raw_index':i,'roles':rr,'local_gain':str(gain),
                    'actual_paid_gain':str(fullgain),
                    'changed_profile':dict(sorted(paid['forward'].items()))}
            if fullgain>0:
                for d in modified:
                    rows,receipt=X.literal_replay(V,trial,modified[d],d=='backward')
                    assert all(rows['L',r]==V.expected(('L',r),[],d=='backward',False)
                               for r in range(632))
                record['dual_632_columns']='PASS'
                # Phase and whole controller remain distinct proof obligations.
                report['status']='DUAL_LITERAL_SCREEN_POSITIVE_PHASE_UNPROVED'
                report['top'].append(record)
            elif len(report['top'])<12:report['top'].append(record)
            tested+=1
        except (AssertionError,ValueError) as ex:
            if len(report['top'])<12:report['top'].append({'raw_index':i,'rejected':str(ex)})
    report['attempted_compilations']=tested
    (HERE/'FUSION_GF2_RECEIPT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(report['status'],dict(checks),'candidate_compiles',tested)
    print('TENTATIVE_FIRST',report['top'][:2])
if __name__=='__main__':run()

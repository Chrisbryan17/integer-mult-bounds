#!/usr/bin/env python3
"""Rebuild Cao #4610's 155 coupled sibling obstructions and 108 GL9 bridges.
A bridge is algebraic potential transport, NOT a physically admitted fusion.
"""
import argparse,gzip,hashlib,json,re,sys
from pathlib import Path
from collections import Counter,defaultdict
PIN='cfcd36b40326d7a5815e1db5313444379b3fb756b27d5201c561574c085cc0dd'

def extend(basis):
    out=[];span={0}
    for v in list(basis)+[1<<i for i in range(9)]:
        if v not in span:
            out.append(v);span|={x^v for x in tuple(span)}
    assert len(out)==9 and len(span)==512
    return out

def linear(cols,x):
    out=0
    for i,c in enumerate(cols):
        if x>>i&1:out^=c
    return out

def bridge(source,target):
    xs=extend(source);ys=extend(target)
    table={0:0}
    for u,v in zip(xs,ys):
        table.update({a^u:b^v for a,b in tuple(table.items())})
    assert len(table)==len(set(table.values()))==512
    cols=[table[1<<i] for i in range(9)]
    inv=[0]*512
    for x,y in table.items():inv[y]=x
    inverse=[inv[1<<i] for i in range(9)]
    assert all(linear(inverse,linear(cols,x))==x for x in range(512))
    return cols,inverse

def run(root):
    frozen=root/'research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz'
    blob=gzip.decompress(frozen.read_bytes())
    assert hashlib.sha256(blob).hexdigest()==PIN
    sys.path.insert(0,str(root/'research/warp-interface-20261022'))
    from warp_merge import synthesize,roles
    word=json.loads(blob);c=word['canonical'];rows=[]
    counts=Counter()
    for direction,program in word['programs'].items():
        raw=[e for e in program if e[0]!='climb']
        ix={};n=-1;byrole=defaultdict(list)
        for i,e in enumerate(program):
            if e[0]!='climb':
                n+=1;ix[i]=n
            elif e[5]==1:byrole[e[2]].append((i,e))
        candidates=[]
        for role,links in byrole.items():
            for (left,a),(right,b) in zip(links,links[1:]):
                if not 2<=right-left<=6 or a[4]!=b[3]:continue
                mids=program[left+1:right]
                if any(e[0]!='scalar' for e in mids):continue
                if not any(role in roles(e) for e in mids):continue
                candidates.append((left,right,role,b[4]))
        assert len(candidates)==(43 if direction=='forward' else 112)
        for left,right,role,target in candidates:
            changed=raw[:]
            for j in range(left+1,right):
                z=raw[ix[j]][:];z[2]=target;changed[ix[j]]=z
            try:
                synthesize(c,changed)
            except (ValueError,AssertionError) as exc:
                pattern=r'role=(\d+) old=(\d+) new=(\d+) dimensions=(\d+),(\d+)'
                match=re.search(pattern,str(exc))
                if match is None:raise
                blocker,old,new,da,db=map(int,match.groups())
                assert blocker!=role and da>=db
                row=dict(direction=direction,source_event_range=[left,right],primary_role=role,
                         sibling_role=blocker,old_frame=old,required_frame=new,
                         source_dim=da,target_dim=db)
                if da>db:
                    row['result']='RANK_DROP_NOT_INVERTIBLE';counts['rank_drop']+=1
                else:
                    assert c['frames'][old]!=c['frames'][new]
                    cols,inv=bridge(c['frames'][old],c['frames'][new])
                    def span(basis):
                        v={0}
                        for x in basis:v|={t^x for t in tuple(v)}
                        return v
                    assert {linear(cols,x) for x in span(c['frames'][old])}==span(c['frames'][new])
                    row.update(result='ALGEBRAIC_GL9_BRIDGE_ONLY',G_columns=cols,
                               G_inverse_columns=inv,physical_admission=False)
                    counts['bridge']+=1
                rows.append(row)
            else:raise AssertionError('Expected scoped forbidden same-register retime')
    assert counts==Counter({'bridge':108,'rank_drop':47}),counts
    return dict(status='PASS_CAO_P16_155_EXACT_COUPLED_FRAME_REPAIRS',
                source_sha256=PIN,source_commit='20bb93cd990d2ff683e4d0fc56b87a42cd5d3296',
                counts=dict(counts),bridges=rows,full_native_dual_replay_of_new_word=False,
                physical_fusion_admitted=False,new_kappa_proved=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();v=run(a.source);a.output.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
    print(v['status'],v['counts'])

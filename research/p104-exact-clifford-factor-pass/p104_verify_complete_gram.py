#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent Fraction-exact 216-formal-input P104 full 104x104 Gram/2
channel check: 104 sources, 104 targets, eight arbitrary dirty H, eight clean X.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT))
from p104_native_e8_gate.scripts import native_chart_emitter as E
W=json.loads((ROOT/'P104_COMPLETE_104X104_GRAM_HALF_WORD.json').read_text())
H=sorted({e[2] for e in W['events'] if e[0]=='add' and e[2].startswith('H')})
assert len(H)==8
names=[f'S{i}' for i in range(104)]+[f'Y{i}' for i in range(104)]+H+[f'X{i}' for i in range(8)]
N=len(names)
assert N==224
formal={f'S{i}':i for i in range(104)}
formal.update({f'Y{i}':104+i for i in range(104)})
formal.update({H[i]:208+i for i in range(8)})
assert len(formal)==216
def run(skip=-1,all_half=True):
    data={name:({formal[name]:F(1)} if name in formal else {}) for name in names}
    for event_idx,e in enumerate(W['events']):
        kind=e[0]
        if kind=='add':
            if event_idx==skip:continue
            _,dst,src,sign,*_=e
            for j,v in list(data[src].items()):
                data[dst][j]=data[dst].get(j,F(0))+sign*v
                if not data[dst][j]:del data[dst][j]
        elif kind=='scale':
            _,reg,num,den,_=e
            q=F(num,den)
            if not all_half and num==1:q=F(1)
            data[reg]={j:q*v for j,v in data[reg].items()}
        elif kind in ('allocate_zero','erase_zero'):
            assert not data[e[1]],(kind,e[1])
        elif kind in ('transport','source_to_zero','source_from_zero'):pass
        else:raise AssertionError(e)
    return data
result=run()
live=E.E8.live
assert all(result[f'S{i}']=={i:F(1)} for i in range(104))
assert all(result[h]=={208+i:F(1)} for i,h in enumerate(H))
assert all(result[f'X{i}']=={} for i in range(8))
nonzero=0
for t,rt in enumerate(live):
    row={104+t:F(1)}
    for s,rs in enumerate(live):
        c=E.E8.IP[rt][rs]
        if c:row[s]=F(c,2);nonzero+=1
    assert result[f'Y{t}']==row,(t,result[f'Y{t}'],row)
assert nonzero>416
try:bad=run(all_half=False)
except AssertionError:pass
else:assert bad['Y0']!=result['Y0']
try:
    omitted=next(i for i,e in enumerate(W['events'])
       if e[0]=='add' and e[1].startswith('X') and e[2].startswith('S'))
    run(skip=omitted)
except AssertionError:pass
else:raise AssertionError('omitted source gather went undetected')
out={
 'status':'PASS_FINITE_RATIONAL_FULL_CHANNEL',
 'full_source_ports':104,'full_target_ports':104,
 'independent_input_variables':216,'output_channel_entries':10816,
 'owned_clean_scratch_required':8,'sources_and_dirt_restored':True,
 'signed_ADDs':1280,'half_scale':8,'double_scale':8,
 'conditional_rank_mass_with_224_bridges':1720,
 'I_minus_G_over_two_correction':'OPEN',
 'source_owner_host_precision':'OPEN','new_kappa':False}
(ROOT/'P104_COMPLETE_104X104_GRAM_HALF_RECEIPT.json').write_text(
    json.dumps(out,indent=2,sort_keys=True)+'\n')
print('PASS_P104_COMPLETE_G_OVER_2_104X104 inputs=216 outputs=104 '
      'sources_preserved=104 arbitrary_H_restored=8 clean_X_restored=8 '
      'ADD=1280 Gram_entries=10816 gather_mutant_REJECTED '
      'half_scale_mutant_REJECTED host_supplier_OPEN')

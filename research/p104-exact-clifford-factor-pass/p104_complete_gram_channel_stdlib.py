#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Full 104x104 E8 Gram/2 finite gather-mix-ungather word.
Exact Fraction Gauss-Jordan, no hidden source or private scratch.
Supplier source ownership, half-scalers, physical hosting and I-G/2 OPEN.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,sys
P=Path(__file__).parent
sys.path.insert(0,str(P))
from p104_native_e8_gate.scripts import native_chart_emitter as E
old=json.loads((P/'P104_BORROWED_DIRTY_WORD.json').read_text())
assert old['source_pin']=='a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39'
L=E.E8.live
R=[pair[0] for pair in E.E8.chosen[1]]
C=[[E.E8.IP[t][r] for r in R] for t in L]
K=[[E.E8.IP[r][s] for s in R] for r in R]
def inverse_exact(A):
    n=len(A)
    aug=[[Q(z) for z in A[i]]+[Q(i==j) for j in range(n)] for i in range(n)]
    det=Q(1)
    for j in range(n):
        row=next(k for k in range(j,n) if aug[k][j])
        if row!=j:aug[j],aug[row]=aug[row],aug[j];det=-det
        pivot=aug[j][j];det*=pivot
        aug[j]=[z/pivot for z in aug[j]]
        for k in range(n):
            if k!=j:
                factor=aug[k][j]
                aug[k]=[x-factor*y for x,y in zip(aug[k],aug[j])]
    assert all(aug[i][j]==int(i==j) for i in range(n) for j in range(n))
    return [[aug[i][n+j] for j in range(n)] for i in range(n)],det
Ki,det=inverse_exact(K)
assert det==1
B=[[sum(Ki[i][j]*C[t][j] for j in range(8)) for t in range(104)] for i in range(8)]
assert all(z in (-1,0,1) for row in B for z in row)
assert sum(bool(z) for row in B for z in row)==416
assert all(sum(C[t][i]*B[i][s] for i in range(8))==E.E8.IP[L[t]][L[s]]
           for t in range(104) for s in range(104))
gather=[['add',f'X{i}',f'S{s}',int(B[i][s]),0] for s in range(104)
        for i in range(8) if B[i][s]]
ungather=[['add',e[1],e[2],-e[3],0] for e in reversed(gather)]
frames=old['frames'];empty=frames.index([])
line={}
for i in range(8):
    visits=[e for e in old['events'] if e[0]=='transport' and e[1]==f'X{i}']
    assert visits and frames[visits[0][2]]==frames[visits[-1][3]]
    assert len(frames[visits[0][2]])==1
    line[i]=visits[0][2]
pre=old['events'][:156];post=old['events'][156:]
assert all(e[0]=='add' for e in pre)
word=(pre
      +[['source_to_zero',f'S{s}',L[s],1] for s in range(104)]
      +[['allocate_zero',f'X{i}'] for i in range(8)]
      +gather
      +[['transport',f'X{i}',empty,line[i],1] for i in range(8)]
      +[['scale',f'X{i}',1,2,line[i]] for i in range(8)]
      +post
      +[['scale',f'X{i}',2,1,line[i]] for i in range(8)]
      +[['transport',f'X{i}',line[i],empty,1] for i in range(8)]
      +ungather
      +[['erase_zero',f'X{i}'] for i in range(8)]
      +[['source_from_zero',f'S{s}',L[s],1] for s in range(104)])
assert sum(e[0]=='add' for e in word)==1280
assert sum(e[0]=='scale' for e in word)==16
assert sum(e[0]=='transport' for e in word)==772
assert sum(e[0] in ('source_to_zero','source_from_zero') for e in word)==208
out={
 'schema':'p104-full-104x104-gram-half-finite/1',
 'source_word_sha256':old['source_pin'],'K_det':int(det),
 'K':K,'B_gather_coefficients':[[int(z) for z in row] for row in B],
 'source_ports':104,'target_ports':104,'gather_signed_ADD':416,
 'decoder_signed_ADD':448,'ungather_signed_ADD':416,
 'total_signed_ADD':1280,'rational_source_halves':8,'source_restoring_doubles':8,
 'new_owned_clean_X_scratch':8,'original_arbitrary_dirty_H_restored':8,
 'original_transport_occurrences':756,'new_X_line_zero_chart_transports':16,
 'new_104_source_line_zero_line_transports':208,
 'conditional_native_rank_mass_if_admitted':1720,
 'owner_host_source_precision':'OPEN','complete_I_minus_G_over_two_side':'OPEN',
 'integer_scaler_native_legality':'OPEN','new_kappa':False,'events':word}
(P/'P104_COMPLETE_104X104_GRAM_HALF_WORD.json').write_text(
    json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
print('PASS_P104_FULL_GRAM_INTEGER_FACTOR 104x104 C104x8 B8x104 detK=1 '
      'B_signed_nonzeros=416 ADD=1280 scaling=16 clean_X=8 '
      'conditional_native_rank=1720 no_new_kappa')

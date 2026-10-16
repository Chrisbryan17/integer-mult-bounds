#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Eliminate local 1/2 scalers with an explicit DYADIC TARGET encoding.
The native integer program computes Ynum <- Ynum + G*S, which represents
Y <- Y + (G/2)*S when the target type is (numerator, denominator=2).
The caller must propagate this typed encoding; NOT a free interface change.
"""
from pathlib import Path
import json,collections
P=Path(__file__).resolve().parent
W=json.loads((P/'P104_INPLACE_SOURCE_WORD.json').read_text())
assert W['new_clean_aggregate_registers']==0 and W['signed_ADD']==1298
assert sum(e[0]=='scale' for e in W['events'])==16
assert all(e[1].startswith('S') for e in W['events'] if e[0]=='scale')
events=[e for e in W['events'] if e[0]!='scale']
cnt=collections.Counter(e[0] for e in events)
assert cnt['add']==1298 and cnt['sign']==12 and cnt['scale']==0
assert cnt['transport']==772
assert cnt['source_to_zero']==cnt['source_from_zero']==104
out={'schema':'p104-inplace-dyadic-target-type/1',
 'source_word_sha256':W['source_word_sha256'],
 'target_type':'dyadic(numerator, denominator=2)',
 'numerator_action':'Ynum_out=Ynum_in+G*S',
 'decoded_semantics':'Yout=Yin+(G/2)*S',
 'input_104_target_encoding':'caller must provide numerator for denominator 2',
 'output_104_target_encoding':'caller must accept/propagate numerator and denominator 2',
 'source_type':'integer-valued',
 'signed_ADD':1298,'signed_NEG':12,'fractional_scale_operations':0,
 'new_clean_aggregate_registers':0,'borrowed_dirty_helpers':8,
 'core_positive_native_children':756,'physical_source_positive_children':208,
 'eight_pivot_charts_in_out':16,'conditional_positive_native_children':980,
 'conditional_rank_mass':1720,
 'full_caller_type_composition':'OPEN','precision_bit_tape':'OPEN',
 'global_source_and_early_Y_owners':'OPEN','side_I_minus_G_over_2':'OPEN',
 'new_kappa':False,'events':events}
(P/'P104_INPLACE_DYADIC_WORD.json').write_text(
 json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
print('PASS_P104_TYPED_DYADIC_NO_FRACTIONAL_PRIMITIVE ADD=1298 SIGN=12'
      ' fractional_native=0 clean_X=0 conditional_child_mass=1720 caller_OPEN')

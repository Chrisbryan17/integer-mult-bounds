#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Cold integration tests for exact W2, coupled Laurent, stage batching.
No claimed improved kappa or physically admitted new primitive.
"""
from pathlib import Path
import json,subprocess,sys,unittest
P=Path(__file__).resolve().parent
class P16Batching(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  for script in ('p16_coupled_query_miter.py','p16_w2_query_rank_gate.py',
                 'p16_tail_idle_virtual.py','p16_stage_major_batch.py',
                 'p16_w2_realpair_clifford.py'):
   p=subprocess.run([sys.executable,'-I','-B',str(P/script)],
                    capture_output=True,text=True,timeout=90)
   if p.returncode:raise AssertionError((script,p.stdout,p.stderr))
 def doc(self,name):
  return json.loads((P/name).read_text())
 def test_full_32_and_64_exact(self):
  r=self.doc('COUPLED_QUERY_FULL_MITER.json')
  self.assertEqual((r['W1_full_entries'],r['W2_full_entries']),(1024,4096))
  self.assertFalse(r['physical_native_coupled_query_admitted'])
 def test_query_rank_no_go(self):
  r=self.doc('W2_RANK_QUERY_NO_GO.json')
  self.assertEqual((r['W2_exact_q_update_rank'],r['minimum_W2_rank1_queries_under_q_free_GL8']),(2,2))
 def test_tail_idle_price(self):
  r=self.doc('TAIL_IDLE_FULL_MITER.json')
  self.assertEqual((r['original_shared_IDLE_rank_mass_per_port'],
                    r['independent_terminal_mask_rank_mass_proxy_per_port']),(352,704))
 def test_stage_batch_det(self):
  r=self.doc('P16_STAGE_MAJOR_BATCH_RECEIPT.json')['batch_screens']['2']
  self.assertEqual((r['formal_batch_count'],r['unpaid_determinant_degree']),(24,40))
  self.assertFalse(r['real_physical_batch_child_admitted'])
 def test_realpair_exact_and_complex_obstruction(self):
  r=self.doc('P16_REALPAIR_CLIFFORD_RECEIPT.json')
  self.assertEqual((r['total_exact_basis_columns'],r['total_random_pairs']),(9216,576))
  self.assertTrue(r['cannot_replace_two_arbitrary_complex_inputs'])
if __name__=='__main__':unittest.main()

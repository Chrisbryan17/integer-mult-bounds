#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Strict standalone acceptance: native chart emitter plus checks, no theorem promotion."""
import subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
for name in ('native_chart_emitter.py','verify_native_chart_word.py','verify_phase_exact.py','native_invoice.py'):
 subprocess.run([sys.executable,'-I','-B',str(P/name)],check=True)
print('PASS_P104_NATIVE_CHART_GATE physical_chart_words=EMITTED_&_PHASE_TESTED clean_ancilla=REQUIRED paid_native_rank_optimal=UNPROVEN full_algorithm=OPEN')

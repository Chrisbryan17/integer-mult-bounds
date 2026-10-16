#!/usr/bin/env python3
"""Reproduce the in-tree signed edge and bank certificates (standard library)."""
import hashlib, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
source=ROOT/'research/complex-frame-pair-decoders/verify.py'
data=source.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
assert blob=='57dd8993e8ac016e8a92a9a885392b58014137bb',('source changed',blob)
for name in ('signed_edge_census.py','single_sign_optimum.py','pareto.py'):
    subprocess.run([sys.executable,'-I','-B',str(HERE/name)],cwd=ROOT,check=True)
print('PASS_P104_SINGLE_SIGN_IN_TREE source_pinned=YES decoder_census=YES bank=YES pareto=YES no_native_supplier no_new_kappa')

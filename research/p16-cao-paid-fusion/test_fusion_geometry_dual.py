#!/usr/bin/env python3
"""Positive and adversarial tests for frozen Cao exact 671-window fusion census."""
from pathlib import Path
from tempfile import TemporaryDirectory
from importlib.util import spec_from_file_location,module_from_spec
import argparse,gzip,json,shutil

HERE=Path(__file__).resolve().parent
spec=spec_from_file_location("fusion_geometry_dual",HERE/"fusion_geometry_dual.py")
module=module_from_spec(spec)
spec.loader.exec_module(module)

FILES=["research/kappa-round3-warp-20261022/ACTUAL-WORD-FREEZE.json",
"research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz",
"research/kappa-round6-compiler-tightening-20261022/ARITHMETIC.json"]

def rejects(f):
    try: f()
    except (AssertionError,ValueError,KeyError,OSError,EOFError):return True
    return False

def main(root):
    good=module.run(root)
    assert good["status"]=="PASS_SOURCE_EXACT_FUSION_GEOMETRY_ONLY"
    assert good["dual_pair_correspondence"]
    assert good["orientations"]["forward"]["distinct_source_hyperplanes"]==670
    assert good["orientations"]["backward"]["equal_source_hyperplanes"]==1
    assert not good["physical_fusion_admitted"] and not good["new_kappa_proved"]
    with TemporaryDirectory() as tmp:
        p=Path(tmp)
        for sub in FILES:
            dst=p/sub
            dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(root/sub,dst)
        assert module.run(p)["dual_pair_correspondence"]
        gz=p/FILES[1]
        b=gz.read_bytes()
        gz.write_bytes(b[:1]+bytes([b[1]^1])+b[2:])
        assert rejects(lambda:module.run(p)), "Corrupted frozen witness was accepted"
        gz.write_bytes(b)
        inv=p/FILES[2]
        data=json.loads(inv.read_text())
        data["paid"]["1"]+=1
        inv.write_text(json.dumps(data))
        assert rejects(lambda:module.run(p)), "Invalid full invoice was accepted"
    print("PASS_FUSION_GEOMETRY_TESTS source, dual constraints, two rejecting mutations")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,required=True)
    main(parser.parse_args().source)

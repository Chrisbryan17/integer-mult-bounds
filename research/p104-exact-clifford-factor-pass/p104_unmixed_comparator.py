#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Same-native-compiler unmixed comparator, 525 exact full-column checks.

This comparator is restricted to the identical fixed home-return chart model.
It is NOT the best already admitted recursive P104 supplier.
"""
import collections, json, sys, time
from pathlib import Path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
import p104_exact_native_factor as F
import p104_verify_all_columns as M
import native_chart_emitter as E

def run():
    W = E.build(bank=0)
    occurrences = collections.Counter(
        (e[2], e[3]) for e in W["events"] if e[0] == "transport")
    counts = collections.Counter()
    start = time.monotonic()
    for i, t in enumerate(W["transports"]):
        old = [tuple(g) for g in t["gates"]]
        new, rank, correction = F.factor_and_correct(old)
        assert M.same(old, new), ("full-column mismatch", i)
        n = occurrences[t["old"], t["new"]]
        counts["distinct_recipes"] += 1
        counts["transport_occurrences"] += n
        counts["frame_rank_mass"] += rank * n
        counts["old_C"] += sum(g[0] == "C" for g in old) * n
        counts["new_C"] += sum(g[0] == "C" for g in new) * n
        counts["affine_coset_occurrences"] += n * bool(correction["u"])
        for gate in new:
            counts["native_" + gate[0]] += n
    assert (
        counts["distinct_recipes"],
        counts["transport_occurrences"],
        counts["frame_rank_mass"],
        counts["old_C"],
        counts["new_C"],
        counts["affine_coset_occurrences"]
    ) == (525, 1144, 2224, 5696, 2560, 168)
    record = {
        "schema": "p104-same-compiler-restricted-unmixed/1",
        "scope": "home-return chart only, not a selected recursive supplier",
        "exact_full_512_columns": True,
        "counts": dict(counts),
        "mixed_new_C": 1832,
        "new_kappa": False,
        "all_size_theorem": "OPEN"
    }
    (ROOT / "P104_UNMIXED_COMPILER_COMPARATOR.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n")
    print("PASS_P104_UNMIXED_EXACT_NATIVE_COMPARATOR C_before=5696 "
          "C_after=2560 mixed_C=1832 full_columns=512 recipes=525 elapsed=%.2f" %
          (time.monotonic() - start))

if __name__ == "__main__":
    run()

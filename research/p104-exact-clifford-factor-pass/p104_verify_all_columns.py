#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent all-512-column exact Gaussian integer / global-phase verifier.

NumPy int64 is used only for vectorization. Every matrix entry is compared
exactly as an integer after clearing powers-of-two from native C factors.
"""
from pathlib import Path
import hashlib, json, time, collections
import numpy as np
ROOT = Path(__file__).parent
M = 512
bits = np.array([(x >> j) & 1 for x in range(M) for j in range(9)],
                dtype=np.int8).reshape(M, 9)
indices = np.arange(M, dtype=np.int64)
cache = {}

def permutation(rows):
    key = ("P", tuple(rows))
    if key not in cache:
        x = np.zeros(M, dtype=np.int64)
        for i in range(9):
            v = sum((bits[:, j] for j in range(9)
                     if (rows[i] >> j) & 1),
                    start=np.zeros(M, dtype=np.int64)) % 2
            x |= v << i
        cache[key] = x
    return cache[key]

def diagonal(Q, alpha):
    key = ("D", tuple(Q), tuple(alpha))
    if key not in cache:
        phase = np.zeros(M, dtype=np.int64)
        for i in range(9):
            phase += int(alpha[i]) * bits[:, i]
            for j in range(i + 1, 9):
                if (Q[i] >> j) & 1:
                    phase += 2 * bits[:, i] * bits[:, j]
        cache[key] = np.asarray(phase % 4, dtype=np.uint8)
    return cache[key]

def exact(gates):
    R = np.eye(M, dtype=np.int64)
    I = np.zeros((M, M), dtype=np.int64)
    level = 0
    for g in gates:
        if g[0] == "P":
            ix = permutation(g[1])
            rr, ii = np.empty_like(R), np.empty_like(I)
            rr[ix], ii[ix] = R, I
            R, I = rr, ii
        elif g[0] == "D":
            phase = diagonal(g[1], g[2])
            rr, ii = R.copy(), I.copy()
            for p in (1, 2, 3):
                m = phase == p
                if p == 1:
                    rr[m], ii[m] = -I[m], R[m]
                elif p == 2:
                    rr[m], ii[m] = -R[m], -I[m]
                else:
                    rr[m], ii[m] = I[m], -R[m]
            R, I = rr, ii
        elif g[0] == "C":
            q, sign = g[1:]
            assert 0 < q < M and sign in (-1, +1)
            ix = indices ^ q
            if sign == +1:
                rr = R - I + R[ix] + I[ix]
                ii = R + I - R[ix] + I[ix]
            else:
                rr = R + I + R[ix] - I[ix]
                ii = I - R + R[ix] + I[ix]
            R, I = rr, ii
            level += 1
        elif g[0] == "PH":
            p = g[1] % 4
            if p == 1:
                R, I = -I, R
            elif p == 2:
                R, I = -R, -I
            elif p == 3:
                R, I = I, -R
        else:
            raise ValueError(g)
    return R, I, level

def same(a, b):
    Ra, Ia, ka = exact(a)
    Rb, Ib, kb = exact(b)
    return (np.array_equal(Ra << kb, Rb << ka) and
            np.array_equal(Ia << kb, Ib << ka))

def main():
    source = ROOT / "p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json"
    candidate_path = ROOT / "P104_MINIMAL_C_CANDIDATES.json"
    original = json.loads(source.read_text())
    candidate = json.loads(candidate_path.read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == candidate["source_word_sha256"]
    old = {(t["old"], t["new"]): t["gates"] for t in original["transports"]}
    assert len(old) == len(candidate["transports"]) == 514
    start = time.monotonic()
    checked = 0
    for t in candidate["transports"]:
        assert same(old[t["old"], t["new"]], t["gates"]), (
            "phase or full-matrix mismatch", t["old"], t["new"])
        checked += 1
    first = candidate["transports"][0]
    mutated = [list(g) for g in first["gates"]] + [["PH", 1]]
    assert not same(old[first["old"], first["new"]], mutated)
    first = next(t for t in candidate["transports"]
                 if any(g[0] == "C" for g in t["gates"]))
    mutated = [list(g) for g in first["gates"]]
    j = next(i for i, g in enumerate(mutated) if g[0] == "C")
    mutated[j][2] *= -1
    assert not same(old[first["old"], first["new"]], mutated)
    occurrences = collections.Counter(
        (e[2], e[3]) for e in original["events"] if e[0] == "transport")
    assert len(occurrences) == 514
    assert sum(t["occurrences"] for t in candidate["transports"]) == 756
    assert sum(occurrences[t["old"], t["new"]] * t["new_C"]
               for t in candidate["transports"]) == 1832
    evidence = {
        "schema": "p104-exact-512-column-verification/1",
        "status": "PASS",
        "transport_recipes": checked,
        "columns_per_recipe": M,
        "matrix_entries_per_recipe": M * M,
        "old_C_occurrences": 4160,
        "new_C_occurrences": 1832,
        "global_phase_mutation": "REJECTED",
        "signed_C_mutation": "REJECTED",
        "source_sha256": candidate["source_word_sha256"],
        "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "full_recursive_invoice": "OPEN",
        "full_all_size_theorem": "OPEN",
        "kappa": "UNCHANGED"
    }
    (ROOT / "P104_512_COLUMN_VERIFICATION.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print("PASS_P104_512_COLUMN_PHASE_EXACT recipes=514 columns=512 "
          "transport_occurrences=756 C_before=4160 C_after=1832 "
          "global_phase_REJECTED C_sign_REJECTED elapsed=%.2f" %
          (time.monotonic() - start))

if __name__ == "__main__":
    main()

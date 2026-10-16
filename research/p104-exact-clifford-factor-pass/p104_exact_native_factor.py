#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact-phase P104 Clifford factorization. Not a priced recursive supplier."""
from pathlib import Path
import sys, json, collections, time
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from p104_minimal_symplectic import factor, symp, dot
sys.path.insert(0, str(ROOT / "p104_native_e8_gate/scripts"))
import verify_phase_exact as V

def rotate(c, p):
    a, b = c
    return [(a, b), (-b, a), (-a, -b), (b, -a)][p % 4]

def vec(g, s):
    out, level = V.phase(g, s)
    return {j: v for j, v in enumerate(out) if v != (0, 0)}, level

def solve(equations):
    pivots = {}
    for mask, rhs in equations:
        while mask:
            j = mask.bit_length() - 1
            if j not in pivots:
                pivots[j] = (mask, rhs)
                break
            m, b = pivots[j]
            mask ^= m
            rhs ^= b
        if not mask and rhs:
            return None
    value = 0
    for j in sorted(pivots):
        mask, rhs = pivots[j]
        value |= (rhs ^ dot(mask & ((1 << j) - 1), value)) << j
    assert all(dot(x, value) == y for x, y in equations)
    return value

def correction(original, candidate):
    # Ten independent probes determine an output Pauli/phase for Clifford
    # operators whose 18 symplectic basis images already agree.
    probes = [0] + [1 << i for i in range(9)]
    Os, Cs = [], []
    for src in probes:
        a, ko = vec(original, src)
        b, kc = vec(candidate, src)
        Os.append(a)
        Cs.append(b)
        assert ko == sum(g[0] == "C" for g in original)
        assert kc == sum(g[0] == "C" for g in candidate)
    y0 = next(iter(Cs[0]))
    shifts = sorted(
        {z ^ y0 for z in Os[0] if {x ^ (z ^ y0) for x in Cs[0]} == set(Os[0])},
        key=lambda x: (bool(x), x.bit_count(), x))
    for u in shifts:
        if any({y ^ u for y in b} != set(a) for a, b in zip(Os, Cs)):
            continue
        for p in range(4):
            equations, valid = [], True
            for a, b in zip(Os, Cs):
                for y, bv in b.items():
                    observed = tuple(z << kc for z in a[y ^ u])
                    expected = rotate(tuple(z << ko for z in bv), p)
                    if observed == expected:
                        equations.append((y, 0))
                    elif observed == (-expected[0], -expected[1]):
                        equations.append((y, 1))
                    else:
                        valid = False
                        break
                if not valid:
                    break
            if not valid:
                continue
            v = solve(equations)
            if v is None:
                continue
            gates = []
            if v:
                gates.append(("D", (0,) * 9, tuple(2 * ((v >> i) & 1) for i in range(9))))
            if u:
                gates.extend([("C", u, +1), ("C", u, +1)])
            if p:
                gates.append(("PH", p))
            return gates, dict(u=u, v=v, p=p, checked_inputs=10)
    raise AssertionError("phase correction not found")

def factor_and_correct(original):
    word, r = factor(original)
    correction_gates, c = correction(original, word)
    if c["u"]:
        # Flip core C signs to absorb Pauli X corrections within the
        # B-image without paying extra native C gates.
        start = next(i for i, g in enumerate(word) if g[0] == "C")
        suffix = word[start+r:]
        ux = [symp(suffix, 1 << i, 0)[0] for i in range(r)]
        chosen = next((mask for mask in range(1 << r) if c["u"] ==
            __import__("functools").reduce(lambda a, b: a ^ b,
                (ux[i] for i in range(r) if (mask >> i) & 1), 0)), None)
        if chosen is not None:
            word = word[:]
            for i in range(r):
                if (chosen >> i) & 1:
                    ix = start + i
                    g = word[ix]
                    word[ix] = ("C", g[1], -g[2])
            correction_gates, c = correction(original, word)
            assert c["u"] == 0
    result = word + correction_gates
    assert sum(g[0] == "C" for g in result) in (r, r + 2)
    for i in range(9):
        assert symp(original, 1 << i, 0) == symp(result, 1 << i, 0)
        assert symp(original, 0, 1 << i) == symp(result, 0, 1 << i)
    return result, r, c

def run():
    from hashlib import sha256
    source = ROOT / "p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json"
    original_sha = "a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39"
    assert sha256(source.read_bytes()).hexdigest() == original_sha
    W = json.loads(source.read_text())
    frames = [tuple(x) for x in W["frames"]]
    occurs = collections.Counter((e[2], e[3]) for e in W["events"] if e[0] == "transport")
    totals, rows = collections.Counter(), []
    t0 = time.monotonic()
    for j, t in enumerate(W["transports"]):
        src = [tuple(g) for g in t["gates"]]
        tgt, r, c = factor_and_correct(src)
        assert r == abs(len(frames[t["old"]]) - len(frames[t["new"]]))
        for probe in (0, 1, 37, 256, 511):
            a, ka = vec(src, probe)
            b, kb = vec(tgt, probe)
            assert {k: (v[0] << kb, v[1] << kb) for k, v in a.items()} == {
                k: (v[0] << ka, v[1] << ka) for k, v in b.items()}
        oldC = sum(g[0] == "C" for g in src)
        newC = sum(g[0] == "C" for g in tgt)
        n = occurs[t["old"], t["new"]]
        totals["old_distinct_C"] += oldC
        totals["new_distinct_C"] += newC
        totals["old_occ_C"] += n * oldC
        totals["new_occ_C"] += n * newC
        totals["extra_C_occ"] += n * (newC - r)
        totals["new_rank_occ"] += n * r
        totals["affine_coset_distinct"] += bool(c["u"])
        totals["affine_coset_occ"] += n * bool(c["u"])
        rows.append(dict(old=t["old"], new=t["new"], rank=r, old_C=oldC,
                         new_C=newC, occurrences=n, correction=c,
                         gates=[list(g) for g in tgt]))
    assert (totals["old_occ_C"], totals["new_occ_C"],
            totals["new_rank_occ"], totals["extra_C_occ"]) == (4160, 1832, 1496, 336)
    output = ROOT / "P104_MINIMAL_C_CANDIDATES.json"
    output.write_text(json.dumps({
        "schema": "p104-exact-phase-native-C-factor/1",
        "source_word_sha256": original_sha,
        "status": "not admitted native supplier; clean helpers and source/owner invoice OPEN",
        "counts": dict(totals), "transports": rows
    }, sort_keys=True, separators=(",", ":")) + "\n")
    print("PASS_P104_PHASE_CORRECT_C_FACTORIZATION distinct=514 weighted_C=1832 "
          "weighted_rank=1496 coset_extra=336 seconds=%.2f" % (time.monotonic() - t0))

if __name__ == "__main__":
    run()

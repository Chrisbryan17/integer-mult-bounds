#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""P104 signed E8 symplectic Bruhat factorization, exact phases verified separately.

This factors the 9-qubit symplectic Clifford action into P,D,C words with the
minimum B-block rank many C gates. This is NOT a complete physical supplier.
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "p104_native_e8_gate/scripts"))
import native_chart_emitter as E

def asrows(cols):
    return tuple(sum(((cols[j] >> i) & 1) << j for j in range(9)) for i in range(9))

def dot(a, b):
    return (a & b).bit_count() & 1

def symp(gates, x=0, z=0):
    for gate in gates:
        kind = gate[0]
        if kind == "P":
            G = gate[1]
            Gi = E.transpose(E.inverse(G))
            x = sum(dot(row, x) << i for i, row in enumerate(G))
            z = sum(dot(row, z) << i for i, row in enumerate(Gi))
        elif kind == "D":
            Q, alpha = gate[1:]
            out = z
            for i in range(9):
                if (x >> i) & 1:
                    if alpha[i] & 1:
                        out ^= 1 << i
                    for j in range(i + 1, 9):
                        if (Q[i] >> j) & 1:
                            out ^= 1 << j
                    for j in range(i):
                        if (Q[j] >> i) & 1:
                            out ^= 1 << j
            z = out
        elif kind == "C":
            if dot(gate[1], z):
                x ^= gate[1]
        elif kind == "PH":
            pass
        else:
            raise ValueError(kind)
    return x, z

def shear(S):
    assert all(((S[i] >> j) & 1) == ((S[j] >> i) & 1)
               for i in range(9) for j in range(9))
    alpha = tuple((S[i] >> i) & 1 for i in range(9))
    Q = tuple(((1 << i) * alpha[i]) |
              (S[i] & ~((1 << (i + 1)) - 1)) for i in range(9))
    return ("D", Q, alpha)

def monomial(sym):
    assert all(sym(0, 1 << j)[0] == 0 for j in range(9))
    A = asrows([sym(1 << i, 0)[0] for i in range(9)])
    assert E.rank(A) == 9
    Ai = E.inverse(A)
    C = asrows([sym(1 << i, 0)[1] for i in range(9)])
    At = E.transpose(Ai)
    S = tuple(sum(dot(C[i], At[j]) << j for j in range(9))
              for i in range(9))
    return [("P", A), shear(S)]

def factor(gates):
    # Determine the isotropic 9-dimensional image of computational Z operators.
    Z = [symp(gates, z=1 << i) for i in range(9)]
    bases = {}
    kernel = []
    for i, (bx, bz) in enumerate(Z):
        v = (bx, bz, 1 << i)
        while v[0]:
            h = v[0].bit_length() - 1
            if h not in bases:
                bases[h] = v
                break
            p = bases[h]
            v = (v[0] ^ p[0], v[1] ^ p[1], v[2] ^ p[2])
        if not v[0]:
            kernel.append(v)
    pivots = sorted(bases, reverse=True)
    X = [bases[k][0] for k in pivots]
    D = [bases[k][1] for k in pivots]
    K = [v[1] for v in kernel]
    r = len(X)
    assert len(K) == 9 - r and E.rank(K) == len(K)
    H = X[:]
    for i in range(9 - r):
        H.append(next(v for v in range(512) if all(
            dot(k, v) == int(j == i) for j, k in enumerate(K))))
    assert E.rank(H) == 9
    G = E.inverse(asrows(H))
    adjusted = [symp([("P", G)], x, z)[1] for x, z in zip(X, D)]
    Scols = [adjusted[i] ^ (1 << i) for i in range(r)]
    for i in range(r, 9):
        Scols.append(sum(((Scols[j] >> i) & 1) << j for j in range(r)))
    left = [("P", G), shear(asrows(Scols))]
    core = [("C", 1 << i, +1) for i in range(r)]
    after = left + [("C", 1 << i, -1) for i in range(r)]
    def right(x, z):
        a, b = symp(gates, x, z)
        return symp(after, a, b)
    candidate = monomial(right) + core + list(E.adjoint(left))
    for v in range(18):
        x, z = ((1 << v, 0) if v < 9 else (0, 1 << (v - 9)))
        assert symp(candidate, x, z) == symp(gates, x, z)
    return candidate, r

if __name__ == "__main__":
    word = json.loads((ROOT /
        "p104_native_e8_gate/scripts/evidence/NATIVE_CHART_WORD.json").read_text())
    frames = [tuple(x) for x in word["frames"]]
    total = 0
    for t in word["transports"]:
        gates, r = factor(t["gates"])
        assert r == abs(len(frames[t["old"]]) - len(frames[t["new"]]))
        total += r
    assert len(word["transports"]) == 514
    assert total == 1185
    print("PASS_P104_SYMPLECTIC_FACTOR recipes=514 sum_C=1185 phase_still_separate")

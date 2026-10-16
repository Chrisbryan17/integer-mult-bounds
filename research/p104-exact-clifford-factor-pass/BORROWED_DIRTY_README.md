# P104 borrowed-dirty helpers: clean-state assumption eliminated in a finite algebraic trace

**Status 2026-10-16:** locally verified signed 104-output E8 trace with **eight arbitrary-dirty helper registers restored identically**, independent 120-column integer logical inverse-transpose, unchanged 514 native Clifford transport recipes, and a second exact-rational historical moment screen. **NOT an admitted selected physical supplier, complete recursive invoice, all-size multiplier, or improved κ.** GPT-6 substantially assisted @Chrisbryan17; Apache-2.0. Credits: #968/#1125 (Ali Romman and predecessors), #2820, #2844, selected #1094 and the fork exact-phase P104 research at `f12cca097815e25009528dd625de829e47df4bf0`.

## Construction and scope

Each of eight already-existing dirty fields begins with arbitrary `d_j` in a common zero chart. The corresponding signed pair value is `g_j(X)=X_a+sigma_j X_b`. Each target `Y_t` uses signed coefficients `c_tj` and the remaining individual source terms `L_t(X)`. Before preparing the helper fields, make one zero-frame, same-chart read

```
Y_t -= c_tj * H_j
```

for each nonzero (t,j). Then prepare each `H_j += g_j(X)`, execute the previously verified signed decoder `Y_t += L_t(X) + sum_j c_tj*H_j`, and clean up `H_j -= g_j(X)`. Thus `Y_t` receives the desired `L_t(X)+sum_j c_tj*g_j(X)` and every `H_j` ends at its **arbitrary original d_j**, with no initialization or erase. This is exact over any additive coefficient group supporting signed ADD. The 156 compensation events touch 100 distinct Y targets. The protocol requires those **100 target owner fields to exist and be writable at the zero chart before helper preparation**. Neither their hosting nor the eight dirty fields is free.

No scalar event is masquerading as a convolution. The 156 new events are genuine signed zero-chart ADDs. This prepass is incidence-optimal **only** in the restricted model where a prepass event may address one H_j and one Y_t, with no Y–Y transfers, helper encoding, or other cancellation mechanism. There are 156 nonzero `c_tj`, so a single direct read can cancel at most one incidence. No universal additive-circuit minimum is asserted.

## Exact finite counts

| Item | Unmixed comparator | Mixed clean | Mixed borrowed-dirty |
| --- | ---: | ---: | ---: |
| Signed ADD | 416 | 292 | **448** |
| Clean initialize/erase | 0 | 8/8 | **0/0** |
| Arbitrary dirty helper restoration | n/a | unsupported | **8/8** |
| Native transports | 1,144 | 756 | **756** |
| Abstract frame-rank | 2,224 | 1,496 | **1,496** |
| Original C occurrences | 5,696 | 4,160 | **4,160** |
| Previously exact-phase-factorized C | 2,560 | 1,832 | **1,832** |
| Early writable Y fields | not required | not required | **100** |

The first 156 new ADDs all occur at chart dimension 0. The original signed ADD rank histogram remains `{1:76,2:88,3:48,4:44,5:24,6:12}`; unmixed uses `{1:104,2:104,3:92,4:68,5:36,6:12}`.

The producer regenerates and pins the original word SHA-256 `a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39`. Every one of 756 original transports and 514 native recipes is preserved by exact frame-pair/gate-word equality. Independent event interpretation checks the complete 120-variable map, preservation of all 104 arbitrary Y values, zero hidden resets, and one omitted-compensation contamination control. The independently checked prior exact 512-column Clifford phase checker applies unchanged to all 514 transport recipes.

## Logical inverse-transpose

On the 120 inputs `(X[8],Y[104],H[8])`, this finite map is the shear

```
F = [ I8   0     0 ]
    [ C    I104  0 ]
    [ 0    0     I8].
```

Its ordinary inverse-transpose is `[[I8,-C^T,0],[0,I104,0],[0,0,I8]]`. A separate exact-integer checker verifies all 120 formal columns and all 14,400 entries of `F^T F^(-T)=I`, with wrong-sign rejection. For ordinary inverse-transpose, (AB)^(-T)=A^(-T) B^(-T), so same chronological order, swapped ADD source/destination and negated sign is correct; reversing the order is incorrect. **Physical Clifford `Delta` endpoint charts, source access, and required charged conversions are still open.**

## Two exact-rational moment calculations — historical scope only

The independent positive-Mercator fixed-point/Taylor checker confirms the predecessor atanh/Taylor certificate for the **historical optimistic P104 replacement**: 0 extra rank units/pass, 1/pass, 2/fail at the selected b, with historical headroom strictly between 1.915 and 1.917. It does **not** compute the new 448-ADD compiler's actual recursive moment. The reviewed selected conditional κ remains **0.001672660197076918**.

## Symbolic restricted-price screen — not a recursive invoice

Let `A0..A5` be costs of rank-r signed ADD, and `C,P,D,PH` independently paid literal gate prices in this provisional model. Relative to equally factorized home-return unmixed, the dirty mixed nominal advantage is:

```
728*C + 776*P + 1094*D + 228*PH
 + 28*A1 + 16*A2 + 44*A3 + 24*A4 + 12*A5 - 156*A0 - DELTA
```

`DELTA` is every extra source/owner/idle/precision/hosting/adaptor cost. This expression is only an auditable sensitivity identity; gates may coalesce, `C(q)` admission is not automatic, and the strong selected #1094 supplier is **not** this unmixed comparison.

## Reproduce

From `research/p104-exact-clifford-factor-pass` with Python 3.10+:

```bash
python3 -I -B p104_native_e8_gate/scripts/native_chart_emitter.py
python3 -I -B p104_dirty_zero_adapter.py
python3 -I -B p104_verify_dirty_adapter.py
python3 -I -B p104_verify_dirty_logical_dual.py
python3 -I -B p104_independent_mercator_screen.py
```

For independent literal 512-column phase equality with NumPy, run the existing `p104_minimal_symplectic.py`, `p104_exact_native_factor.py`, and `p104_verify_all_columns.py`. The reproducible earlier companion package has all 36 original archived research files; the GitHub branch uses pinned regenerated source words instead of committing large redundant generated JSON files.

## Open next questions (hard admission boundaries)

1. Prove that pre-access to 100 initial Y at chart zero and all eight dirty fields is legal for selected P104 mutable-source/host ownership; fully charge these long lifetimes, 156 extra reads and any initialization/placement.
2. Admit paid rank-r native children and every source, monomial, signed C/phase/Pauli and physical inverse-transpose word under the selected producer. Check the real unoptimized-versus-optimized comparison with the selected #1094 supplier.
3. Construct complete source-hashed per-side recursive child/host/scalar/tape/precision invoice and run **both** independent exact moment engines on that *new actual profile*.
4. Certify uniform all-size recursion, analytic transfer, rounding, bit-side H1–H5 and strict joint outer inequality. Previous upstream conditional theorem obligations remain; no current end-to-end theorem claim.

**This contribution closes a narrower finite dirty-helper correctness gate, not the complete algorithm.** A negative result on early Y accessibility or price must be recorded as such rather than bypassed with a hidden ZERO/ERASE.

## Further advance: one exact positive native F_r child per transport

The separate `p104_rank_r_native_recipes.py` converts every prior phase-correct signed Clifford recipe into the retained accepted recipe **syntax** `L ; F_r ; R`, with a single **positive** rank-r child and two validated monomial records. The exact relations `C(q,+)^2=X(q)` and `C(q,-)=C(q,+)X(q)` remove the 336 surplus literal C occurrences and replace negative core C directions with explicit, charged X-offset address maps. Each monomial is emitted in the retained `quadratic_rows / linear_Z4 / matrix_rows / offset / phase` schema with symmetric quadratic rows, matching diagonal parity, invertible binary matrix and explicit phase. The independent checker `p104_verify_rank_r_all_columns.py` passed **all 514 recipe × 512 basis-column exact Gaussian-integer comparisons**, with global phase and X-offset mutation controls rejected.

This yields **756 exact positive native rank-r child calls**, with **1,496 total child-rank mass**, unchanged 156 zero-frame cancellation ADDs, and explicit left/right monomial sides per call. There are **168 affine X-coset correction occurrences** before monomial fusion; the actual charged address complexity must be derived from the final records. This is a finite native-operator-factorization result, **not automatically a supplier**. Native endpoint owner legality, early writable target fields, actual address/phase/precision costs, source hosting, tape and physical inverse-transpose remain unverified. In particular, do not treat P,D,X,PH as zero-cost operations or compare against only the restricted unmixed reference when claiming an exponent.

Cold reproduction commands, after generating the phase-correct candidate records:

```bash
python3 -I -B p104_rank_r_native_recipes.py
python3 -I -B p104_verify_rank_r_all_columns.py
```

The first phase-candidate generator is `p104_exact_native_factor.py`, which requires `p104_minimal_symplectic.py` and the pinned source word. This contribution leaves the selected κ unchanged.

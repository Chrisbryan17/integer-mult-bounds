# P104 in-place 104-source E8 channel: Gram-half and I−Gram-half

**Research result 2026-10-16. Scope: exact finite P104 integer-numerator
construction, not a full recursive supplier, improved κ, or all-size integer
multiplication theorem.** The reviewed selected conditional
κ remains 0.001672660197076918. New research for @Chrisbryan17 with
substantial GPT-6 assistance under Apache-2.0. Preserve predecessors
#968, #1071, Ali Romman/#1125, #2820, #2844, the selected #1094, and
the reviewed `research/p104-native-channel` and
`research/p104-physical-corrected-dual` packages. No reviewed source,
selected frontier, or `upstream/` file is changed.

## Core mathematical innovation: eliminate eight clean aggregate scratch fields

Let `G` be the exact 104×104 doubled-root-line Gram/2 integer matrix
(the diagonal is 2, each off-diagonal entry is 0 or ±1). Pick the eight
physical E8 basis roots `R` of the frozen P104 signed decoder and define

```
C[t,i] = IP(live[t],R[i])           104×8
K[i,j] = IP(R[i],R[j])              8×8, det(K)=1
B = K^(-1) C^T                     8×104, entries 0,±1
G = C B                             104×104, exact over integers.
```

Choose existing **source register ports** indexed
`P=[23,55,61,62,38,11,26,60]` (all from the 104 actual live ports).
The 8×8 submatrix `B_P` has determinant **+1**, so `B_P^{-1}`
is integral. Partition the 104 sources into pivot values `S_P` and
96 other values `S_O`. With `U = B_P^{-1} B`, construct

```
S_P <- S_P + U[:,O] S_O
S_P <- B_P S_P                 # aggregate X = B S
...
S_P <- B_P^(-1) S_P
S_P <- S_P - U[:,O] S_O        # exactly restore all sources
```

All of these changes are explicit signed **unit** ADDs, sign gates and
register swaps expanded into **three signed ADDs plus one NEG**. No free
swap, temporary copy, zero allocation or hidden half-scalar is used.
`p104_inplace_source.py` regenerates these operations by exact rational
integer elimination and emits the full literal source/target/helper event
stream. Independent `p104_verify_inplace_source.py` checks all 216
independent formal columns, 10,816 Gram coefficients, all 46,656 logical
inverse-transpose entries, legal common-chart changes and four mutation
controls.

## Two typed programs: no native fractional scalar primitive

A raw signed ADD circuit cannot produce ±1/2 from integral, unencoded
inputs. Instead declare the target type to be a **numerator with a shared
denominator 2**, and require the caller to preserve this type.

1. Gram-half program, on the numerator: `Ynum <- Ynum + G*S`.
   Its decoded semantics is `Y <- Y + (G/2)*S`.
2. Full side-correction program: while S and Y are in the zero chart,
   explicitly add `2*S_t` to each of the 104 target numerators
   (208 signed unit ADDs), then execute the mixed decoder with all eight
   aggregate carriers negated and restored. Result:
   `Ynum <- Ynum + (2I-G)*S`, decoded as
   `Y <- Y + (I-G/2)*S`.

Both exactly restore 104 original source values and eight arbitrary-dirty
helper values. Neither allocates any additional clean aggregate. The source
and target representation change is **not free**; final rounding, global
target typing, sign/phase, dyadic carry budget, and the selected real/bit
interfaces remain unproved. These are complete **finite algebraic**
channel maps, not simultaneously host-admitted supplier words.

| Literal finite metric | G/2 numerator | I−G/2 numerator |
| --- | ---: | ---: |
| Signed unit ADDs | **1,298** | **1,506** |
| Scalar NEG | **12** | **28** |
| Native divide-by-two primitives | 0 | 0 |
| New clean aggregate registers | 0 | 0 |
| Original eight dirty helpers restored | 8 | 8 |
| Positive native rank-r children (conditional) | 980 | 980 |
| Rank mass (conditional) | 1,720 | 1,720 |
| Source entry/exit native H1 | 208 | 208 |
| Pivot zero/line native H1 | 16 | 16 |
| Core positive native transports | 756 | 756 |
| Early writable Y roles | 100 | 104 |

The precise new child-rank histogram (including the 224 bridges) is
`{1:544,2:272,3:72,4:56,5:24,6:12}`.
The model still requires priced chronological owners for all source/target
and borrowed helper roles. Unlike the original clean-scratch word, a selected
source port is temporarily mutated but is **exactly** restored; this
preservation does not establish host/mutable-source permission.

## Exact physical E8 native transport admission

The predecessor abstract 9-bit labels had 7,168 standard-dot mismatches
among 14,400 root pairings, so we use the certified physical GF(2)^9
orthonormal isometry instead. The original 514 distinct core chart recipes
have 756 exact positive rank-r child uses. The present package additionally
checks all 104 intrinsic source entrances and 104 exits as **208 separate
physical rank-one positive children**, and all 16 pivot zero/true-root-line
bridges. Every new primitive is compared on **all 512 complex input
columns**, not only its projective tableau; global phase is included.
The existing exact positive rank-r core verifier covers the 514 recipes.
All downstream source and monomial wrapper costs remain unpriced.

## All-prefix coefficient-growth guard

`p104_verify_inplace_prefix_guard.py` independently replays every scalar
intermediate over 216 formal input symbols, computing exact absolute
coefficient row sums (ℓ1). For the optimized determinant-one pivot:

- G/2 numerator word: maximum ℓ1 **105** (target); sources peak 98;
  maximum individual coefficient 3.
- I−G/2 numerator word: maximum ℓ1 **103**; sources peak 98;
  maximum individual coefficient 3.

If each formal input has absolute magnitude at most M, every **scalar
logical** intermediate is bounded by `105*M` (or `103*M` for side).
Thus seven extra **magnitude** bits suffice for this fixed scalar kernel
relative to a common p-bit input magnitude bound:
`ceil(log2(105))=7`. This is not a bit-growth proof for the native Gaussian
address matrices, global recursion, tape, numerical errors, or rounding.
The previous determinant-minus-one pivot required an eighth guard bit
(ℓ1=130). The 40,000-candidate seeded pivot search is exploratory and
does not certify globally optimal ADD/precision counts.

## Cold reproduction

Python 3.11+ with NumPy. From
`research/p104-exact-clifford-factor-pass`:

```sh
python -I -B p104_native_e8_gate/scripts/native_chart_emitter.py
python -I -B p104_dirty_zero_adapter.py
python -I -B p104_physical_e8_isometry.py
python -I -B p104_minimal_symplectic.py
python -I -B p104_exact_native_factor.py
python -I -B p104_rank_r_native_recipes.py
python -I -B p104_complete_gram_channel_stdlib.py
python -I -B p104_inplace_source.py
python -I -B p104_verify_inplace_source.py
python -I -B p104_inplace_physical_source_ports.py
python -I -B p104_inplace_pivot_native.py
python -I -B p104_inplace_dyadic_target.py
python -I -B p104_verify_inplace_dyadic.py
python -I -B p104_inplace_side.py
python -I -B p104_verify_inplace_side.py
python -I -B p104_verify_inplace_prefix_guard.py
```

The dedicated `.github/workflows/p104-inplace-source-dyadic.yml` is
committed with two Python versions. **Remote CI success is not yet
confirmed**, and a passing finite test is not an all-size result.

## Remaining honest acceptance gates

1. Selected source contract must allow 104 source entry/exit changes,
   mutating/restoring eight actual source owners, all early Y writes
   (100/104), 8 borrowed helpers, and their physical field locations.
   Nonmonotone visits and peak live storage must be charged.
2. Complete both-side physical ordinary inverse transpose with source
   encoding conversions and paid monomial/canonical endpoint adapters.
3. Compare this full local word with the **strongest actual reviewed**
   supplier including **all** owner, idle/residual child, tape, host, phase,
   address, scalar and precision costs. Do not compare only an artificial
   home-return unmixed reference.
4. Run two independent exact recursive moments on the newly charged
   complete per-side profile, plus bit H1–H5, strict joint outer
   inequalities, rounding and all-size analytic transfer.
5. Bind a uniform all-operand-length integer multiplication algorithm to
   these interfaces without assuming free dyadic conversion or circular
   precision. A 104×104 finite result cannot alone establish a new κ.

**Selected κ remains 0.001672660197076918. No new κ or full theorem.**

## Additional finite physical inverse-transpose and ownership checkpoints

`p104_inplace_chrono_dual.py` emits a literal **same-chronology ordinary
inverse-transpose** of both full typed words: for each ADD
`destination += sign * source` it emits
`source += -sign * destination`, preserving all frame visits in conjugate
`Delta = conjugate(Gamma)` charts; scalar signs transpose unchanged.
`p104_verify_inplace_chrono_dual.py` independently replays both 216-variable
dual words, verifies each source and helper response, and rejects an incorrect
dual ADD sign or reversed event chronology. All **46,656 matrix entries per
dual** agree with the exact triangular shear inverse-transpose.

The 104 source intrinsic conjugate C(q) entrances/exits reuse explicitly
opposite signed root-line operations, already lowered to **positive** native
rank-one children and full 512-column verified. The eight physical pivot
source entries/exits are separately conjugated and lowered to 16 positive F1
children; `p104_inplace_pivot_delta_native.py` checks all 512 columns of
each operator including global phase. The 514 physical E8 core transport duals
retain the earlier independently checked exact Clifford action. Thus **980
finite rank-r positive native calls, rank mass 1,720 per orientation** remain
the exact stated local transport inventory. However, **ordinary canonical
endpoint data charts are not the conjugate-Delta caller interface**, and the
required phase/address/host adapters must still be admitted and charged.

The fail-closed `p104_inplace_owner_boundary.py` scans the actual chronological
event stream and reports **216 required distinct logical fields** (104 S,
104 Y and eight arbitrarily dirty H), no new clean scratch, and 100 early
borrow-compensation Y registers (104 early Y for the side program's identity
prepass). Of the 980 native transport events, exactly **308 are rank-decreasing**
with total rank mass **444** (104 source entrances and 204 core/pivot moves);
672 are rank-increasing with mass 1,276. A positive child factorization
proves exact operator realizability; it **does not** by itself assign legal
chronological owners or make a nonmonotone source move affordable. These
decreasing edges are now an explicit physical admission blocker, not an
unpriced implicit free reset.

Extra reproduction commands, after the typed words and positive native
recipes are emitted:

```sh
python -I -B p104_inplace_chrono_dual.py
python -I -B p104_verify_inplace_chrono_dual.py
python -I -B p104_inplace_pivot_delta_native.py
python -I -B p104_inplace_owner_boundary.py
```

A second full 104×104 physical owner assignment, per-side tape/precision
invoice and selected strong comparator are still necessary before either
exact moment engine can be applied to a legitimate candidate. All-size
analytic transfer/rounding and bit-side H1–H5 remain unresolved. **No new κ.**

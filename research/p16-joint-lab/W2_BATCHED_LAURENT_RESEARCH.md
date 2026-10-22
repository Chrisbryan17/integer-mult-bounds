# P16 W=2 batched Laurent and Clifford research (2026-10-22)

**Scope: exact source-pinned construction research, NOT a new accepted native supplier or a new multiplication exponent.** Selected maintainer-reviewed conditional κ remains 0.00302015. No upstream selected certificate/merged PR is changed. Work for @Chrisbryan17 with GPT-6 assistance; new source Apache-2.0; native/math lineage and other contributors retained.

## Source and threat model

Pinned selected PR #4470 `CrocSwap/integer-mult-bounds@b9a13c1673e0e9697de410de16e8bbf3207a7363`; original 154 `physical_events` from `research/joint-helper-lattice/CONTROLLER.json` (blob `49a2f0675819f9deeea27ed77be2c2b6ff2e87e5`). Compact serialized event SHA-256 `624305383d5e7e1687e01356d5e41ff4ee3d4f06b3cab71cf9a65ea22fc8dd52`. Final selected paid-job invoice: 64,620 jobs, 10,928 productive outputs, unlike the older embedded controller fixture. Open #4535 is a separate critical-root transfer proposal.

## E1: exact four-port coupled query factorization

Every one of the 15 PR4470 five-event windows is an exact rank-one Laurent update. For old-pair source a/b, new-pair source u/v, and central monomial q:

    a += u; v -= b; b += q*a; a -= u; v += b

is equivalent on ALL arbitrary independent inputs to the **formal** four-port macro:

    b += q*(a+u); v += q*(a+u)

(The two right-hand sides use the same pre-operation a+u.) `p16_coupled_query_miter.py` reconstructs the exact 154-event controller, emits 15 formal COUPLED_QUERY macros (94 total events instead of 154), and verifies all 1024 entries of the full multivariate 32×32 rational Laurent matrix, including every stage and central Gaussian sign. A mutation is rejected. The exact 64×64 direct sum of two independent copies (4096 entries) also passes. Unit ADDs drop 90→30 **in the extended instruction set**, but this four-port primitive is **NOT** physically native/admitted, and the original 15 query obligations (112 rank-one children each) remain unchanged. A legitimate physical lowering through the original source/query alphabet reintroduces the four signed ADDs at each window. Thus **no κ gain**.

## E2: W=2 rank oracle obstruction

A single real or complex rank-one QUERY shear has the coefficient of q equal to an outer product (rank 1). The two independent source-copy window updates give a rank-2 q-coefficient. q-independent invertible integer preprocess/postprocess cannot reduce rank, so at least two rank-one query oracles are necessary. `p16_w2_query_rank_gate.py` certifies the exact 4×4 and 8×8 q-coefficients, exhaustively tests 0-, 1-, 2-shear conjugations, and performs 100 independent cross-copy mixer controls. One query plus arbitrary q-independent preprocessing is not enough. This applies to the **fixed rank-one query alphabet**, not more powerful batched native primitives.

## E3: right-tail IDLE deferral and stage-major grouping

The eight IDLEs following the last LOCAL can be deferred across their remaining backward ADDs as Laurent metadata if the ADDs become weighted and the terminal masks are physically realized. The exact 32×32 matrix miter passes: eight deferred IDLEs create **18 weighted ADDs** and **16 terminal monomial-mask obligations**. Under a naive individual-output rank-mass proxy, the masks cost 704 versus the original 352 per port. **No cheap elimination.**

The eight tail stage masks are nested. They contain **nine distinct Laurent stage axes** with multiplicities `[1,2,3,4,5,6,7,8,8]`. A formal stage-major batch primitive with capacity two would use 24 shared rank-eight operations, and its *hypothetical* paid profile would make the κ=0.006 raw moment favorable. This is **NOT** an admitted κ. The original eight tail IDLEs carry total stage determinant degree 88. Twenty-four existing single-pair rank-eight operations supply only degree 48, leaving **40 independent Laurent determinant degrees unpaid**. Each original stage job on one pair has determinant z², whereas the sought joint two-pair stage must carry z⁴. To break this barrier one needs a genuinely new productive/physical broadcast with independently priced output/owner rights, not free SIMD bookkeeping.

## E4: actual positive W=2 exact REAL-input Clifford packing

For commuting rank-r Clifford butterflies `F_r=prod_{j<r}(I+i X_{2^j})/sqrt(2)`, exact unitary/symmetric identities give

    F_r F_r^T = i^r X_{2^r-1}.
    w = F_r(x+i*y), where x,y are INDEPENDENT REAL integer arrays.
    F_r(x) = (w+i^r X_mask conjugate(w))/2.
    F_r(y) = (w-i^r X_mask conjugate(w))/(2i).

`p16_w2_realpair_clifford.py` proves exact Gaussian-integer numerator identities (common sqrt(2)^r denominator) for r=1..9, all 1024 individual real basis cases per rank (9216 total) plus 576 signed random paired inputs. Every division by two is proved exact by even-numerator parity, global phases included. Thus two **real** Clifford transforms can be recovered from one complex Clifford child plus a charged conjugate/permutation/phase/arithmetic reconstruction. This is a valid mathematical batching identity potentially useful for the **BIT/real-input side**. It cannot replace two arbitrary-complex productive fields: `(x,y)->x+i*y` has a nontrivial complex-linear kernel, demonstrated by an explicit collision. Its full BIT encoding, field ownership, memory/tape, error budget and recursive admission have not been proved. **No new κ.**

## Acceptance and next attack

1. Determine whether the source native-operator grammar admits a four-port rank-one query with fewer physically paid ADD/owner operations. If no, preserve the one-query window minimum as an obstruction.
2. Seek a genuinely **two-pair determinant-bearing** rank-r child and certify four independent terminal fields, both exact Clifford orientations, owner/host/tape and true per-port paid rank. This is the only path by which the stage-major batch2 raw-moment counterfactual could become a record.
3. Integrate real-pair packing into a source-legal BIT or real-subchannel kernel. Price recovery, Gaussian reality restrictions and no false complex-field productive credit. Re-run full BIT, outer and all-size requirements.
4. Only then run two independent rational moments on a new fully paid 64,620-job-comparable whole profile and check all-size transfer/rounding.

## Reproduction

```sh
cd research/p16-joint-lab
python3 -I -B p16_coupled_query_miter.py
python3 -I -B p16_w2_query_rank_gate.py
python3 -I -B p16_tail_idle_virtual.py
python3 -I -B p16_stage_major_batch.py
python3 -I -B p16_w2_realpair_clifford.py
python3 -I -B test_p16_w2_batching.py
```

Native full-output miter, determinant and rank barriers, and real-pair packing are independently checked mathematical results. Hosted GitHub CI remains a separate acceptance check.

## Source-specific BIT reality caveat

A direct inspection of the retained `research/query-thinned-controllers/PROOF.md` and `BIT-CONTROLLER.json` confirms the selected BIT supplier is a **binary F2 projector/involution architecture** with 111 ports, not a real Gaussian-integer FFT. The exact real-pair complex packing identity therefore **cannot be installed into its existing binary child alphabet without a new embedding theorem**. That theorem must preserve binary arbitrary-source independence and exact recovery, count the Gaussian encoding/conjugation/reconstruction and evaluate the resulting BIT paid moment. The real-pair identity is mathematically exact but not a ready-made BIT supplier.

The frontier-selected **complex** native supplier has arbitrary independent Gaussian-complex helpers; no complex-linear packing of two such arbitrary fields into one complex field is injective. Hence the successful real-pair test creates no extra selected productive-helper credit and cannot presently improve the complete P16 raw κ.

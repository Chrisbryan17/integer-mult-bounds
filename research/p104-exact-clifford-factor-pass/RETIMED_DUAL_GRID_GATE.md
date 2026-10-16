# P104 retimed E8 physical dual, all-depth grid, and address ledger

**Finite verified research contribution; NOT a complete integer-multiplication theorem or a new κ.** Created for @Chrisbryan17 with substantial GPT-6 assistance, Apache-2.0. Preserves #968/#1071, Ali Romman/#1125, merged #2820/#2844, reviewed selected #1094, the P104 native/physical-dual predecessor attribution, and selected `κ=0.001672660197076918`. Parent: `research/p104-intersection-retime-rank-optimal-20261016` at `b615ab957e672851ec524a66dfa13b34fc9fddc0`. Native word SHA-256 `a5fca1d880512630d23691d2f8be5cf6074c43b4a7182a4bd149e411e2b6ef39`.

## Four independently checked finite improvements

1. **Ordinary physical inverse-transpose**: all 485 distinct retimed G/2 Clifford recipes and 493 I−G/2 recipes are compiled in `Delta_W=conjugate(Gamma_W)=Gamma_W^(-T)` and verified using 18 Clifford symplectic generator images plus 10 exact Gaussian input columns, including global phase, with PH/C/X negative controls. Both use one *positive* native F_r child per transport. Internal occurrences: **687 / 703**. Including 208 source-port rank-one children: **895 / 911**, rank mass **1,446 per orientation**. No legal chronological physical owner is yet assigned.
2. **Canonical/conjugate intrinsic endpoint conversion**: for each of all 104 actual physical E8 roots q, `C(q,+)=X(q)C(q,-)` and `F9*C(q,-)=X(511 xor q)*conjugate(F9*C(q,-))`. All 208 source/target identities pass exact Clifford checks with 512-column samples. **No added recursive Fourier child**; **208 nonfree X address-mask adapter roles** still need charging.
3. **Exact all-prefix forward/dual scalar bounds**: all 216 formal inputs are replayed, all 104×104 Gram and side matrix coefficients are checked. G/2 forward max ℓ1=105 (**7 magnitude guard bits**), ordinary dual ℓ1=135 (**8 bits**); I−G/2 forward 103 (7 bits), dual 127 (7 bits). The dual G/2 peak is S75 at event 1700, 83 nonzero coefficients summing in absolute value to 135: an adversarial ±1 input attains the bound.
4. **Constructive reversible address/phase invoice**: all 651 distinct physical GL(9,2) matrices in the internal monomial records are independently lowered to in-place CNOT/SWAP address maps and checked at all 512 addresses (≤96 CNOT-equivalent gates per one matrix). Internal-occurrence weights:

| Word | Monomial records | CNOT equivalents | CZ cross terms | Linear phases | Nonzero X offsets |
|---|---:|---:|---:|---:|---:|
| G/2 forward | 1374 | 21177 | 9920 | 4442 | 450 |
| G/2 dual | 1374 | 21177 | 9920 | 4385 | 584 |
| I−G/2 forward | 1406 | 21320 | 9938 | 4451 | 455 |
| I−G/2 dual | 1406 | 21320 | 9938 | 4415 | 592 |

These address counts are neither Fourier children nor a physical tape invoice. In a separately specified random-access array model with `D=512^lambda`, a conservative constructive internal-word address access bound is `D*(21177*lambda+3648)` for G/2 forward and `D*(21177*lambda+3916)` dual; side forward `D*(21320*lambda+3722)` and dual `D*(21320*lambda+3996)`. Excludes source wrappers, target adapters and other costs.

## Uniform local tensor-payload exact-grid lemma (not the all-size integer multiplier)

For a payload tensor factor depth `lambda>=1`, an input real/imaginary Gaussian grid `2^-f Z`, and the **exact** literal native gates: all physical frames have dimension at most 8; initial source chart dimension 1 and other initial dimensions 0; coefficients are integers; maximum native F_r child rank is 6. Hence atomic event values lie in `2^-(f+9lambda) Z[i]`, while every butterfly prefix lies in `2^-(f+15lambda) Z[i]`. Exact ideal division at this common grid is integer-divisible and needs no rounding. A conservative stored complex-component bound is `H*2^(ceil((9lambda+1)/2)+8)`, with scratch bound `H*2^(ceil((9lambda+1)/2)+10)`, given real/imag input magnitudes ≤H. The typed numerator target requires one additional denominator-two bit at its decoded interface. These statements concern the local tensor lift, not approximate recursive child execution, all-size bit interchange, tape/host, or analytic transfer.

## Fail-closed remaining obligations

**NOT ADMITTED**: 216 owner/family roles and 100/104 early writable Y fields; 104 temporarily mutated sources; eight arbitrary-dirty helpers; the rank-optimal but **307 unavoidable descending rank units** under the frozen fixed-anchor and source-interface model. Actual owner/idle/residual/tape scheduling; physical address movement; selected strongest #1094 whole-supplier comparator; full per-side recursive profile; two independent exact moment inequalities *for that full profile*; bit H1–H5, dyadic caller, uniform all-size correctness, analytic transfer and rounding. Unknown is never zero. Thus **no change to the conditional κ**.

## Reproduction

From `research/p104-exact-clifford-factor-pass`, generate the inherited pinned native E8 source and both intersection words per the previous README, then run:

```sh
python -I -B p104_routed_native_audit.py
python -I -B p104_retimed_delta_native.py
python -I -B p104_retimed_canonical_delta.py
python -I -B p104_retimed_grid.py
python -I -B p104_retimed_address_ledger.py
```

`.github/workflows/p104-retimed-dual-grid.yml` cold-replays both programs on Python 3.11/3.13. **Hosted CI pass has not been independently observed.** The separate full original research archive and new handoff preserve all original source hashes.

**Next decisive change:** selected-source-bound physical chronological owners for those 307 descending rank units, with explicit hosting/idle/tape upper bounds or a proven rejection that triggers a changed scalar/source protocol. Do not apply selected moment or promote κ until the full invoice and all-size theorem actually close.

# P104 E8 delta dual and Gram-half interface audit

Finite result only (2026-10-16). **No new kappa, no admitted supplier and no all-size multiplication theorem.** Built on #968/#1071, Ali Romman's #1125, merged #2820/#2844, reviewed selected #1094, PR1972 native G/2 channel and physical-dual research #2497/#2551/#2586. @Chrisbryan17 with substantial GPT-6 assistance; Apache-2.0.

All 514 conjugate native Clifford transport recipes have exact 512-column Gaussian equality to Delta_B Delta_A^-1, global phase included. There are 756 positive rank-r children and 1496 rank units per orientation. The independent verifier rejects sign and PH mutations. A physical counterexample X0<-Y22 on input address 0 yields (1-i)/2; replacing Delta with Gamma gives (1+i)/2. Canonical endpoints are **not free**.

Critical correction: the existing mixer computes signed G (416 coefficients +/-1) but the reviewed P104 native channel requires G/2 (416 coefficients +/-1/2). Integer-only signed ADD cannot construct half-integer coefficients. A separate Fraction-exact 120-column rational bridge uses eight explicit X halvings before the 448-ADD, 756-transport word and eight X doublings afterwards. It restores all X and dirty H, and 14,400 inverse-transpose entries pass; 16 scalings remain unpriced and possibly unavailable in the integer model.

The forward/dual conditional combined finite bill is 1512 positive rank-r child calls, rank mass 2992, 896 signed ADDs, and 3024 monomial sides. The fail-closed source audit lists 156 early zero-chart H-to-Y reads touching 100 Y fields. Their physical owners and source availability remain unknown. No owner, tape, phase, scaler, precision or host cost is assumed zero.

Reproduce by regenerating the pinned source and positive rank-r recipes and running p104_dual_native_check.py, p104_verify_dual_native.py, p104_half_gram_bridge.py, p104_verify_half_gram.py and p104_forward_dual_owner_audit.py. Two-version cold-replay CI is committed, not yet confirmed green.

**Unresolved gates:** 100 Y/8 H owners, legal 16 scalers, G/2 and I-G/2 full source channel, accepted physical endpoints, paid whole-call recursion, optimized selected supplier comparison, independent moments, analytic/rounding, all-size theorem. Selected conditional κ remains 0.001672660197076918.


## Physical E8 isometry: previous abstract labels were insufficient

The original nine-bit compressed labels have **7168 mismatches among the 14400 required standard binary dot-product root pairings**. Although the earlier 514 Clifford recipes were internally phase exact, they were in an uncalibrated coordinate system and were **not a certificate of the physical supplier labels**. `p104_physical_e8_isometry.py` reconstructs the 9x9 Gram form, supplies a fully verified orthonormal basis over F2, proves all 14400 physical E8 pairings and all 104 rank-eight sink hyperplanes, and transforms all 239 frames. No abstract-to-physical identity assumption remains.

`p104_isometric_native_compiler.py` re-emits and phase-corrects all 514 native recipes in that exact physical basis, again producing one positive rank-r child per transition, 756 occurrences and 1496 rank units. `p104_verify_isometric_native.py` independently checks all 514 forward and 514 conjugate-dual operators by the mathematically complete Clifford criterion: equal action on 18 symplectic generators and equal exact Gaussian amplitudes on computational address 0 and the nine singleton addresses. Because operators with identical unsigned symplectic action differ by a Pauli times scalar phase, those ten columns determine the residual Pauli X/Z and phase. Additionally it compares 14 complete 512-column matrices in each orientation.

In the physical basis, the 8 source intrinsic adapters `Gamma_line C_q^-1` and 104 target intrinsic adapters `F9 C_q^-1 Gamma_sink^-1` are **exact rank-zero Gaussian monomials**, including full phase. All 112 use the exact Clifford generator/ten-column criterion; 3 source and 8 target adapters receive additional full 512-column checks. This certifies the finite native Clifford and boundary algebra for the pinned geometry, **not** 16 fractional scalers, 100 early Y owners, global hosting, the remaining I-G/2 correction, selected #1094 competitive costs, moments or the all-size theorem.

Reproduction after generating the original word and inherited rank-r recipes:

```sh
python -I -B p104_physical_e8_isometry.py
python -I -B p104_isometric_native_compiler.py
python -I -B p104_verify_isometric_native.py
```

The GitHub workflow now contains these three extra cold checks. The conditional frontier remains unchanged.

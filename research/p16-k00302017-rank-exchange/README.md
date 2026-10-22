# P16 κ = 0.00302017: smallest rank-surplus-preserving paid/productive exchange screen

**Status (22 October 2026): EXACT MOMENT SCREEN POSITIVE; NO PHYSICAL OPERATOR; κ=0.00302017 IS NOT PROVED.** Existing selected κ=0.00302015 and the pending #4568 claim κ=0.00302016597 are unchanged. New work for @Chrisbryan17 with GPT-6 assistance, Apache-2.0; preserve source attribution to Cinna Davis, zxv, Jacob Alan Sussman, Dillon, Ryanson Jonathan and hexapode.

## Source

Use the exact source-bound #4470 p16 supplier at `CrocSwap/integer-mult-bounds@b9a13c1673e0e9697de410de16e8bbf3207a7363`:
- Productive fields: 10,928, rank mass 239,886.
- Paid jobs: 64,620, rank mass 239,134.
- Difference: 752, nonnegative and exact.
- Native local helpers: `{4:28,7:7,8:47,9:326}`.
- Native local paid: `{1:2237,2:388,3:494,4:147,5:36,8:8}`.
- Controller includes 18 full uses, 15 query-only shears, and 3,360 idle jobs.

The true current selected moment is **strictly negative** at the user's κ target `0.00302017`:

`T(1-κ)-P(1-κ) = -0.00099511104066963991959798…`.

The raw-root bracket of this exact supplier is `0.0030201659770 < κ_raw < 0.0030201659771`, so no tighter outer transfer alone can attain κ=0.00302017.

## Precise NEW counterfactual source-level exchange target

A *single* occurrence in the **whole-controller** invoice would change:
- One independently productive target **rank 4 → rank 5**.
- One **paid rank 8 → rank 9** positive child.

This preserves field/job **counts**, and raises both rank masses by **one**; the rank surplus remains exactly **752**. At κ=0.00302017, by strict concavity of `r^(1-κ)`:

`Δmoment = (5^(1-κ)-4^(1-κ)) - (9^(1-κ)-8^(1-κ))`
`         = +0.00190896108375712838…`.

It changes the full moment from `-0.00099511104067` to **`+0.00091385004308748846…`**. Exact rational outward enclosures, independently checked with 70-digit Decimal and both rank-mass totals, certify these signs.

This is an **exact sensitivity target**, NOT a new multiplication construction. A formal change of histogram entries is insufficient. Specifically, the existing eight full-call rank-eight owned centres cannot simply be declared rank nine; the 28 rank-four helpers cannot simply be declared productive rank five. We must construct a joint source/owner/phase-correct circuit with:
1. Full arbitrary independent input/output operator equality, both forward and ordinary inverse-transpose, including absolute Gaussian phase.
2. One genuinely productive rank-five output with a legitimate independent owner and correct source account.
3. One legally available rank-nine centre child, replacing the prior rank-eight job (no hidden extra children, cleanup or phase costs).
4. Complete scalar, owner, idle, source, host, transport, monomial-address, physical tape and precision invoice.
5. New per-call ledger and 16-pair consumer profile, exact mirror/root proofs and two independent moments, finite uniform all-size compiler, ordinary BIT/outer 54 gates and analytic/rounding closure.

**If the only implementable exchange occurs once per local supplier instead of once per whole p16 invoice**, multiply both rank deltas by the actual 18 supplier calls and independently recheck every main/idle/source obligation. No duplicate productive credit is allowed.

## Reproduce

```sh
python -I -B research/p16-k00302017-rank-exchange/rank_exchange_screen.py
```

All exact moment signs are fail-closed, but `candidate_native_positive_operator_admitted=false`, `new_kappa_proved=false`. CI must run the script on Python 3.11 and 3.13; hosted runs are not a scientific proof.

## Related clean PR submission

Separate **clean upstream-based** fork branch `research/p16-tight-transfer-upstream-clean-20261022` has four files and proves only the tighter **conditional arithmetic** κ=0.0030201659769. GitHub's API returned a **403 Resource not accessible by integration** when creating the upstream PR. The branch is pushed, but the PR remains to be opened by the user or a GitHub credential with PR-write scope. This clean branch must not be conflated with the present unattained κ target.

**This project has NOT reached κ=0.00302017.**

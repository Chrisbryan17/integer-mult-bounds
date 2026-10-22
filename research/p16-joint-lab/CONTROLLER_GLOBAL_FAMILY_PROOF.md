# Global P16 controller-family barrier and next valid breakthrough target

**Research date:** 2026-10-22. **Status:** proved restricted structural exclusion; NO new κ, NO new physical supplier. Original developer/contributor attribution unchanged. Author @Chrisbryan17 with substantial GPT-6 assistance, Apache-2.0.

## Source pins

- Source selected PR #4470, `CrocSwap/integer-mult-bounds@b9a13c1673e0e9697de410de16e8bbf3207a7363`, `research/joint-helper-lattice/PROOF.md` and `RESULT.json`.
- Controller formula source `research/query-thinned-controllers/controller.py`, function `inventories()` (PR #4440). Native local target histogram `{4:28,7:7,8:47,9:326}`, paid `{1:2237,2:388,3:494,4:147,5:36,8:8}`.
- Selected conditional `κ=0.00302015`; raw-root bracket `0.0030201659770 < κ_raw < 0.0030201659771`. Open PR #4535 is a distinct all-size transfer proposal.

## Exact theorem (all p, not a finite parameter sweep)

Fix the selected native supplier, all 112 ports, `p+2` full native stages, `p-1` thin query stages and the PR #4440 prefix/suffix interval cost formula. Let p be any integer >=2 and a any integer with 0<=a<=p-1. With `t=1-κ`, define the selected native local moment surplus

`L(t)=sum_{r} H_r*r^t - sum_r P_r*r^t`.

The complete controller moment surplus for these fixed design rules is

`S(p,a,t) = (p+2)L(t) +224*(8p+17)^t -112*(p-1) +224*[sum_{j=1}^{a} g_j(t)+sum_{j=1}^{p-1-a} g_j(t)]`

with `g_j(t)=(8j+9)^t-(8j+8)^t`.

For `0<t<1`, strict concavity of `x^t` makes `g_j` positive and strictly decreasing. Consequently the two arms are optimal when their lengths differ by at most one. For those balanced arms the next-pair surplus increment is

`S(p+1)-S(p) = L(t)-112 +224*[(8p+25)^t-(8p+17)^t] +224*g_floor((p+1)/2)(t).`

The main increment decreases strictly with p, while the last term is nonincreasing. **Therefore S(p) has strictly decreasing successive differences for every p>=2**, with no numerical cutoff.

The accompanying `controller_family_theorem.py` uses the exact rational outward moment enclosures of `frontier_rational_gate.py` (28-term positive atanh log bounds and alternating exponential polynomials, outward 10^-20 integer quantization). Uniform over the published raw-root bracket:

- `S(16)-S(15)>0`, about +0.285137.
- `S(17)-S(16)<0`, about -0.008270.
- Therefore **p=16, a=7 or 8 is the global optimum** for this *entire* fixed-native/controller family.
- At κ=0.006, `S(2)<0` (about -175.453), and `S(3)-S(2)<0` (about -30.199). Strictly decreasing pairwise increments imply **S(p,a)<0 for all p>=2 and all a**. Thus none reaches the double-κ moment screen while retaining these design rules.

This is not an impossibility theorem for integer multiplication, other scalar DAGs, controllers, or productive helper mechanisms. A winning algorithm **must change at least one frozen premise**, not simply add pairs or redistribute the two arms.

## Critical caution about previous cost-only targets

The earlier model found that deleting 12 rank-64 idle paid jobs *without replacing them* or producing six additional rank-9 helper outputs per full native call with only six paid rank-1 jobs would make a κ=0.006 moment inequality favorable. Neither is a valid operator construction. Under the existing inventory, deleting the idle work changes target-minus-paid rank mass by 768; the helper proposal changes it by 864 across 18 calls and requires 108 new independently owned input fields. Both alter the declared source/whole-controller mass and ownership boundary; no bookkeeping-only credit is permitted.

**Another auditing trap:** pinned `CONTROLLER.json`'s embedded `invoice` contains the prior native local helper/paid basis: its paid count is 69,012. Selected `RESULT.json` recomputes the actual 64,620-job invoice after installing the joint helper patch. The upstream `verify.py` explicitly replays the controller and recomputes the chosen native profile. This intentional fixture distinction is **not by itself a selected proof discrepancy**. Every new search must compare against the final selected 64,620-job bill, not the stale fixture invoice.

## Executable reproducer

```bash
cd research/p16-joint-lab
python3 -I -B frontier_rational_gate.py
python3 -I -B controller_family_theorem.py
```

The code emits `CONTROLLER_FAMILY_CERTIFICATE.json` with signed exact intervals, theorem scope and explicit `new_kappa=false`. CI should run Python 3.11 and 3.13; a committed workflow is not a confirmed hosted CI pass.

## New search mandate

The next mathematical candidate must change **controller idle geometry, productive terminal ownership, stage reuse, or the native scalar dependency DAG** while preserving exact Laurent matrices, both Clifford orientations, 112-port independence, paid owner/idle/source/tape costs and full all-size/BIT transfer. An isolated rank moment gain is a *screen*, never an admitted result. Prefer replacing at least one rank-64 idle obligation with an operator-equivalent shared physical computation, accompanied by exact source/host witnesses; if it cannot be constructed, record the obstruction rather than delete its bill.

**The selected conditional κ remains 0.00302015. No claimed new record.**

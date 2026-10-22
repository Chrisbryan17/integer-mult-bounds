# P16 joint native/controller optimization campaign (2026-10-22)

**Status:** New source-pinned exact-rational root/moment verifier committed and locally executed. A broader local research ZIP contains phases A–E, 1,688 screened scenarios, 160 dependency-cone mutation tests, 250 toy Laurent controller rewrite tests, 80 heterogeneous worker proof jobs and nine unit tests. Those *additional files* are provided as an artifact in the associated research conversation; they have not all been pushed to this branch. This README makes that distinction explicit.

**Baseline:** CrocSwap/integer-mult-bounds, selected source-bound #4470 commit `b9a13c1673e0e9697de410de16e8bbf3207a7363`, maintainer-selected conditional κ = `0.00302015`. Open #4535 claims `0.003020165`. Selected PRs and all inherited foundations are unchanged.

## Executable exact rational gate

Run `python3 research/p16-joint-lab/frontier_rational_gate.py`. It uses the complete 10,928-productive / 64,620-paid approved histograms and outward **pure Fraction** moment bounds, not approximate floating-point comparisons. It strictly brackets the published raw root by κ=0.0030201659770 (positive) and κ=0.0030201659771 (negative), proves the same full baseline moment negative at κ=0.006, and proves the nine-axis fixed-count/fixed-mass concavity shape envelope is also negative at 0.006.

The gate separately computes **counterfactual** minimum changes that would make the moment favorable at 0.006: deleting 12 paid rank-64 idle jobs *without replacement*, or adding six rank-nine productive helper outputs **per** native call paid by exactly one rank-one child per output. These are **NOT admissible constructions**: neither provides the necessary operator, source/owner and tape proof. No improved κ is claimed.

## Local laboratory phases

- **A, Silicon Safe persistent invariant cache:** reproduce source histogram checks; immutable cached rank moments vs direct scoring, identical results.
- **B, dependency-aware exact incremental replay:** 600 signed ADD nodes, 160 mutations, around 95.3% fewer re-evaluated nodes; no approximate bounded replay.
- **C, confidence-scheduled rational checks:** candidate scores affect verification order, not proof truth. Deferred candidates are not rejected. Twelve top scenarios checked with independent exact rational moments.
- **D, fused evaluator / exact Laurent microkernel:** 250 independent 2×2 Laurent shear rewrites, complete polynomial matrix parity, illegal noncommuting swaps rejected. This is **not** the full P16 112-port controller.
- **E, heterogeneous CPU scheduling:** 80 GF(2), signed-DAG, Laurent and exact-moment tasks; exactly identical content results under one and two worker processes. DeepInfer is an architectural reference, **not** a runtime dependency.

1,688 relaxed cases were screened across controller-idle changes, added productive helpers, fixed-mass scalar rank redistributions, heterogeneous native supplier mixing, and BIT/outer boundary changes. Some favorable moments arise only because physical costs were hypothetically reduced; no whole-word alternative was admitted.

**Open theorem gates:** actual native/controller word materialization, 112-port Laurent parity, 408 helper independent output credit, both phase-correct physical orientations, chronological owners, full paid recursive cost with source/tape/precision, two exact full-profile engines, BIT and 54 outer predicates, and uniform all-size correctness/rounding. No selected κ update.

**Attribution:** This research is for @Chrisbryan17 with substantial GPT-6 assistance, Apache-2.0. Predecessor contributor credits are preserved, especially zxv, Cinna Davis, Jacob Alan Sussman and Ali Romman. The new code is a research audit, not a claim that the upstream algorithm is invalid.

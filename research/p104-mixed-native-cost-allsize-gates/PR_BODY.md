## Scope (no new κ)

New P104 single-sign mixed-carrier construction, extending merged #2844, #2820, #1125 and #968. Each of the 12 cube edges has 27 target reads requiring one sign and exactly one exceptional opposite-sign read, at the six-vertex complement of the **antipodal edge**. Retaining the dominant sign alone and falling back to the two original terms at that exception gives a new restricted eight-helper construction. This is not a native supplier.

## Exact finite results

All 7,168 decoder checks and 2,408,448 signed pair-read incidences passed in the local source-bound E8 reconstruction; an additional in-repo verifier is provided. Literal signed E8 104-target abstract trace restores all originals and zero-cleans all eight auxiliary registers.

| Return-home model | Helpers | ADDs | Frame rank | ADD-rank mass |
| --- | ---: | ---: | ---: | ---: |
| Unmixed reference | 0 | 416 | 2224 | 1112 |
| Previous two-sign bank | 16 | 320 | 1520 | 824 |
| New best eight-edge single-sign bank | 8 | 292 | 1496 | 764 |
| All twelve single-sign edges | 12 | 288 | 1504 | 776 |

An exhaustive 4096-bank search certifies a 14-point nondominated cost frontier. One prepared single-sign helper costs 12 frame-rank units including source movements, creation and zero restoration. The optimizer includes the unique wrong-sign target; it does not silently give that target a free valid mixture.

## Reproduce

```sh
python3 -I -B research/p104-mixed-native-cost-allsize-gates/run_all.py
```

This runner authenticates the merged #968 predecessor file by Git blob, executes the all-decoder signed-edge census, the 4096-bank cost verifier and the Pareto checker. A **separate local archival package** also records the full abstract 104-target event trace, selected #1094 rational moment and gate ledger; those files are not all mirrored in this PR branch, so do not claim an in-repo cold replay of the complete native/price/all-size bundle.

## Open obligations and review boundary

The native source-chart/COPY/phase/gate compiler, arbitrary dirty inverse orientation, physical source access, exact recursive child histogram, globally hosted width/tape/precision, selected complex/bit double-engine moment, and uniform all-size integer-multiplication theorem are all open. Our older frozen P104 optimistic profile has less than two rank-one units of moment slack per call, conditional on its other costs being unchanged. Nothing here claims a new multiplication exponent.

Predecessor credit: #968, #1125, #2820, #2844, original CrocSwap native-channel research. Prepared for @Chrisbryan17 with substantial GPT-6 assistance; Apache-2.0.

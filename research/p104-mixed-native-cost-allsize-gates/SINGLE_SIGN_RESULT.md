# P104 signed E8 edge asymmetry: single-sign carrier improvement

**New scoped finite result.** Built on merged #2844 (signed mixed P104 bank), merged #2820 (survivor projections), and the reviewed #968/#1125 decoder family. No native supplier, κ claim, or all-size theorem.

## Exact all-decoder sign census

An independently reconstructed frame-pair census checks all **7,168** admissible P104 decoders, **12** cube edges per decoder and **28** targets containing each edge, or **2,408,448 signed edge/target incidences**. Each edge always has exactly **27 targets of one relative sign and 1 target of the other**.

The unique minority-sign target is the **six-vertex support complementary to the antipodal edge**. For edge (i,j) in the canonical F2^3 cube chart, its antipodal edge is (i XOR 7, j XOR 7). A target with the majority sign may read one prepared mixture m=x_i+s_ij x_j; the exceptional target must use the two originals (or another independently suitable mixture). Both signed mixtures are unnecessary in this scoped target-selectable scheme.

All decoder/edge cases have positive minority count. So *deleting one signed variant while retaining the old target matching unchanged* is invalid. The revised matching explicitly excludes the exceptional edge/target incidence.

Across all decoders, the sign splits have the exact distribution:
- **53,760** decoder/edge instances: 27 equal-sign demands, 1 opposite-sign demand;
- **32,256** instances: 1 equal-sign demand, 27 opposite-sign demands.

The underlying sign lemma is certified by the standalone local `signed_edge_variants.py` and is **not independently reproduced by the published bank-only optimizer**. Reviewers should run the complete local archival evidence before accepting the family-wide claim.

## Corrected full abstract charge

One signed helper per edge, prepared from original carriers in the rank-two home frame, requires **two build ADDs and two inverse cleanup ADDs**. Its complete frame-move rank bill is **12 per edge**, including both originals' climbs and returns in build and cleanup, and the helper's zero-to-rank-two and rank-two-to-zero movements. It is **not eight**.

For q prepared edges, and for each target with n required terms and p disjoint permitted prepared pairs, the explicit *unoptimized home-return* schedule costs:

- Frame-move rank: `832 + 12q + sum_targets(n(n-1)-2p(n-p))`;
- Signed ADDs: `4q + sum_targets(n-p)`;
- Rank-weighted ADD mass: `8q + sum_targets(n(n+1)/2-p(n-p))`.

The target order is all unused original singletons **first**, then its mixed pairs. Reversing the order can invalidate the frame-cost formula. The literal `Trace` simulator independently replays these operations and returns all eight originals unchanged and every auxiliary to zero.

| Restricted scheme | Helpers | Signed ADDs | Frame-move rank | Frame-weighted ADD rank |
|---|---:|---:|---:|---:|
| Unmixed return-home reference | 0 | 416 | 2224 | 1112 |
| Earlier eight-edge **two-sign** rank-two bank | 16 | 320 | 1520 | 824 |
| New best eight-edge **single-sign** bank | **8** | **292** | **1496** | **764** |
| All twelve **single-sign** edges | 12 | 288 | 1504 | 776 |

The single-sign eight-edge bank wins on the sum of frame-move and ADD-rank masses, and the 4096-case search has six symmetry-related winners. The all-twelve bank achieves the lowest ADD count but has slightly higher rank costs and more helpers. These are abstract cost measures, not paid recursive operations. Neither construction is being compared to an optimized physical incumbent supplier.

**Negative/verification boundaries:** The final signed 104-output trace was checked using actual E8 row coefficients, not synthetic alternating signs, and reverses its helper preparations exactly. This does not prove scalar/phase-native gate legality, all 7168 complete physical traces, available source access, live host count, recursive child pricing, or the all-size multiplication theorem.

## Division of remaining work

1. **Native owner:** adapt the general canonical `Gamma_W` frame compiler and independent signed Clifford/phase interpreter already checked for the native P104 channel. Emit one *actual* two-source rank-two mixer, check arbitrary initial dirty registers and source/target adapters, then replay the full eight-helper event word in both orientations.
2. **Invoice owner:** bind emitted actions to literal positive-rank children, source operations, helper owners, full hosting and tape. Re-run both selected exact-moment engines. The historical unchanged P104 knob has less than two spare rank units per call, so any viable construction needs offsetting savings elsewhere.
3. **Theorem owner:** prove uniform recursive realization, error/precision and tape bounds, bit H1–H5 compatibility, analytic transfer and correct rounding. A finite signed-decoder census does not discharge these obligations.

Prepared for @Chrisbryan17 with substantial GPT-6 assistance. Apache-2.0; preserve predecessor attribution.

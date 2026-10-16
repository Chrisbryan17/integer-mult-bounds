# P104 optimal intersection routing: finite rank proof and physical host obstruction

**2026-10-16. Status: scoped finite construction PASS; full supplier and multiplication theorem OPEN.** Research for @Chrisbryan17 with substantial GPT-6 assistance. Apache-2.0. This branch preserves source provenance, reviewed upstream #1094 conditional κ = 0.001672660197076918, merged #2820/#2844 and the Ali Romman #968/#1125 E8 lineage. It builds on the pinned borrowed-dirty, unimodular source and dyadic numerator words of research/p104-source-unimodular-inplace-20261016. It does not modify upstream, selected certificate or predecessor packages.

## New theorem with precisely stated restrictions

Let V be the 9-dimensional binary physical E8 label space. A register's admissible elementary chart transport is an edge between **nested subspaces** A and B, priced |dim(A)-dim(B)| as one positive native rank-r child. Its prescribed scalar ADD/SIGN and source entry/exit events are held in the exact original chronological order; each event specifies the register's exact required chart. Transport can be retimed between successive uses of the *same* register, and arbitrary intermediate binary subspaces are allowed. No source/owner/tape/precision costs are assigned in this relaxed theorem.

Define the subspace distance

    d(A,B) = dim(A)+dim(B)-2dim(A intersection B).

It obeys the triangle inequality: for any W,
dim(A intersection B) >= dim(A intersection W)+dim(W intersection B)-dim(W).
Therefore every nested-frame path between A and B costs at least d(A,B). The explicit path A -> A intersection B -> B consists of nested moves and attains this bound. Since scalar/source anchor frames and their order are frozen, each register's consecutive segments add independently. Summing their distances is thus the exact least **rank mass** in the stated relaxed fixed-anchor model. This does not minimize the number of children, physical idle resources or the entire supplier.

Both actual signed-E8 104x104 typed numerator words attain exactly **1238 internal rank units**, down from 1512, through 19 additional canonical intersection frames. The original 208 separately verified source-entry/exit rank-one children remain charged, so the local positive-child **rank mass is 1446 rather than 1720**.

| Literal finite item | Prior G/2 | Retimed G/2 | Prior I-G/2 | Retimed I-G/2 |
| --- | ---: | ---: | ---: | ---: |
| Internal nested transport occurrences | 772 | **687** | 772 | **703** |
| Internal rank mass | 1512 | **1238** | 1512 | **1238** |
| Source port rank-one transport children | 208 | 208 | 208 | 208 |
| Local positive native calls | 980 | **895** | 980 | **911** |
| Local native rank mass | 1720 | **1446** | 1720 | **1446** |
| Internal descending calls | 204 | 162 | 204 | 170 |
| Internal descending rank mass | 340 | **203** | 340 | **203** |
| Extra clean aggregate scratch registers | 0 | 0 | 0 | 0 |
| Signed unit ADD and scalar sign events | 1298 / 12 | unchanged | 1506 / 28 | unchanged |

The rank profile INCLUDING all 208 source legs:
- G/2: {1:564, 2:228, 3:34, 4:33, 5:24, 6:12}.
- I-G/2: {1:596, 2:212, 3:34, 4:33, 5:24, 6:12}.

**A second lower bound:** 203 *internal* descending rank units are forced by the same fixed scalar/source anchor frame pairs. The selected intrinsic source-to-zero entrance requires another 104 descending rank-one children. Thus this exact word requires at least **307 descending rank units** under the stated source interface. A strictly nondecreasing register chart owner cannot implement it unchanged. This is a *fixed-anchor/source-contract obstruction*, not a universal impossibility theorem for P104 or integer multiplication; a changed source protocol or new owner rule may escape it.

## Checks that are actually completed

1. Producer emits both full chronological event streams and all 19 new binary intersection frames. Every new transport is nested, has positive rank and paid rank equal to dimension difference; no original scalar, sign, source or terminal event is deleted.
2. Independent checker (does not import the router) replays all 216 formal inputs, exact 104x104 signed E8 Gram numerator and full side correction, sources and eight arbitrary-dirty helper identities, both terminal frame maps, and the per-register lower bound.
3. True physical E8 Gram isometry: all 14400 root pairings and 104 sink planes from predecessor. All **485 distinct G/2** and **493 distinct side-word** routed Clifford recipes are independently checked: action on all 18 symplectic generators plus exact Gaussian amplitudes for address 0 and nine singleton addresses. This criterion determines each Clifford including global phase. Each recipe has exactly one positive rank-r child with explicit left/right selected-format Gaussian monomials. Deliberate phase, signed-C and address-offset mutations are rejected. These are complete-operator checks but not full 512-column brute-force checks on every new recipe.
4. Eager descent / late ascent is a second schedule using the **identical** native edge multiset and scalar anchors. G/2 at 1518 matched scalar/source milestones: peak sum of frame dimensions 536 -> **520** and cumulative sum 331182 -> **319629** relative to lazy intersection routing. Side at 1742 milestones: 536 -> **520**, sum 334766 -> **323117**. These sums are event-index **chart-rank occupancy proxies**, NOT physical memory, tape, time, idle costs or an owner map.

## Honest supplier comparisons

Reviewed upstream research/p104-native-channel (PR1972, reviewed #1991) proves a complete native **G/2** low-rank *finite local* word with 1410 native transport occurrences, rank mass 2368, 2624 scalar ADDs and 72 dirty helpers plus owned private copy. Our retimed **G/2 integer-numerator** word has 895 calls, rank mass 1446, 1298 ADDs and eight borrowed dirty helpers; **the caller representation is different**, as are source mutation, early target rights, private owner contracts and unpriced address/phase work. These numeric differences are NOT a legitimate full recursive invoice saving or selected κ gain. Do not compare the I-G/2 side directly with the G/2 baseline as an equivalent component.

At the historical selected complex b = 67018507072324140917/40000000000000000000000, the unnormalized nine-axis rank-moment sum `sum n_r (r/9)^(1-b)` is about 263.74058 for the #1991 G/2 profile versus 161.08503 for this new local G/2 profile. This is a **conditional relaxed component-only screen**, not the selected m=73 global moment and not an admitted recursion theorem. Unknown source, host/idle, tape, precision, monomial and endpoint costs may invalidate the gain.

## Required next work

- Resolve **307 unavoidable descending rank units** against the selected global chronological owner/bridge/deadline rules; no assignment is asserted. Eight borrowed dirty helpers, 104 mutable source roles, 100/104 early target writes and all monomial data movements must be covered, with exact live owners. Retiming changes time spans, so prior owner maps cannot be reused without fresh checking.
- Conjugate Delta physical inverse-transpose and exact canonical caller adapters must be re-emitted for the retimed words (the telescoping chart identity is exact, but selected owner paths and costs remain open).
- Price both sides' native children, source/host/idle/residual and phase/monomial operations, signed scalars, dyadic target encoding, bit growth, tape and rounding. Compare with the **strongest selected complete supplier**, not only #1991.
- Only then run two independent exact recursive moments, joint bit H1-H5/outer inequalities, uniform all-size realization and analytic transfer. Keep the reviewed conditional κ unchanged.

### Replay

From research/p104-exact-clifford-factor-pass regenerate the pinned original E8 native word, borrowed-dirty word, complete Gram channel, unimodular 104-source word, typed G/2 and side word. Then:

```bash
python -I -B p104_intersection_router.py
python -I -B p104_verify_intersection_router.py
python -I -B p104_eager_idle_retime.py
python -I -B p104_physical_e8_isometry.py
python -I -B p104_minimal_symplectic.py
python -I -B p104_exact_native_factor.py
python -I -B p104_rank_r_native_recipes.py
python -I -B p104_routed_native_audit.py
```

New cold two-Python GitHub Actions workflow is committed; remote CI outcome must be checked independently. **No new κ, no full multiplication theorem.**

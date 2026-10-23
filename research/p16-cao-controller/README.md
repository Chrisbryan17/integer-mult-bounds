# Cao P16 controller restructuring: exact 16-split cost audit

The retained source controller has 16 pairs, 18 full native calls, 15 query-shears, and a prefix/suffix split parameter `a+b=15`. Cao #4610 uses `a=7,b=8`.

`controller_split_audit.py` reads Cao's **frozen** native receipt and exact full arithmetic certificate, reconstructs the source `controller.py:inventories()` main/idle histogram for each of the 16 choices, verifies the original invoice byte-for-byte at `a=7`, and prices all 16 complete paid-versus-productive histograms with 70-digit decimal arithmetic at κ=0.0030217758. Every candidate retains 10,928 productive fields, 64,404 paid calls, and exactly 752 rank-mass surplus.

**Result reproduced on the Dell:** `PASS_16_SPLITS_EXACT_SOURCE_HISTOGRAM`. The 7/8 and 8/7 allocations tie for the best moment; every other split is strictly worse at Cao's κ. The original split's positive whole moment is 0.00001749755253235353507…; the nearest choices a=6 or9 have negative moment -0.14760192828564798754… . The tied a=8 histogram is NOT automatically an independently factored or executable alternate controller.

This is a **complete screen of the retained 16 prefix/suffix choices only**, not a proof of global controller optimality. A genuine next controller win must vary the 18 thick stages or the exact query/idle placement and refactor the 32x32 rational Laurent boundary identity. Every replacement must charge 18 native calls, selected target credits, 15 queries, 15 idles and all sign/route/precision costs. The source code intentionally does not claim κ improvement.

Run against frozen PR4610 checkout:
`python -I -B research/p16-cao-controller/controller_split_audit.py /path/to/frozen-repo`

Source `CrocSwap/integer-mult-bounds@20bb93cd990d2ff683e4d0fc56b87a42cd5d3296`. Credit Cao Yifan, Cinna Davis, zxv, Jacob Alan Sussman and predecessor authors. New experiment prepared for Chrisbryan17 with GPT-6 assistance, Apache-2.0.

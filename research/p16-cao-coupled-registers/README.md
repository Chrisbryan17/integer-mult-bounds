# Cao P16: coupled-register redesign and physical bridge gates

**Research checkpoint (2026-10-23).** Frozen Cao Yifan #4610 native source commit `20bb93cd990d2ff683e4d0fc56b87a42cd5d3296`, canonical payload SHA256 `cfcd36b40326d7a5815e1db5313444379b3fb756b27d5201c561574c085cc0dd`.

### Executed findings

- Reproduced all **155** source-native same-register `H1 / scalar(s) / H1` attempted retimings. **Every one has a sibling-register chart obstruction**. Of these **108** are equal-rank, incomparable binary frames and **47** require a rank decrease.
- `source_bound_bridge_replay.py` builds a **specific invertible GF(2) 9×9 G map and exact inverse for every one of the 108 equal-rank pairs**, verifies every one of their 512 possible input bit-vectors, and confirms each G sends the actual source frame to the target frame. The 47 rank-loss cases cannot be repaired by an invertible G alone. **These are transport maps, not verified full native rewrites.**
- The accompanying full experiment bundle tests two larger models on the original 21,449-event word: upward GF(2) chart propagation across *all* touched registers and all signed native G maps; and a bounded bidirectional contact-graph search with GF(2) meet/join edits on **17,693 active nodes, 34,398 constraints**, up to **350 states per seed and 24 changed contacts**. Neither admitted an improved paid histogram for these 155 seeds.
- A model-specific algebraic check rules out substituting two independent `F_q × F_q` products with one `F_{q²}` **field** product surrounded exclusively by invertible linear encoders and decoders (zero-divisor obstruction). **It does not establish the actual Cao H2 child has this same algebra.** An exact `F3` check examined all **2,304** pairs of 2×2 invertible input encoders.

**No higher κ has been established**: Cao's conditional `κ=0.0030217758` is unchanged, and the desired hypothetical `κ=0.0030220` remains conditional on a paid, dual-valid, phase-exact `H1+H1→H2` physical fusion.

### Reproduce source-bound bridge reconstruction
```bash
python -I -B research/p16-cao-coupled-registers/source_bound_bridge_replay.py \
 --source /path/to/frozen-Cao-PR4610-checkout \
 --output /tmp/COUPLED_BRIDGES.json
```

Python standard library only. Source dependency: unchanged upstream `research/warp-interface-20261022/warp_merge.py` and its frozen original native dependencies. Full local beam-search code, tests, source receipts and explicit candidate list are preserved in the `Cao_P16_Coupled_Register_Reengineering_2026-10-23.zip` research artifact; the standalone source-bound bridge replay here regenerates the central constructive result without that prior receipt.

### Further admission gate

Take one algebraic G/G⁻¹ pair and **construct a coupled scalar/warp program whose entire operator remains exactly unchanged on arbitrary inputs**. Charge every restoration, owned buffer and frame climb; regenerate the full forward/backward 632-column words, verify absolute phases, and only then price the full P16 invoice and compiler. Simply presenting an invertible G is insufficient.

Credit Cao Yifan/intqwq #4610, Cinna Davis #4470, Dugongue, zxv, Jacob Alan Sussman and all inherited contributors. New scoped research prepared for Chrisbryan17 with GPT-6 assistance; no practical speedup or independent complete theorem verification claimed.

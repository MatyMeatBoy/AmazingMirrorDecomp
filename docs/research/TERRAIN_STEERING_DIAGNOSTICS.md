# Rejected EU terrain compiler-barrier diagnostics

These experiments are diagnostics only, explicitly separated from the defined C reconstruction and its layout proof. They are not proposed source, historical evidence, matching C, or yellow-count additions. Core source is untouched. The pinned agbcc59b966ed1b8f371856dcf99f1546c2fe89c678ca, original flags and EU preprocessing profile remain unchanged.

Two source baselines were used: A is the preserved defined3588-byte draft (frame0x3C); B is the scoped-destination/inline-wrapped-point3584-byte experiment (frame0x60). The reference is3596bytes, frame0x3C. A and B both lack12 signed-halfword bounding-array loads relative to the reference. The earlier diagnostic notes must not be read as a0x40 frame claim for B.

Each modification was independent. `volatile` applies only to the initialized local signed16 bounding array. The empty input-memory asm is inserted immediately after each four-component object-bound update, with only `"m"(array)` input. An additional explicitly artificial read/write-memory operand (`"+m"(array)`) was tested to distinguish observation from cache invalidation. The latter claims a write that the empty instruction does not perform and is particularly unsuitable as recovered game source.

| Baseline / modification | Function bytes | Frame | First fixed divergence | Normalized instructions |
| --- | ---: | ---: | ---: | ---: |
| A / volatile local bbox | 3692 | 0x30 | 0xA | 1631 |
| A / empty asm, input memory | 3604 | 0x40 | 0xA | 1585 |
| A / empty asm, read/write memory | 3586 | 0x30 | 0xA | 1579 |
| B / volatile local bbox | 3646 | 0x40 | 0xA | 1614 |
| B / empty asm, input memory | 3600 | 0x64 | 0xA | 1582 |
| B / empty asm, read/write memory | 3502 | 0x40 | 0xA | 1565 |
| Reference | 3596 | 0x3C | n/a | 1561 |

Volatile does not recover the desired signed-load pattern: the reference has44 more LDRSH instructions, while the candidates use many LDRH loads plus explicit shifts. Input-only memory asm leaves the deficit of12 LDRSH intact and adds four stack stores plus pointer setup. The read/write operand forces reloads, but overshoots by four LDRSH and adds eight LDRH accesses at bounding offset2; it also changes signed-byte object offset loading. None reproduces the initial pointer assignment or complete instruction stream.

All emitted call-symbol sequences match the reference. A's variants have267 branch instructions versus269 in the reference and their branch-mnemonic sequences differ; B's variants have269 and the same mnemonic sequence. This is only a sequence comparison, **not CFG/dataflow equivalence**: targets, registers, stack locations and intervening instructions still differ. Every complete fixed-byte comparison fails; no unique masked candidate site exists.

Removing all four empty-memory asm statements and recompiling restores the complete emitted text byte-for-byte to each corresponding original baseline (3588 and3584bytes). The checked-in defined candidate contains neither volatile nor assembly barriers. These negative tests do not justify retaining steering or widening progress credit. Scratch reproduction scripts/objects remain ignored under `build/research/terrain_barrier_diagnostics.py`, `terrain_input_diagnostics.py` and `terrain_diagnostic_compare.py`; no object, ROM payload or generated assembly is committed.


## Selective upper-limit diagnostics after the natural CFG repair

These tests were explicitly conditioned on the naturally repaired q-subobject variant's305-block/edge pairing. Each empty read/write-memory asm follows initialized object bounds; no game objects are volatile. With only bounds[2] as its memory operand,3600bytes/frame0x40 recover exactly four missing LDRSH; with only bounds[3],3600bytes/frame0x40 recover exactly eight. Both retain305 paired blocks and all actual edges. A final single asm with those two memory operands together recovers all12 missing LDRSH with no signed-load count excess, again3600bytes/frame0x40 and the same305 paired blocks.

This is not a match: the combined case still has3252 different fixed bytes, first0xA, and lacks the reference's high-half directional-point constants. It retains additional shifts/spills and different arithmetic; frame0x40 differs from reference0x3C. No asm is retained in the preserved candidate or contextual patch. The diagnostics isolate upper-bound promotion as a remaining issue independent of the far-right store-join repair; they do not establish a historically correct barrier or production implementation. The natural q-subobject source was freshly recompiled without barriers and preserved separately.

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

# European runtime and library verification

The production European profile now compiles the 24 archive members selected by
`linker.ld`, using the pinned agbcc commit
`59b966ed1b8f371856dcf99f1546c2fe89c678ca` and the original archive recipes.
This accounts for 56 C functions (10,106 bytes), 20 assembly functions (726 bytes),
and 56 alignment bytes. Assembly and alignment receive no C credit.

`library_metadata.py` does not read a ROM. It records the exact archive member,
compiler binary, flags, preprocessed input, complete header dependencies, source
hashes, ELF sections and symbol aliases. The double-precision member uses both
original floating-point bit-order and word-order defines. Members sharing one
source file retain separate identities and compiler profiles.

The European matcher anchors the final 84-byte `memset` body uniquely at
`0x0815C6C0`, ending at the independently established `0x0815C714` code boundary.
The linker-selected order and word-aligned complete member sizes determine the
preceding library positions. Every member still requires complete byte and
relocation proof; adjacency alone does not award credit. This also locates short
members whose instruction bytes would be ambiguous in isolation.

Regional runtime changes preserve the B8KP game identifier, saved-language
validation (English through Italian, including Spanish), European link protocol
constants, submenu display-enable timing, and multilingual multiboot tables.
The Area Map and title sources use European layout and assets. Unknown fields
and symbols retain unknown names. Existing USA source branches remain available;
isolated USA object comparisons are not a USA full-ROM verification.

Partial-function verification maps each complete referenced data object
independently. It rejects unknown extents, contradictory mappings and overlaps;
it does not assume that all European objects retain one section-wide delta.
Short callbacks require a proven real caller relocation and complete target-body
comparison. Context from a rejected caller must never survive. Global callback
bindings must agree across callers even when the target body remains pending.

The recorded owner-local gate reconstructs all 16 MiB and compares every byte and
SHA1 against the owned European dump. Unsupported spans remain explicit raw-ROM
fallbacks. Thus this gate proves the credited source spans within a hybrid
reconstruction; it is not yet a standalone native European link from recovered
source. CI receives source evidence and reports, never the owned ROM.

The fixed C metric keeps its original denominator of 1,427,032 executable-region
bytes. Original assembly, alignment and unresolved gaps remain outside C credit.
Function inventory totals describe recovered source instances, including separately
listed libraries and auxiliary programs; they are not a definitive count of every
physical function in every embedded European program.

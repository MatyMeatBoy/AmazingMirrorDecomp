# Retained European assembly

The owner-local European reconstruction now assembles and proves the original
startup, BIOS wrappers, m4a assembly, MultiSio assembly and the still-unmatched
terrain routine. These remain assembly; they add **zero C credit**. The terrain
routine's C draft remains pending independently of its original assembly proof.

`EU_RETAINED_ASSEMBLY.json` records the six emitted code fragments, their complete
text hashes, object hashes and actual relocation evidence. Together they cover
7,420 bytes. Startup is split into the ARM entry instruction at offset 0 and the
body at offset 0xC0. The 188-byte cartridge header at offsets 4 through 0xBF is
excluded. The entry must be the original unconditional ARM branch to 0xC0;
header bytes are never masked into a code match.

The m4a input contains one `R_ARM_THM_JUMP8` relocation. Its handling follows
the [Arm ELF ABI's static Thumb-16 relocation rules](https://github.com/ARM-software/abi-aa/blob/main/aaelf32/aaelf32.rst).
Only its immediate byte is variable. The branch condition and opcode remain
fixed comparison evidence. The object addend must be -4; the symbol must be a
Thumb function in the same complete text input; its decoded ROM target must
equal the ELF-derived local address. External targets and partial-text proofs
are rejected. Emission checks signed displacement range and preserves the
original condition. This is relocation support for original assembly, not an
instruction patch or a compiler-steering device.

Six focused tests cover signed displacements, invalid conditional opcodes,
overflow, alignment, local-target disagreement, partial/external rejection and
the startup/header boundary. The complete 107-test reporting suite passed.
The subsequent owner-local gate accepted 227 units and reproduced all 16 MiB
and the expected European SHA1; verified C remained 1,415,336 bytes (99.1804%).

Reproduce with the pinned compiler installed and the owned B8KP dump using
`make record-eu`. The full generated `build/eu/receipt.json` contains the
assembly units in `modules`; the compact production receipt remains focused
on C credit and source provenance. The JSON here is a research record, not a
replacement for a fresh gate. The reconstruction still has explicit raw
fallbacks and is not yet a standalone native European link.

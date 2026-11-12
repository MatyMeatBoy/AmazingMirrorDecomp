# European primary decompilation

The user supplied an owned European ROM and explicitly chose Europe as our primary target, including Spanish and the original five selectable languages. Its identity is B8KP, revision 0, 16 MiB, SHA1 `6f478a455383a2a12378f292581dfd7300300700`. Search existing forks first, then maximize matching source reuse against that exact dump. Never substitute USA percentages for European results.

The fork search inspected build identity/checksum inputs across all 91 direct-fork branches. They retain USA/B8KE. KatAM-Randomizer has useful MIT regional address tables, imported with original notices as unverified hints; each inferred address and source span still requires independent binary evidence.

Reuse the pinned original C compiler and source as regional candidates. Match only fixed instruction/data bytes with actual supported ELF relocations, and prove local data, callback addresses, global/local definitions and RAM extents. Compile and relocate the source anew; never copy relocation-site instruction bytes from the ROM into credited C. Ambiguous or unsupported candidates remain raw pending spans. Reconstruct all 16 MiB and require byte equality plus the owned ROM SHA1 before granting C credit.

The executable boundary is offset `0x15C714`, established independently by the exact compiled final libc `memcpy` and `memset` objects. Exclude the 188-byte cartridge header. Code outside credited function spans stays pending, including libraries not reconstructed from C. Do not invent a denominator for the number of European functions or identified data formats.

Keep the original USA Makefile and source identifiers as a secondary reference. GNUmakefile selects the European default and explicitly delegates USA builds and editable-asset conversions. Legacy address-derived source identifiers retain their original names; actual EU addresses come from verified spans and bindings.

Public reports use a compact owner-local verification receipt with complete portable source fingerprints, raw binary source hashes, compiler/recipe provenance and per-span hashes. Missing or changed evidence clears C credit. CI validates that recorded evidence and regenerates European views plus a separate USA reference without acquiring the owned ROM. No ROM, extracted assets, objects or private source paths are published.

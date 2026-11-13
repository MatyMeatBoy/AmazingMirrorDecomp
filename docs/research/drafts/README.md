# Compile-checked readable drafts

These research sources are excluded from the default game build. A compilable draft is not a matching implementation or proof of semantic equivalence. Yellow accounting uses the independently identified reference function's extent, and must remain separate from verified matching C.

## Buddy terrain draft

`sub_0800F044.c` derives from sh1ftmaker's original `60bb564a0f46a856479ee3f56ae80bff648c5d3a`, through the current-type rebase in authored patch `3f92d3ab211bc1ac00909c20fee20def0cccdbd6` carried by `sh1ftmaker/katam-port` main `1249ebf6bc68e45b24cacc3050f27ffdcdac6bc2`. MatyMeatBoy's adaptation uses the current canonical headers, corrects the obsolete `u32` coordinate prototype to the actual `u16` declaration, and marks the provisional grid layout and cross-array pointer arithmetic for investigation. It does not assert that contiguous fields make those C accesses defined.

The source compiles and assembles with pinned agbcc `59b966ed1b8f371856dcf99f1546c2fe89c678ca` and the normal matching C flags. Its object text is 3,576 bytes. The existing reference assembly has 3,596 bytes and 28 relocations; exact relocation emission identifies its EU span as `0x0800F06C–0x0800FE78`, end-exclusive. The C does not have a complete masked EU match. At function offset `0xA`, the reference allocates `0x3C` stack bytes and the draft allocates `0x64`; subsequent register/spill differences remain.

The [evidence sidecar](sub_0800F044.evidence.json) records normalized-LF source and dependent-header hashes, compiler identity, precise flags, object/text hashes and the linked EU reference-span hash. The object itself remains an ignored local build artifact. Recompile if any recorded source/header hash changes before claiming that the draft remains compilable.

Example compilation from the repository root on MSYS2 (omit `.exe` suffixes on Linux):

```sh
gcc -E -iquote include -Wno-trigraphs -DMODERN=0 -I tools/agbcc/include -I tools/agbcc -nostdinc -DREVISION=0 -DENGLISH docs/research/drafts/sub_0800F044.c | tools/preproc/preproc.exe -i docs/research/drafts/sub_0800F044.c > build/research/terrain_isolated.i
tools/agbcc/bin/agbcc.exe -mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g -o build/research/terrain_isolated.s build/research/terrain_isolated.i
arm-none-eabi-as -mcpu=arm7tdmi --defsym REVISION=0 --defsym ENGLISH=1 -o build/research/terrain_isolated.o build/research/terrain_isolated.s
```

## Deduplication and other variants

The commented baseline terrain draft and the historical standalone terrain versions describe the same function. Count this EU reference span only once. The four existing readable `NONMATCHING` bodies for `sub_0802E78C`, `sub_0811A934`, `sub_0811AA80` and `sub_0811AB74` were already compiled and assembled against current declarations; their default assembly spans remain outside matching-C credit. Earlier Shotzo/effect variants duplicate those symbols, and the weaker engine drafts duplicate code already recovered by PR #411. They add no new yellow extent.

Native port audio/platform adapters are references for different execution targets, not newly compile-checked GBA function drafts. No additional yellow extent is assigned to them here. The combined default EU matching result is unchanged by storing these research files.

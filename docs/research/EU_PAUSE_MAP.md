# European pause-map reconstruction

Baseline: c7d295b, subsequent help-menu commits ab85386 and a94c6e2. Existing katam implementation remains attributed to its original contributors; regional reconstruction by MatyMeatBoy.

Europe factors common UI setup into AreaMapLoadUI at 0x08127398. Its language switch selects five distinct LZ77 tilesets (German 0x08368208, French 0x08366BE4, Spanish 0x0836AD68, Italian 0x08369790, English/default 0x0836C384). Explicit Japanese and English cases share the original default target. The source uses ordinary C and original compiler flags. No register steering, width changes or ROM patches were introduced. New externs identify only the graphics role directly established by the decompression destination and language switch; their editable asset recovery is outstanding.

The European map UI clipping rectangles have five language rows of five rectangles of four u16 coordinates. Area-title graphics pointer rows contain nine area pointers per language. Both use the existing u16 language minus LANGUAGE_ENGLISH. The repeated coordinate reads, bounds and loop order remain intact. USA declarations and implementation are retained under the original branch.

Pinned agbcc 59b966ed1b8f371856dcf99f1546c2fe89c678ca; original flags -mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g; CPP adds REGION_EU only.

Independently compiled European .text is 7560 bytes and has a unique complete fixed-byte match at 0x08126BFC using only actual supported ELF relocations as masks. All 24 function implementations are present. AreaMapLoadUI is232bytes, AreaMapChooseUI572bytes at0x0812715C, WorldMapPauseEnableUI172bytes at0x08127480, CreateAreaMap1656bytes at0x08127AFC. Individual strict proofs pass for AreaMapChooseUI (seven bindings) and WorldMapPauseEnableUI (five bindings). The helper has zero fixed-byte differences but old full-section local-data proof rejects its switch table. CreateAreaMap has zero fixed-byte differences but full proof rejects conflicting local section binding. Thus this dossier does not grant all7560bytes European C credit.

The complete local data references imply two different .rodata bases, 0x08365BC8 and0x0836B368; regional assets interposed among shared objects explain why a single section-base model is insufficient. A production proof must verify every referenced local object's complete bytes and relocations or recover the regional data layout. Matching text alone is insufficient.

USA compatibility: independent compilation of HEAD original and modified source without REGION_EU produces identical7556-byte .text, full .rodata and text relocation signatures. This is not the six-output USA ROM gate.

Experiments: simply removing inline from AreaMapEnableUI failed (1644-byte constructor with1197fixed differences). Recovering the common regional helper and typed language tables yielded the unique whole-text match. A local languageIndex variable restores the actual load-before-table address order naturally. The temporary metadata CPP recipe remains uncommitted.

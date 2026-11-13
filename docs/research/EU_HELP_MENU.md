# European help-menu code recovery

Baseline: c7d295b; owned B8KP rev0 SHA1 6f478a455383a2a12378f292581dfd7300300700.

The European loader indexes a five-row table at 0x08D6B59C by the existing u16 language minus LANGUAGE_ENGLISH. Each row has four eight-byte {tiles, tilesVram} entries. The region-specific declaration and natural local languageIndex recover this indexing while retaining the USA branch verbatim. No compiler steering or language-width change is used. Original katam contributors retain attribution for the existing implementation; regional reconstruction by MatyMeatBoy.

Pinned agbcc: 59b966ed1b8f371856dcf99f1546c2fe89c678ca. Flags: -mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g. CPP adds only -DREGION_EU to the original profile. The temporary metadata recipe is deliberately not part of this source commit; production must declare the regional profile explicitly.

European object .text is 4008 bytes, uniquely located at 0x08124084. All 14 functions have complete fixed-byte matches, with strict relocation and referenced-local-data proof in the full European gate. CreateHelpMenu spans 1428 bytes at 0x08124478; the out-of-line tile helper spans 52 bytes at 0x08124FF8. The remaining source-local data still includes USA graphics and is not claimed as European data recovery in this cohort.

Commands: python tools/progress/metadata_build.py --jobs 4; python tools/progress/eu_build.py (with the explicit local European CPP profile). Result: 172 objects, 1414060 executable section bytes; 1206 verified units, 1349856 credited C bytes, 94.59185217990907%; complete 16 MiB comparison and expected SHA1 passed. These totals describe this worktree and matcher version, not an attribution of every increase to this change.

USA compatibility check: independently compile HEAD's original pause_help.c and this source without REGION_EU using the same pinned compiler; compare .text, full .rodata and relocation signatures. All equal (.text 3916 bytes). This does not claim the original six-output USA ROM gate.

Asset follow-up: the 15 European tile blocks differ from all three USA payloads. Their 1024-byte consumer transfers and matching sprite animation metadata establish the 4bpp tile format; reconstruction as editable PNG and exact conversion roundtrip is a separate cohort.

## Editable European button tiles

Fifteen PNGs under graphics/pause_menu/helpmenu_buttons/eu preserve the original indexed pixels. Each is 32x64 pixels (32 tiles, 1024 bytes in tiled 4bpp). Consumers transfer exactly 0x400 bytes to OBJ VRAM, use the same verified sprite animation metadata and existing 4bpp rendering path. No palette colors or artwork were invented; converter grayscale displays indices only.

ROM order is German, French, Italian, Spanish, English, each B/SELECT/empty, at offsets 0x359A7C through 0x35D67C exclusive. Language identification comes from the five-row address table indexed by the existing language enum, not the physical order alone. EU_HELP_ASSETS.json records exact offsets, lengths and hashes. Conversion command: tools/gbagfx/gbagfx input.4bpp output.png -width 4; inverse: tools/gbagfx/gbagfx output.png roundtrip.4bpp. All 15 inverse conversions are byte exact. Intermediate extracted 4bpp files remain ignored under build/research, not committed.

With the EU declarations in original physical order, strict prove_module verifies the complete 4008-byte text and all referenced local data (44 bindings), including the formerly mismatching graphics. The USA declarations and assets remain unchanged. This is original game artwork reconstruction, with copyright retained by its original owners.

# European primary target and languages

The requested primary target is the European revision-0 release, game code `B8KP`, with Spanish preferred while preserving English, German, French and Italian. The owned local image is 16 MiB, SHA1 `6f478a455383a2a12378f292581dfd7300300700`. Its identity agrees with the [Game Boy hardware database's cartridge and dump record](https://gbhwdb.gekkio.fi/cartridges/AGB-B8KP-0/3615retro-1.html), which lists the five European languages. The ROM remains local and ignored. [The regional profile](../config/eu_profile.json) records identity and layout facts; it is deliberately not a build receipt or a completion claim.

The inherited source and normal linker map describe the USA `B8KE` release. Its original checksum and six-output comparison remain useful USA regression evidence, but a successful USA build cannot be presented as European verification. Regional C coverage requires evidence against the owned European image, including regional relocation values and complete function or module extents. Candidate drafts, names and a ROM hash alone establish no C coverage.

## Search for an existing European base

The direct-fork audit found USA build profiles across the exposed fork branches. The independent `sh1ftmaker/katam-port` branches checked here were `master` at `0c83b1f12ef93db48659da2f026c716b8124b109`, `main` at `1249ebf6bc68e45b24cacc3050f27ffdcdac6bc2`, `coop` at `13b97a2e5464bc79899b6d18b9da3f89452af3c1`, and `menus` at `a3d55b07c1b3e73d702731adb1d0162817202eb3`. They contain multilingual tables, but no European matching build was established. The main and menus branches explicitly pin the USA checksum in `tools/gen_asset_manifest.py`, `tools/katam/lib/rom.mjs` and `platform/res_manifest.h`; generated data addresses are USA addresses. `zalo/katam-port` shares several of those exact branch heads and is not independent regional recovery. Accepting a ROM in a host loader is also weaker than proving that the code and address tables implement that region.

The European address reference from KatAM-Randomizer is useful for relocation anchors, but it is a randomizer's regional patch support rather than a complete European decompilation. Those addresses remain external hints until checked against source consumers and the owned ROM.

## Independently checked end of main code

The European end-exclusive main-code offset `0x15C714` was checked independently of the previously reported forum address. The pinned matching compiler's original libc make rules compiled `string/memcpy.c` and `string/memset.c` with `old_agbcc -O2 -fno-builtin`. Reading the resulting object `.text` sections and searching the owned image established these exact byte matches:

| Anchor | European ROM offset | Object text length | End-exclusive offset |
|---|---|---|---|
| `libc` `memcpy` | `0x15C660` | 96 bytes | `0x15C6C0` |
| `libc` `memset` | `0x15C6C0` | 84 bytes | `0x15C714` |
| `asm/libagbsyscall.s` | `0x159C28` | 100 bytes | `0x159C8C` |

The full `memset` and BIOS-wrapper text each have one occurrence in the owned image. `memcpy` also occurs in embedded auxiliary images, so its main-code instance is identified by adjacency to the unique `memset` match. The inherited linker orders `memcpy.o` then `memset.o` as its final `.text` inputs, followed by `.rodata`. These independent code anchors support the European `0x0815C714` boundary. For comparison, the USA first raw rodata symbol is `gUnk_0815BDD8` at `0x0815BDD8`. Their difference is not a universal relocation delta: other regional offsets vary.

These boundary anchors do not prove that every preceding byte is a recovered function, that all libraries are counted as game C, or that the European ROM can already be linked from source. The profile stores the anchor hashes and extents without storing ROM bytes.

## Spanish and runtime language handling

`include/constants/languages.h` assigns Japanese `0`, English `1`, German `2`, French `3`, Spanish `4` and Italian `5`. Existing game consumers index language-specific graphics and animation tables with `gLanguage`; changing the Makefile's compile define to `SPANISH` is not the runtime language-selection mechanism. No bare `ENGLISH`, `SPANISH` or other regional language preprocessor/assembly conditional was found in the inspected main source, headers, constants or assembly. Those command-line defines must not be confused with the `LANGUAGE_*` runtime constants.

There is direct European table evidence for Spanish. All 192 bytes of the six-row, sixteen-halfword `gUnk_08385C14` menu-background table reconstructed from the source occur together once at European ROM offset `0x38FBC0`. Its Spanish row is at `0x38FC40`; the following Italian row is at `0x38FC60`, and the complete table ends at `0x38FC80`. The Japanese row remains present in the data, but the five-language European product and selector must not be relabeled as six selectable languages merely because `NUM_LANGUAGES` is six.

The European runtime language variable is at IWRAM address `0x03000468`, unlike the inherited USA `gLanguage` initialized ROM entry at `0x08D60A80`. The [regional behavior notes](https://tcrf.tiago.zip/wiki/Kirby_%26_the_Amazing_Mirror) identify the European language setting, and the owned image independently contains code literals for that IWRAM address. Direct adjacent Thumb instruction decoding establishes halfword reads, for example a pointer load at `0x0800023C` followed by a halfword load at `0x0800023E`, and corresponding pairs at `0x0801A054/0x0801A056` and `0x0801A69E/0x0801A6A0`. The European language storage therefore supports the existing `u16` declaration; changing it to `u8` is not justified.

The selector's confirmation path at `0x0814AABE–0x0814AAC6` loads the language-variable pointer, reads the signed menu selection, adds one and stores a halfword. This is consistent with the European language IDs `1–5`, including Spanish ID `4`, and provides a concrete regional control-flow target for future source recovery. The confirmation path itself does not prove every selector transition or save-load path. A separate language write at `0x0800A93C` also needs its complete save/init contract preserved.

Finally, neither `src/kirby.c` nor `src/code_0806F780.c` references `gLanguage` in the inspected tree. A language-declaration change cannot directly explain a missing whole-module match in those files. Their remaining regional differences require their own instruction, ABI and data-reference investigation, without silently substituting source names or partial function matches for complete evidence.

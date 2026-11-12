# Data and editable asset recovery audit

This audit measures checked-in source representations, not whole-ROM decompilation. It was run against the current USA main-target sources with `python tools/progress/data_inventory.py`. The ignored result is `build/progress/data-inventory.json`. No original ROM was available, no game data was changed, and no data round trip or final ROM comparison was performed.

## Measured inventory

The repository contains 35 `src/data/**/*.c` translation units. They contain room background palettes, tilemap/tileset descriptors, and pause-map assets. They are excluded from the executable-only metadata build because that build measures code. Their existence must not be treated as zero data progress or silently added to the executable percentage.

Tracked main graphics and sound sources include 74 PNG images, one JASC palette, 79 binary files, 225 AIFF samples, 19 PCM files, and 424 MIDI files. These counts exclude generated `.4bpp`, `.gbapal`, `.lz`, and similar outputs. A binary tilemap is still an editable binary source representation rather than a recovered semantic C table. File counts cannot be converted into byte completion percentages because compression, padding, palettes, descriptors, and shared references change emitted sizes.

There are 130 C `INCBIN_*` wrappers across the tracked source tree. A declaration such as `const u32 tiles[] = INCBIN_U32(...)` establishes container alignment and inclusion, but does not by itself establish semantic recovery of the payload. The inventory lists these wrappers separately.

| Independent coordinate space | Raw baserom directives | Union of referenced byte ranges |
|---|---:|---:|
| Main ROM | 28,505 | 9,574,560 |
| `multi_boot/subgame_loaders/payload` | 23 | 11,848 |
| `multi_boot/unk_8D94B9C` | 216 | 77,672 |
| `multi_boot/unk_8E1FE28` | 250 | 89,216 |
| `multi_boot/unk_8E8490C` | 287 | 111,892 |

These values count only literal `.incbin "baserom.gba", offset, length` directives in tracked assembly. Intervals are unioned to prevent overlapping ranges from inflating totals. Each auxiliary ROM owns its own offsets; those offsets must never be unioned into the main ROM. The nearest enclosing Makefile determines ownership, so the nested payload is not confused with its loader. Loader assembly without baserom directives contributes no raw-range bytes to this table.

Of the main raw ranges, 363,184 bytes belong to six opaque loader/image ranges in `data/multi_boot_images.s`. The remaining union is 9,211,376 bytes. The embedded, rebuilt auxiliary `.gba` inclusions are a different representation and are not counted as raw baserom directives. Neither number is a whole-ROM “remaining data” denominator: executable code, decoded source assets, explicit assembly directives, padding, reconstructed tables, and embedded rebuilt images have different representations.

Reading the existing 176 metadata objects without changing them found 247,912 bytes of `.rodata` and 1,088 bytes of `.data`. These are partial unlinked section totals and include included asset payloads and padding; they are not “typed data decompiled” credit. The 35 data-only C units and assembly data objects were not compiled by that code-only build. `common_data`, BSS, and other RAM-oriented sections are excluded from these ROM-data totals.

## Concrete recovery candidates

| Candidate | Boundary and consumer evidence | Appropriate next step |
|---|---|---|
| `gRoomProps`, USA `0x089331AC–0x0893CB44` | `data/data_8.s` supplies exactly `0x9998` bytes. `include/data.h` declares `struct RoomProps` of size `0x28`; the range holds exactly 983 records. Consumers in `src/code_080023A4.c` use `doorsIdx`; `src/code_0800ECAC_2.c` uses room-specific indices through `gRoomProps`. | Extract the 983 records from an owned USA ROM, verify every field offset and signedness against consumers, and replace one bounded range with a typed array. Preserve unknown fields. Check the next symbol at `0x0893CB44`, linker placement, and all emitted bytes. |
| `gLanguage`, USA `0x08D60A80–0x08D60A84` | `data/data_08D60980.s` places four raw bytes in `.data`; `include/data.h` declares writable `u16 gLanguage` with a matching-related note. Numerous source consumers use it to index localized tables. | Inspect all writes and original bytes before choosing a two-byte value plus padding or a four-byte object. Do not widen the declared type or mark it `const` merely to consume the four-byte range. This is small but a useful boundary/alignment validation case. |
| `gUnk_08D6CD0C` through `gUnk_08D6DCAC`, USA `0x08D6CD0C–0x08D6DD04` | `include/data.h` already describes a `0x4C` room-related record and an eight-byte secondary record; `src/code_0800ECAC_2.c` traverses `roomId`, `unk46`, and pointer-linked data. Raw subdivisions include odd lengths `0x2F9`, `0x2FB`, and `0x41D`. | Recover the pointer graph and record boundaries before creating arrays. Those raw label lengths are not evidence that each label is a complete pointer table or record array. Preserve unresolved fields and placement in the `0x08D60980–0x08D6DD04` initialized-data region. |
| Existing room tiled backgrounds | `src/data/room_tiled_bgs/rainbow_route_1.c` contains an explicit RGB palette, compressed tileset inclusion, tilemap inclusion, and a typed background descriptor. Corresponding PNG and tilemap sources exist under `graphics/rooms/backgrounds/`. | Use this established format for another background only after tracing the actual loader/decompressor, destination VRAM or palette memory, dimensions, and exact raw range. Reuse existing conversion rules and verify an exact round trip; do not classify the largest anonymous blobs by appearance or compression signature alone. |
| Main embedded auxiliary images | `data/multi_boot_images.s` explicitly separates raw loader/image ranges, rebuilt auxiliary ROM inclusions, and zero-filled space. | Track each target independently. Improve source/data inside the auxiliary project and verify that target before changing the embedding representation. Do not count the embedded ROM once as main recovered data and again as auxiliary recovered data in a combined denominator. |

The European hacking guide linked in the external research describes a `0x28` room-property record. That is useful corroboration of a format already evidenced locally, but its European addresses must not be copied into this USA build. The USA boundaries above come from this repository's assembly and declarations. No conversion is justified solely by an external address list.

## Reporting and implementation priorities

Keep executable source progress, typed table recovery, editable graphics/audio sources, and auxiliary targets as separate measurements. Start additional data work with the room-property table because its current declaration, exact divisible range, and consumers provide a concrete bounded experiment. Then recover small initialized-data objects and typed pointer graphs incrementally. Larger graphics ranges should follow proven consumer paths and the repository's existing asset formats.

Before awarding byte credit to any converted range, require the original byte extent, recovered type/shape, every consumer needed to establish that interpretation, exact regenerated bytes including alignment, and a dependency-aware authoritative build. The absence of an owned ROM currently prevents extracting the unknown values and performing those checks. The inventory provides a work queue and source-format baseline without implying that opaque bytes have been recovered.

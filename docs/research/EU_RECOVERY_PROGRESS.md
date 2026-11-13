# European source recovery results

The primary profile uses the owned European B8KP revision-0 image, 16 MiB, SHA1 `6f478a455383a2a12378f292581dfd7300300700`. Its executable boundary is `0x15C714`; 188 header bytes are excluded from the 1,427,032-byte executable denominator. The following source experiments used the same strict relocation and source-provenance checks. Each recovered contribution was compared against the preceding credited physical intervals; none lost previously verified C bytes.

| Source cohort | Verified C bytes | European C share | Additional verified bytes |
|---|---:|---:|---:|
| Original katam source | 1,312,544 | 91.977195% | Baseline |
| Object engine, ending cutscenes and Flamer | 1,336,086 | 93.626912% | 23,542 |
| Remaining Prank source | 1,340,540 | 93.939029% | 4,454 |
| Sprite-effect translation-unit recovery | 1,344,996 | 94.251285% | 4,456 |
| Scoped Shotzo recovery | 1,347,220 | 94.407133% | 2,224 |
| Explicit SDK NOLOAD work-area proof | 1,350,708 | 94.651557% | 3,488 |
| European menus, help UI and editable regional graphics | 1,381,360 | 96.799511% | 30,652 |

The ending/object/Flamer contribution sources are upstream PRs #397, #411 and #398. Prank comes from the original PR #394 contribution. Sprite effects come from PR #395, with targeted current-context conflict resolution and the existing `gMultiSioEnabled` name. Shotzo uses only the Shotzo hunks of the original author's documented rebase patch; engine and terrain hunks from that combined patch were excluded. Git history retains original source authors, with MatyMeatBoy's integration and current-symbol/linker adaptations separate.

All sixteen megabytes of the final default European build were compared byte-for-byte against the owned dump, and the expected SHA1 passed. The compact [local verification receipt](../../config/regions/eu_verified.json) records source fingerprints, compiler provenance and per-span hashes. A fresh dependency-aware `make record-eu` rebuilt the metadata and European result through the primary GNUmakefile dispatch. The public pipeline validates current receipt provenance; CI does not acquire the ROM.

The sprite-effect fallback `sub_0802E78C` remains 496 assembly bytes. Shotzo retains assembly fallbacks of 160, 244 and 872 bytes. Those four functions earn no C credit. The remaining terrain collision function also remains assembly in the primary source; its historical readable draft is preserved separately. These readable alternatives and names add no matching-C bytes merely by existing.

Focused `NONMATCHING` compilation and assembly succeeded for the recovered Prank, sprite-effect and Shotzo units under the pinned compiler and original flags. This does not establish a complete whole-project `NONMATCHING` link or a USA ROM comparison. USA source coverage and its original six-output gate remain separate references.

Two final bounded, isolated profile experiments checked whether available readable alternatives or the older compiler behavior could recover more European bytes. Both freshly compiled all 172 main inventory objects and used the same strict EU reconstruction checks. `-DNONMATCHING` added zero bytes and lost 211,150 bytes relative to the default; omitting only `-f2003-patch` added zero bytes and lost 188,540. Both physical unions equal the default 1,347,220 verified C bytes, so neither variant was adopted. These experiments do not prove the original compiler's history or a complete auxiliary/whole-project link.

The data evidence view additionally unions verified initialized local C-data extents from the successful build. These source-backed bytes include ordinary C initializers and included source assets; raw fallback bytes and repeated references do not inflate that total. It is not a semantic format-identification percentage. Multilingual bytes, including the original Spanish selector and resources, are preserved exactly rather than replaced with USA data.

On 2026-11-13, four existing SDK/runtime modules became fully provable after accounting for their explicit linker ownership: `common_data` is zero-initialized writable PROGBITS in the input ELF, but its source-object selector belongs to an IWRAM `NOLOAD` output. The matcher now requires that explicit selector, zero bytes, no relocations in the work area, complete aligned RAM bounds and object bounds. It verifies the compiled text and all ROM data as before, gives RAM no ROM-data credit, and checks RAM definitions across accepted units. Input recorder adds 238 C bytes, MultiSio 1,272, Sio32MultiLoad 840 and m4a 1,138. No source algorithm or game behavior changed. The dependency-aware full 16 MiB rebuild and expected EU SHA1 passed at 1,350,708 verified C bytes.

The next independently tested regional cohort adds the European menu VRAM clears and background scroll offset, the five-language help-button indexing and twenty editable PNG sources reconstructed from the owned European assets. Every reconstructed asset roundtrips through the repository tools to the expected uncompressed or compressed bytes. These are original European program differences, guarded by `REGION_EU`; without that define the affected USA object text, local data and text relocations remain unchanged. The minigame/menu contributions add 28,016 C bytes and the help UI adds 2,636 relative to the SDK cohort, with zero loss of previously verified intervals. The combined default EU build passes full 16 MiB comparison and SHA1 at 1,381,360 C bytes. Details are in [EU_MINIGAME_RECOVERY.md](EU_MINIGAME_RECOVERY.md), [EU_HELP_MENU.md](EU_HELP_MENU.md) and the adjacent asset hash inventories.

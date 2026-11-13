# Sources for the remaining European code

Follow-up public-source search on 2026-11-12, after European integration at `f6b3861`. AI-assisted research by MatyMeatBoy. The verified European result remains **1,347,220 / 1,427,032 C bytes (94.407133%)**. This search establishes no additional matching bytes.

## Where reuse would help

The current European matcher rejects complete translation units for menus, minigames, pause screens and some shared runtime code, while accepting individual functions from many of those units. Much of the missing European coverage therefore already has USA C: finding another USA copy is insufficient. A useful new contribution must resolve a regional instruction/data difference, a still-unverified relocation or layout, or one of the remaining assembly functions.

Largest current source candidates are `code_08138D64.c`, `subgames.c`, `pause_area_map.c`, `kirby.c`, `title_screen.c`, `subgame_menu.c` and `pause_help.c`. The object sizes in the companion inventory are **USA-source C bytes without accepted European spans**, not measurements of European missing-function sizes. Source and regional instruction lengths can differ. The 79,812-byte European uncredited region also includes assembly, libraries and padding; it is not a count of missing C source alone.

## Fresh fork and branch check

The previous 24 external katam forks were refreshed through the GitHub API: all **91 branch heads were unchanged**. The only additional direct fork returned was this project. Upstream still exposes `master` at `1197474f80e5de282fbedcd0025ebfa61f61a764` and `jzw` at `3bbc5aba2d7eaa3ad327d6b43227a4a19a1536af`. Latest upstream PR metadata was checked again; no newer matching-EU source contribution was identified.

The expanded tool/recomp/randomizer survey inspected **18 repositories and 89 exposed branch trees**, with no recursive-tree truncation reported. Another Android repository's README and build configuration were checked separately. Tree inspection is not equivalent to reading every file. Selected source/configuration files were read; game images, generated game-code shards and binaries were not downloaded. The [companion inventory](remaining_source_search.json) records the exact default heads and branch heads inspected. Earlier broader forge-search limitations remain in [EXTERNAL_FORGES.md](EXTERNAL_FORGES.md).

## Concrete leads and limitations

| Source | What it supplies | Relevance and limitation |
|---|---|---|
| [icky-yucky modkit](https://github.com/icky-yucky/kirby-amazing-mirror-modkit/tree/00ac303e71ac4d3dbd0210bca7e9e58ddfe774f7) | Sprite/palette and room-map formats, collision experiments, editors | Its `CONTRIBUTING.md` fixes USA SHA1 `274b102b…`; useful data-analysis leads, not an EU matching implementation. Collision-arena observation cells are blank: their labels are not verified meanings. |
| [hasherwi Archipelago](https://github.com/hasherwi/Archipelago-kirbyam/tree/a58d79223214d4e274b57afda5845a491e7c9e71/worlds/kirbyam) | Native-hook contracts, room/ability/enemy data, patch tooling | `rom.py` fixes the USA MD5; `patch_rom.py` verifies USA byte contracts and adds behavior. Its hooks can guide investigation but must not be copied into an original-behavior matching build. |
| [Unovamata randomizer](https://github.com/Unovamata/Amazing-Mirror-Randomizer/tree/2ea1c963535405e1ba7d678bb4361a7f5c30703b) | Enemy/item/miniboss/mirror lists and scanner source | README targets Japan. Potential semantic/data leads. This is distinct from the EU address-table source already preserved in `config/reference/katam-randomizer`; no new EU C match demonstrated. |
| [soiryl-pas ReflexMinimap](https://github.com/soiryl-pas/ReflexMinimap/tree/da18751c026b26630a44983bc366fce7ba504a02) | Live room/foreground/solidity-map readers | Lua labels its addresses explicitly US-ROM. Useful consumer evidence for tables, requiring independent EU address/layout checks. |
| [adrianfernando recomp](https://github.com/adrianfernando617-byte/kirby-mirror-recomp/tree/e89b8757348c407e0086cafa44642bcda45b1323) | Runtime/mod code and imported decomp symbols | `KATAM_symbols.toml` explicitly says auto-generated from the decomp and fixes USA SHA1. This does not supply independently recovered matching C for our gaps. |
| [Felipe recomp](https://github.com/Felipe-Gomes-Amorim/kirby-amazing-mirror-recomp/tree/2bb49d0631cb54d928d70f97e6aacf79a4b15fb6) | Translation/runtime/hardware framework | Native translation infrastructure is distinct from original agbcc matching source. No inspected EU matching build. |
| [Android recomp](https://github.com/sempai3050-create/KirbyMirrorRECOMP/tree/7b9fc0032d8029a29d39c04f91c6259b9040c984) | Android/runtime wrapper around generated code | README requires USA; CMake fixes the USA SHA1. Not another European decomp. |
| [sh1ftmaker katam-port](https://github.com/sh1ftmaker/katam-port), [zalo katam-port](https://github.com/zalo/katam-port) | Readable source adaptations, port diagnostics and original decomp requests | Already surveyed source family. Port reachability/playability reports do not establish original EU binary matching. Original-source recoveries already integrated are listed in [EU_RECOVERY_PROGRESS.md](EU_RECOVERY_PROGRESS.md). |

Also surveyed: HeyImTG randomizer, Mode8fx randomizer, Labreezy practice notes, ShyGuyOmega Archipelago, lucasvtoor Archipelago, Fyyyyik object editor, translation and Humming repositories, katam-rando-dev. No inspected source established a ready-made European replacement for the remaining code.

## Result

No additional European C credit is justified by this search. Preserve the candidate links and investigate their exact data consumers rather than importing unrelated runtime changes. The strongest next engineering target is direct comparison of the European menu/minigame/pause routines against their existing C and local-data definitions. Tables and readable drafts remain valuable even when they earn no matching-C credit; naming and layout claims still require independent review.

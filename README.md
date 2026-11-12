# AmazingMirrorDecomp

This is a disassembly of Kirby & The Amazing Mirror (USA).

This repository is MatyMeatBoy's AmazingMirrorDecomp research and progress base, preserving the original katam history. See [credits](CREDITS.md), [public-source research](docs/research/), and [local reuse findings](docs/research/LOCAL_REUSE.md). Candidate contributions are recorded with their provenance and validation status; being listed does not mean they have been merged or verified.

## Progress

![Compiled C in measured main-object text](docs/progress/badge_decompiled.svg) ![ROM verification](docs/progress/badge_rom.svg) ![Existing names](docs/progress/badge_names.svg) ![Data recovery](docs/progress/badge_data.svg)

![Compiled main-object text inventory](docs/progress/treemap.svg)

<details>
<summary>Existing function names</summary>

![Existing names in the measured inventory](docs/progress/names_treemap.svg)

</details>

<details>
<summary>Data recovery</summary>

![Data recovery status](docs/progress/data.svg)

</details>

The [generated progress report](docs/progress/progress.md) measures the compiled main-game object text available to the ROM-free metadata build. It excludes compiler libraries and auxiliary targets that were not linked into that inventory. This is an object inventory, not a verified ROM build or a whole-game decompilation percentage. Data recovery is unmeasured. Existing names are naming coverage evidence, not proof of semantic correctness.

Generate the inventory with the matching agbcc toolchain and GNU ARM binutils installed:

```sh
python tools/progress/metadata_build.py --jobs 4
python tools/progress/report.py --metadata-dir build/metadata --out docs/progress
python -m unittest discover -s tests
```

The separate [progress workflow](.github/workflows/progress.yml) builds ROM-free metadata and uploads only the generated reports. Publication regenerates reports from a fresh `main`, restricts commits to `docs/progress/`, and retries a concurrent branch advance. It does not publish ROMs, extracted assets, objects, maps or metadata build artifacts.

The original matching build remains authoritative: run the top-level `make compare -j$(nproc)` with an owned USA ROM and the matching toolchain before claiming a match. All six checksum checks must succeed: `katam.gba`, `payload.gba`, `speed_eaters.gba`, `unk_8D94B9C.gba`, `unk_8E1FE28.gba`, and `unk_8E8490C.gba`. A separate complete `NONMATCHING` compilation checks the readable branches. Neither validation is established by the ROM-free reports.

## Original matching target

It builds the following ROM:

* [**katam.gba**](https://datomatic.no-intro.org/index.php?page=show_record&s=23&n=1692) `sha1: 274b102b6d940f46861a92b4e65f89a51815c12c`

To set up the repository, see [INSTALL.md](INSTALL.md).

## Contacts

You can find us on [Discord](https://discord.gg/d5dubZ3).

# Local reuse findings

The existing local AmazingMirrorDecomp checkout is the original katam source, with origin `https://github.com/jiangzhengwenjz/katam.git`. Its inspected baseline was `1197474f80e5de282fbedcd0025ebfa61f61a764`. The README identifies the USA target with SHA1 `274b102b6d940f46861a92b4e65f89a51815c12c`.

Bounded searches of the local GBA projects, PrimatesGBA, backup projects, experiment projects and ReKHCoM build areas found no Kirby & The Amazing Mirror ROM or additional Kirby implementation. Other games' ROM files were excluded from reuse. No Kirby ROM checksum or header was validated, and no ROM was copied or uploaded. This finding covers the inspected locations rather than proving that no copy exists elsewhere.

PrimatesGBA contained dependency and tool directories, including SDL2, with no related game source found. A paginated public-repository listing of MatyMeatBoy returned 25 repositories during the initial audit, including GBANoCable, but no Kirby, katam, AmazingMirror or Primates repository. Private repositories and unrelated storage remain outside this search.

## Baseline source inventory

The main source tree contained 200 C files. A textual scan found no `NAKED` or `ASM_FUNC` in main C, 92 `NONMATCHING` occurrences and 143 `INCBIN` occurrences. These are source occurrence counts, not function or byte progress. The `NONMATCHING` markers frequently select alternate C expressions or compiler-steering forms, so counting each marker as an assembly fallback would be incorrect. The baseline had no `asm/nonmatching` directory.

The auxiliary `multi_boot` tree contained no C files, 45 assembly files, 49 include files and five linker scripts/checksum files. Its four `NAKED` occurrences were header macro definitions. Auxiliary code must have a separate denominator rather than silently receiving the main game's C percentage.

## Measurement implications

The original `calcrom.pl` uses linked input-section sizes and ELF symbol sizes. It separates source-origin code from assembly, excludes designated intentional assembly from remaining decompilation debt, and deducts functions listed in `asm/nonmatching` from C coverage. That fallback directory was absent at the inspected revision. Its raw-data debt scan counts direct baserom `.incbin` ranges separately from intentionally preserved generated binary assets.

An object-only inventory must label its narrower scope, exclude missing libraries and unmeasured auxiliary targets, deduplicate function aliases, and reject stale metadata. Source `NONMATCHING` counts, raw `INCBIN` counts, names and matching-ROM checks answer different questions. Data recovery remains unmeasured until exact ranges and classifications support a separate report.

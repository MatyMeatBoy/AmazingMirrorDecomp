# Preserved naming proposals and readable drafts

This AI-assisted research for MatyMeatBoy preserves useful historical work without adding it to the primary verified-code numerator. Original authorship remains unchanged. New research and adaptation commits belong to MatyMeatBoy.

## Published reference heads

| Reference | Exact original head | Original author | Original parent | Intended non-primary branch |
|---|---|---|---|---|
| [Naming proposals, original PR #371](https://github.com/jiangzhengwenjz/katam/pull/371) | `78d5a544ce1e12aa04c00d080641ef9586078c96` | jackmgaller | `60e50b84fa64ea5d73ff15ac6ffe2a7d86462a62` | `research/naming-proposals-pr371` |
| [Readable buddy collision draft](https://github.com/sh1ftmaker/katam/commit/60bb564a0f46a856479ee3f56ae80bff648c5d3a) | `60bb564a0f46a856479ee3f56ae80bff648c5d3a` | sh1ftmaker | `fdad26898be4bb065b9c6a4932f30d83c5568ac0` | `research/terrain-collision-draft` |

The local comparison refs are `refs/remotes/candidates/reference-pr371` and `refs/remotes/candidates/reference-terrain`. They were fetched and safety-checked before publication as [naming proposals](https://github.com/MatyMeatBoy/AmazingMirrorDecomp/tree/research/naming-proposals-pr371) and [the collision draft](https://github.com/MatyMeatBoy/AmazingMirrorDecomp/tree/research/terrain-collision-draft). These are research references, not release, integration or verified-build branches; they add zero matching-C credit to the European primary target.

These are historical trees, not patches to copy over the current main tree. Relative to audited upstream baseline `1197474f80e5de282fbedcd0025ebfa61f61a764`, the naming tip has 307 added/modified and 86 removed paths; the terrain tip has 325 added/modified and 72 removed paths. Much of that difference is old upstream state. Merging either entire tree into current main would regress unrelated source and tooling. Recover one proposal or function with explicit adaptation instead.

## Naming proposal corpus

The original naming commit changes 223 source/header/assembly files and proposes a large vocabulary across objects, Kirby and menus. [NAMING_AND_DRAFTS.md](NAMING_AND_DRAFTS.md) and [candidates.json](candidates.json) already distinguish extracted identifier pairs from accepted semantic facts and identify proposals whose old names have since disappeared or changed.

Preserving the original commit keeps its complete context and authorship available for review. It does not accept every proposed name. For each adoption, inspect all callers, data uses, callback lifecycle, table references and original assembly; preserve unknown names where the evidence remains incomplete. Do not equate a proposed “nearest” helper with a priority/fallback selector or assume a matching ROM proves semantic names. Naming an existing C function adds zero compiled-code bytes.

## Terrain collision draft and existing baseline draft

The original terrain contribution adds `src/sub_0800F044.c`, moves reference assembly into `asm/nonmatching/sub_0800F044.inc`, changes the linker owner, and removes the superseded commented C draft from its older `src/code_0800ECAC.c`. Its complete function remains a NAKED assembly wrapper in the default build, with readable C under `NONMATCHING`. Therefore preservation of this contribution adds **zero verified matching-C bytes**.

| Original source path at `60bb564a...` | Git blob SHA-1 | SHA-256 | Size |
|---|---|---|---|
| `src/sub_0800F044.c` | `762d6b59d767b27ede2f8cb2f9a6ca8cf3092dfa` | `6ba96b73df999666e07d8bfe1f9259da112cf8607f5a94d8e110e6ffc39ced58` | 16,200 bytes / 491 lines |
| `asm/nonmatching/sub_0800F044.inc` | `7e37df2d0ee6ebe2bef8ea7de25a69954d854551` | `2d7174c2cd12e4dcab2979085647a25b13af82d8d2881472da1acb992bb29146` | 30,252 bytes / 1,885 lines |

The draft uses older declarations such as `struct Object2` and old field names. It cannot be treated as a drop-in implementation for the current baseline. The commit's claim that its default wrapper reproduces reference bytes and relocations is external evidence, not proof that its C branch matches or has been rebuilt here. The apparent terrain-grid layout still needs a complete readers/writers and bounds audit.

The baseline already preserves a [commented readable draft in `src/code_0800ECAC.c`, beginning near line 119](https://github.com/jiangzhengwenjz/katam/blob/1197474f80e5de282fbedcd0025ebfa61f61a764/src/code_0800ECAC.c#L119), through approximately line 564, and links [decomp.me scratch Au4Qp](https://decomp.me/scratch/Au4Qp). The root research attempted that scratch and encountered an access challenge; no current scratch source or match percentage was recovered from that attempt. The checked-in baseline draft and preserved historical contribution remain independently available without inventing a scratch result.

## Safety check before publishing reference branches

Both tips were compared with baseline `1197474f80e5de282fbedcd0025ebfa61f61a764`. The naming head introduces one newly reachable commit and 223 new reachable blobs; the terrain head introduces 14 newly reachable commits and 57 new reachable blobs. Every new blob was inspected. All were UTF-8 text without NUL bytes. None had ELF, PE/MZ, WebAssembly or archive magic. No `.gba`, BIOS, `.elf`, `.o`, `.exe`, library, shared-library, wasm or archive path appeared in either complete tip tree. No new binary blob was found.

This check covers newly reachable historical blobs, not only the final tree, so a removed binary in a new ancestor would not silently pass the review. Existing upstream PNG, MIDI and other source assets reachable from the baseline were not duplicated or presented as newly licensed content. It is a bounded artifact check, not a legal reclassification of game-derived material.

The durable [preserved_drafts.json](preserved_drafts.json) records exact tree differences, blob identities, authors, source hashes and safety outcomes. These references are suitable for explicit non-primary preservation after the root orchestrator's publication step. No push, source application, default-branch change, build, ROM comparison or semantic acceptance was performed by this preservation audit.

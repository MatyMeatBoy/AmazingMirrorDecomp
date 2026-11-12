# Naming, types and readable drafts

This inventory broadens the reusable work beyond matching C. It records proposed names, type/field facts, readable drafts, data interpretations and port diagnostics against the original game baseline `1197474f80e5de282fbedcd0025ebfa61f61a764`. The [structured candidate inventory](candidates.json) distinguishes externally proposed names from independently checked facts. No name, draft, data hypothesis or port adapter in this inventory has been added to the progress numerator.

## The large naming corpus

[Upstream PR #371](https://github.com/jiangzhengwenjz/katam/pull/371), by `jackmgaller`, contains a substantial reusable vocabulary. Its exact base is `60e50b84fa64ea5d73ff15ac6ffe2a7d86462a62`; its head is `78d5a544ce1e12aa04c00d080641ef9586078c96`. The author reports 1,456 function, 329 data and seven type renames, and matching checksums. The maintainer requested smaller subsystem PRs, a detailed evidence manifest per naming decision and conservative confidence. The PR was closed unmerged; the closure is a reviewability limitation rather than proof that every proposed name is wrong.

The full Git diff across 223 changed files yielded **1,792 distinct old-to-proposed identifier pairs** using single-token replacement extraction. This avoids the GitHub files API's omitted patches: the API returned patches for only 193 of the 223 files. The extracted identifier-prefix totals differ from the author's category totals, so the machine inventory describes pairs rather than claiming an independently verified function/type census. It does not reconstruct changes to identifiers outside the address-derived extraction patterns, such as `Kirby_110` to `KirbyMoveScriptStep`.

Of those pairs, **1,741 old identifiers still occur** in the inspected baseline; 51 are absent. Absence requires deduplication, because later naming work sometimes chose a different name. For example, the old `sub_0803E308` is now `ObjectSetBounds`, while the proposed `FindClosestKirby` for absent `sub_0803D368` must be reconciled with the current helper's actual selection contract. The pair inventory records both old and proposed identifier occurrences and source paths rather than assuming every absent old identifier was merged.

The pair inventory maps **1,410 proposals to currently measured unnamed function cells**, spanning 442,374 bytes in the existing unlinked main-object report. These are potential semantic-review targets, not accepted names and not newly decompiled bytes. None of these matched function cells belongs to the pending assembly category. A rename cannot resolve the remaining assembly by itself.

## Eight switch names with source evidence

[PR #403](https://github.com/jiangzhengwenjz/katam/pull/403), head `8cacafd24d75f270e10c4bdc639dce1dd6239e66`, is a focused follow-up with explicit evidence and upstream review. Its range is the switch subsystem beginning at `0x0811938C`; the final renamed function begins at `0x08119C0C`. The eight old names remain in baseline `src/big_small_switch.c`. All eight are already compiled C.

| Old name | Proposed name | Independently checked invariant |
|---|---|---|
| `sub_0811938C` | `SwitchSetFunc` | Installs the main callback and clears press/timer state; already-unlocked big switches select despawn instead. |
| `sub_081194DC` | `SwitchCheckPressAndGiveTomato` | Detects several press sources and conditionally creates a tomato for a human hitting a big switch. |
| `sub_081197D4` | `SwitchUpdatePressState` | Updates held/press/release bits, the release timer and the new-press sound. |
| `sub_08119980` | `SwitchMain` | Runs press handling, sprite selection and one template-selected effect each frame. |
| `sub_08119A20` | `SwitchUpdateHeldCount` | Increments the selected room counter on press and decrements it on release without underflow. |
| `sub_08119B3C` | `SwitchTryWorldMapUnlock` | Defers a pressed switch's world-map callback until the interlude gate permits it. |
| `sub_08119BB8` | `SwitchUpdateCPUKirbyTrigger` | Runs held-count handling, then raises room slot `0xF` while held. |
| `sub_08119C0C` | `SwitchDespawn` | Sets the flag that `ObjectMain` consumes to destroy the task. |

The upstream review specifically corrected a predicate-like name that concealed tomato creation and replaced “Start” with “Try” for an effect called every frame. The revised names account for those contracts. Room-placement totals quoted by the PR were not reproduced without an owned ROM. Keep `sub_0811942C`, `sub_08119AA8` and `nullsub_127` unnamed until their remaining semantic uncertainty is resolved.

## Useful field and data evidence, with a rejected claim

`zalo/katam` commit [`6f470934be50d2990c71e2470344b222c46196e3`](https://github.com/zalo/katam/commit/6f470934be50d2990c71e2470344b222c46196e3), branch `contrib-field-docs`, adds field and AI notes. It is 209 upstream commits behind the inspected baseline, so its comments must be checked against current declarations and consumers.

The input-latch interpretation is directly supported by current `sub_0803F324`: Kirby offset `0x118` holds the selected input, `0x11A` is current bits absent from the previous input and `0x11C` is previous bits absent from current input. The source can select linked human input or synthesized CPU input, and a suppression path clears all three. “Raw hardware buttons” would therefore be too narrow. These are strong field semantics, while a repository-wide rename still requires every writer and reader to be reviewed.

The same source offers useful hypotheses for animation tables. Current `sub_0806E4EC` copies `0xB9` normal `AnimInfo` entries from `gUnk_0834C5D4`, then applies `gUnk_0834C8B8` overrides under the mouthful flag. Current `sub_0806F358` copies `0x7A` entries from `gUnk_0834C9AC`. PR #371's normal/stuffed-cheeks/sword body-animation names have concrete consumer evidence worth reviewing. These tables are already typed C data; naming them does not establish additional data recovery.

One proposed box comment conflicts with the current source and must **not** be imported verbatim. `sub_0803E2B0` writes `ObjectBase` offsets `0x38` and `0x39`, then half absolute extents at `0x3A` and `0x3B`. `ObjectSetBounds`, formerly `sub_0803E308`, writes direct argument values at `0x3C–0x3F`. The external comment reverses these setters and describes the first group's extent fields as corners. A shared `ObjectBase::flags` legend also needs owner-specific context: `0x1000` participates in Kirby platform-drop logic and object task destruction. A global name inferred from only one consumer would be misleading.

## Drafts that still help assembly work

The baseline retains 3,596 measured assembly bytes in `asm/sub_0800F044.s`. The existing commented draft and [decomp.me scratch `Au4Qp`](https://decomp.me/scratch/Au4Qp) are already linked from `src/code_0800ECAC.c`. The zalo notes describe a 5×5 buddy terrain grid, hazard/solid/destructible cell classes, boundary sentinels and moving-platform merging. The callers in `sub_08018610` and `sub_08018640` support the AI context. The grid layout and cell meanings remain a behavioral dossier requiring instruction-level confirmation; the baseline explicitly questions the array boundaries around `Unk_02038590::unk1C`. No name or recovered struct layout is accepted from that hypothesis alone.

[Closed PR #395](https://github.com/jiangzhengwenjz/katam/pull/395), head `0cb8f35a8c9f3f25d0dab7cce9673f3a5f7bb922`, provides readable C for the 28 functions in `0x0802E57C–0x0802F8D8`, plus motion-record/data work through `0x082EB9A4`. The author reports 27 matching functions and a readable `NONMATCHING` branch for `sub_0802E78C`; the default branch retains assembly. The closure explanation says the change exceeded the preceding PR's scope. It should be reviewed as useful draft/source-boundary work, not discarded solely because it was closed. Its 40 neighboring functions from PR #378 already exist in baseline and must not be counted again.

## Port facts and deduplication

Pinned [`sh1ftmaker/katam-port` master `0c83b1f12ef93db48659da2f026c716b8124b109`](https://github.com/sh1ftmaker/katam-port/tree/0c83b1f12ef93db48659da2f026c716b8124b109) synchronizes an external decomp checkout and adapts a copy through `tools/portify.py`. It supplies host adapters and diagnostic tools rather than a separate checked-in `src/` game implementation. `zalo/katam-port` shares this master and several branch heads, so those references are duplicates rather than independent recovery.

The port's `DECOMP-REQUESTS.md`, `NATIVE.md` and `SIXTYFOUR.md` provide useful table-boundary and host-ABI investigations. They also preserve corrections: an inferred 12-entry table was actually three entries, and `STATUS.md` still lists missing-function claims that `DECOMP-REQUESTS.md` later withdraws. `tools/stub_returns.conf` deliberately changes stub results to let a host loop continue. Such diagnostics identify where to investigate; stub behavior and host guards are not matching implementations and cannot raise the matching-C numerator.

## Existing candidate CI

On 2026-11-12 the ROM-free Linux checks completed successfully for this repository's draft [PR #2](https://github.com/MatyMeatBoy/AmazingMirrorDecomp/pull/2), [PR #3](https://github.com/MatyMeatBoy/AmazingMirrorDecomp/pull/3) and [PR #4](https://github.com/MatyMeatBoy/AmazingMirrorDecomp/pull/4), which evaluate upstream PRs #411, #397 and #398 separately. Those checks establish compilation/report generation within the object-only scope. They do not establish a ROM match, compatibility of all candidates together, or semantic correctness. Their measured percentages must come from their generated artifacts rather than estimates from deleted assembly sizes.

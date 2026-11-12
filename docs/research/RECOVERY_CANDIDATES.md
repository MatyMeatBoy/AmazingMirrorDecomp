# Further recoverable source candidates

This AI-assisted follow-up records concrete contributions beyond the three priority candidates in the initial audit. It is research for MatyMeatBoy, not an assertion that any candidate has been integrated or locally ROM-verified.

## Sprite-effect unit: original upstream PR #395

[PR #395](https://github.com/jiangzhengwenjz/katam/pull/395), sh1ftmaker head `0cb8f35a8c9f3f25d0dab7cce9673f3a5f7bb922`, parent `a0d35ac494260cdb45fd768d2621328953bbd09b`, was withdrawn for scope. The author did not report a failed comparison. It replaces `asm/code_0802E57C.s`, merges the existing `src/code_0802F8D8.c` into `src/code_0802E57C.c`, recovers interleaved tables as one translation unit, and retains one default assembly fallback for `sub_0802E78C`. The author claims 27/28 functions match and six successful checksums plus a complete NONMATCHING link; these are external results only.

New assembly range: `0x0802E57C–0x0802F8D8`, end-exclusive, 4,956 bytes. Fallback interval: `0x0802E78C–0x0802E97C`, 496 bytes, excluded from matching-C credit. Converted rodata: `0x082EB6DC–0x082EB9A4`, 712 bytes. Forty existing functions move from the neighboring C file; their relocation is not new code coverage.

The fetched ref is `refs/remotes/candidates/pr395`. Against `origin/main` `545f0face8f5e5cd7b8527f49957bd2d797a0b2b`, both original-patch application and no-commit merge-tree analysis fail on `asm/code_0802E57C.s`, `include/functions.h`, and `linker.ld`. This candidate is not a clean merge. The replacement C still uses obsolete `gUnk_03002558` twice; baseline uses `gMultiSioEnabled`. A separate MatyMeatBoy adaptation must reconcile this rename, current subsystem declarations, preserved `code_0802E16C.o` placement, and merged text/rodata order. No candidate code was applied by this research.

## Prank: withdrawn source contribution

[PR #394](https://github.com/jiangzhengwenjz/katam/pull/394), sh1ftmaker head `78f9da4f7e66472755227aed6b02ef15029a5883`, same parent `a0d35ac494260cdb45fd768d2621328953bbd09b`, replaces the rest of `asm/prank.s` with 649 added C lines, updates `include/prank.h`, and removes its assembly linker contribution. Its body claims 43 remaining functions match, with six clean checksums and NONMATCHING link. Closure was the author's focus/scope decision, not a recorded mismatch.

Its known overlap is the already-merged Cookin declarations for `sub_080A158C` and `sub_080A245C`. Preserve baseline callers and current declarations; do not restore an old complete tree. A hand-expanded object-creation macro is retained for a measured code-generation difference. It needs independent full-object and pointer/linkage validation. The original maintainer's later PR #412 comment says Prank is claimed by Mateo; this is ownership/coordination evidence, not proof that the withdrawn implementation is wrong or automatically accepted upstream.

## Shotzo: partial PR versus unpublished full-file candidate

[PR #412](https://github.com/jiangzhengwenjz/katam/pull/412), head `2f44c446cc51766e64dfd5dd38b29537dcf038a9`, base `1197474f80e5de282fbedcd0025ebfa61f61a764`, proposes only `sub_0811B3E4`, `sub_0811B400`, `sub_0811B44C`, and `sub_0811B48C` (47 added C lines). Its body reports a main-ROM checksum result only, not the full six-output verification. The maintainer closed it because the file was already claimed by snake_oil_salesman. Do not conflate that coordination rejection with a technical validation result.

A larger separate original commit exists in sh1ftmaker/katam all-work: [`eab26275164aad9f4d20b6f6678d30047d546705`](https://github.com/sh1ftmaker/katam/commit/eab26275164aad9f4d20b6f6678d30047d546705), parent `60c993e1b18bd438937738347fbdffc913c9fe53`, 2026-08-04. It supplies 741 C lines and claims 13/16 functions matching, retaining NAKED reference includes for `sub_0811A934`, `sub_0811AA80`, and `sub_0811AB74`. Its commit reports byte/relocation comparison, which this research has not reproduced. The partial four-function PR overlaps the same source range; never add both candidates' function totals or merge both wholesale.

## Buddy terrain grid: readable but not matching C

[`60bb564a0f46a856479ee3f56ae80bff648c5d3a`](https://github.com/sh1ftmaker/katam/commit/60bb564a0f46a856479ee3f56ae80bff648c5d3a), sh1ftmaker, parent `fdad26898be4bb065b9c6a4932f30d83c5568ac0`, 2026-08-04, adds `src/sub_0800F044.c` and moves the old assembly into an `asm/nonmatching` include. The entire function remains NAKED assembly by default; the C is an independently reviewable NONMATCHING hypothesis. This contributes zero default matching-C bytes until matched. Its commit claims 0xE04 reference text bytes and 28 equivalent relocations; that supports the wrapper, not proof that the readable C matches. The maintainer's ownership note assigns this function to Ultra.

## Existing port patch series: exact recovery route and limitations

[Port commit `69ab254328d1f782e5a2cae7ce9cbcf202bf49a8`](https://github.com/sh1ftmaker/katam-port/commit/69ab254328d1f782e5a2cae7ce9cbcf202bf49a8) carries a decomp source patch series; on main `1249ebf6bc68e45b24cacc3050f27ffdcdac6bc2` it lives under `tools/legacy-sync/patches-decomp/`. This is concrete recoverable source provenance, not a reason to import the independent host runtime. Its author claims comparison succeeded after each patch; no local comparison was run here.

| Patch | Original mail-patch identity / blob | Use and limitation |
|---|---|---|
| `0001-Decompile-code_0802B4A8.c-105-functions.patch` | See tracked port tree | Duplicates the ending-cutscene candidate family already under review; do not add coverage twice. |
| `0002-Decompile-the-rest-of-flamer.patch` | See tracked port tree | Duplicates the Flamer candidate family already under review. |
| `0003-Decompile-the-rest-of-prank-43-functions.patch` | See tracked port tree | Rebased withdrawn Prank contribution; compare to the original PR before reuse. |
| `0004-Decompile-code_0802E57C.c.patch` | Original `83a5c926fde7b412f935578242a7aaf1cddac138` | Older variant claims 26/28 C matches and two fallbacks, versus PR #395's 27/28 and one fallback. Do not replace the newer source with this variant. |
| `0005-Follow-upstream-rename-gUnk_03002558-gMultiSioEnable.patch` | Original `e6209744e160590d793db7edf50c7cc5df3ce39c`; blob `1e8085155080915c14b2af7501ed0498777f4d42` | Concrete reference for the two obsolete-global replacements needed by PR #395. |
| `0006-Bring-shotzo.c-code_0806F734.c-and-sub_0800F044.c-ov.patch` | Original `3f92d3ab211bc1ac00909c20fee20def0cccdbd6`; blob `6f09b1c75b9187ec97cd04f37dfeb0a91de66d81` | Mixes three recovered units and six NAKED fallbacks. Must split and validate by unit; its engine section overlaps the original-author PR #411 and retains two fallbacks. |

The six fallback functions in patch 0006 are `sub_0811A934`, `sub_0811AA80`, `sub_0811AB74`, `sub_08098E54`, `sub_0809924C`, and `sub_0800F044`. Its engine reconstruction is a weaker matching-C candidate than original-author PR #411, which is already tracked independently. Preserve original authorship and distinguish source adaptation from independently licensed port infrastructure. No blanket import of the all-work branch or patch series is warranted.

## Required review

Before any candidate leaves draft, perform the repository's clean non-modern six-output `make compare`, complete NONMATCHING compile/link, full affected object/relocation and data-boundary checks, raw pointer/linkage audit, and `git diff --check`. No user-owned ROM was available to this research, so none of those binary results is claimed. A new branch or imported historical commit is not a measured progress increase.

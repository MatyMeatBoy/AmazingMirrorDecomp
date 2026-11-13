# Terrain sample layout audit and defined draft

This is research for `sub_0800F044`, not default game integration. The original draft by sh1ftmaker is pinned to `60bb564a0f46a856479ee3f56ae80bff648c5d3a`; the previous recovered source and attribution remain unchanged. MatyMeatBoy's new alternative is `drafts/sub_0800F044_defined.c`. It is the same original symbol, not an additional function or an additional yellow span.

## Allocation and source audit

The uniquely matching 344-byte EU initializer is at `0x0800ECD4`. The instruction at `0x0800ECEE` loads the per-player stride **0xF4**, and the initializer clears the state object. The struct's next unrelated halfword is at **0x3C** and its Kirby pointer is at **0x40**. Therefore the existing three byte-array declarations occupy one contiguous **32-byte region at 0x1C..0x3B**. This establishes storage extent, not a 5x5 C array declaration.

All named references to `Unk_02038590` were checked in `code_0800ECAC.c`, `code_0800ECAC_2.c`, `code_08025650.c`, `code_0802E16C.c` and `kirby.c`. The only compiled named sample writer is `asm/sub_0800F044.s`; the large C copy in `code_0800ECAC.c` is commented out. The two initialization/reset routines and the callback dispatch were inspected. `terrain_layout.audit.json` lists all **37 sample reads in 13 functions**, their source lines and constant/dynamic indices, plus every observed spatial sample.

The writer establishes a sparse lattice with center at state offset0x28 (region index12). Its 13 observed sites are indices2,6,7,8,10,11,12,13,14,16,17,18,22. Horizontal tile-query offsets change the index by1; vertical offsets change it by5. These facts do not prove that every one of25 positions is sampled, nor establish a 25-byte array extent. Bytes23..31 have no observed sample accesses here.

`sub_080157B0` does not require three separate arrays. Its direction variable is exactly -1 or+1, its next index is1 or3, and its combined index is0 or4. The legacy views therefore address region indices16/18,10/14 and11/13, all within the observed sample set. Treating those views as a single array changes no caller-level storage contract.

The query runs through `sub_08018610` or `sub_08018640`, selected by phase-2 callbacks `sub_0801852C`/`sub_0801858C`. Updates are gated by matching low counter/player-index bits and skipped in room0x397. The task invokes callbacks0,1,2,3 in order; decision readers can consume the retained cache when no query update runs. This is not a fresh-grid-every-reader assumption.

## Defined aggregate model

`drafts/terrain_layout.patch` proposes one **named union** at0x1C: a complete byte array `samples[0x20]` and a named `legacy` struct containing the existing10/5/17-byte views. The new writer indexes only the complete array. Existing readers retain bounded accesses to the legacy views. No cast between unrelated struct-pointer types, no pointer arithmetic across separately declared array objects, and no guessed 5x5 type are needed.

The members contain unsigned bytes only. Access through the named union uses its object-representation views; this is the union access covered by [WG14 defect report283](https://open-std.org/jtc1/sc22/wg14/www/docs/dr_283.htm), rather than a pointer cast to an unrelated aggregate. The pinned C compiler independently confirms all sizes and offsets. This is a valid reconstruction model, not proof that the original author wrote this exact union.

The patch also propagates the named legacy path to every compiled reader in `code_0800ECAC_2.c`. Recompiling the entire reader translation unit produces exactly the original **40552-byte .text**, identical text relocations, and identical .rodata. A flat-array-only rewrite changed one reader's instruction sequence; it is excluded. Neither this patch nor the new draft is applied to core files.

## Types, lifetimes and comparison

The original assembly stores Kirby's pixel coordinates as zero-extended16-bit values, then sign-extends them at the object-bound comparisons. The new source represents that explicitly. Object coordinates remain signed16-bit, as established by their ASR sequences. The four repeated directional query points are shared across the mutually exclusive branches, reflecting their common role and avoiding four independent sets of stack storage.

Compiled result with pinned agbcc `59b966ed1b8f371856dcf99f1546c2fe89c678ca` and unchanged original flags:

- Function and text section: **3588 bytes**, 28 actual relocations.
- Stack frame: **0x3C**, equal to the original; the previous provisional draft used0x64.
- Reference EU span: **0x0800F06C..0x0800FE78**, 3596 bytes.
- Complete match: **false**; no masked candidate site.
- First fixed difference now occurs at0xE, in the initial pointer/register assignment.

The eight-byte size gap does **not** mean that only eight bytes differ. There are still broad register, spill and instruction-layout differences. Full semantic equivalence has not been established. No register-binding tricks, assembly, dummy variables or flags were used. The original branch conditions, classification masks (including downward0x20C), bounds and unusual near/far else-if behavior are preserved.

## Reproduction and accounting

Run from the repository root:

```text
python docs/research/drafts/check_terrain_defined.py --evidence build/research/terrain_defined_check.json
```

The checker requires the pinned compiler and owned B8KP ROM. It copies headers into a fresh ignored scratch directory, applies the context-checked research patch there, compiles the candidate, compiles the original and adapted reader modules, and compiles an independent sizeof/offsetof record. It never edits core files, links a ROM or grants C credit. The checked-in `sub_0800F044_defined.layout-proof.json` records the actual object, LF source/patch/header hashes, explicit profile, layout values and results. Its distinct suffix keeps this overlay-dependent experiment out of automatic standalone-draft registration.

The original registered draft is retained. The improved alternative requires its declared header overlay and must not be treated as a plain-header compilation. Both are candidates for the same3596-byte original assembly symbol: **matching C credit is zero and yellow accounting must deduplicate them**. No full-ROM claim is made for this research-only candidate.

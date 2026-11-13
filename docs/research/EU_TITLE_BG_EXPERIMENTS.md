# European title background: unresolved register allocation

AI-assisted experiments for the European B8KP profile. These are internal experiments in this fork; no upstream contribution or source-authenticity claim is made. No ROM bytes or object files accompany this dossier.

The current natural reconstruction emits **584 bytes**, with **10 fixed-byte differences**. A local callback-copy experiment reduces that to **two differences**, but remains unverified matching C and must not earn additional C credit. No experiment here was applied to the game source.

## Reproduction baseline

- Source: `src/title_screen_eu.inc`, snapshot LF SHA256 `37a42ddec2a33f0d9b46b21a330f1212967e855186eb056e01f9f9255d7e9d85`.
- Compiler: agbcc commit `59b966ed1b8f371856dcf99f1546c2fe89c678ca`.
- Preprocessing: `gcc -E -iquote include -Wno-trigraphs -DMODERN=0 -DREGION_EU -I tools/agbcc/include -I tools/agbcc -nostdinc -DREVISION=0 -DENGLISH`, followed by the repository preprocessor.
- Compiler flags: `-mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g`.
- Assembler: `-mcpu=arm7tdmi --defsym REVISION=0 --defsym ENGLISH=1`.
- Function: `sub_0814A62C`, European address `0x0814A62C`.
- Complete title `.text`: 5,016 bytes, compared at European address `0x08149DCC`.
- Method: compare fixed bytes against the owned local European ROM using `eu_match.Elf` and `relocation_mask`. Relocation-masked byte comparison alone is **not** the complete relocation/data/full-ROM matching gate.

Scratch scripts and generated assembly were kept outside the repository. Experiments used one immutable snapshot to avoid concurrent source edits changing the baseline. Each variant was compiled separately with the flags above.

## Findings by source hypothesis

| Hypothesis | Result for BG |
|---|---|
| Baseline natural reconstruction | 584 bytes / 10 differences |
| Palette/loop scopes, separate loop counters, unsigned 32-bit background index | Same 10 differences |
| Local Object11 pointer or palette-animation-info pointer in ABC4 | Same 10 differences |
| `register` / `restrict` parameter qualifiers; static versus external inline ABC4 | Same 10 differences |
| Four language-control bytes represented as an array or nested struct | Same 10 differences; no evidence to adopt either layout |
| Background index narrowed to u8 | 11 differences, adding `+0x171` |
| Background index changed to s16 | 117 differences |
| Remove background-index temporary | 600 bytes / 157 differences |
| Shared explicit zero temporary | 584 bytes / 36 differences |
| Natural byte/flags suffix extracted into inline helper | 592 bytes / 454 differences |
| Natural byte/flags/ABC4 suffix extracted into inline helper | 592 bytes / 454 differences |
| Complete state-preparation suffix extracted into inline helper | 600 bytes / 480 differences |
| Callback helper takes Object11 and callback-slot pointers | 568 bytes / 464 differences |
| Callback helper takes contiguous Object11/callback subobject | 564 bytes / 461 differences |
| DMA source local / inline palette-copy helper | 584 bytes / 35 differences |
| DMA destination declared before source | 584 bytes / 22 differences |
| Existing DMA Defvars macro | 584 bytes / 37 differences |
| DMA register pointer signedness | Same 10 differences |
| Global flags assignment versus compound assignment; flags temporaries | Same 10 differences |
| Palette inline-wrapper offset argument u16/u32/s32, length u16 | Same 10 differences |
| Palette inline-wrapper length widened to u32 | 16 differences: adds six bytes at `+0x18A..+0x18F` |
| BG-loader index narrowed to u8 | Adds differences at `+0x4D`, `+0xAF`, `+0x111` |
| Empty memory/cc barriers at branch, byte store or callback boundary | No improvement |

The whole-title pointer passed through the inline helper is material: direct expansion or passing a narrower subobject changes hoisting and the prologue. The existing prototypes of `sub_0814F3C4` and `LoadBgPaletteWithTransformation` agree with their available C definitions; no prototype change is justified by these trials.

## Best partial candidate

The optional [callback patch](drafts/eu_title_bg_callback_partial.patch) duplicates ABC4's two operations in a **local static inline copy**, called only by BG. The original ABC4 remains unchanged. The callback target is initialized in r0 and the actual callback-slot pointer in r1, tied to an empty read/write extended-asm statement. It emits no hand-written instructions. This is explicit compiler steering, not evidence of an original helper boundary.

Fixed-byte results for that candidate:

- BG: **584 bytes / two differences**, at `+0x1CF` and `+0x1D0` (absolute European addresses `0x0814A7FB`, `0x0814A7FC`).
- Complete title `.text`: **5,016 bytes / those same two differences**; all other fixed bytes retain the baseline result.
- ROM loads the `unk36D` member displacement into r3 and uses `adds r0,r7,r3`; the candidate uses r1 instead. The displacement and destination address are otherwise the same.
- Removing the local callback steering returns the original eight additional differences. Applying the steering directly to shared ABC4 instead of its local copy moves eight differences into standalone ABC4: BG improves, but the complete translation unit does not.

The patch contains a local TODO explaining the unresolved differences and removal condition. It must not be applied as a matching completion. Its duplication and fixed-register constraints are technical debt; prefer a natural source reconstruction when one produces the same complete proof.

## Failed attempts to resolve the final two differences

A real `offsetof(struct EuTitle, unk36D)` initialized in r3 was tested both as a read/write operand and an input-only operand. Access through a character pointer produced 31 differences on the baseline and 39 with the callback copy, losing reuse of zero in r4. Keeping the typed field store with the input-only offset added a r3-to-r1 copy and produced 72 differences. These variants are rejected.

Register-constrained pointers to the real byte subobject also changed zero reuse. Character lvalues, alternate equivalent byte-store expressions and reusing the loop counter did not resolve the final load. No extra register constraints, changed compiler flags, volatile game fields, fabricated values or hand-written instructions are part of the optional patch.

## Acceptance boundary

A future candidate must pass the **entire title translation unit**, all relevant relocations/local data and the full owned European ROM rebuild. Verify that prior matching functions retain their output, and remove each steering adjustment independently to establish its actual effect. Two residual bytes are still a mismatch; byte similarity establishes neither original source structure nor semantic naming correctness.

# European title background: complete source-object proof

AI-assisted experiments for the European B8KP profile. These are internal experiments in this fork; no upstream contribution or source-authenticity claim is made. No ROM bytes or object files accompany this dossier.

The final source emits **584 matching background bytes**, and the complete title `.text` emits **5,016 matching bytes**. The complete module proof also verifies and emits **252 bytes of local `.rodata`**, with **42 consistent external bindings and 202 relocation records**. This is a source-object and local-data proof against the owned European ROM; the coordinator must still run the official full-ROM rebuild before updating published credit.

The final patch uses one initialized member-offset register constraint and an empty input-only asm statement, plus a defined zero assignment through the existing loop counter. This is documented matching debt, not recovered historical source. A separate incorrect callee in the title exit routine was corrected from direct ROM evidence and the corresponding original source caller.

## Reproduction baseline

- Source: `src/title_screen_eu.inc`, snapshot LF SHA256 `37a42ddec2a33f0d9b46b21a330f1212967e855186eb056e01f9f9255d7e9d85`.
- Final commented source LF SHA256: `3b0e0bac40ac9babd285dc94a0765080135c42c6587067d839941c5a5ac41750`.
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

## Final minimized source form

Inside BG, before the existing flags update:

```c
{
    register u32 displacement asm("r3") = offsetof(struct EuTitle, unk36D);
    s8 *slot = &title->unk36D;
    asm("" : : "r"(displacement));
    i = 0;
    *slot = i;
}
```

`stddef.h` supplies the real member offset. The slot is the actual byte member, so no numeric layout guess or untyped whole-object write remains. Both values are initialized. The empty asm has only an input operand and emits no instructions; it creates no call, memory write or additional ABI dependency. r3 is caller-saved and this value is dead before the following calls. The existing loop counter is set to zero before the byte store; its source form permits the compiler's zero reuse in r4. The later `unk358 = 0` remains a literal: changing it to `i` was unnecessary and was removed.

There is **no callback clone, fixed callback pointer, output asm operand or hand-written instruction** in the final source. All other fixed bytes remain unchanged; the complete final module emits exact ROM bytes, including the corrected AFE4 call relocation. The source contains a local TODO with the measured effects and removal condition.

### Final-source removal checks

Each row recompiles the final commented source with one change; no other variant is combined into these counts.

| Removed or simplified element | BG / full-title fixed-byte result |
|---|---|
| Final source | 584 / 5,016 bytes; zero differences |
| Remove empty input-only asm | Ten differences, all in BG |
| Remove r3 binding while retaining initialized input operand | Three differences: BG `+0x1CF`, `+0x1D0`, `+0x1D4` |
| Replace `i = 0; *slot = i` with `*slot = 0` | 31 differences, all in BG |

Earlier minimization established that a fixed r0 slot binding, a second asm operand, a read/write operand and assigning `i` to the later `unk358` store are unnecessary. They were removed before the final-source checks. Removing both initial bindings from the earlier two-operand form gave three differences. A plain typed slot with no displacement constraint returned the baseline ten differences.

The original ten BG differences were at `+0x1CF`, `+0x1D0`, `+0x1F6`, `+0x1F8`, `+0x201`, `+0x202`, `+0x204`, `+0x209`, `+0x20A`, `+0x20C`. They were register encodings, not opcode/control-flow changes. The offset constraint and real zero lifetime interact; their isolated failure counts do not prove an independent cause for each changed register.

## Correct title-exit callee

Fixed-byte masking initially concealed an independent source error: `sub_0814AFE4` called `CreateCutscene`, while its European BL at `0x0814B01A` targets `0x08138BEC`, the already verified implementation retaining the original identifier `sub_08138B44`. The analogous USA source exit caller in `src/title_screen.c` also calls `sub_08138B44` after the same palette fills and `TaskDestroy`. Only the European exit call was changed; no semantic rename or USA-source modification was made.

`sub_0814A9DC` still calls `CreateCutscene`, whose European target is `0x08026080`. The complete proof now establishes the distinct Thumb bindings `CreateCutscene = 0x08026081` and `sub_08138B44 = 0x08138BED`. Before this correction, complete-module proof rejected conflicting bindings even when all fixed bytes matched.

## Complete-module verification

The final commented source was compiled again under the pinned profile. `prove_module` verified the entire title module at `0x08149DCC`, with its explicit linker NOLOAD ownership. `relocate` then emitted the complete text and every referenced local extent, and each was compared byte-for-byte with the owned European ROM:

- `.text`: **5,016 bytes**, exact.
- Local `.rodata` objects: **48 + 36 + 168 = 252 bytes**, exact.
- **42 external bindings**, consistent across the complete module.
- **202 relocation records** handled by the complete proof.
- BG itself: **584 bytes**, exact; all other title fixed bytes retain their baseline output.

No ROM, object, generated assembly, private local path or extracted bytes are included in this dossier. The full dependency-aware ROM gate remains the coordinator's subsequent check.

## Superseded callback-copy candidate

The archived [callback-only experimental patch](drafts/eu_title_bg_callback_partial.patch) is **not the final source patch and must not be applied**. It records an intermediate result: a local inline callback copy reduced BG to two fixed differences (`+0x1CF`, `+0x1D0`, European addresses `0x0814A7FB`, `0x0814A7FC`) while keeping the rest of the title's fixed bytes unchanged. Applying its constraints to shared ABC4 instead moved eight differences into standalone ABC4. The final source needs neither the clone nor callback constraints.

## Failed attempts to resolve the final two differences

A real `offsetof(struct EuTitle, unk36D)` initialized in r3 was tested both as a read/write operand and an input-only operand. Access through a character pointer produced 31 differences on the baseline and 39 with the callback copy, losing reuse of zero in r4. Keeping the typed field store with the input-only offset added a r3-to-r1 copy and produced 72 differences. These variants are rejected.

Register-constrained pointers to the real byte subobject alone also changed zero reuse. Character lvalues and loop-counter reuse alone did not resolve the mismatch. The successful combination was then minimized to the final typed-slot, single-input form above. No changed compiler flags, volatile game fields, fabricated values or hand-written instructions are part of the final source.

## Acceptance boundary

The source-object checks above pass the **entire title translation unit** and all relevant relocations/local data. Before publication, run the full owned European ROM rebuild and confirm prior matching functions retain their output. Remove the steering when a natural reconstruction passes the same complete checks. Exact emitted bytes establish neither original source structure nor semantic naming correctness.

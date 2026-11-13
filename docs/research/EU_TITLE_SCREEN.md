# European title screen recovery

The complete European title screen is reconstructed in `src/title_screen_eu.inc`, selected by `REGION_EU`. The original USA implementation remains unchanged under `#else`. Existing katam contributors retain attribution for the original implementation and analogous helpers; regional reconstruction is by MatyMeatBoy. No external code or generated ROM bytes are imported as C.

The task layout is 0x380 bytes. Every field has a verified offset comment: 21 sprites begin at 0xC, the main callback is at 0x354, a signed counter at 0x358, Object11 at 0x35C, auxiliary callback at 0x368, signed language and menu selections at 0x36C–0x36F, and eight saved palette colors at 0x370. The new eight-byte sprite configuration type follows actual byte/halfword loads; its unexplained field remains `unk5`.

The constructor validates the existing u16 gLanguage to 1..5 and sets key repeat intervals to 20/4. Destruction frees all 21 sprites and restores 20/8. The five-language selector preserves A/Start acceptance, B cancellation, Up/Down wrap, original sounds, UpdateSaveBufferByOffset(0, 0), and the original final update. Its language write at 0x0814AAC6 is STRH. All five languages, including Spanish, remain selectable. Menu palette changes, sprite placement/drawing, animation callbacks, fade timing, idle timer and transitions to demo/cutscene are preserved.

An original mistake remains: sub_0814ADD0 conditionally assigns AE68, then immediately overwrites it with AE2C. A local comment records this; it is not repaired. The local auxiliary sprite uses the defined assignment `unk1B = 0xff`; this already emits the original instructions, so no indeterminate read or intentional undefined behavior was needed.

## Compiler and evidence

Pinned agbcc: `59b966ed1b8f371856dcf99f1546c2fe89c678ca`.

Flags: `-mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g`. The original CPP profile adds only `REGION_EU`. Assembler: `-mcpu=arm7tdmi --defsym REVISION=0 --defsym ENGLISH=1`.

The complete object text is **5016 bytes**, corresponding to EU 0x08149DCC–0x0814B164 exclusive. Normal source definition order and deferred emission of inline helpers reproduce the original physical function order. There are 39 emitted functions, totaling 5014 bytes, plus two alignment bytes. Thirty-eight complete functions (4430 bytes) pass strict candidate relocation/local-data proof at their corresponding EU addresses. The remaining 584-byte function is pending. Alignment is not function C credit.

`EU_TITLE_EVIDENCE.json` records LF-normalized source hashes, compiler profile, every function range, actual relocation count, complete fixed-byte comparison, and strict candidate-proof result. This research evidence is not a production receipt or a whole-module C claim. Some functions have repeated instruction patterns; the coherent source layout and real callback relocations supply context, and production must independently verify bindings.

The only remaining instruction differences are in `sub_0814A62C`, the 584-byte background setup function. It has the original algorithm, control flow and size, but ten fixed bytes select r1/r2/r3 differently at offsets 0x1CF, 0x1D0, 0x1F6, 0x1F8, 0x201, 0x202, 0x204, 0x209, 0x20A and 0x20C. No dummy operations, register bindings, volatile objects or assembly were added to force these choices. Actual supported ELF relocation fields alone are masked.

Structural experiments: direct palette loading instead of the original inline wrapper increases differences to 16. Expanding the Object11 initializer manually yields 568 bytes and 463 differences; recovering its inline function and ordinary call yields the original 584-byte shape. Independent scratch review tried aggregate locals, loop/palette scopes and wider background-index types without resolving the final ten bytes. Those unsuccessful variants are excluded.

The sprite configuration at 0x08391D34 and auxiliary animation table at 0x08391DDC are now explicit structured C initializers. Their formats and counts come from the consumers: 21 eight-byte records and six three-u16 records. Together with the 48-byte background index table, the complete 252-byte compiled .rodata matches EU 0x08391D04�0x08391E00 exactly. Unknown record fields retain their exact values without invented semantics. EU_TITLE_DATA.json records all three ranges and hashes. The background index table is identical to the existing USA table, including its preserved Japanese row; EU selectable languages remain five.

## Regional validation

This isolated worktree's final gate: 172 objects, 1416196 executable object bytes; 1228 verified units; **1356262 credited C bytes, 95.04075591857786%**; complete 16 MiB comparison and expected B8KP SHA1 `6f478a455383a2a12378f292581dfd7300300700` passed. These are measurements with this worktree's older matcher, not the current combined production branch. The 584-byte mismatch remains raw fallback and receives no C credit.

Commands: `python tools/progress/metadata_build.py --jobs 4`, then `python tools/progress/eu_build.py`, with the explicit experimental European CPP recipe. The temporary recipe is excluded from source commits. Production must rebuild with its own declared European profile.

USA compatibility was independently checked against the original source without REGION_EU: identical 2884-byte .text, full .rodata and text relocation signatures. All later changes are confined to the excluded EU include. This does not claim the original six-output USA ROM gate.


## Structured-data follow-up gate

After recovering the additional 204 bytes of sprite configuration and auxiliary animation data, the complete compiled .rodata is 252 bytes and remains byte exact. All 38 previously passing complete-function proofs still pass. The full European reconstruction also passes: 1229 verified units, 1356494 credited C bytes (95.05701343768044%), full 16 MiB comparison and expected SHA1. The data change itself adds no code credit. This gate includes the separate European pause-map palette commit 5a8ab5a and uses the older local matcher; production must independently rebuild.

The constructor now records a TODO for another preserved ordering issue: it initializes its language-indexed Object11 before validating gLanguage. Inputs beyond the table range can index out of bounds. The original ordering is retained instead of moving validation and changing behavior.

# European title screen and language selector

Original katam title implementation remains under the USA #else branch. Regional reconstruction by MatyMeatBoy derives directly from the owned B8KP rev0 ROM (SHA1 6f478a455383a2a12378f292581dfd7300300700), preserving the original contributors' implementation and attribution. No external code was imported.

The European task allocates0x380bytes, contains21sprites at0xC, main state callback0x354, signed state counter0x358, Object11 at0x35C, auxiliary callback0x368 and three signed language fields at0x36C/36E/36F. Its flags replace the USA numeric state. Unknown fields remain unnamed. The region-specific implementation is included from title_screen_eu.inc only with REGION_EU. Remaining unimplemented callbacks are explicit extern functions and remain ROM-backed pending code, not invented C.

The constructor validates the existing u16 gLanguage to1..5, stores the zero-based selection and changes key repeat intervals20/4. Destruction frees all21sprites and restores intervals20/8. The main routine preserves the original timeout field, flag tests, auxiliary callback and main callback ordering. The selector at0x0814AA70 preserves A/Start acceptance, B cancellation, five-language Up/Down wrap, original sounds, UpdateSaveBufferByOffset(0,0) and final update call. Its language write at0x0814AAC6 is STRH; the constructor's final byte read is represented by a read cast, not a changed storage declaration. All five languages, including Spanish, remain selectable.

Individually compiled with pinned agbcc59b966ed1b8f371856dcf99f1546c2fe89c678ca and original -mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g, CPP REGION_EU only. Complete fixed-byte comparison and strict relocation proof pass at these candidate addresses:

| Function | EU address | Bytes |
|---|---:|---:|
|CreateTitleScreen|0x08149DCC|300|
|EuTitleDestroy|0x08149EF8|116|
|EuTitleMain|0x08149F6C|132|
|sub_0814AA70|0x0814AA70|248|
|sub_0814ABC4|0x0814ABC4|60|
|sub_0814AC00|0x0814AC00|32|
|sub_0814AC20|0x0814AC20|68|
|sub_0814AC64|0x0814AC64|72|
|sub_0814ACAC|0x0814ACAC|68|
|sub_0814B090|0x0814B090|36|
|sub_0814B0B4|0x0814B0B4|68|
|sub_0814B0F8|0x0814B0F8|72|
|sub_0814B140|0x0814B140|36|

Total compiled source text1308bytes. Some complete functions legitimately have multiple identical instruction patterns: AC20/ACAC, B090/B140, and other fade states. Their sites require consistent callback/relocation context; the table does not itself grant C credit or claim unique matches for them. No partial-function credit is requested.

Independent USA compilation of the unchanged branch versus HEAD original yielded identical2884-byte .text, full .rodata and text relocation signatures. This is not the six-output USA ROM gate. The first548-byte European cohort passed full16MiB comparison/SHA1 with1353120creditedCbytes; adding the248-byte selector passed with1353368Cbytes. These worktree totals precede the final additional-state cohort and are not production receipts. Production must rebuild using its explicitly declared regional CPP profile; the local metadata recipe used for experiments is not committed.

Final1308-byte cohort gate:172objects,1412488executable object bytes;1209verifiedunits,1353532creditedCbytes,94.84944976706899%; complete16MiB comparison and expected SHA1 passed. Increase over selector cohort is164creditedbytes; remaining348new source bytes are not claimed as credit by this matcher because their repeated patterns/context are not yet resolved. This distinction is intentional.

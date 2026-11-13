# EU Shotzo aiming callback: unmatched C audit

`sub_0811AB74` starts at EU `0x0811ABBC` in the Shotzo module at `0x0811A788`. The owned `B8KP` image is 16 MiB with SHA1 `6f478a455383a2a12378f292581dfd7300300700`. The readable draft remains under `NONMATCHING`; this audit awards no C bytes and does not replace the assembly fallback.

## Function extent and alignment

The default object's assembly `STT_FUNC` reports 872 bytes, whereas the readable C definition reports 870. These sizes do not mean that the C body lost a two-byte instruction. Both versions put the next callback at the same address and occupy 872 bytes through that boundary. The final `bx r0` ends at function offset `0x366` in both versions. The assembly include's final `.align 2, 0` is inside its function symbol; the compiler's alignment after the C definition is outside that symbol.

| Contribution | Default assembly | Readable C |
|---|---:|---:|
| Instruction bytes | 796 | 798 |
| Literals and jump table | 72 | 72 |
| Internal literal alignment | 2 | 0 |
| Final alignment | 2 | 2 |
| Extent to next callback | 872 | 872 |

The 72 data bytes comprise a four-byte jump-table pointer, sixteen four-byte jump-table entries, and a four-byte callback pointer. In the assembly, internal padding occupies `[+0x2A2,+0x2A4)` before the callback literal at `+0x2A4`. Both versions have final padding `[+0x366,+0x368)`. The C callback literal is at `+0x298` and needs no internal padding. Thus the C version has one additional net Thumb instruction, compensated by two fewer internal alignment bytes; neither the symbol-size difference nor aggregate section size establishes matching.

## Identified compiler transformation

The compiler is `jiangzhengwenjz/agbcc` revision `59b966ed1b8f371856dcf99f1546c2fe89c678ca`, using the original new-compiler flags including `-O2 -f2003-patch`. The first fixed difference is a conditional-branch displacement at function `+0x98`: target halfword `D020`, draft `D022`. This is an early consequence of different later block layout, rather than the first different operation executed on every path.

The draft initially emits both `unk83 == 3` reads: its `.greg` dump, after register allocation and reload, contains load/compare instruction IDs `309/313` for cases 7/8 and `723/727` for cases 9/10. The `.jump2` dump retains the first pair and removes the second. The actual IDs are diagnostic for this exact input and may change when unrelated source or debug-line inputs change.

The pinned `gcc/toplev.c` runs `jump_optimize(insns, JUMP_CROSS_JUMP, JUMP_NOOP_MOVES, ...)` after reload and immediately before the `.jump2` dump. In `gcc/jump.c`, `find_cross_jump` walks backward over suffixes ending at the same destination, compares the already assigned register RTL with `rtx_renumbered_equal_p`, and `do_cross_jump` redirects one predecessor and deletes its duplicate instructions. This explains why two source-level reads survive allocation but only one survives the last jump pass. It is not evidence of an earlier type-width fold or of a different regional function boundary.

To retain a separate read naturally, its continuation must cease being the same cross-jumpable suffix: distinct incoming value lifetimes or a genuine shared update/join boundary are relevant; merely spelling the same comparison twice is insufficient. Explicit shared-store and clear joins, inverted conditions, nested arms, and narrow direction temporaries tested so far change other blocks without reproducing the full target. There is no verified natural reconstruction yet. A label or an empty asm chosen solely to defeat this pass would be matching debt, not proof of original control flow.

Generate the two pass dumps from a freshly preprocessed draft with:

```sh
tools/agbcc/bin/agbcc -mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g -dJg -dumpbase build/research/shotzo-audit/passes -o build/research/shotzo-audit/passes.s build/research/shotzo-audit/draft.i
```

## Reproducing the bounded execution experiment

Install optional research dependency `unicorn==2.1.4` in a separate Python environment. From an MSYS2 shell at the repository root, compile two fresh objects without changing source:

```sh
mkdir -p build/research/shotzo-audit
for mode in default draft; do
    extra=
    if [ "$mode" = draft ]; then extra=-DNONMATCHING; fi
    gcc -E -iquote include -Wno-trigraphs -DMODERN=0 -I tools/agbcc/include -I tools/agbcc -nostdinc -iquote include -DREVISION=0 -DENGLISH -DREGION_EU $extra src/shotzo.c | tools/preproc/preproc -i src/shotzo.c > build/research/shotzo-audit/$mode.i
    tools/agbcc/bin/agbcc -mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g -o build/research/shotzo-audit/$mode.s build/research/shotzo-audit/$mode.i
    { cat build/research/shotzo-audit/$mode.s; printf '\n.text\n.align 2, 0\n'; } | arm-none-eabi-as -mcpu=arm7tdmi --defsym REVISION=0 --defsym ENGLISH=1 -o build/research/shotzo-audit/$mode.o -
done
python docs/research/scripts/check_shotzo_aiming.py --rom baserom_eu.gba --reference-object build/research/shotzo-audit/default.o --candidate-object build/research/shotzo-audit/draft.o --output build/research/shotzo-audit/semantic-result.json
```

The script first requires a unique, fully relocated default-module match against the EU image; it does not trust an external symbol list or a cached binding receipt. It relocates the compiled candidate with those proven external bindings and executes the actual Thumb instructions in Unicorn. It records the ROM and object hashes. Generated objects and result JSON stay under ignored `build/`.

The tested domain is 16 angle bins × four `unk83` values × two facing-bit values × `unk85` values `{0,1,255}` × subtype values `{0,1,2,3,255}`: 1,920 cases. `FindTargetKirby` returns one controlled object, `ArcTan2` returns the selected angle bin, and `sub_0811AEDC` / `sub_0811A874` record their calls without executing their effects. The check compares final object bytes, callback identity, helper names/arguments/object snapshots, callee-saved registers, and stack restoration. All 1,920 cases pass for the current draft. A negative control changing one increment from one to two is rejected, first in angle bin 9, direction 0, facing bit 1, with the differing object byte correctly identified as `0x83`.

This is finite, stubbed execution evidence. It does not establish all input values, helper side effects, interrupts, timing, hardware behavior, undefined-behavior freedom, original source authenticity, or binary matching. The fixed coordinate inputs also do not exhaust coordinate-wrap boundaries. The authoritative EU byte comparison remains necessary before any additional C credit.

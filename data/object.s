    .include "asm/macros.inc"
    .include "constants/constants.inc"

    .section .rodata

gUnk_0835105C:: @ 0835105C
	.incbin "baserom.gba", 0x35105C, 0x0000020

    .include "data/object_spawn_table.inc"

gUnk_083513E8:: @ 083513E8
	.incbin "baserom.gba", 0x3513E8, 0x0000070

gUnk_08351458:: @ 08351458
	.incbin "baserom.gba", 0x351458, 0x00000D8

gUnk_08351530:: @ 08351530
	.incbin "baserom.gba", 0x351530, 0x00000D8

gUnk_08351608:: @ 08351608
	.incbin "baserom.gba", 0x351608, 0x0000020

gUnk_08351628:: @ 08351628
	.incbin "baserom.gba", 0x351628, 0x0000020

gUnk_08351648:: @ 08351648
	.incbin "baserom.gba", 0x351648, 0x0001488

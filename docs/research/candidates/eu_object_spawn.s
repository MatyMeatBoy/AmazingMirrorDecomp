/* B8KP source-data candidate. Not yet selected by an EU data linker profile. */
    .ifndef REGION_EU
    .error "EU object data requires REGION_EU=1"
    .endif
    .section .rodata
    .balign 4
    .type gUnk_0835105C, %object
    .global gUnk_0835105C
gUnk_0835105C: /* EU 0x08352B3C; existing unknown identifier retained. */
    .2byte 0x03E7, 0x0144, 0x02C6, 0x01A1, 0x0336, 0x00DB, 0x0204, 0x02E2
    .2byte 0x0081, 0x038D, 0x038E, 0x0390, 0x0392, 0x0394, 0x0396, 0x0397
    .size gUnk_0835105C, . - gUnk_0835105C

    .include "data/object_spawn_table.inc"

	.syntax unified
	.text

	push {lr}
	adds r3, r0, #0
	movs r0, #0x9e
	adds r0, r0, r3
	mov ip, r0
	ldrb r0, [r0]
	lsls r1, r0, #0x18
	lsrs r0, r1, #0x18
	cmp r0, #7
	bhi _0811AB06
	adds r0, r3, #0
	adds r0, #0x83
	ldrb r0, [r0]
	cmp r0, #1
	beq _0811AAB8
	cmp r0, #1
	bgt _0811AAA8
	cmp r0, #0
	beq _0811AAAE
	b _0811AAE8
_0811AAA8:
	cmp r0, #3
	beq _0811AAC0
	b _0811AAE8
_0811AAAE:
	ldr r2, _0811AAB4 @ =gUnk_08357C14
	b _0811AAC2
	.align 2, 0
_0811AAB4: .4byte gUnk_08357C14
_0811AAB8:
	ldr r2, _0811AABC @ =gUnk_08357C24
	b _0811AAC2
	.align 2, 0
_0811AABC: .4byte gUnk_08357C24
_0811AAC0:
	ldr r2, _0811AB34 @ =gUnk_08357C34
_0811AAC2:
	lsrs r0, r1, #0x19
	lsls r0, r0, #2
	adds r0, r0, r2
	ldrh r0, [r0]
	lsrs r0, r0, #8
	adds r1, r3, #0
	adds r1, #0x54
	strb r0, [r1]
	mov r0, ip
	ldrb r1, [r0]
	movs r0, #1
	orrs r0, r1
	lsls r0, r0, #1
	adds r0, r0, r2
	ldrh r0, [r0]
	lsrs r0, r0, #8
	adds r1, r3, #0
	adds r1, #0x55
	strb r0, [r1]
_0811AAE8:
	adds r1, r3, #0
	adds r1, #0x9e
	ldrb r0, [r1]
	adds r0, #1
	strb r0, [r1]
	ldr r0, [r3, #8]
	movs r1, #1
	ands r0, r1
	cmp r0, #0
	beq _0811AB06
	adds r1, r3, #0
	adds r1, #0x54
	ldrb r0, [r1]
	rsbs r0, r0, #0
	strb r0, [r1]
_0811AB06:
	ldrh r0, [r3, #4]
	subs r0, #1
	strh r0, [r3, #4]
	lsls r0, r0, #0x10
	cmp r0, #0
	bne _0811AB70
	adds r1, r3, #0
	adds r1, #0x9e
	movs r0, #0
	strb r0, [r1]
	adds r1, #1
	ldrb r0, [r1]
	adds r0, #1
	strb r0, [r1]
	lsls r0, r0, #0x18
	lsrs r0, r0, #0x18
	cmp r0, #2
	bls _0811AB38
	adds r0, r3, #0
	bl sub_0811A9D4
	b _0811AB70
	.align 2, 0
_0811AB34: .4byte gUnk_08357C34
_0811AB38:
	adds r0, r3, #0
	adds r0, #0x87
	ldrb r0, [r0]
	cmp r0, #1
	beq _0811AB5A
	cmp r0, #1
	bgt _0811AB4C
	cmp r0, #0
	beq _0811AB56
	b _0811AB66
_0811AB4C:
	cmp r0, #2
	beq _0811AB5E
	cmp r0, #3
	beq _0811AB62
	b _0811AB66
_0811AB56:
	movs r0, #0x32
	b _0811AB68
_0811AB5A:
	movs r0, #0x28
	b _0811AB68
_0811AB5E:
	movs r0, #0x1e
	b _0811AB68
_0811AB62:
	movs r0, #0x16
	b _0811AB68
_0811AB66:
	movs r0, #0x11
_0811AB68:
	strh r0, [r3, #4]
	adds r0, r3, #0
	bl sub_0811AEDC
_0811AB70:
	pop {r0}
	bx r0
	.syntax divided

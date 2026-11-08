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
	bhi _0811A9BA
	adds r0, r3, #0
	adds r0, #0x83
	ldrb r0, [r0]
	cmp r0, #1
	beq _0811A96C
	cmp r0, #1
	bgt _0811A95C
	cmp r0, #0
	beq _0811A962
	b _0811A99C
_0811A95C:
	cmp r0, #3
	beq _0811A974
	b _0811A99C
_0811A962:
	ldr r2, _0811A968 @ =gUnk_08357C14
	b _0811A976
	.align 2, 0
_0811A968: .4byte gUnk_08357C14
_0811A96C:
	ldr r2, _0811A970 @ =gUnk_08357C24
	b _0811A976
	.align 2, 0
_0811A970: .4byte gUnk_08357C24
_0811A974:
	ldr r2, _0811A9D0 @ =gUnk_08357C34
_0811A976:
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
_0811A99C:
	adds r1, r3, #0
	adds r1, #0x9e
	ldrb r0, [r1]
	adds r0, #1
	strb r0, [r1]
	ldr r0, [r3, #8]
	movs r1, #1
	ands r0, r1
	cmp r0, #0
	beq _0811A9BA
	adds r1, r3, #0
	adds r1, #0x54
	ldrb r0, [r1]
	rsbs r0, r0, #0
	strb r0, [r1]
_0811A9BA:
	ldrh r0, [r3, #4]
	subs r0, #1
	strh r0, [r3, #4]
	lsls r0, r0, #0x10
	cmp r0, #0
	bne _0811A9CC
	adds r0, r3, #0
	bl sub_0811A874
_0811A9CC:
	pop {r0}
	bx r0
	.align 2, 0
_0811A9D0: .4byte gUnk_08357C34
	.syntax divided

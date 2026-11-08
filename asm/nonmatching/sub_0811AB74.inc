	.syntax unified
	.text

	push {r4, r5, r6, lr}
	adds r4, r0, #0
	bl FindTargetKirby
	adds r2, r0, #0
	adds r0, r4, #0
	adds r0, #0xac
	str r2, [r0]
	ldr r0, [r2, #0x40]
	ldr r1, [r4, #0x40]
	subs r0, r0, r1
	lsls r0, r0, #8
	ldr r1, [r2, #0x44]
	ldr r2, [r4, #0x44]
	subs r1, r1, r2
	lsls r1, r1, #8
	asrs r0, r0, #0x10
	asrs r1, r1, #0x10
	bl ArcTan2
	lsls r0, r0, #0x10
	lsrs r0, r0, #0x1c
	cmp r0, #0xf
	bls _0811ABA6
	b _0811AECE
_0811ABA6:
	lsls r0, r0, #2
	ldr r1, _0811ABB0 @ =_0811ABB4
	adds r0, r0, r1
	ldr r0, [r0]
	mov pc, r0
	.align 2, 0
_0811ABB0: .4byte _0811ABB4
_0811ABB4: @ jump table
	.4byte _0811ADBA @ case 0
	.4byte _0811AE4A @ case 1
	.4byte _0811AE4A @ case 2
	.4byte _0811AE4A @ case 3
	.4byte _0811AE8C @ case 4
	.4byte _0811AE8C @ case 5
	.4byte _0811AE8C @ case 6
	.4byte _0811ABF4 @ case 7
	.4byte _0811ABF4 @ case 8
	.4byte _0811AC6A @ case 9
	.4byte _0811AC6A @ case 10
	.4byte _0811ACE0 @ case 11
	.4byte _0811ACE0 @ case 12
	.4byte _0811AD36 @ case 13
	.4byte _0811AD36 @ case 14
	.4byte _0811ADBA @ case 15
_0811ABF4:
	adds r0, r4, #0
	adds r0, #0x83
	ldrb r5, [r0]
	adds r3, r0, #0
	cmp r5, #0
	bne _0811AC40
	ldr r1, [r4, #8]
	movs r5, #1
	adds r0, r1, #0
	ands r0, r5
	adds r2, r1, #0
	cmp r0, #0
	beq _0811AC50
	adds r1, r4, #0
	adds r1, #0x85
	ldrb r0, [r1]
	cmp r0, #0
	bne _0811AC1A
	b _0811AD7C
_0811AC1A:
	adds r0, r4, #0
	adds r0, #0x87
	ldrb r0, [r0]
	cmp r0, #1
	beq _0811AC38
	cmp r0, #1
	bgt _0811AC2E
	cmp r0, #0
	beq _0811AC34
	b _0811ADFE
_0811AC2E:
	cmp r0, #2
	beq _0811AC3C
	b _0811ADFE
_0811AC34:
	movs r0, #0x50
	b _0811AE00
_0811AC38:
	movs r0, #0x3c
	b _0811AE00
_0811AC3C:
	movs r0, #0x28
	b _0811AE00
_0811AC40:
	ldr r1, [r4, #8]
	movs r0, #1
	ands r0, r1
	adds r2, r1, #0
	cmp r0, #0
	beq _0811AC50
	subs r0, r5, #1
	b _0811AE32
_0811AC50:
	ldrb r0, [r3]
	cmp r0, #3
	beq _0811AC58
	b _0811AE30
_0811AC58:
	movs r1, #1
	orrs r2, r1
	str r2, [r4, #8]
	movs r0, #2
	strb r0, [r3]
	adds r0, r4, #0
	adds r0, #0x9f
	strb r1, [r0]
	b _0811AEC6
_0811AC6A:
	adds r0, r4, #0
	adds r0, #0x83
	ldrb r5, [r0]
	adds r6, r5, #0
	adds r3, r0, #0
	cmp r6, #1
	bne _0811ACB8
	ldr r1, [r4, #8]
	adds r0, r1, #0
	ands r0, r6
	adds r2, r1, #0
	cmp r0, #0
	beq _0811ACD8
	adds r1, r4, #0
	adds r1, #0x85
	ldrb r0, [r1]
	cmp r0, #0
	beq _0811ACB4
	adds r0, r4, #0
	adds r0, #0x87
	ldrb r0, [r0]
	cmp r0, #1
	beq _0811ACAC
	cmp r0, #1
	bgt _0811ACA2
	cmp r0, #0
	beq _0811ACA8
	b _0811ADFE
_0811ACA2:
	cmp r0, #2
	beq _0811ACB0
	b _0811ADFE
_0811ACA8:
	movs r0, #0x50
	b _0811AE00
_0811ACAC:
	movs r0, #0x3c
	b _0811AE00
_0811ACB0:
	movs r0, #0x28
	b _0811AE00
_0811ACB4:
	strb r6, [r1]
	b _0811AECE
_0811ACB8:
	ldr r1, [r4, #8]
	movs r0, #1
	ands r0, r1
	adds r2, r1, #0
	cmp r0, #0
	beq _0811ACD8
	cmp r6, #0
	bne _0811ACD4
	adds r0, r5, #1
	strb r0, [r3]
	adds r0, r4, #0
	adds r0, #0x85
	strb r6, [r0]
	b _0811AECE
_0811ACD4:
	subs r0, r5, #1
	b _0811AE32
_0811ACD8:
	ldrb r0, [r3]
	cmp r0, #3
	beq _0811AC58
	b _0811AE30
_0811ACE0:
	adds r0, r4, #0
	adds r0, #0x83
	ldrb r2, [r0]
	adds r3, r0, #0
	cmp r2, #3
	bne _0811AD2A
	ldr r0, [r4, #8]
	movs r2, #1
	ands r0, r2
	cmp r0, #0
	beq _0811ACF8
	b _0811AE2A
_0811ACF8:
	adds r1, r4, #0
	adds r1, #0x85
	ldrb r0, [r1]
	cmp r0, #0
	bne _0811AD04
	b _0811AE1C
_0811AD04:
	adds r0, r4, #0
	adds r0, #0x87
	ldrb r0, [r0]
	cmp r0, #1
	beq _0811AD22
	cmp r0, #1
	bgt _0811AD18
	cmp r0, #0
	beq _0811AD1E
	b _0811ADFE
_0811AD18:
	cmp r0, #2
	beq _0811AD26
	b _0811ADFE
_0811AD1E:
	movs r0, #0x50
	b _0811AE00
_0811AD22:
	movs r0, #0x3c
	b _0811AE00
_0811AD26:
	movs r0, #0x28
	b _0811AE00
_0811AD2A:
	ldr r1, [r4, #8]
	movs r0, #1
	ands r1, r0
	cmp r1, #0
	beq _0811ADAE
	b _0811AE2A
_0811AD36:
	adds r0, r4, #0
	adds r0, #0x83
	ldrb r2, [r0]
	adds r5, r2, #0
	adds r3, r0, #0
	cmp r5, #1
	bne _0811AD80
	ldr r0, [r4, #8]
	ands r0, r5
	cmp r0, #0
	bne _0811AE2A
	adds r1, r4, #0
	adds r1, #0x85
	ldrb r0, [r1]
	cmp r0, #0
	beq _0811AD7C
	adds r0, r4, #0
	adds r0, #0x87
	ldrb r0, [r0]
	cmp r0, #1
	beq _0811AD74
	cmp r0, #1
	bgt _0811AD6A
	cmp r0, #0
	beq _0811AD70
	b _0811ADFE
_0811AD6A:
	cmp r0, #2
	beq _0811AD78
	b _0811ADFE
_0811AD70:
	movs r0, #0x50
	b _0811AE00
_0811AD74:
	movs r0, #0x3c
	b _0811AE00
_0811AD78:
	movs r0, #0x28
	b _0811AE00
_0811AD7C:
	strb r5, [r1]
	b _0811AECE
_0811AD80:
	ldr r1, [r4, #8]
	movs r6, #1
	ands r1, r6
	cmp r1, #0
	bne _0811AE2A
	cmp r5, #3
	bne _0811ADAE
	subs r0, r2, #1
	strb r0, [r3]
	lsls r0, r0, #0x18
	lsrs r0, r0, #0x18
	cmp r0, #2
	beq _0811AD9C
	b _0811AEC6
_0811AD9C:
	adds r0, r4, #0
	adds r0, #0x9f
	strb r6, [r0]
	b _0811AEC6
_0811ADA4:
	adds r1, r4, #0
	adds r1, #0x9f
	movs r0, #2
	strb r0, [r1]
	b _0811AE32
_0811ADAE:
	adds r0, r2, #1
	strb r0, [r3]
	adds r0, r4, #0
	adds r0, #0x85
	strb r1, [r0]
	b _0811AECE
_0811ADBA:
	adds r1, r4, #0
	adds r1, #0x83
	ldrb r2, [r1]
	adds r3, r1, #0
	cmp r2, #0
	bne _0811AE20
	ldr r0, [r4, #8]
	movs r2, #1
	ands r0, r2
	cmp r0, #0
	bne _0811AE2A
	adds r1, #2
	ldrb r0, [r1]
	cmp r0, #0
	beq _0811AE1C
	adds r0, r4, #0
	adds r0, #0x87
	ldrb r0, [r0]
	cmp r0, #1
	beq _0811ADF6
	cmp r0, #1
	bgt _0811ADEC
	cmp r0, #0
	beq _0811ADF2
	b _0811ADFE
_0811ADEC:
	cmp r0, #2
	beq _0811ADFA
	b _0811ADFE
_0811ADF2:
	movs r0, #0x50
	b _0811AE00
_0811ADF6:
	movs r0, #0x3c
	b _0811AE00
_0811ADFA:
	movs r0, #0x28
	b _0811AE00
_0811ADFE:
	movs r0, #0x14
_0811AE00:
	strh r0, [r4, #4]
	adds r1, r4, #0
	adds r1, #0x9e
	movs r0, #0
	strb r0, [r1]
	ldr r0, _0811AE18 @ =sub_0811A934
	str r0, [r4, #0x78]
	adds r0, r4, #0
	bl sub_0811AEDC
	b _0811AED4
	.align 2, 0
_0811AE18: .4byte sub_0811A934
_0811AE1C:
	strb r2, [r1]
	b _0811AECE
_0811AE20:
	ldr r0, [r4, #8]
	movs r5, #1
	ands r0, r5
	cmp r0, #0
	beq _0811AE36
_0811AE2A:
	ldrb r0, [r3]
	cmp r0, #1
	beq _0811ADA4
_0811AE30:
	adds r0, #1
_0811AE32:
	strb r0, [r3]
	b _0811AEC6
_0811AE36:
	subs r0, r2, #1
	strb r0, [r1]
	lsls r0, r0, #0x18
	lsrs r0, r0, #0x18
	cmp r0, #2
	bne _0811AEC6
	adds r0, r4, #0
	adds r0, #0x9f
	strb r5, [r0]
	b _0811AEC6
_0811AE4A:
	ldr r0, [r4, #8]
	movs r2, #1
	ands r0, r2
	cmp r0, #0
	beq _0811AE70
	adds r1, r4, #0
	adds r1, #0x83
	ldrb r0, [r1]
	cmp r0, #1
	bne _0811AE6A
	adds r2, r4, #0
	adds r2, #0x9f
	movs r0, #2
	strb r0, [r2]
	strb r0, [r1]
	b _0811AEC6
_0811AE6A:
	adds r0, #1
	strb r0, [r1]
	b _0811AEC6
_0811AE70:
	adds r1, r4, #0
	adds r1, #0x83
	ldrb r0, [r1]
	cmp r0, #0
	beq _0811AE7E
	subs r0, #1
	strb r0, [r1]
_0811AE7E:
	ldrb r0, [r1]
	cmp r0, #2
	bne _0811AEC6
	adds r0, r4, #0
	adds r0, #0x9f
	strb r2, [r0]
	b _0811AEC6
_0811AE8C:
	ldr r1, [r4, #8]
	movs r3, #1
	adds r0, r1, #0
	ands r0, r3
	cmp r0, #0
	beq _0811AEA8
	adds r1, r4, #0
	adds r1, #0x83
	ldrb r0, [r1]
	cmp r0, #0
	beq _0811AEC6
	subs r0, #1
	strb r0, [r1]
	b _0811AEC6
_0811AEA8:
	adds r2, r4, #0
	adds r2, #0x83
	ldrb r0, [r2]
	cmp r0, #3
	bne _0811AEC2
	orrs r1, r3
	str r1, [r4, #8]
	movs r0, #2
	strb r0, [r2]
	adds r0, r4, #0
	adds r0, #0x9f
	strb r3, [r0]
	b _0811AEC6
_0811AEC2:
	adds r0, #1
	strb r0, [r2]
_0811AEC6:
	adds r1, r4, #0
	adds r1, #0x85
	movs r0, #0
	strb r0, [r1]
_0811AECE:
	adds r0, r4, #0
	bl sub_0811A874
_0811AED4:
	pop {r4, r5, r6}
	pop {r0}
	bx r0
	.align 2, 0
	.syntax divided

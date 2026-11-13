#include "code_0800ECAC.h"
#include "kirby.h"
#include "functions.h"
#include "object_collision.h"
#include "constants/kirby.h"

// TODO: Verify the terrain-grid interpretation against every reader and writer.
// The apparent 5x5 grid spans unk1C, unk26 and unk2B, but contiguous fields alone
// do not establish valid C pointer arithmetic across separate array objects.
// TODO(layout): This provisional C can index beyond the declared array object;
// recover the allocation and combined layout before treating those accesses as defined.
// TODO(match): Recover matching C for the complete function. The readable branch
// is a compile-checked hypothesis; its behavior and regional match are unverified.

void sub_0800F044(struct Unk_02038590 *a1) {
    struct Kirby *kirby = a1->unk40;
    struct LevelInfo *li = a1->unk14;
    s16 array[4] = {
        li->unk_S32Vec2_6C.x >> 12, li->unk_S32Vec2_6C.y >> 12,
        li->unk_S32Vec2_74.x >> 12, li->unk_S32Vec2_74.y >> 12,
    };
    u16 kirbyCellX;
    s32 kirbyCellY;
    u8 *r5;
    u8 *q;
    bool32 r6;
    struct Object **objs;
    s32 xm1, xp1, ym1, yp1;
    s16 kirbyPixelX, kirbyPixelY;

    kirbyCellX = kirby->base.x >> 12;
    kirbyCellY = (u16)(kirby->base.y >> 12);
    r6 = FALSE;
    a1->unk26[2] = 0;
    switch (gCollisionAttributes[sub_080024F0(a1->unk14, kirbyCellX, kirbyCellY)] & 0xF0000000) {
    case 0x20000000:
    case 0x30000000:
    case 0x40000000:
    case 0x60000000:
        r6 = TRUE;
        break;
    }
    r5 = a1->unk26;
    xm1 = kirbyCellX - 1;
    if ((u16)array[0] >= xm1 || xm1 >= (u16)array[2])
        r5[1] = 0xFF;
    else if (a1->unk26[2])
        r5[1] = a1->unk26[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, (u16)(kirbyCellX + -1), kirbyCellY)];

        if (r1 & 0x2000)
            r5[1] = 1;
        else if (r1 & 0x200) {
            if (r6)
                r5[1] = 0;
            else if (r1 & 0x1000)
                r5[1] = 3;
            else
                r5[1] = 2;
        } else if (r1 & 0x400) {
            r5[1] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[1] = 0;
        }
    }
    if ((u16)array[0] >= kirbyCellX - 2 || kirbyCellX - 2 >= (u16)array[2])
        r5[0] = 0xFF;
    else if (a1->unk26[1])
        r5[0] = a1->unk26[1];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, (u16)(kirbyCellX + -2), kirbyCellY)];

        if (r1 & 0x2000)
            r5[0] = 1;
        else if (r1 & 0x200) {
            if (r1 & 0x1000)
                r5[0] = 3;
            else
                r5[0] = 2;
        } else if (r1 & 0x400) {
            r5[0] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[0] = 0;
        }
    }
    xp1 = kirbyCellX + 1;
    if ((u16)array[0] >= xp1 || xp1 >= (u16)array[2])
        r5[3] = 0xFF;
    else if (a1->unk26[2])
        r5[3] = a1->unk26[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, (u16)xp1, kirbyCellY)];

        if (r1 & 0x2000)
            r5[3] = 1;
        else if (r1 & 0x200) {
            if (r6)
                r5[3] = 0;
            else if (r1 & 0x1000)
                r5[3] = 3;
            else
                r5[3] = 2;
        } else if (r1 & 0x400) {
            r5[3] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[3] = 0;
        }
    }
    q = r5;
    if ((u16)array[0] >= kirbyCellX + 2 || kirbyCellX + 2 >= (u16)array[2])
        q[4] = 0xFF;
    else if (a1->unk26[3])
        q[4] = a1->unk26[3];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, (u16)(kirbyCellX + 2), kirbyCellY)];

        if (r1 & 0x2000)
            q[4] = 1;
        else if (r1 & 0x200) {
            if (r1 & 0x1000)
                q[4] = 3;
            else
                q[4] = 2;
        } else if (r1 & 0x400) {
            q[4] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[4] = 0;
        }
    }
    r5 = a1->unk1C;
    ym1 = kirbyCellY - 1;
    if ((u16)array[1] >= ym1 || ym1 >= (u16)array[3])
        r5[7] = 0xFF;
    else if (a1->unk26[2])
        r5[7] = a1->unk26[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, kirbyCellX, (u16)(kirbyCellY + -1))];

        if (r1 & 0x2000)
            r5[7] = 1;
        else if (r1 & 0x200) {
            if (r1 & 0x1000)
                r5[7] = 3;
            else
                r5[7] = 2;
        } else if (r1 & 0x400) {
            r5[7] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[7] = 0;
        }
    }
    if ((u16)array[1] >= kirbyCellY - 2 || kirbyCellY - 2 >= (u16)array[3])
        r5[2] = 0xFF;
    else if (a1->unk1C[7])
        r5[2] = a1->unk1C[7];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, kirbyCellX, (u16)(kirbyCellY + -2))];

        if (r1 & 0x2000)
            r5[2] = 1;
        else if (r1 & 0x200) {
            if (r1 & 0x1000)
                r5[2] = 3;
            else
                r5[2] = 2;
        } else if (r1 & 0x400) {
            r5[2] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[2] = 0;
        }
    }
    yp1 = kirbyCellY + 1;
    if ((u16)array[1] >= yp1 || yp1 >= (u16)array[3])
        r5[0x11] = 0xFF;
    else if (a1->unk26[2])
        r5[0x11] = a1->unk26[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, kirbyCellX, (u16)yp1)];

        if (r1 & 0x2000)
            r5[0x11] = 1;
        else if (r1 & 0x20C) {
            if (r1 & 0x1000)
                r5[0x11] = 3;
            else
                r5[0x11] = 2;
        } else if (r1 & 0x400) {
            r5[0x11] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[0x11] = 0;
        }
    }
    if ((u16)array[1] >= kirbyCellY + 2 || kirbyCellY + 2 >= (u16)array[3])
        r5[0x16] = 0xFF;
    else if (a1->unk2B[2])
        r5[0x16] = a1->unk2B[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, kirbyCellX, (u16)(kirbyCellY + 2))];

        if (r1 & 0x2000)
            r5[0x16] = 1;
        else if (r1 & 0x20C) {
            if (r1 & 0x1000)
                r5[0x16] = 3;
            else
                r5[0x16] = 2;
        } else if (r1 & 0x400) {
            r5[0x16] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[0x16] = 0;
        }
    }
    q = r5;
    if ((u16)array[0] >= xm1 || xm1 >= (u16)array[2]
        || (u16)array[1] >= ym1 || ym1 >= (u16)array[3])
        q[0x6] = 0xFF;
    else if (a1->unk26[2])
        r5[0x6] = a1->unk26[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, (u16)(kirbyCellX + -1), (u16)(kirbyCellY + -1))];

        if (r1 & 0x2000)
            r5[0x6] = 1;
        else if (r1 & 0x200) {
            if (r1 & 0x1000)
                r5[0x6] = 3;
            else
                r5[0x6] = 2;
        } else if (r1 & 0x400) {
            r5[0x6] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[0x6] = 0;
        }
    }
    q = r5;
    if ((u16)array[0] >= xp1 || xp1 >= (u16)array[2]
        || (u16)array[1] >= ym1 || ym1 >= (u16)array[3])
        q[8] = 0xFF;
    else if (a1->unk26[2])
        r5[8] = a1->unk26[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, (u16)xp1, (u16)(kirbyCellY + -1))];

        if (r1 & 0x2000)
            r5[8] = 1;
        else if (r1 & 0x200) {
            if (r1 & 0x1000)
                r5[8] = 3;
            else
                r5[8] = 2;
        } else if (r1 & 0x400) {
            r5[8] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[8] = 0;
        }
    }
    q = r5;
    if ((u16)array[0] >= xp1 || xp1 >= (u16)array[2]
        || (u16)array[1] >= yp1 || yp1 >= (u16)array[3])
        q[0x12] = 0xFF;
    else if (a1->unk26[2])
        r5[0x12] = a1->unk26[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, (u16)xp1, (u16)yp1)];

        if (r1 & 0x2000)
            r5[0x12] = 1;
        else if (r1 & 0x20C) {
            if (r1 & 0x1000)
                r5[0x12] = 3;
            else
                r5[0x12] = 2;
        } else if (r1 & 0x400) {
            r5[0x12] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[0x12] = 0;
        }
    }
    q = r5;
    if ((u16)array[0] >= xm1 || xm1 >= (u16)array[2]
        || (u16)array[1] >= yp1 || yp1 >= (u16)array[3])
        q[0x10] = 0xFF;
    else if (a1->unk26[2])
        r5[0x10] = a1->unk26[2];
    else {
        u32 r1 = gCollisionAttributes[sub_080024F0(li, (u16)(kirbyCellX + -1), (u16)yp1)];

        if (r1 & 0x2000)
            r5[0x10] = 1;
        else if (r1 & 0x20C) {
            if (r1 & 0x1000)
                r5[0x10] = 3;
            else
                r5[0x10] = 2;
        } else if (r1 & 0x400) {
            r5[0x10] = kirby->ability != KIRBY_ABILITY_MINI ? 2 : 0;
        } else {
            r5[0x10] = 0;
        }
    }
    objs = GetRoomSolidCollisionList(&kirby->base);
    kirbyPixelX = kirby->base.x >> 8;
    kirbyPixelY = kirby->base.y >> 8;
    if (kirby->base.yspeed > 0) {
        if (kirby->base.flags & 1) {
            if (*objs != NULL) {
                s16 ty1 = kirbyPixelY - 0x10;
                s16 ty2 = kirbyPixelY - 0x20;
                s16 tx1 = kirbyPixelX - 0x10;
                s16 tx2 = kirbyPixelX - 0x20;

                do {
                    s16 rx = (*objs)->base.x >> 8;
                    s16 ry = (*objs)->base.y >> 8;

                    array[0] = (*objs)->base.unk3C + rx;
                    array[1] = (*objs)->base.unk3D + ry;
                    array[2] = (*objs)->base.unk3E + rx;
                    array[3] = (*objs)->base.unk3F + ry;
                    if (array[0] <= kirbyPixelX && array[2] >= kirbyPixelX) {
                        if (!r5[7]) {
                            if (array[1] <= ty1 && array[3] >= ty1)
                                r5[7] = 2;
                        } else if (!r5[2]) {
                            if (array[1] <= ty2 && array[3] >= ty2)
                                r5[2] = 2;
                        }
                    }
                    if (array[1] <= kirbyPixelY && array[3] >= kirbyPixelY) {
                        if (!r5[0xB]) {
                            if (array[0] <= tx1 && array[2] >= tx1)
                                r5[0xB] = 2;
                        } else if (!r5[0xA]) {
                            if (array[0] <= tx2 && array[2] >= tx2)
                                r5[0xA] = 2;
                        }
                    }
                    if (!r5[0x6]) {
                        s16 zz = kirbyPixelY - 0x10;

                        if (array[0] <= tx1 && array[2] >= tx1
                            && array[1] <= zz && array[3] >= zz)
                            r5[0x6] = 2;
                    }
                    objs++;
                } while (*objs != NULL);
            }
        } else {
            if (*objs != NULL) {
                s16 ty1 = kirbyPixelY - 0x10;
                s16 ty2 = kirbyPixelY - 0x20;
                s16 tx1 = kirbyPixelX + 0x10;
                s16 tx2 = kirbyPixelX + 0x20;

                do {
                    s16 rx = (*objs)->base.x >> 8;
                    s16 ry = (*objs)->base.y >> 8;

                    array[0] = (*objs)->base.unk3C + rx;
                    array[1] = (*objs)->base.unk3D + ry;
                    array[2] = (*objs)->base.unk3E + rx;
                    array[3] = (*objs)->base.unk3F + ry;
                    if (array[0] <= kirbyPixelX && array[2] >= kirbyPixelX) {
                        if (!r5[7]) {
                            if (array[1] <= ty1 && array[3] >= ty1)
                                r5[7] = 2;
                        } else if (!r5[2]) {
                            if (array[1] <= ty2 && array[3] >= ty2)
                                r5[2] = 2;
                        }
                    }
                    if (array[1] <= kirbyPixelY && array[3] >= kirbyPixelY) {
                        if (!r5[0xD]) {
                            if (array[0] <= tx1 && array[2] >= tx1)
                                r5[0xD] = 2;
                        } else if (!r5[0xE]) {
                            if (array[0] <= tx2 && array[2] >= tx2)
                                r5[0xE] = 2;
                        }
                    }
                    if (!r5[8]) {
                        s16 zz = kirbyPixelY - 0x10;

                        if (array[0] <= tx1 && array[2] >= tx1
                            && array[1] <= zz && array[3] >= zz)
                            r5[8] = 2;
                    }
                    objs++;
                } while (*objs != NULL);
            }
        }
    } else {
        if (kirby->base.flags & 1) {
            if (*objs != NULL) {
                s16 ty1 = kirbyPixelY - 0x10;
                s16 ty2 = kirbyPixelY - 0x20;
                s16 tx1 = kirbyPixelX - 0x10;
                s16 tx2 = kirbyPixelX - 0x20;

                do {
                    s16 rx = (*objs)->base.x >> 8;
                    s16 ry = (*objs)->base.y >> 8;

                    array[0] = (*objs)->base.unk3C + rx;
                    array[1] = (*objs)->base.unk3D + ry;
                    array[2] = (*objs)->base.unk3E + rx;
                    array[3] = (*objs)->base.unk3F + ry;
                    if (array[0] <= kirbyPixelX && array[2] >= kirbyPixelX) {
                        if (!r5[7]) {
                            if (array[1] <= ty1 && array[3] >= ty1)
                                r5[7] = 2;
                        } else if (!r5[2]) {
                            if (array[1] <= ty2 && array[3] >= ty2)
                                r5[2] = 2;
                        }
                    }
                    if (array[1] <= kirbyPixelY && array[3] >= kirbyPixelY) {
                        if (!r5[0xB]) {
                            if (array[0] <= tx1 && array[2] >= tx1)
                                r5[0xB] = 2;
                        } else if (!r5[0xA]) {
                            if (array[0] <= tx2 && array[2] >= tx2)
                                r5[0xA] = 2;
                        }
                    }
                    if (!r5[0x10]) {
                        s16 zz = kirbyPixelY + 0x10;

                        if (array[0] <= tx1 && array[2] >= tx1
                            && array[1] <= zz && array[3] >= zz)
                            r5[0x10] = 2;
                    }
                    objs++;
                } while (*objs != NULL);
            }
        } else {
            if (*objs != NULL) {
                s16 ty1 = kirbyPixelY - 0x10;
                s16 ty2 = kirbyPixelY - 0x20;
                s16 tx1 = kirbyPixelX + 0x10;
                s16 tx2 = kirbyPixelX + 0x20;

                do {
                    s16 rx = (*objs)->base.x >> 8;
                    s16 ry = (*objs)->base.y >> 8;

                    array[0] = (*objs)->base.unk3C + rx;
                    array[1] = (*objs)->base.unk3D + ry;
                    array[2] = (*objs)->base.unk3E + rx;
                    array[3] = (*objs)->base.unk3F + ry;
                    if (array[0] <= kirbyPixelX && array[2] >= kirbyPixelX) {
                        if (!r5[7]) {
                            if (array[1] <= ty1 && array[3] >= ty1)
                                r5[7] = 2;
                        } else if (!r5[2]) {
                            if (array[1] <= ty2 && array[3] >= ty2)
                                r5[2] = 2;
                        }
                    }
                    if (array[1] <= kirbyPixelY && array[3] >= kirbyPixelY) {
                        if (!r5[0xD]) {
                            if (array[0] <= tx1 && array[2] >= tx1)
                                r5[0xD] = 2;
                        } else if (!r5[0xE]) {
                            if (array[0] <= tx2 && array[2] >= tx2)
                                r5[0xE] = 2;
                        }
                    }
                    if (!r5[0x12]) {
                        s16 zz = kirbyPixelY + 0x10;

                        if (array[0] <= tx1 && array[2] >= tx1
                            && array[1] <= zz && array[3] >= zz)
                            r5[0x12] = 2;
                    }
                    objs++;
                } while (*objs != NULL);
            }
        }
    }
}

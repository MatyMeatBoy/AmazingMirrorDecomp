/* European title state; unexamined fields remain explicitly unnamed. */
struct EuTitle {
    /* 0x000 */ u32 unk0;
    /* 0x004 */ u32 flags;
    /* 0x008 */ s16 unk8;
    /* 0x00A */ s16 unkA;
    /* 0x00C */ struct Sprite sprites[21];
    /* 0x354 */ u32 (*unk354)(struct EuTitle *);
    /* 0x358 */ s16 unk358;
    /* 0x35A */ u8 filler35A[2];
    /* 0x35C */ struct Object11 unk35C;
    /* 0x368 */ void (*unk368)(struct EuTitle *);
    /* 0x36C */ s8 selectedLanguage;
    /* 0x36D */ s8 unk36D;
    /* 0x36E */ s8 cursorLanguage;
    /* 0x36F */ s8 previousLanguage;
    /* 0x370 */ u16 savedPalette[8];
}; /* size = 0x380 */

#include "save.h"
static const u16 gUnk_08387D58[][4] = {
    [LANGUAGE_JAPANESE] = { 0xDF, 0xDE, 0xE2, 0xE3 },
    [LANGUAGE_ENGLISH]  = { 0xCF, 0xCE, 0xE2, 0xE3 },
    [LANGUAGE_GERMAN]   = { 0xCB, 0xCA, 0xE2, 0xE3 },
    [LANGUAGE_FRENCH]   = { 0xD7, 0xD6, 0xE2, 0xE3 },
    [LANGUAGE_SPANISH]  = { 0xD3, 0xD2, 0xE2, 0xE3 },
    [LANGUAGE_ITALIAN]  = { 0xDB, 0xDA, 0xE2, 0xE3 },
};

struct EuTitleSpriteInfo {
    /* 0x0 */ u16 animId;
    /* 0x2 */ u8 variant;
    /* 0x3 */ u8 numTiles;
    /* 0x4 */ u8 palId;
    /* 0x5 */ u8 unk5;
    /* 0x6 */ u8 unk6[2];
}; /* size = 0x8 */
const struct EuTitleSpriteInfo gEuTitleSpriteInfos[21] = {
    {0x3aa, 11, 28, 0, 25, {0, 0}},
    {0x3aa, 0, 192, 1, 19, {0, 0}},
    {0x3aa, 17, 4, 2, 25, {0, 0}},
    {0x3aa, 17, 4, 2, 25, {0, 0}},
    {0x3aa, 17, 4, 2, 10, {0, 0}},
    {0x3aa, 17, 4, 2, 10, {0, 0}},
    {0x3aa, 1, 6, 4, 15, {0, 0}},
    {0x3aa, 6, 2, 4, 20, {0, 0}},
    {0x3aa, 12, 28, 0, 25, {0, 0}},
    {0x3aa, 2, 6, 5, 15, {0, 0}},
    {0x3aa, 7, 2, 5, 20, {0, 0}},
    {0x3aa, 13, 28, 0, 25, {0, 0}},
    {0x3aa, 3, 6, 6, 15, {0, 0}},
    {0x3aa, 8, 2, 6, 20, {0, 0}},
    {0x3aa, 14, 28, 0, 25, {0, 0}},
    {0x3aa, 4, 6, 7, 15, {0, 0}},
    {0x3aa, 9, 2, 7, 20, {0, 0}},
    {0x3aa, 15, 28, 0, 25, {0, 0}},
    {0x3aa, 5, 6, 8, 15, {0, 0}},
    {0x3aa, 10, 2, 8, 20, {0, 0}},
    {0x3aa, 16, 28, 0, 25, {0, 0}},
};
const u16 gEuTitleAuxSpriteInfos[6][3] = {
    {0x3aa, 0x12, 0x3},
    {0x3aa, 0x13, 0x9},
    {0x3aa, 0x14, 0xa},
    {0x3aa, 0x15, 0xb},
    {0x3aa, 0x16, 0xc},
    {0x3aa, 0x17, 0xd},
};

void CreateTitleScreen(void);
static void EuTitleDestroy(struct Task *task);
static void EuTitleMain(void);
inline void sub_0814ABC4(struct EuTitle *title);
void sub_08149FF0(struct EuTitle *title);
void sub_0814A134(struct EuTitle *title);
void sub_0814A1F0(struct EuTitle *title);
void sub_0814A30C(struct EuTitle *title);
void sub_0814A468(struct EuTitle *title);
u16 sub_0814A5BC(struct EuTitle *title);
static inline void EuTitleLoadBg(u8 bg, u16 r0, void* dest);
static inline void LoadBgPaletteWithTransformation_wrapper(const u16* a1, u8 a2, u16 a3);
u32 sub_0814A62C(struct EuTitle *title);
u32 sub_0814A874(struct EuTitle *title);
u32 sub_0814A8D4(struct EuTitle *title);
u32 sub_0814A9DC(struct EuTitle *title);
u32 sub_0814AA70(struct EuTitle *title);
void sub_0814AB68(u8 bg);
void sub_0814AB90(u8 bg);
inline void sub_0814AC00(struct EuTitle *title);
inline void sub_0814AC20(struct EuTitle *title);
inline void sub_0814AC64(struct EuTitle *title);
inline void sub_0814ACAC(struct EuTitle *title);
inline u32 sub_0814ACF0(struct EuTitle *title);
inline u32 sub_0814AD10(struct EuTitle *title);
inline u32 sub_0814AD60(struct EuTitle *title);
inline u32 sub_0814AD98(struct EuTitle *title);
inline u32 sub_0814ADD0(struct EuTitle *title);
inline u32 sub_0814AE2C(struct EuTitle *title);
inline u32 sub_0814AE68(struct EuTitle *title);
inline u32 sub_0814AEAC(struct EuTitle *title);
inline u32 sub_0814AEF4(struct EuTitle *title);
inline u32 sub_0814AF38(struct EuTitle *title);
inline u32 sub_0814AF80(struct EuTitle *title);
inline u32 sub_0814AFB0(struct EuTitle *title);
inline u32 sub_0814AFE4(struct EuTitle *title);
inline u32 sub_0814B040(struct EuTitle *title);
inline u32 sub_0814B090(struct EuTitle *title);
inline u32 sub_0814B0B4(struct EuTitle *title);
inline u32 sub_0814B0F8(struct EuTitle *title);
inline u32 sub_0814B140(struct EuTitle *title);

void CreateTitleScreen(void) {
    u8 i;
    struct Task *task;
    struct EuTitle *title;
    gDispCnt = DISPCNT_OBJ_ON | DISPCNT_BG2_ON | DISPCNT_BG1_ON | DISPCNT_OBJ_1D_MAP;
    gBgCntRegs[0] = BGCNT_TXT512x256 | BGCNT_SCREENBASE(0x1e) | BGCNT_PRIORITY(1);
    gBgCntRegs[1] = BGCNT_SCREENBASE(0x1d) | BGCNT_CHARBASE(1) | BGCNT_PRIORITY(2);
    gBgCntRegs[2] = BGCNT_SCREENBASE(0x1c) | BGCNT_CHARBASE(2) | BGCNT_PRIORITY(3);
    gBgScrollRegs[0][0] = 0x100;
    gBgScrollRegs[0][1] = 0;
    for (i = 1; i < 4; i++) {
        gBgScrollRegs[i][0] = gBgScrollRegs[i][1] = 0;
    }
    gBldRegs.bldCnt = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BD | BLDCNT_TGT1_OBJ | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG0;
    gBldRegs.bldAlpha = 0;
    gBldRegs.bldY = 16;
    for (i = 0; i < NUM_KEYS; i++) {
        gKeysFirstRepeatIntervals[i] = 20;
        gKeysContinuedRepeatIntervals[i] = 4;
    }
    task = TaskCreate(EuTitleMain, sizeof(struct EuTitle), 0x1000, TASK_USE_IWRAM, EuTitleDestroy);
    title = TaskGetStructPtr(task);
    CpuFill16(0, title, sizeof(struct EuTitle));
    title->flags |= 0x50;
    title->unk354 = sub_0814ACF0;
    /* TODO: The original initializes this language-indexed object before validating
     * gLanguage; values beyond the table can index out of bounds. Preserve the order. */
    sub_0814ABC4(title);
    if ((u16)(gLanguage - LANGUAGE_ENGLISH) > 4) {
        gLanguage = LANGUAGE_ENGLISH;
    }
    title->selectedLanguage = (u8)gLanguage - LANGUAGE_ENGLISH;
}

static void EuTitleDestroy(struct Task *task) {
    struct EuTitle *title, *tmp;
    u8 i;
    tmp = TaskGetStructPtr(task);
    title = tmp;
    for (i = 0; i < 21; i++) {
        struct Sprite *cur = &title->sprites[i];
        if (cur->tilesVram != 0) {
            VramFree(cur->tilesVram);
            cur->tilesVram = 0;
        }
    }
    for (i = 0; i < NUM_KEYS; i++) {
        gKeysFirstRepeatIntervals[i] = 20;
        gKeysContinuedRepeatIntervals[i] = 8;
    }
}

static void EuTitleMain(void) {
    struct EuTitle *title, *tmp;
    tmp = TaskGetStructPtr(gCurTask);
    title = tmp;
    title->unk0++;
    if (title->unk368 != NULL) {
        title->unk368(title);
    }
    if (title->unkA > 0x257 && !(title->flags & 0x28)) {
        title->flags |= 0x20;
        title->unk354 = sub_0814ADD0;
    }
    title->unk354(title);
}

inline void sub_0814ABC4(struct EuTitle *title) {
    sub_0814F3C4(&title->unk35C, *gUnk_08D626F0[gLanguage][1]);
    title->unk368 = sub_0814AC00;
}

void sub_08149FF0(struct EuTitle *title) {
    u8 i;
    struct Sprite *sprite;
    struct Sprite aux;
    for (i = 0; i < 21; i++) {
        sprite = &title->sprites[i];
        sprite->tilesVram = VramMalloc(gEuTitleSpriteInfos[i].numTiles);
        sprite->unk14 = gEuTitleSpriteInfos[i].unk5 << 6;
        sprite->animId = gEuTitleSpriteInfos[i].animId;
        sprite->variant = gEuTitleSpriteInfos[i].variant;
        sprite->unk16 = 0;
        sprite->unk1B = 0xff;
        sprite->unk1C = 0x10;
        sprite->palId = gEuTitleSpriteInfos[i].palId;
        sprite->x = -64;
        sprite->y = -64;
        sprite->unk8 = 0;
        sub_08155128(sprite);
    }
    title->sprites[3].unk8 |= 0x400;
    title->sprites[5].unk8 |= 0x400;
    for (i = 0; i < 6; i++) {
        aux.tilesVram = 0;
        aux.unk14 = 0xff;
        aux.animId = gEuTitleAuxSpriteInfos[i][0];
        aux.variant = gEuTitleAuxSpriteInfos[i][1];
        aux.unk16 = 0;
        aux.unk1B = 0xff;
        aux.unk1C = 0x10;
        aux.palId = gEuTitleAuxSpriteInfos[i][2];
        aux.x = -64;
        aux.y = -64;
        aux.unk8 = 0;
        sub_08155128(&aux);
    }
    title->savedPalette[0] = gObjPalette[9];
    title->savedPalette[1] = gObjPalette[10];
    title->savedPalette[2] = gObjPalette[6];
    title->savedPalette[3] = gObjPalette[7];
    title->savedPalette[4] = gObjPalette[31];
    title->savedPalette[5] = gObjPalette[30];
    title->savedPalette[6] = gObjPalette[21];
    title->savedPalette[7] = gObjPalette[20];
}

void sub_0814A134(struct EuTitle *title) {
    u8 i;
    struct Sprite *sprite;
    sprite = &title->sprites[title->selectedLanguage * 3 + 8];
    sprite->x = 120;
    sprite->y = 118;
    sprite = &title->sprites[0];
    sprite->x = 120;
    sprite->y = 132;
    sprite = &title->sprites[2];
    sprite->x = 52;
    sprite->y = title->unk36D * 14 + 118;
    sprite->palId = 2;
    sprite = &title->sprites[3];
    sprite->x = 188;
    sprite->y = title->unk36D * 14 + 118;
    sprite->palId = 2;
    for (i = 0; i < 5; i++) {
        sprite = &title->sprites[3 * i + 7];
        sprite->x = (i - 2) * 18 + 120;
        sprite->y = 132;
        sprite->palId = i + 4;
    }
    gObjPalette[7 - (u8)title->unk36D * 3] = title->savedPalette[0];
}

void sub_0814A1F0(struct EuTitle *title) {
    u8 i = title->unk36D;
    u8 j;
    u8 other = (title->unk36D + 1) % 2;
    struct Sprite *sprite;
    s32 y;
    gObjPalette[6 - i * 3] = title->savedPalette[0];
    gObjPalette[7 - i * 3] = title->savedPalette[1];
    gObjPalette[6 - other * 3] = title->savedPalette[2];
    gObjPalette[7 - other * 3] = title->savedPalette[3];
    gMainFlags |= MAIN_FLAG_OBJ_PALETTE_SYNC_ENABLE;
    sprite = &title->sprites[2];
    y = i * 14 + 118;
    sprite->y = y;
    if (!sub_08155128(sprite)) sprite->unk1B = 0xff;
    DisplaySprite(sprite);
    sprite = &title->sprites[3];
    sprite->y = y;
    if (!sub_08155128(sprite)) sprite->unk1B = 0xff;
    DisplaySprite(sprite);
    DisplaySprite(&title->sprites[0]);
    DisplaySprite(&title->sprites[title->selectedLanguage * 3 + 8]);
    for (j = 0; j < 5; j++) {
        DisplaySprite(&title->sprites[3 * j + 7]);
    }
}

void sub_0814A30C(struct EuTitle *title) {
    u8 i;
    struct Sprite *sprite;
    struct Sprite *rightArrow;
    sprite = &title->sprites[1];
    sprite->x = 120;
    sprite->y = 77;
    for (i = 0; i < 5; i++) {
        sprite = &title->sprites[3 * i + 6];
        sprite->x = 90;
        sprite->y = (i - 2) * 16 + 77;
    }
    sprite = &title->sprites[4];
    sprite->x = 71;
    sprite->y = title->selectedLanguage * 16 + 45;
    sprite = &title->sprites[5];
    sprite->x = 169;
    sprite->y = title->selectedLanguage * 16 + 45;
    for (i = 0; i < 5; i++) {
        if (i != title->cursorLanguage) {
            sprite = &title->sprites[3 * i + 7];
            sprite->palId = i + 9;
        }
    }
    sprite = &title->sprites[2];
    rightArrow = &title->sprites[3];
    sprite->palId = 3;
    rightArrow->palId = 3;
    for (i = 0; i < 5; i++) {
        if (i == title->cursorLanguage) {
            gObjPalette[i * 2 + 21] = title->savedPalette[4];
            gObjPalette[i * 2 + 20] = title->savedPalette[5];
        }
        else {
            gObjPalette[i * 2 + 21] = title->savedPalette[6];
            gObjPalette[i * 2 + 20] = title->savedPalette[7];
        }
    }
    gObjPalette[7 - (u8)title->unk36D * 3] = gObjPalette[13];
    gMainFlags |= MAIN_FLAG_OBJ_PALETTE_SYNC_ENABLE;
}

void sub_0814A468(struct EuTitle *title) {
    u8 selected = title->cursorLanguage, previous = title->previousLanguage;
    u8 i;
    struct Sprite *sprite;
    s32 y;
    if (selected != previous) {
        gObjPalette[selected * 2 + 21] = title->savedPalette[4];
        gObjPalette[selected * 2 + 20] = title->savedPalette[5];
        gObjPalette[previous * 2 + 21] = title->savedPalette[6];
        gObjPalette[previous * 2 + 20] = title->savedPalette[7];
        gMainFlags |= MAIN_FLAG_OBJ_PALETTE_SYNC_ENABLE;
    }
    DisplaySprite(&title->sprites[1]);
    for (i = 0; i < 5; i++) {
        DisplaySprite(&title->sprites[3 * i + 6]);
    }
    sprite = &title->sprites[4];
    y = (selected - 2) * 16 + 77;
    sprite->y = y;
    if (!sub_08155128(sprite)) sprite->unk1B = 0xff;
    DisplaySprite(sprite);
    sprite = &title->sprites[5];
    sprite->y = y;
    if (!sub_08155128(sprite)) sprite->unk1B = 0xff;
    DisplaySprite(sprite);
    DisplaySprite(&title->sprites[0]);
    DisplaySprite(&title->sprites[title->selectedLanguage * 3 + 8]);
    for (i = 0; i < 5; i++) {
        DisplaySprite(&title->sprites[3 * i + 7]);
    }
    DisplaySprite(&title->sprites[2]);
    DisplaySprite(&title->sprites[3]);
}

u16 sub_0814A5BC(struct EuTitle *title) {
    if (gPressedKeys & A_BUTTON) return A_BUTTON;
    else if (gPressedKeys & START_BUTTON) return START_BUTTON;
    else if (gPressedKeys & B_BUTTON) return B_BUTTON;
    else if (gRepeatedKeys & DPAD_UP) return DPAD_UP;
    else if (gRepeatedKeys & DPAD_DOWN) return DPAD_DOWN;
    else if (gRepeatedKeys & DPAD_LEFT) return DPAD_LEFT;
    else if (gRepeatedKeys & DPAD_RIGHT) return DPAD_RIGHT;
    return 0;
}

static inline void EuTitleLoadBg(u8 bg, u16 r0, void* dest) {
    u16 r5, j;
    u32 r1;
    void* r6;
    const u32* r0_2;
    const u16* r7;

    r0_2 = gUnk_082D7850[r0]->tileset;
    r7 = gUnk_082D7850[r0]->tilemap;
    r5 = gUnk_082D7850[r0]->height;
    r1 = (gBgCntRegs[bg] >> 2) & 3;
    r6 = (((gBgCntRegs[bg] >> 8) & 0x1f) << 0xb) + dest;
    LZ77UnCompVram(r0_2, (r1 << 0xe) + (void*)VRAM);

    for (j = 0; j < r5; j++) {
        CpuCopy16(r7 + j * 30, r6 + j * 64, 0x3c);
    }
}

static inline void LoadBgPaletteWithTransformation_wrapper(const u16* a1, u8 a2, u16 a3) {
    LoadBgPaletteWithTransformation(a1, a2, a3);
}

u32 sub_0814A62C(struct EuTitle *title) {
    u8 i;
    u16 bg;
    for (i = 0; i < 3; i++) sub_0814AB68(i);
    for (i = 0; i < 8; i++) sub_0814AB90(i);
    EuTitleLoadBg(0, gUnk_08387D58[gLanguage][1], (void *)(VRAM + 0x800));
    EuTitleLoadBg(1, gUnk_08387D58[gLanguage][0], (void *)VRAM);
    EuTitleLoadBg(2, gUnk_08387D58[gLanguage][2], (void *)VRAM);
    bg = gUnk_08387D58[gLanguage][0];
    if (gMainFlags & MAIN_FLAG_BG_PALETTE_TRANSFORMATION_ENABLE) {
        LoadBgPaletteWithTransformation_wrapper(gUnk_082D7850[bg]->palette, 0, 0x100);
    }
    else {
        DmaCopy16(3, gUnk_082D7850[bg]->palette, gBgPalette, 0x200);
        gMainFlags |= MAIN_FLAG_BG_PALETTE_SYNC_ENABLE;
    }
    title->unk36D = 0;
    title->flags |= 0x50;
    sub_0814ABC4(title);
    sub_0814A134(title);
    title->unk358 = 0;
    title->unk354 = sub_0814A874;
    return 0;
}

u32 sub_0814A874(struct EuTitle *title) {
    title->unk358++;
    gBldRegs.bldY = 16 - title->unk358 * 16 / 15;
    if (title->unk358 > 14) {
        gBldRegs.bldY = 0;
        gBldRegs.bldAlpha = 0;
        gBldRegs.bldCnt = 0;
        title->flags &= ~0x10;
        title->unk354 = sub_0814AD10;
    }
    sub_0814A1F0(title);
    return 0;
}

u32 sub_0814A8D4(struct EuTitle *title) {
    u16 keys = sub_0814A5BC(title);
    if (!(title->flags & 0x40)) {
        if (gPrevInput == gHeldKeys) title->unkA++;
        else title->unkA = 0;
    }
    else {
        if (++title->unkA > 74) title->flags &= ~0x40;
    }
    if (!(title->flags & 0x40)) {
        if (!(title->flags & 0x30) && (keys & (A_BUTTON | START_BUTTON))) {
            if (title->unk36D == 0) {
                title->unk354 = sub_0814AEF4;
                title->flags |= 0x20;
            }
            else {
                title->unk354 = sub_0814B040;
                title->flags |= 8;
            }
            m4aSongNumStart(0x21e);
        }
        if ((keys & DPAD_DOWN) && title->unk36D == 0) {
            title->unk36D = 1;
            m4aSongNumStart(0x21d);
        }
        else if ((keys & DPAD_UP) && title->unk36D == 1) {
            title->unk36D = 0;
            m4aSongNumStart(0x21d);
        }
    }
    sub_0814A1F0(title);
    return 0;
}

u32 sub_0814A9DC(struct EuTitle *title) {
    if (gUnk_03000554 == 0) {
        TaskDestroy(gCurTask);
        CreateCutscene();
    }
    else {
        CpuFill16(RGB_WHITE, gBgPalette, 0x200);
        CpuFill16(RGB_WHITE, gObjPalette, 0x200);
        gMainFlags |= MAIN_FLAG_BG_PALETTE_SYNC_ENABLE | MAIN_FLAG_OBJ_PALETTE_SYNC_ENABLE;
        gBldRegs.bldCnt = 0;
        gBldRegs.bldAlpha = 0;
        gBldRegs.bldY = 0;
        TaskDestroy(gCurTask);
        CreateDemo(sub_08025F2C());
    }
    return 1;
}

u32 sub_0814AA70(struct EuTitle *title) {
    u16 keys = sub_0814A5BC(title);
    title->previousLanguage = title->cursorLanguage;
    if (keys & (A_BUTTON | START_BUTTON)) {
        if (title->selectedLanguage == title->cursorLanguage) {
            title->unk354 = sub_0814B090;
        }
        else {
            title->selectedLanguage = title->cursorLanguage;
            gLanguage = title->cursorLanguage + LANGUAGE_ENGLISH;
            UpdateSaveBufferByOffset(0, 0);
            title->unk354 = sub_0814B0B4;
        }
        m4aSongNumStart(0x21e);
    }
    else if (keys & B_BUTTON) {
        title->unk354 = sub_0814B090;
        m4aSongNumStart(0x21f);
    }
    else if (keys & DPAD_DOWN) {
        title->cursorLanguage = (title->cursorLanguage + 1) % 5;
        m4aSongNumStart(0x21d);
    }
    else if (keys & DPAD_UP) {
        if (--title->cursorLanguage < 0) {
            title->cursorLanguage = 4;
        }
        m4aSongNumStart(0x21d);
    }
    sub_0814A468(title);
    return 0;
}

void sub_0814AB68(u8 bg) {
    CpuFill16(0, (void *)VRAM + (bg << 14), 0x4000);
}

void sub_0814AB90(u8 bg) {
    CpuFill16(0x1ff, (void *)VRAM + ((31 - bg) << 11), 0x800);
}

inline void sub_0814AC00(struct EuTitle *title) {
    if (!(title->flags & 0x10)) {
        title->unk368 = sub_0814AC20;
    }
}

inline void sub_0814AC20(struct EuTitle *title) {
    if (!sub_0814F274(&title->unk35C)) {
        sub_0814F3C4(&title->unk35C, *gUnk_08D626F0[gLanguage][0]);
        title->unk368 = sub_0814AC64;
    }
}

inline void sub_0814AC64(struct EuTitle *title) {
    if (!sub_0814F274(&title->unk35C)) {
        sub_0814F3C4(&title->unk35C, *gUnk_08D626F0[gLanguage][1]);
        title->unk368 = sub_0814ACAC;
    }
}

inline void sub_0814ACAC(struct EuTitle *title) {
    if (!sub_0814F274(&title->unk35C)) {
        sub_0814F3C4(&title->unk35C, *gUnk_08D626F0[gLanguage][0]);
        title->unk368 = sub_0814AC64;
    }
}

inline u32 sub_0814ACF0(struct EuTitle *title) {
    sub_08149FF0(title);
    title->unk354 = sub_0814A62C;
    return 0;
}

inline u32 sub_0814AD10(struct EuTitle *title) {
    title->unk358 = 0;
    gBldRegs.bldCnt = 0x241;
    gBldRegs.bldAlpha = BLDALPHA_BLEND(16, 16);
    gBldRegs.bldY = 0;
    gDispCnt |= DISPCNT_BG0_ON;
    title->unk354 = sub_0814AD60;
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AD60(struct EuTitle *title) {
    if (++title->unk358 > 2) {
        title->unk354 = sub_0814AD98;
        title->unk358 = 0;
    }
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AD98(struct EuTitle *title) {
    m4aSongNumStartOrChange(1);
    title->unkA = 0;
    title->unk358 = 0;
    title->unk354 = sub_0814A8D4;
    sub_0814A134(title);
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814ADD0(struct EuTitle *title) {
    title->unk368 = NULL;
    title->unk35C.unk6 &= ~0x40;
    if (!sub_0814F274(&title->unk35C)) {
        title->unk354 = sub_0814AE68;
    }
    /* The original immediately overwrites the preceding state assignment. */
    title->unk354 = sub_0814AE2C;
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AE2C(struct EuTitle *title) {
    if (!sub_0814F274(&title->unk35C)) {
        m4aMPlayFadeOut(&gMPlayInfo_0, 4);
        title->unk354 = sub_0814AE68;
    }
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AE68(struct EuTitle *title) {
    gDispCnt &= ~DISPCNT_BG0_ON;
    gBldRegs.bldCnt = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BD | BLDCNT_TGT1_OBJ | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG0;
    gBldRegs.bldAlpha = 0;
    gBldRegs.bldY = 0;
    title->unk358 = 0;
    title->unk354 = sub_0814AEAC;
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AEAC(struct EuTitle *title) {
    title->unk358++;
    gBldRegs.bldY = title->unk358 * 16 / 60;
    if (title->unk358 > 59) {
        title->unk354 = sub_0814A9DC;
    }
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AEF4(struct EuTitle *title) {
    gDispCnt &= ~DISPCNT_BG0_ON;
    gBldRegs.bldCnt = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BD | BLDCNT_TGT1_OBJ | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG0;
    gBldRegs.bldAlpha = 0;
    gBldRegs.bldY = 0;
    title->unk358 = 0;
    title->unk354 = sub_0814AF38;
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AF38(struct EuTitle *title) {
    title->unk358++;
    gBldRegs.bldY = title->unk358 * 16 / 10;
    if (title->unk358 > 9) {
        title->unk354 = sub_0814AF80;
    }
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AF80(struct EuTitle *title) {
    m4aSongNumStop(1);
    title->unk358 = 0;
    title->unk354 = sub_0814AFB0;
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AFB0(struct EuTitle *title) {
    if (++title->unk358 > 4) {
        title->unk354 = sub_0814AFE4;
    }
    sub_0814A1F0(title);
    return 0;
}

inline u32 sub_0814AFE4(struct EuTitle *title) {
    CpuFill16(RGB_WHITE, gBgPalette, 0x200);
    CpuFill16(RGB_WHITE, gObjPalette, 0x200);
    gMainFlags |= MAIN_FLAG_BG_PALETTE_SYNC_ENABLE | MAIN_FLAG_OBJ_PALETTE_SYNC_ENABLE;
    TaskDestroy(gCurTask);
    CreateCutscene();
    return 1;
}

inline u32 sub_0814B040(struct EuTitle *title) {
    title->cursorLanguage = title->selectedLanguage;
    title->previousLanguage = (title->cursorLanguage + 1) % 5;
    sub_0814A30C(title);
    sub_0814A468(title);
    title->unk354 = sub_0814AA70;
    return 0;
}

inline u32 sub_0814B090(struct EuTitle *title) {
    title->flags &= ~8;
    title->unk354 = sub_0814AD98;
    sub_0814A468(title);
    return 0;
}

inline u32 sub_0814B0B4(struct EuTitle *title) {
    gDispCnt &= ~DISPCNT_BG0_ON;
    gBldRegs.bldCnt = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BD | BLDCNT_TGT1_OBJ | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG0;
    gBldRegs.bldAlpha = 0;
    gBldRegs.bldY = 0;
    title->unk358 = 0;
    title->unk354 = sub_0814B0F8;
    sub_0814A468(title);
    return 0;
}

inline u32 sub_0814B0F8(struct EuTitle *title) {
    title->unk358++;
    gBldRegs.bldY = title->unk358 * 16 / 10;
    if (title->unk358 > 9) {
        title->unk354 = sub_0814B140;
    }
    sub_0814A468(title);
    return 0;
}

inline u32 sub_0814B140(struct EuTitle *title) {
    title->flags &= ~8;
    title->unk354 = sub_0814A62C;
    sub_0814A468(title);
    return 0;
}

/* European title state; unexamined fields remain explicitly unnamed. */
struct EuTitle {
    u32 unk0;
    u32 flags;
    s16 unk8;
    s16 unkA;
    struct Sprite sprites[21];
    u32 (*unk354)(struct EuTitle *);
    s16 unk358;
    u8 filler35A[2];
    struct Object11 unk35C;
    void (*unk368)(struct EuTitle *);
    s8 selectedLanguage;
    u8 unk36D;
    s8 cursorLanguage;
    s8 previousLanguage;
    u8 filler370[0x10];
};

static void EuTitleMain(void);
extern u32 sub_0814ADD0(struct EuTitle *);
extern u32 sub_0814ACF0(struct EuTitle *);
extern void sub_0814ABC4(struct EuTitle *);
static void EuTitleDestroy(struct Task *);

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

#include "save.h"
extern u16 sub_0814A5BC(struct EuTitle *);
extern void sub_0814A468(struct EuTitle *);
extern u32 sub_0814B090(struct EuTitle *);
extern u32 sub_0814B0B4(struct EuTitle *);

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

void sub_0814AC00(struct EuTitle *);
void sub_0814AC20(struct EuTitle *);
void sub_0814AC64(struct EuTitle *);
void sub_0814ACAC(struct EuTitle *);
void sub_0814ABC4(struct EuTitle *title) {
    sub_0814F3C4(&title->unk35C, *gUnk_08D626F0[gLanguage][1]);
    title->unk368 = sub_0814AC00;
}
void sub_0814AC00(struct EuTitle *title) {
    if (!(title->flags & 0x10)) {
        title->unk368 = sub_0814AC20;
    }
}
void sub_0814AC20(struct EuTitle *title) {
    if (!sub_0814F274(&title->unk35C)) {
        sub_0814F3C4(&title->unk35C, *gUnk_08D626F0[gLanguage][0]);
        title->unk368 = sub_0814AC64;
    }
}
void sub_0814AC64(struct EuTitle *title) {
    if (!sub_0814F274(&title->unk35C)) {
        sub_0814F3C4(&title->unk35C, *gUnk_08D626F0[gLanguage][1]);
        title->unk368 = sub_0814ACAC;
    }
}
void sub_0814ACAC(struct EuTitle *title) {
    if (!sub_0814F274(&title->unk35C)) {
        sub_0814F3C4(&title->unk35C, *gUnk_08D626F0[gLanguage][0]);
        title->unk368 = sub_0814AC64;
    }
}

extern u32 sub_0814AD98(struct EuTitle *);
extern u32 sub_0814A62C(struct EuTitle *);
u32 sub_0814B0F8(struct EuTitle *);
u32 sub_0814B140(struct EuTitle *);
u32 sub_0814B090(struct EuTitle *title) {
    title->flags &= ~8;
    title->unk354 = sub_0814AD98;
    sub_0814A468(title);
    return 0;
}
u32 sub_0814B0B4(struct EuTitle *title) {
    gDispCnt &= ~DISPCNT_BG0_ON;
    gBldRegs.bldCnt = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BD | BLDCNT_TGT1_OBJ | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG0;
    gBldRegs.bldAlpha = 0;
    gBldRegs.bldY = 0;
    title->unk358 = 0;
    title->unk354 = sub_0814B0F8;
    sub_0814A468(title);
    return 0;
}
u32 sub_0814B0F8(struct EuTitle *title) {
    title->unk358++;
    gBldRegs.bldY = title->unk358 * 16 / 10;
    if (title->unk358 > 9) {
        title->unk354 = sub_0814B140;
    }
    sub_0814A468(title);
    return 0;
}
u32 sub_0814B140(struct EuTitle *title) {
    title->flags &= ~8;
    title->unk354 = sub_0814A62C;
    sub_0814A468(title);
    return 0;
}

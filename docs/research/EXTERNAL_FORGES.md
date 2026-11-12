# External public forge and semantic-reference audit

AI-assisted research for MatyMeatBoy, snapshot 2026-11-12T21:56:33.771686+00:00. Baseline `1197474f80e5de282fbedcd0025ebfa61f61a764`. This extends [the GitHub audit](REPOSITORY_AUDIT.md); it does not repeat the three original code candidates already staged for review.

## Result

No additional matching-code, symbol-map, recovered-type or typed-data source artifact was verified outside GitHub in the public surfaces searched. This is a bounded public-discovery result, not a claim that no other work exists. The usable additional knowledge identified here comes from already-known semantic branches and direct baseline cross-checks; it does not increase code-matching percentage.

## Forge coverage

| Public forge | Search result | Interpretation |
|---|---|---|
| [GitLab.com](https://gitlab.com/api/v4/projects?search=katam&simple=true&per_page=100&page=1) | `katam (two pages, 103 results)`, `amazing mirror (3 results)`, `AmazingMirror (0)`, `kirby-mirror (0)`, `MirrorRecomp (0)`, `katam-port (0)`, `jiangzhengwenjz (one unrelated Pokemon archive)`, `B8KE (one README-only project)`, `kirby (first 100, CMS-heavy, incomplete)` | No matching-decomp source project identified. One exact-game-title emulator wrapper excluded after complete tree inspection. |
| [Codeberg.org](https://codeberg.org/api/v1/repos/search?q=AmazingMirror&limit=50) | `katam`, `kirby`, `amazing mirror`, `AmazingMirror` | HTTP 429; browser search also reports robots exclusion. Not negative evidence about repository existence. |
| [Bitbucket.org](https://api.bitbucket.org/2.0/repositories?q=name~%22katam%22&pagelen=100) | `katam`, `amazing mirror` | Global repository API returned 404; UI query returned 202 with empty body. Targeted indexed web searches produced no relevant artifact; no complete forge search established. |
| [SourceHut](https://git.sr.ht/?search=katam) | `katam`, `kirby`, `Amazing Mirror` | HTTP 200 was welcome/login HTML, not search results. Indexed search was robots-limited. Unlisted/private repositories cannot be covered. |
| [Gitea.com](https://gitea.com/api/v1/repos/search?q=katam&limit=50) | `katam`, `amazing mirror` | Public search API returned empty data for both queries. |
| [GitGud.io](https://gitgud.io/api/v4/projects?search=katam&simple=true&per_page=100) | `katam`, `amazing mirror` | Public project search API returned empty arrays for both queries. |
| [Gitdab.com](https://gitdab.com/api/v1/repos/search?q=katam&limit=50) | `katam`, `amazing mirror` | Public repository search API returned empty data for both queries. |
| [git.sdf.org](https://git.sdf.org/api/v1/repos/search?q=katam&limit=50) | `katam` | Public repository search API returned empty data. |
| [git.disroot.org](https://git.disroot.org/api/v1/repos/search?q=katam&limit=50) | `katam`, `amazing mirror` | Both public API requests timed out; no negative repository conclusion. |
| [NotABug.org](https://notabug.org/api/v1/repos/search?q=katam&limit=50) | `katam` | Attempted repository search endpoint returned 404; no negative repository conclusion. |
| [repo.or.cz](https://repo.or.cz/?a=project_list;pf=katam) | `katam`, `kirby` | HTTP 200 returned an anti-bot challenge, not project results. |
| [SourceForge.net](https://sourceforge.net/) | `katam decomp`, `Amazing Mirror source` | Targeted indexed search found unrelated Katam surname references, no verified game artifact. Native catalogue coverage not established. |

The GitLab `katam` query returned 103 project records across two pages; none was identified as this game's decompilation by name/description. The broad `kirby` query retrieved only its first 100 records and is dominated by Kirby CMS projects; it is not claimed complete. Exact game/recomp/author identifiers supplemented it. Codeberg rate limits and challenge/login surfaces were recorded without treating them as empty catalogues.

## Exact-title GitLab result excluded

[cmug/kirby-the-amazing-mirror](https://gitlab.com/cmug/kirby-the-amazing-mirror) has default branch `web`, head `594c698da6ec95b7c72fbb95cf91c28f484f4d4d`, committed 2025-11-10 09:20:30 UTC. Its complete five-entry recursive tree contains an empty README, web/CI wrapper files and a game-image blob. It supplies no C/assembly decompilation, recovered names or typed data. Only repository metadata and tree entries were inspected; the game image was not downloaded. The `main` branch is the initial README commit `8a63de7a225e4c9f52d53956e6b1af545b5f529f`. The separate GitLab B8KE-substring hit has a README-only tree and offers no source candidate.

## Semantic candidate: eight switch names

[Upstream PR #403](https://github.com/jiangzhengwenjz/katam/pull/403), exact head `8cacafd24d75f270e10c4bdc639dce1dd6239e66`, is a two-file naming contribution based on the audited baseline. It changes `include/big_small_switch.h` and `src/big_small_switch.c`. The table below separates direct source evidence from limitations. Original contributor ROM-placement counts and clean six-ROM comparison claims have not been independently reproduced.

| Old symbol | Proposed name | Baseline evidence | Limitation |
|---|---|---|---|
| `sub_0811938C` | `SwitchSetFunc` | Installs the main callback; resets press state or installs despawn for an already-unlocked world slot. | Includes already-unlocked fallback; not an unconditional constructor. |
| `sub_081194DC` | `SwitchCheckPressAndGiveTomato` | Checks block/Kirby/attack routes; calls BonusCreateTomato only for an eligible human hit on a big switch before unlock-start flag. | Tomato is conditional; return TRUE also has routes without a tomato. |
| `sub_081197D4` | `SwitchUpdatePressState` | Maintains held/new-press/release bits and release timer; latching template flag prevents normal release. | Held duration is not a fresh press every frame. |
| `sub_08119980` | `SwitchMain` | Calls press-state update, sets sprite state, dispatches template effects, increments counter. | Four effect routes exist, one intentionally remains unnamed. |
| `sub_08119A20` | `SwitchUpdateHeldCount` | Increments room slot on press-edge bit; decrements on release-edge bit only when nonzero. | This is a shared room slot, not a count of allocated objects. |
| `sub_08119B3C` | `SwitchTryWorldMapUnlock` | Marks pending after press, gates callback table dispatch on CanStartInGameInterlude. | Request can wait; avoid an unconditional Start or Unlock name. |
| `sub_08119BB8` | `SwitchUpdateCPUKirbyTrigger` | Also updates held count; raises room slot0xF while held. Same slot appears in cpu_kirby_trigger.c and CPU script reader. | Per-template threshold; not proof that every switch triggers CPU AI. |
| `sub_08119C0C` | `SwitchDespawn` | Sets generic object flag0x1000; ObjectMain destroys the task on that flag. | Deferred destruction by ObjectMain rather than immediate TaskDestroy call. |

Primary evidence: [baseline switch source](https://github.com/jiangzhengwenjz/katam/blob/1197474f80e5de282fbedcd0025ebfa61f61a764/src/big_small_switch.c), [generic ObjectMain destruction](https://github.com/jiangzhengwenjz/katam/blob/1197474f80e5de282fbedcd0025ebfa61f61a764/src/object.c#L184), [CPU trigger writer](https://github.com/jiangzhengwenjz/katam/blob/1197474f80e5de282fbedcd0025ebfa61f61a764/src/cpu_kirby_trigger.c), and [CPU script slot reader](https://github.com/jiangzhengwenjz/katam/blob/1197474f80e5de282fbedcd0025ebfa61f61a764/src/code_0800ECAC_2.c#L2220). Before importing, audit all pointer-table references and mechanical propagation and run authoritative comparison. Keep the three intentionally unnamed functions unknown until their contracts are recovered.

## Port field comments: useful leads and a rejected generalization

[Zalo field-documentation commit](https://github.com/zalo/katam/commit/6f470934be50d2990c71e2470344b222c46196e3), head `6f470934be50d2990c71e2470344b222c46196e3`, modifies `include/data.h`, `include/kirby.h`, `src/code_0800ECAC.c`, and `src/kirby.c`. It is a source of hypotheses, not permission to copy all proposed semantics into a shared struct.

A narrow fact can be established independently from [baseline sub_0803F324](https://github.com/jiangzhengwenjz/katam/blob/1197474f80e5de282fbedcd0025ebfa61f61a764/src/kirby.c#L6452): `movementState` receives the selected held-input word; `unk11A` is current held bits absent from the previous word, and `unk11C` is previous held bits absent from the current word. Human input can come from local, linked or mode-specific input; CPU input comes from the AI word in the relevant branches. Therefore a “raw local pad” name would be too narrow. Full usage review is still needed before a field rename.

The proposed broad ObjectBase flag `0x1000` description as Kirby platform drop-through is unsafe as a generic declaration comment. [ObjectPreUpdate](https://github.com/jiangzhengwenjz/katam/blob/1197474f80e5de282fbedcd0025ebfa61f61a764/src/code_0806F780.c#L727) destroys the current task when that bit is set; [ObjectMain](https://github.com/jiangzhengwenjz/katam/blob/1197474f80e5de282fbedcd0025ebfa61f61a764/src/object.c#L184) does the same for ordinary objects; the switch despawn callback sets it. This establishes a generic destruction-request role in those paths and prevents adopting one Kirby-specific interpretation across all object classes.

Other proposed field flags, fixed-point scales, vulnerability words, terrain-grid layout and animation-table boundaries remain unverified in this audit. The 5×5 AI-grid comment is especially a layout hypothesis: do not erase the baseline out-of-bounds/layout TODO without reconstructing the declaration and every reader/writer. No port comment was imported.

## What can legitimately improve progress

- Matching-code progress requires previously uncovered functions compiled and verified against the exact reference; source age or a new repository does not establish this.
- Naming/type progress can be recorded separately as evidence-backed symbols or fields. Renaming an already-matching function adds no compiled bytes.
- Typed-data progress requires a proven range, type/count, input section, alignment, relocations and exact round trip. A raw blob, a symbol list or an extracted asset does not by itself meet that threshold.
- Original author and license provenance remain intact. Unlicensed independent port code was not imported; no permissive license was invented for game-derived material.

## Reproducibility and limits

The companion [external_forges.json](external_forges.json) contains the forge outcomes, exact candidate identities, semantic evidence, and SHA-256 digests of the locally cached API/HTML responses. Raw responses are ignored under `build/research/external-forges/`; they contain metadata and tree listings, not downloaded game binaries.

Indexed web searches combined exact game title, `katam`, `AmazingMirror`, `B8KE`, `decomp`, `disasm`, symbols and site restrictions for GitLab, Codeberg, Bitbucket, SourceHut, Gitea, GitGud, SourceForge and smaller forge hosts. Directory entries and GitHub proxy sites that point back to known katam repositories are discovery links, not independent source provenance. No archived/private/unlisted repository search or universal forge enumeration was established. Re-run these queries before a later integration. No build, gameplay run, ROM comparison or source import was performed by this research.

# Public repository audit

Public GitHub snapshot: 2026-11-12T21:45:31.544710+00:00. Baseline: [`jiangzhengwenjz/katam` master](https://github.com/jiangzhengwenjz/katam/tree/1197474f80e5de282fbedcd0025ebfa61f61a764), commit `1197474f80e5de282fbedcd0025ebfa61f61a764`. This research was AI-assisted. New research is authored for MatyMeatBoy; existing contributors retain their authorship.

## Scope and interpretation

This audit enumerated all 24 direct public forks and all 91 currently exposed branches, compared every branch against the exact baseline, and checked 399 historical upstream pull requests. It also inspected six independent recompilation or port repositories, including every exposed branch of both katam-port repositories. The machine-readable inventory contains complete returned commit identities, authors, changed-file metadata, comparison links, branch heads, and PR associations.

A recent push is not evidence of new decompilation. A branch ahead count is not evidence that its patch is absent upstream: many contributions were squash-merged or rebased. Historical merged PRs and identical file blobs are recorded separately. Counts below describe Git ancestry only. No matching percentage or native-playability claim was measured in this audit.

## Direct fork inventory

| Repository | Default head | Ahead / behind | Branches | Finding |
|---|---|---|---|---|
| [plemulabs/katam](https://github.com/plemulabs/katam) | `8689e4cc2ea9e03183442a2959f4662789bec3ad` | 0 / 10 | 2 | Default is upstream ancestor; ahead branches: `midi` |
| [bungerFan192/katam3ds](https://github.com/bungerFan192/katam3ds) | `8689e4cc2ea9e03183442a2959f4662789bec3ad` | 0 / 10 | 3 | Default is upstream ancestor; ahead branches: `3ds-port-foundation`, `3ds-systems-port` |
| [toweroflondon1090-droid/katam](https://github.com/toweroflondon1090-droid/katam) | `1197474f80e5de282fbedcd0025ebfa61f61a764` | 0 / 0 | 2 | Identical baseline; ahead branches: `midi` |
| [EliasXbox/katam](https://github.com/EliasXbox/katam) | `7d969fbce14fdc838d2c1ea01389717fb96c3189` | 0 / 115 | 1 | Default is upstream ancestor |
| [Crazycolbster/katam_kommented](https://github.com/Crazycolbster/katam_kommented) | `6e0b5b5d0cd5ba77ec373d60ee15deda06c0713b` | 0 / 1 | 2 | Default is upstream ancestor; ahead branches: `colby-comments` |
| [zalo/katam](https://github.com/zalo/katam) | `3d5d061d5212e9290ac1ebe5e7cb5d17102fe3a3` | 0 / 206 | 4 | Default is upstream ancestor; ahead branches: `buddy-extraction`, `contrib-dump-tools`, `contrib-field-docs` |
| [jackmgaller/katam](https://github.com/jackmgaller/katam) | `60c1c2370e528c6ae8ac5c994e642541840b5210` | 0 / 209 | 23 | Default is upstream ancestor; ahead branches: `agents-md`, `decompile-big-small-switch`, `decompile-code`, `decompile-cutscene-trigger`, `decompile-multi-sio-08158934`, `decompile-objects`, `decompile-six-files`, `dissolve-kirby-union`, `fix-legacy-variable-names`, `match-sub_080B819C`, `match-sub_08141300`, `name-big-small-switch`, `name-bonkers`, `name-kirby-swim-water`, `name-level-music-getobjectcounter`, `naming-engine-core`, `naming-symbols`, `pr-sub_080B819C`, `rename-object-structs`, `todo-match-half` |
| [sh1ftmaker/katam](https://github.com/sh1ftmaker/katam) | `60c1c2370e528c6ae8ac5c994e642541840b5210` | 0 / 209 | 17 | Default is upstream ancestor; ahead branches: `all-work`, `decomp-0802B4A8`, `decomp-0802E16C`, `decomp-0802E57C`, `decomp-code_08025650`, `decomp-cookin`, `decomp-flamer`, `decomp-kirby_cannon`, `decomp-large-star-stone-block`, `decomp-leap`, `decomp-star-stone-block`, `decomp-sub_08153184`, `decomp-work`, `decomp-work-post375`, `pr-code-0802F8D8`, `pr-code-08020220` |
| [BlameMateo/katam](https://github.com/BlameMateo/katam) | `3d5d061d5212e9290ac1ebe5e7cb5d17102fe3a3` | 0 / 206 | 2 | Default is upstream ancestor |
| [IoIxD/katam](https://github.com/IoIxD/katam) | `8f8b1dbc1ecf863283687a406656453589e97422` | 0 / 308 | 3 | Default is upstream ancestor; ahead branches: `kirby_doc`, `levelinfodoc` |
| [Kurausukun/katam](https://github.com/Kurausukun/katam) | `2dca539005bbb82d050d229e17ae7733186a223b` | 0 / 492 | 4 | Default is upstream ancestor; ahead branches: `audio_dump`, `midi`, `not_working` |
| [ultra-azu/katam](https://github.com/ultra-azu/katam) | `69aa58e8c79acbfa84f0fb86e04ab7085ea97537` | 0 / 467 | 8 | Default is upstream ancestor; ahead branches: `code_08026044`, `droppy`, `goal_game_bonus`, `haley`, `makefiles`, `sfx`, `sirkibble` |
| [achristensen4/katam](https://github.com/achristensen4/katam) | `db411844f8705a3dc36dd10c3180fff600d29a14` | 0 / 550 | 1 | Default is upstream ancestor |
| [soiryl-pas/katam](https://github.com/soiryl-pas/katam) | `1197474f80e5de282fbedcd0025ebfa61f61a764` | 0 / 0 | 1 | Identical baseline |
| [ventiph/katam](https://github.com/ventiph/katam) | `feb7c958e270d647050de96e94ac0de35b51cbe7` | 6 / 559 | 1 | Divergent historical default; inspect before reuse; ahead branches: `master` |
| [Lrs121/katam](https://github.com/Lrs121/katam) | `1677a2b2e6e9ffa9138fed115ed649825a717d27` | 0 / 563 | 2 | Default is upstream ancestor; ahead branches: `jzw` |
| [NeonWolf532/katam](https://github.com/NeonWolf532/katam) | `1b352c29ef8f0f240952a2d7d68152cc8c822610` | 0 / 600 | 2 | Default is upstream ancestor; ahead branches: `jzw` |
| [Cofflag/katam](https://github.com/Cofflag/katam) | `26b47916b1ee68a201948c142cd94cefac2166f2` | 0 / 625 | 1 | Default is upstream ancestor |
| [Shalmezad/katam](https://github.com/Shalmezad/katam) | `3765dfdd0056e445aebaaa9b71cadb9ca488e932` | 0 / 714 | 1 | Default is upstream ancestor |
| [EpochFlame/katam](https://github.com/EpochFlame/katam) | `454c333d5ed965d9609ec55991e6f38f4829bf7d` | 0 / 712 | 3 | Default is upstream ancestor; ahead branches: `jzw` |
| [fserve/katam](https://github.com/fserve/katam) | `3d1486a67c2bd27fc561a0a0d21cd2797d949a46` | 0 / 1012 | 3 | Default is upstream ancestor; ahead branches: `jzw` |
| [UraYukimitsu/katam](https://github.com/UraYukimitsu/katam) | `96cdb63fe363f7e6a452949dd69a0de9acdd5b0c` | 0 / 1048 | 2 | Default is upstream ancestor |
| [Jenna1337/katam](https://github.com/Jenna1337/katam) | `83f1618cab9bccccc963d89632a6c7c1acbbcca4` | 0 / 162 | 2 | Default is upstream ancestor |
| [Cleverking2003/katam](https://github.com/Cleverking2003/katam) | `6df872283c4cf1317d000c5dfcf6623bd89af077` | 16 / 1344 | 1 | Divergent historical default; inspect before reuse; ahead branches: `master` |

## Every fork branch

Full hashes and individual non-upstream commits are in [repositories.json](repositories.json). `merged PR` identifies a matching PR head, so an ahead branch with that label must not be imported again solely because of its ahead count.

### plemulabs/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `8689e4cc2ea9e03183442a2959f4662789bec3ad` | 0 / 10 | No ahead commit |
| `midi` | `265606058ad25ef1b0a5ce55d92cc7a394210993` | 1 / 199 | [merged PR #374](https://github.com/jiangzhengwenjz/katam/pull/374) |

### bungerFan192/katam3ds

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `3ds-port-foundation` | `a53fcf632f00a530dc861a63444fee1c06cb2c2d` | 20 / 10 | No matching head among historical upstream PRs; novelty not presumed |
| `3ds-systems-port` | `51dbc88484358c0427b6a99e60a0bff6f6c692be` | 46 / 10 | No matching head among historical upstream PRs; novelty not presumed |
| `master` | `8689e4cc2ea9e03183442a2959f4662789bec3ad` | 0 / 10 | No ahead commit |

### toweroflondon1090-droid/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `1197474f80e5de282fbedcd0025ebfa61f61a764` | 0 / 0 | No ahead commit |
| `midi` | `265606058ad25ef1b0a5ce55d92cc7a394210993` | 1 / 199 | [merged PR #374](https://github.com/jiangzhengwenjz/katam/pull/374) |

### EliasXbox/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `7d969fbce14fdc838d2c1ea01389717fb96c3189` | 0 / 115 | No ahead commit |

### Crazycolbster/katam_kommented

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `colby-comments` | `f632e4a89113cf8d0ad9d695890c8d25220d9269` | 7 / 1 | No matching head among historical upstream PRs; novelty not presumed |
| `master` | `6e0b5b5d0cd5ba77ec373d60ee15deda06c0713b` | 0 / 1 | No ahead commit |

### zalo/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `buddy-extraction` | `5b9d5412ee022c5c27bb807a0d869a03baa992df` | 1 / 209 | No matching head among historical upstream PRs; novelty not presumed |
| `contrib-dump-tools` | `d1d74db29f51081c0ae55a40003e03b3cbe8e500` | 1 / 209 | No matching head among historical upstream PRs; novelty not presumed |
| `contrib-field-docs` | `6f470934be50d2990c71e2470344b222c46196e3` | 1 / 209 | No matching head among historical upstream PRs; novelty not presumed |
| `master` | `3d5d061d5212e9290ac1ebe5e7cb5d17102fe3a3` | 0 / 206 | No ahead commit |

### jackmgaller/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `agents-md` | `b58a6b424216582fbb1dadad139386b212077655` | 4 / 196 | [merged PR #380](https://github.com/jiangzhengwenjz/katam/pull/380) |
| `decompile-big-small-switch` | `c9fc6e203d59a65d7addb2a57e217eb0f9362549` | 3 / 13 | [merged PR #402](https://github.com/jiangzhengwenjz/katam/pull/402) |
| `decompile-code` | `abde2bf29b363095441b5b4ecef3792cc3e892cc` | 4 / 196 | [merged PR #381](https://github.com/jiangzhengwenjz/katam/pull/381) |
| `decompile-code-08032E98` | `f0737880acf63c0ec503618e16041b8aa6815e56` | 0 / 21 | No ahead commit |
| `decompile-cutscene-trigger` | `361da5edac2b47d9f3725ac2be351717246137a1` | 9 / 125 | [merged PR #387](https://github.com/jiangzhengwenjz/katam/pull/387) |
| `decompile-multi-sio-08158934` | `cb769dd697e73dae1919c3225afc8782e20bae6a` | 5 / 10 | [merged PR #404](https://github.com/jiangzhengwenjz/katam/pull/404) |
| `decompile-objects` | `135f235305de9168ebfca89726bdf015b76044ad` | 2 / 199 | [merged PR #373](https://github.com/jiangzhengwenjz/katam/pull/373) |
| `decompile-six-files` | `5c664941b18765e0af1885402a7829b95c9ac29b` | 2 / 209 | [merged PR #366](https://github.com/jiangzhengwenjz/katam/pull/366) |
| `decompile-sprite-and-door` | `d9806a0b76e01a0da5107e07bbc2ff9911b6510f` | 0 / 126 | No ahead commit |
| `dissolve-kirby-union` | `0e10b3e0c05e21176e57b8b06bf73b2b7f45dc69` | 8 / 170 | [merged PR #386](https://github.com/jiangzhengwenjz/katam/pull/386) |
| `fix-legacy-variable-names` | `26a9ee171a3fa43798f402cccf640a4afe0abfe6` | 2 / 117 | [merged PR #389](https://github.com/jiangzhengwenjz/katam/pull/389) |
| `master` | `60c1c2370e528c6ae8ac5c994e642541840b5210` | 0 / 209 | No ahead commit |
| `match-sub_080B819C` | `0fbdb741c7d7ac19d828221246ceca95961f00ad` | 29 / 206 | No matching head among historical upstream PRs; novelty not presumed |
| `match-sub_08141300` | `e9e25b94ef2cf7c8aaba889cc98ea293e28a34ed` | 1 / 202 | [merged PR #370](https://github.com/jiangzhengwenjz/katam/pull/370) |
| `name-big-small-switch` | `8cacafd24d75f270e10c4bdc639dce1dd6239e66` | 3 / 0 | [open PR #403](https://github.com/jiangzhengwenjz/katam/pull/403) |
| `name-bonkers` | `11ee931f5930b76a221a08d395c08b2cd027e8a1` | 1 / 201 | [merged PR #372](https://github.com/jiangzhengwenjz/katam/pull/372) |
| `name-kirby-swim-water` | `e1abfb721299e391659fe327ce071367d001eff1` | 1 / 182 | [merged PR #384](https://github.com/jiangzhengwenjz/katam/pull/384) |
| `name-level-music-getobjectcounter` | `decdfa575caf33b2dd1c021a0c6ac85015e78326` | 2 / 184 | [merged PR #383](https://github.com/jiangzhengwenjz/katam/pull/383) |
| `naming-engine-core` | `18628344df26366a7d9c62d786e04f55e16d53c5` | 1 / 197 | [merged PR #375](https://github.com/jiangzhengwenjz/katam/pull/375) |
| `naming-symbols` | `78d5a544ce1e12aa04c00d080641ef9586078c96` | 1 / 201 | [closed PR #371](https://github.com/jiangzhengwenjz/katam/pull/371) |
| `pr-sub_080B819C` | `e5dfaa51370c180075901225eadc2f7c473c1635` | 3 / 205 | [merged PR #369](https://github.com/jiangzhengwenjz/katam/pull/369) |
| `rename-object-structs` | `bdaa496d37b87952c35303b687355c47229c25ff` | 11 / 181 | [merged PR #385](https://github.com/jiangzhengwenjz/katam/pull/385) |
| `todo-match-half` | `7c0831e49ce3fdea81ebf5cbb2ac5b1521047fb3` | 8 / 0 | [open PR #413](https://github.com/jiangzhengwenjz/katam/pull/413) |

### sh1ftmaker/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `all-work` | `e99bebf4f0aa75d4b502576115e92705d0ab390b` | 188 / 197 | [closed PR #376](https://github.com/jiangzhengwenjz/katam/pull/376) |
| `decomp-0802B4A8` | `e1f1592c4c0e3dc3fb34ee6c1f59c76043a74212` | 1 / 1 | [open PR #397](https://github.com/jiangzhengwenjz/katam/pull/397) |
| `decomp-0802E16C` | `5f8214c96ff857920708df3970c88740bdd3495c` | 1 / 16 | [merged PR #396](https://github.com/jiangzhengwenjz/katam/pull/396) |
| `decomp-0802E57C` | `0cb8f35a8c9f3f25d0dab7cce9673f3a5f7bb922` | 1 / 19 | [closed PR #395](https://github.com/jiangzhengwenjz/katam/pull/395) |
| `decomp-code_08025650` | `ca1a15863599f8c0af73354d7cf0ec4c822ca3a1` | 1 / 2 | [merged PR #408](https://github.com/jiangzhengwenjz/katam/pull/408) |
| `decomp-cookin` | `f2ecfac271920f57accacf39a5b1e50141f49633` | 1 / 17 | [merged PR #393](https://github.com/jiangzhengwenjz/katam/pull/393) |
| `decomp-flamer` | `5ce4445455e7bf501f482c5a1638e64f1b379106` | 1 / 13 | [open PR #398](https://github.com/jiangzhengwenjz/katam/pull/398) |
| `decomp-kirby_cannon` | `8b4435286fa03bebe8533530c95456e016d9d554` | 1 / 3 | [merged PR #407](https://github.com/jiangzhengwenjz/katam/pull/407) |
| `decomp-large-star-stone-block` | `f9e0fd98895ad6aee589e2166e97480c2514a57e` | 1 / 14 | [merged PR #400](https://github.com/jiangzhengwenjz/katam/pull/400) |
| `decomp-leap` | `f2de80ac6cc8c7073f80abbb3d76c1ba7ee35342` | 1 / 18 | [merged PR #392](https://github.com/jiangzhengwenjz/katam/pull/392) |
| `decomp-star-stone-block` | `77e8874e0be5149b0aae78c96f9f7e6e439d3117` | 1 / 15 | [merged PR #399](https://github.com/jiangzhengwenjz/katam/pull/399) |
| `decomp-sub_08153184` | `c59b6814a37caf8ee2b2d4912d68e0e0d3b6f079` | 1 / 1 | [merged PR #410](https://github.com/jiangzhengwenjz/katam/pull/410) |
| `decomp-work` | `c68a09e381e564f9abd533198671b617e258db10` | 1 / 19 | [merged PR #379](https://github.com/jiangzhengwenjz/katam/pull/379) |
| `decomp-work-post375` | `5e7d5e3e773dfac24a451e6ab9a89d7e123c61f3` | 6 / 197 | [merged PR #375](https://github.com/jiangzhengwenjz/katam/pull/375) |
| `master` | `60c1c2370e528c6ae8ac5c994e642541840b5210` | 0 / 209 | No ahead commit |
| `pr-code-0802F8D8` | `822f5023aa523817ce8099a6277a4c38356c7f0a` | 1 / 20 | [merged PR #378](https://github.com/jiangzhengwenjz/katam/pull/378) |
| `pr-code-08020220` | `6ff689c91019a144224b78b987b55512656799ce` | 2 / 196 | [merged PR #377](https://github.com/jiangzhengwenjz/katam/pull/377) |

### BlameMateo/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `Naming-Sound-Effects` | `bbac8d385d43ffeacf57bf474a170a52a1794967` | 0 / 210 | No ahead commit |
| `master` | `3d5d061d5212e9290ac1ebe5e7cb5d17102fe3a3` | 0 / 206 | No ahead commit |

### IoIxD/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `kirby_doc` | `e8db6c263df9a684c04fd9fd00b66d876c2f3a73` | 4 / 307 | [merged PR #340](https://github.com/jiangzhengwenjz/katam/pull/340) |
| `levelinfodoc` | `e160b77a8b1b3a7f5df3639a658a10845aee518e` | 9 / 318 | [merged PR #338](https://github.com/jiangzhengwenjz/katam/pull/338) |
| `master` | `8f8b1dbc1ecf863283687a406656453589e97422` | 0 / 308 | No ahead commit |

### Kurausukun/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `audio_dump` | `080747fee66ce9cb2f420d7af530b45075c58eb1` | 6 / 490 | [merged PR #304](https://github.com/jiangzhengwenjz/katam/pull/304) |
| `master` | `2dca539005bbb82d050d229e17ae7733186a223b` | 0 / 492 | No ahead commit |
| `midi` | `21d18e961fc25f5762617a11a38aabb2f3076857` | 5 / 490 | No matching head among historical upstream PRs; novelty not presumed |
| `not_working` | `f097554a7dac1514aa7930271da9c8e9d2f1c15c` | 3 / 492 | No matching head among historical upstream PRs; novelty not presumed |

### ultra-azu/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `code_08026044` | `b7fd9e28258d647b4e29a935fcfdc9fa07bf7289` | 6 / 276 | [merged PR #352](https://github.com/jiangzhengwenjz/katam/pull/352) |
| `droppy` | `95db18d78c2e4e55cf05ac57dabfd05ccf0bc63c` | 11 / 484 | [merged PR #306](https://github.com/jiangzhengwenjz/katam/pull/306) |
| `goal_game_bonus` | `f3f50b51d61b4fba8e585eaa8418b87686c3ab93` | 3 / 470 | [merged PR #308](https://github.com/jiangzhengwenjz/katam/pull/308) |
| `haley` | `4792e9c492a623b3c729fc4814b07d3a08621fa8` | 1 / 492 | [merged PR #303](https://github.com/jiangzhengwenjz/katam/pull/303) |
| `makefiles` | `cbf33aac23802eb9b59f6fc4b86fbbab159ed9a1` | 33 / 443 | [merged PR #311](https://github.com/jiangzhengwenjz/katam/pull/311) |
| `master` | `69aa58e8c79acbfa84f0fb86e04ab7085ea97537` | 0 / 467 | No ahead commit |
| `sfx` | `11ccb2bc2e1d9b93a31964bd7eea5f28dadd7e33` | 37 / 386 | [merged PR #321](https://github.com/jiangzhengwenjz/katam/pull/321) |
| `sirkibble` | `66d33d1d031219025ada52ddad5909434631ac75` | 12 / 504 | [merged PR #302](https://github.com/jiangzhengwenjz/katam/pull/302) |

### achristensen4/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `db411844f8705a3dc36dd10c3180fff600d29a14` | 0 / 550 | No ahead commit |

### soiryl-pas/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `1197474f80e5de282fbedcd0025ebfa61f61a764` | 0 / 0 | No ahead commit |

### ventiph/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `feb7c958e270d647050de96e94ac0de35b51cbe7` | 6 / 559 | [merged PR #288](https://github.com/jiangzhengwenjz/katam/pull/288) |

### Lrs121/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `jzw` | `39a31fdda97b033d2318c4e427b0feacf365d877` | 1 / 563 | [merged PR #284](https://github.com/jiangzhengwenjz/katam/pull/284) |
| `master` | `1677a2b2e6e9ffa9138fed115ed649825a717d27` | 0 / 563 | No ahead commit |

### NeonWolf532/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `jzw` | `8ce3676a96ae3460fb5ac67b6d9be28c045606dd` | 1 / 600 | [merged PR #267](https://github.com/jiangzhengwenjz/katam/pull/267) |
| `master` | `1b352c29ef8f0f240952a2d7d68152cc8c822610` | 0 / 600 | No ahead commit |

### Cofflag/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `26b47916b1ee68a201948c142cd94cefac2166f2` | 0 / 625 | No ahead commit |

### Shalmezad/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `3765dfdd0056e445aebaaa9b71cadb9ca488e932` | 0 / 714 | No ahead commit |

### EpochFlame/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `jzw` | `b290f0b0a22a1e23e42537b11a6a4fd2ba809cd8` | 1 / 828 | No matching head among historical upstream PRs; novelty not presumed |
| `master` | `454c333d5ed965d9609ec55991e6f38f4829bf7d` | 0 / 712 | No ahead commit |
| `working` | `c3b8a235be094f7387b5ff903d0791a8e5fba28e` | 0 / 843 | No ahead commit |

### fserve/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `jzw` | `645fedbfc577a9e3f0168eee07d8d8d6483ac3ce` | 9 / 1013 | [merged PR #63](https://github.com/jiangzhengwenjz/katam/pull/63) |
| `master` | `3d1486a67c2bd27fc561a0a0d21cd2797d949a46` | 0 / 1012 | No ahead commit |
| `working` | `3d1486a67c2bd27fc561a0a0d21cd2797d949a46` | 0 / 1012 | No ahead commit |

### UraYukimitsu/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `96cdb63fe363f7e6a452949dd69a0de9acdd5b0c` | 0 / 1048 | No ahead commit |
| `working` | `1db7ec95501f68414be12e1cde4be81d94e022b4` | 0 / 1107 | No ahead commit |

### Jenna1337/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `83f1618cab9bccccc963d89632a6c7c1acbbcca4` | 0 / 162 | No ahead commit |
| `working` | `12fbf76b875cc8448a32f4d93e4ac37816f0a412` | 0 / 1052 | No ahead commit |

### Cleverking2003/katam

| Branch | Head | Ahead / behind | Upstream review evidence |
|---|---|---|---|
| `master` | `6df872283c4cf1317d000c5dfcf6623bd89af077` | 16 / 1344 | [merged PR #9](https://github.com/jiangzhengwenjz/katam/pull/9), [merged PR #11](https://github.com/jiangzhengwenjz/katam/pull/11) |

## Priority candidate manifest

These are review candidates, not imported or locally verified work. Preserve the original authors and commits. Do not replace the baseline with stale fork trees. A reasonable combined order is PR #411, #397, then #398; their source files do not overlap and their linker edits use distinct anchors. Textual compatibility does not prove binary compatibility.

### PR #411 — Completes the remaining assembly unit of the shared object/Kirby engine

[Original PR](https://github.com/jiangzhengwenjz/katam/pull/411); original contributor `jiangzhengwenjz`. Exact PR base `1197474f80e5de282fbedcd0025ebfa61f61a764`, head `3bbc5aba2d7eaa3ad327d6b43227a4a19a1536af`.

Code range, end-exclusive: 0x08098E54–0x08099B80; additional rewrites in the existing code_0806F780 object. No additional dependency identified from file manifest; full object/link validation remains necessary.

Files: `asm/code_0806F734.s`, `include/code_0806F780.h`, `linker.ld`, `src/code_0806F780.c`.

Body only says Collaborated by GPT; no comparison result.

### PR #397 — 105 ending-cutscene functions and typed private tables

[Original PR](https://github.com/jiangzhengwenjz/katam/pull/397); original contributor `sh1ftmaker`. Exact PR base `6e0b5b5d0cd5ba77ec373d60ee15deda06c0713b`, head `e1f1592c4c0e3dc3fb34ee6c1f59c76043a74212`.

Code range, end-exclusive: 0x0802B4A8–0x0802E16C. Data range: 0x082EB4A0–0x082EB6DC. PR396 already merged in baseline

Files: `asm/code_0802B4A8.s`, `data/data_17.s`, `include/code_0802B4A8.h`, `include/functions.h`, `linker.ld`, `src/code_0802B4A8.c`, `src/code_0802E16C.c`, `src/dark_mind.c`.

PR body claims clean make compare (six outputs) and complete NONMATCHING link; not independently verified here.

### PR #398 — 38 remaining Flamer states/effect functions

[Original PR](https://github.com/jiangzhengwenjz/katam/pull/398); original contributor `sh1ftmaker`. Exact PR base `a9dfd22949f49828c0a74421a1d43ba203cb8bd5`, head `5ce4445455e7bf501f482c5a1638e64f1b379106`.

Code range, end-exclusive: 0x080B8954–0x080BAB78; existing flamer C also changes. No additional dependency identified from file manifest; full object/link validation remains necessary.

Files: `asm/flamer.s`, `linker.ld`, `src/flamer.c`.

PR body claims clean make compare (six outputs) and complete NONMATCHING link; not independently verified here.

PR #397 replaces the ending-cutscene assembly and converts its private rodata plus the neighboring language table. Verify all converted bytes, table relocations, `0x082EB6DC` as the first untouched datum, every static function referenced by raw pointers, and the complete linked image. PR #411 and #398 also rewrite existing C, so comparing only the deleted assembly ranges cannot validate the full patch.

Without a user-supplied baseline ROM, a per-object byte and relocation comparison may establish narrower evidence for code whose reference assembly is available; it cannot establish all ROM-dependent data or all six final outputs. The required authoritative check remains a dependency-aware non-modern top-level `make compare` with six successful checksums, followed by a complete `NONMATCHING` compile/link.

## Additional useful work and exclusions

- [PR #403](https://github.com/jiangzhengwenjz/katam/pull/403), head `8cacafd24d75f270e10c4bdc639dce1dd6239e66`, names eight switch functions in `include/big_small_switch.h` and `src/big_small_switch.c`. It is semantic documentation, not additional decompiled code; verify each lifecycle/side-effect claim independently.
- [PR #413](https://github.com/jiangzhengwenjz/katam/pull/413), head `7c0831e49ce3fdea81ebf5cbb2ac5b1521047fb3`, changes `src/hot_head.c`, `src/palette_effects.c`, `src/sprite.c`, and `src/waddle_doo.c`. It reduces matching debt but retains volatile affine locals and a one-pass loop; do not report all matching tricks removed. Full object validation is necessary.
- `sh1ftmaker/katam` branch `decomp-0802E57C`, head `0cb8f35a8c9f3f25d0dab7cce9673f3a5f7bb922`, is closed unmerged PR #395. It combines two translation units and retains `asm/nonmatching/sub_0802E78C.inc`; it is a separate lower-priority candidate with source-boundary and linker work.
- `zalo/katam` heads `d1d74db29f51081c0ae55a40003e03b3cbe8e500` and `6f470934be50d2990c71e2470344b222c46196e3` add `tools/dump_kirby_sprites.py`, `tools/dump_sfx.py`, and field documentation in four existing source/header files. The buddy-extraction head `5b9d5412ee022c5c27bb807a0d869a03baa992df` additionally includes generated wasm and extracted gameplay code. Do not import the binary or assume these extractions constitute matching decompilation.
- `bungerFan192/katam3ds` systems head `51dbc88484358c0427b6a99e60a0bff6f6c692be` adds 21 files, mainly `port/3ds/`, plus CI. It is platform scaffolding/adapters, not proof of a playable full game or extra ROM-matching functions.
- `Crazycolbster/katam_kommented` head `f632e4a89113cf8d0ad9d695890c8d25220d9269` adds comments in Big Waddle Dee and Moonlight Mansion background sources, alongside editor/build metadata. Evaluate comments as hypotheses; omit personal editor/generated metadata.
- `ventiph`, `Cleverking2003`, old `jzw` branches, and `sh1ftmaker/all-work` retain divergent history. Their ahead counts must not be added to completion totals. Many older jackmgaller, ultra-azu, IoIxD and sh1ftmaker topic heads are already represented by merged PRs.

## Independent recompilation and port projects

| Project and exact default head | Evidence and compatibility | Reuse scope |
|---|---|---|
| [LuisDevGaming/AmazingMirrorRecomp](https://github.com/LuisDevGaming/AmazingMirrorRecomp) `39d872c29c15a3cec374655e77cca4baa725de40` | Eight tracked files: README, BIOS/game/controller/user configuration and controller database. `game.toml` selects static recomp settings. No recompiler or game implementation is tracked. The description says 120 FPS; no such runtime result was verified. | No root license found; controller DB has its own separate notice. No unique implementation to merge. |
| [Felipe-Gomes-Amorim/kirby-amazing-mirror-recomp](https://github.com/Felipe-Gomes-Amorim/kirby-amazing-mirror-recomp) `2bb49d0631cb54d928d70f97e6aacf79a4b15fb6` | Independent ARM/Thumb-to-C emitter (`recomp/emit.py`), ROM analysis (`tools/analyze_rom.py`), runtime, hardware model and tests. Instruction translation is not recovered matching source. README describes interpreter fallback and limited gameplay coverage. | Root LICENSE explicitly MIT, copyright Felipe Gomes 2026. Original tooling can be evaluated separately with its notice and dependency review; it is not a drop-in katam source patch. |
| [adrianfernando617-byte/kirby-mirror-recomp](https://github.com/adrianfernando617-byte/kirby-mirror-recomp) `e89b8757348c407e0086cafa44642bcda45b1323` | gbarecomp runner, symbols/config and `src/mod_widescreen.cpp`. Source reads a room canvas from guest RAM and calibrates visible background samples for wide margins. Depends on a separate runtime and decomp symbols. | Root PolyForm Noncommercial 1.0.0, not MIT. Preserve terms; symbol provenance has separate unresolved upstream licensing. No import into a permissive combined runtime without review. |
| [sempai3050-create/KirbyMirrorRECOMP](https://github.com/sempai3050-create/KirbyMirrorRECOMP) `7b9fc0032d8029a29d39c04f91c6259b9040c984` | Android packaging around gbarecomp; CMake and `src/main.cpp` call MobileProcessOptions/mobile_prepare_process. Tracks roughly 130 MB of generated C++ shards, not recovered source. | No root license found. Vendored runtime and SDL licenses do not automatically cover original app code. Exclude generated game code/binaries and audit dependencies independently. |
| [sh1ftmaker/katam-port](https://github.com/sh1ftmaker/katam-port) and [zalo/katam-port](https://github.com/zalo/katam-port), default `master` `0c83b1f12ef93db48659da2f026c716b8124b109` | Same default commit and tree, despite different push dates. Separate software PPU, DMA, m4a mixer, source adaptation and desktop/browser host. This is a decomp-based port, not additional matching progress. Nondefault branches are substantially newer. | No root license found in inspected trees. Do not import unique runtime/tooling code merely because public. Game-derived assets and original-game rights remain separate. |

### Port branch audit

`master` README limitations must not be applied automatically to newer `main`. `main` includes a shelved netplay handoff; `coop` is a different gameplay/network approach. Branch commit messages and documents are evidence of intended features, not local play verification.

| Repository / branch | Exact head | Ahead / behind port master | Complete changed paths |
|---|---|---|---|
| sh1ftmaker/katam-port / `coop` | `13b97a2e5464bc79899b6d18b9da3f89452af3c1` | 192 / 0 | 719 |
| sh1ftmaker/katam-port / `editor` | `1a4b33d2b2612fbc457135a8c61f3830d46b86f1` | 187 / 0 | 724 |
| sh1ftmaker/katam-port / `gh-pages` | `43cacd01dffabdd49747990051b88a9ac0cd0da6` | unrelated / unrelated | 173 |
| sh1ftmaker/katam-port / `lighting` | `37ff38e23a97204dcf84d0ed5b8a3ef1a9067a46` | 181 / 0 | 704 |
| sh1ftmaker/katam-port / `main` | `1249ebf6bc68e45b24cacc3050f27ffdcdac6bc2` | 179 / 0 | 703 |
| sh1ftmaker/katam-port / `master` | `0c83b1f12ef93db48659da2f026c716b8124b109` | 0 / 0 | 0 |
| sh1ftmaker/katam-port / `menus` | `a3d55b07c1b3e73d702731adb1d0162817202eb3` | 181 / 0 | 705 |
| sh1ftmaker/katam-port / `multiplayer` | `d339363b7c5e8a2755342a71e580e86aad920bf5` | 23 / 1 | 35 |
| sh1ftmaker/katam-port / `quality-of-life` | `778d9a8d7905f56c8706b43c19c2ba0eab7e7881` | 1 / 60 | 84 |
| zalo/katam-port / `coop` | `13b97a2e5464bc79899b6d18b9da3f89452af3c1` | 192 / 0 | 719 |
| zalo/katam-port / `editor` | `1a4b33d2b2612fbc457135a8c61f3830d46b86f1` | 187 / 0 | 724 |
| zalo/katam-port / `gh-pages` | `28a39f07d636813e7346d21675af574617e35c1f` | unrelated / unrelated | 163 |
| zalo/katam-port / `lighting` | `cbe8aecf4690602264577d14fa2c9a4efd22372e` | 197 / 0 | 714 |
| zalo/katam-port / `main` | `1249ebf6bc68e45b24cacc3050f27ffdcdac6bc2` | 179 / 0 | 703 |
| zalo/katam-port / `master` | `0c83b1f12ef93db48659da2f026c716b8124b109` | 0 / 0 | 0 |
| zalo/katam-port / `multiplayer` | `d339363b7c5e8a2755342a71e580e86aad920bf5` | 23 / 1 | 35 |
| zalo/katam-port / `quality-of-life` | `778d9a8d7905f56c8706b43c19c2ba0eab7e7881` | 1 / 60 | 84 |

The machine inventory supplies all changed paths from complete recursive trees, including comparisons whose API file list hits its 300-file cap. `gh-pages` histories have no common ancestor with port master and are deployment artifacts. Identical heads across forks are duplicates. Zalo lighting head `cbe8aecf4690602264577d14fa2c9a4efd22372e` has additional lighting work relative to sh1ftmaker lighting `37ff38e23a97204dcf84d0ed5b8a3ef1a9067a46`; do not treat the entire zalo port as a mirror.

## Actual latest commit dates

The latest source-branch head found among these projects is sh1ftmaker/katam-port `menus`, commit `a3d55b07c1b3e73d702731adb1d0162817202eb3`, authored and committed **2026-11-12 19:24:00 UTC**: “Menus proof of concept: SETTINGS opens a settings screen inside the game”. This is an experimental menu feature in a decomp-based port, not a new complete static recompilation. Its deployment head `43cacd01dffabdd49747990051b88a9ac0cd0da6` is timestamped 19:24:05 UTC, five seconds later, but is a publication artifact.

LuisDevGaming commit `39d872c29c15a3cec374655e77cca4baa725de40` is authored/committed **2026-11-11 18:56:15 UTC**, while its repository push timestamp is 18:56:18 UTC. It is the newest default head among the four separately named recomp repositories, but it is not the newest source branch in the broader port audit. The newer coop documentation head is 2026-11-11 22:58:54 UTC. Exact author and committer timestamps for every related-project branch head are recorded in the JSON; dates refer to commits, not relative ages or push timestamps.

## Licensing and validation boundary

Upstream katam has no root license declared in the API/tree inspected. Public visibility and GitHub fork/PR mechanics are not a general software license. Upstream-family contributions and original-author PRs can be tracked with their provenance for review; independent port/runtime code must not be merged under an invented permissive license. No game ROM, BIOS, generated recompilation shards, or extracted binary was imported by this audit. Copyright notices and historic authors must remain intact.

This document records evidence and candidates, not a legal determination. No external project was built or executed, no ROM comparison was performed, and no aggregate completion percentage was calculated from repository names, commit counts or README claims.

## Discovery and reproducibility

Queries: `katam in:name`; `"amazing mirror" decomp`; `"amazing mirror" recomp`; `kirby mirror recomp`; `AmazingMirror in:name fork:true`; `"katam" "port" in:name,description fork:true`; `"Kirby" "decompilation" in:description fork:true`. The first broad search has more than 100 results and only the first 100 were retrieved; targeted searches and the complete direct fork endpoint provide the relevant coverage. Search indexing, renamed/deleted branches, unindexed repositories, private repositories, off-GitHub projects and changes after the snapshot remain limitations.

API evidence was cached locally in ignored `build/research/`. Main endpoints were repository metadata, paginated direct forks, branch lists, exact-base compare endpoints, recursive trees, 399 historical PR records, selected PR detail/files, README and selected implementation files. The tracked JSON keeps the durable relevant data without copying source implementations or binaries. Re-run discovery before a later integration; branch names and push dates are mutable.

## Prepared integration references

The three original PR heads have been fetched without changing the active branch or checking out candidate code. `git apply --check` passed individually for each original single-commit patch against the current baseline-based working tree. This verifies textual applicability only; no candidate code was applied, merged, built, or ROM-verified.

| PR | Local comparison ref | Original upstream branch | Deleted reference ASM bytes | Converted data bytes |
|---|---|---|---|---|
| #411 | `refs/remotes/candidates/pr411` | `jzw` | 3372 | 0 |
| #397 | `refs/remotes/candidates/pr397` | `decomp-0802B4A8` | 11460 | 572 |
| #398 | `refs/remotes/candidates/pr398` | `decomp-flamer` | 8740 | 0 |

The exact original heads and parent commits are listed in the candidate manifest above. Their only shared changed path is `linker.ld`, with edits at separate text/rodata anchors; no source/header/data paths overlap. This supports the proposed #411 → #397 → #398 order, but a combined application and byte/relocation comparison have not been performed by this audit. Imported original commits must retain Zhengwen Jiang and sh1ftmaker as their respective authors; new integration or research commits may be authored MatyMeatBoy.

## Check of the existing GBANoCable project

[MatyMeatBoy/GBANoCable](https://github.com/MatyMeatBoy/GBANoCable/tree/58ed012052bc1e19b5866e3be70bb83a39c0f3df), default `main`, head `58ed012052bc1e19b5866e3be70bb83a39c0f3df`, was inspected through its complete 32-entry recursive tree, README and selected porting/reference documents. It contains the generic MIT-licensed C slot engine in `reference/src/gbanocable.c`, tests, a Python relay, and link/recompilation guidance. No Kirby/katam game source or game-specific protocol file appears in that tree. The selected porting documents refer to ReKHCoM and Shining Soul II; they do not establish an earlier Kirby decompilation. This finding is limited to the inspected default tree and documents; no historical/deleted branch audit was performed.

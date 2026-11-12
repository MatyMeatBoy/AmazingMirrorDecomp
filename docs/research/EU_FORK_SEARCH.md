# European support search across audited forks

AI-assisted research for MatyMeatBoy, snapshot 2026-11-12T22:11:32.654230+00:00. This answers whether an existing European matching build was available before adapting the project.

## Result

**No existing European matching target was found in the 24 audited decompilation forks and all 91 branch heads.** Every root Makefile was read successfully: all 91 specify `GAME_CODE := B8KE` and `GAME_LANGUAGE := ENGLISH`. Every root checksum file was read successfully: all 91 expect USA SHA-1 `274b102b6d940f46861a92b4e65f89a51815c12c`. Header templates were also read for all 91 heads. This conclusion is based on actual build inputs, not README labels alone.

There is nevertheless a concrete useful European research source: the separately maintained, MIT-licensed KatAM Randomizer has regional address tables and links its added code against European addresses. It is not a complete European decompilation or a byte-identical rebuild of the original game.

## Owned regional identity and Spanish

The root task identified the user-owned 16 MiB ROM as `B8KP`, SHA-1 `6f478a455383a2a12378f292581dfd7300300700`. The [Game Boy hardware database entry](https://gbhwdb.gekkio.fi/cartridges/AGB-B8KP-0/3615retro-1.html) independently records that identity as Europe, with English/French/German/Spanish/Italian. This research did not re-hash or publish the local image.

The USA decompilation already defines `LANGUAGE_SPANISH` alongside six language constants. Multilingual assets or Spanish menu support in a USA-derived tree do not make that tree a European rebuild. `GAME_LANGUAGE` is a build preprocessor definition, distinct from the game’s runtime selected language. Changing the cartridge header alone does not resolve regional code/data layout.

## Exact coverage

| Surface | Checks | Finding |
|---|---|---|
| 24 decomp forks / 91 branch refs | Root `Makefile`, `katam.sha1`, `asm/rom_header.inc`, language header | 91/91 Makefiles B8KE + ENGLISH; 91/91 checksum files USA; 91 headers read; 80 language headers present, 11 absent in older trees. |
| 17 decomp-port branch refs | Actual Makefiles, game/recomp TOML, entry points, platform loader and native host where present | No B8KP, owned EU SHA-1 or Europe token in those checked files. This is not proof that every generic loader rejects Europe. |
| Four independent recompilation heads | Actual game/recomp config and entry points; additional Felipe build driver | USA identities appear in the configured projects. Felipe `tools/build_all.py` contains a supported SHA-1 dictionary with only the USA identity. No existing verified EU recomp target found. |
| 107 cached branch comparison sets | Commit messages and available changed-file patches | No EU/B8KP/owned-SHA hit. API file-list limits remain as documented in the main audit. |
| Upstream issues/PR search | Europe, European, EUR, B8KP | No relevant upstream issue/PR target found in the queried results. |
| Exact SHA and broader public search | Code search and indexed web search | Exact-SHA code hits were ROM databases, not build source; a broader issue search exposed the randomizer regional-support lead. |

The audit made 528 targeted file-endpoint checks, of which 399 succeeded and 129 were missing/unavailable. Missing optional port files are not negative evidence about regional support. [The machine evidence](eu_fork_search.json) records each audited branch head, file outcome, Git blob identity and matching regional/configuration lines.

## MIT regional address hints imported as references

[Unovamata/KatAM-Randomizer](https://github.com/Unovamata/KatAM-Randomizer/tree/f7c813da659c80f0c06a474e2ea8e0a19f2d79bc), exact commit `f7c813da659c80f0c06a474e2ea8e0a19f2d79bc`, provides `ROM Expansion/versions/europe.txt`, `usa.txt`, and `japan.txt`. Its original [LICENSE](../../config/reference/katam-randomizer/LICENSE) is MIT, copyright 2024 Bryan; that notice is preserved. Only the three text tables and license were imported, byte-for-byte with Git blob hashes verified. No expansion code, generated code, binary or asset was imported.

| Local reference | Original Git blob SHA-1 | Role |
|---|---|---|
| `config/reference/katam-randomizer/europe.txt` | `3214a0ab87273b57174bca7a3ab3dfd72963d543` | External regional hint table |
| `config/reference/katam-randomizer/usa.txt` | `06e02e23a632db823e786b4b3eff184c6582b441` | External regional hint table |
| `config/reference/katam-randomizer/japan.txt` | `31c3f018be76687c6644767771016b6692970502` | External regional hint table |
| `config/reference/katam-randomizer/LICENSE` | `554d6825907fb0b4b717801040fce69a451bfe79` | Original MIT notice |

The parsed view is `config/regions/eu_external_symbols.json`. It has **400 unique names: 399 address values and one count, `AnimCount = 939`**. The raw European file has 404 records and four identical repeated names: `GetCollisionTile`, `gUnk_03002EC0`, `gUnk_030039A4`, and `sub_0804E09C`. The original file is unchanged; only identical duplicates are collapsed in the parsed view. There are no conflicting duplicate values. Every parsed entry is explicitly `reference_hint_not_verified`, `verified: false`.

The originating `find_symbols.py` uses masked Thumb instruction anchors (ignoring BL encodings and literal-pool words), data references from matched functions, and a nearest-symbol shift fallback for remaining values. Those methods offer useful hypotheses but do not prove every label or type. Its normal workflow also expects a built USA ROM and ELF. The user-owned EU image alone does not establish that this external matching process has been reproduced here.

| Example symbol | USA reference | EU reference | Difference |
|---|---|---|---|
| `ObjectMain` | `0x08099B80` | `0x08099BC8` | `+0x48` |
| `TaskCreate` | `0x08152B00` | `0x0815343C` | `+0x93C` |
| `gCollisionAttributes` | `0x082D88B8` | `0x082DA758` | `+0x1EA0` |
| `gKirbys` | `0x02020EE0` | `0x02020EE0` | `0` |

The varying differences show why one uniform address shift or cartridge-code replacement is insufficient. These are external reference values, not newly verified local bindings.

## Cross-check against the independent local partial matcher

Compared the imported hints with `build/eu/receipt.json` snapshot SHA-256 `cae8d2998ee02c9bb5a1af7996885c48e4d898580c2ab7f3820f65c5f6602400` containing 142 modules. There were **210 shared external bindings**: 95 exactly equal and 115 differing only by the Thumb function-pointer bit. There were **121 shared defined symbols**: 120 exactly equal and one Thumb-bit-only difference. **No conflicting shared address was found.**

Thumb-bit normalization was allowed for function-like external names and for defined `.text` symbols, not arbitrary global data names. Agreement is a consistency cross-check; the external table is not promoted to verified evidence merely by agreeing with inferred bindings. The local matcher’s byte/relocation checks remain the authority for its own credited modules. Names not shared with that receipt remain unchecked reference hints. The full pairwise comparison is retained in the machine evidence.

## Limits and next use

No already-finished European matching build was discovered in the audited fork inputs. The useful existing European work is an attributed address/patching reference, which can seed independent relocation, function, type and data-boundary investigation. Full regional image reconstruction and Spanish runtime verification remain separate validation tasks. This research neither changes the original game sources nor claims a matching European ROM based on configuration, names or table agreement alone.

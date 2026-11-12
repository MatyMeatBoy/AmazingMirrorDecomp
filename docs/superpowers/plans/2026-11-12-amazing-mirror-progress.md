# Amazing Mirror progress implementation plan

> **For agentic workers:** Use executing-plans for the coordinator and parallel independent research workers. Follow this plan task by task.

**Goal:** Publish an attributed combined research base and reproducible progress inventory for AmazingMirrorDecomp.

**Architecture:** Preserve katam's matching source and exact compiler. Independent workers audit public sources, locate local work, and build isolated object metadata. The coordinator implements reporting and integrates reviewed results.

**Tech Stack:** Python standard library, GNU ARM binutils, matching agbcc, SVG, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-12-amazing-mirror-design.md`.

## Global constraints

- Preserve original game behavior, source history and credits; author our commits as MatyMeatBoy.
- No ROM, binary assets, objects or private local paths in public reports.
- No whole-game match claim without all six comparison checks.
- Code, embedded ASM, original ASM, names, assets and ports receive distinct measurements.
- New metadata/reporting tools do not alter the original compilation or linker recipes.

## Review focus

- Missing or stale sources must invalidate metadata rather than retaining positive badges.
- Inline ASM and NONMATCHING default fallbacks must receive no compiled-C credit.
- Duplicate aliases must not inflate byte coverage or function totals.
- Missing library and auxiliary targets must remain explicitly outside an object-only denominator.
- Imported contributions need exact provenance and validation; fork push time is not commit time.

### Task 1: Audit reusable sources

- [x] Record public repository/default-branch commit inventory and all original direct forks.
- [x] Compare unique fork commits and identify compatible contributions and port-only changes.
- [x] Locate existing local source/ROM and document available validation. No owned Kirby ROM was located; full comparison remains unavailable.

### Task 2: Build isolated metadata

**Files:** `tools/progress/metadata_build.py`, `tests/test_metadata_build.py`.

- [x] Write failing guard/classification tests, run them, then implement the builder.
- [x] Pin the compiler, preserve upstream flags and isolate outputs under ignored build paths.
- [x] Produce a manifest of source inputs, objects, text sections, function spans and provenance.

### Task 3: Render truthful progress

**Files:** `tools/progress/report.py`, `tools/progress/render.py`, `tests/test_report.py`, `docs/progress/`.

- [x] Test byte accounting, alias deduplication, stale evidence, original assembly and embedded ASM.
- [x] Generate code/names maps, data status, badges, Markdown and JSON from the manifest.
- [x] Add a separate ROM-free workflow; document commands, scope and retained original gates.

### Task 4: Review and publish

- [x] Run tests and real metadata build; inspect final source diff and SVG rendering. All 28 tests passed; 176 compiled objects have unchanged hashes versus the baseline archive.
- [x] Apply eligible unique contributions or document exact blockers without counting hypothetical gains. Three exact upstream PR heads are ready for draft review; six-output matching validation requires the owned ROM.
- [ ] Review independently, commit, publish PR and verify Linux generated results.

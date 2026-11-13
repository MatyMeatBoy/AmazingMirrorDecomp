# European object-spawn data candidate

This bounded recovery covers the 32-byte table retaining identifier `gUnk_0835105C` and the 876-byte `gSpawnFuncTable1`. The standalone candidate is [eu_object_spawn.s](candidates/eu_object_spawn.s). It uses only the owned B8KP ROM and verified EU function definitions from the coordinator's receipt. Baseline: `b302fb97d7b792bf57b55e236ecfbb0ae7f165e1`.

The 219 dispatch entries were already symbolic source. Their order is now shared through `data/object_spawn_table.inc`, rather than duplicated for Europe. The existing USA `data/object.s` includes the same table between its unchanged raw ranges. Explicit ELF object types and sizes add metadata without adding ROM bytes.

## Extents and evidence

| Object | EU address | Size | Evidence |
|---|---:|---:|---|
| `gUnk_0835105C` | `0x08352B3C` |32 bytes /16 halfwords| Existing `const u16[]` declaration; verified readers; adjacent table address |
| `gSpawnFuncTable1` | `0x08352B5C` |876 bytes /219 pointers| Existing dispatch source; verified reader binding; every function definition and complete function span |
| `gSpawnFuncTable2` | `0x082DB074` |16 bytes /4 NULL pointers| Existing native C definition and complete verified local extent |

The end of table1 is `0x08352EC8`, independently bound as the next existing symbol `gUnk_083513E8`. Every entry equals its corresponding verified global function definition; all target pointers retain the Thumb bit. There are 159 distinct function symbols, and every entry has a complete verified C function span. No name, callback identity, argument type, or source boundary was inferred from visual behavior.

The unknown halfword table is read as room identifiers by existing code, but its identifier and element order remain unchanged. `sub_080103BC` scans all 16 entries; HUD and Kirby paths inspect bounded subsets, and cutscene-trigger code accesses entries 10 and 15. This supports the existing halfword representation and complete 32-byte extent without introducing a semantic rename.

`include/data.h` declares both dispatch tables as arrays of function pointers taking `const struct ObjectTemplate *` and `u8`. `src/code_080023A4.c` selects table1 for `spawnTable == 1` and table2 for `spawnTable == 2`, then indexes by the existing byte-wide `type` field. This patch changes neither the dispatch ABI nor index validation. Table2 is already recovered C and is not redefined by the candidate; its four zero entries do not establish that the associated path is safe or unused.

## Assembly and comparison

The candidate resides under `docs/research/candidates/`, outside the Makefile's `data/*.s` and `data/*/*.s` wildcard inputs. It rejects assembly without the explicit European selector:

```sh
arm-none-eabi-as -mcpu=arm7tdmi --defsym REGION_EU=1 \
  -o build/research/eu_spawn/object_spawn_eu.o \
  docs/research/candidates/eu_object_spawn.s
```

Its `.rodata` contains exactly 908 bytes: 16 explicit halfwords, followed by 219 `R_ARM_ABS32` relocations with zero object addends. Applying verified global function definitions through the normal relocator produces all 908 bytes exactly at `0x08352B3C`. No relocation bytes were copied from the ROM. ELF reports exact `STT_OBJECT` extents of 32 and 876 bytes.

A separate assembly comparison of the original table block and shared include confirmed identical section bytes and all 219 relocation records. The existing representation changes only through extraction into the shared include and explicit object metadata. No USA ROM was used, and the six full USA checksum checks were not run.

The machine-readable [evidence](EU_OBJECT_SPAWN.json) records every slot, symbol, pointer, verified function span, extent, and emitted hash. The owner receipt snapshot is identified by its SHA256; no private ROM, object, or generated assembly is committed.

## Integration boundary

The candidate has no `incbin`, so this 908-byte prefix can be assembled without either regional ROM. A future European data linker must select it in place of the corresponding prefix of `data/object.s` and resolve its 219 symbols against linked EU functions. It must preserve placement, avoid duplicate definitions, verify surrounding data, and perform the full dependency-aware EU rebuild.

This commit does not select the candidate in a build profile, import the opaque remainder of `data/object.s`, change game code, or increase C/data completion credit. Only the header's numeric source representation is new; the existing symbolic spawn table has been confirmed and made reusable for EU.

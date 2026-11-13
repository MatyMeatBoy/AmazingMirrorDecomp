# European minigame source recovery

This experiment starts at `c7d295b75effd9a3a7d9f3146a13209e5bf6de99` and uses the owned 16 MiB B8KP ROM, SHA1 `6f478a455383a2a12378f292581dfd7300300700`, and pinned agbcc `59b966ed1b8f371856dcf99f1546c2fe89c678ca`.

## Two original regional behaviors

`sub_08138B44` starts at EU `0x08138BEC`. After clearing the background scroll registers, EU writes 24 to `gBgScrollRegs[1][1]`. The store at `0x08138C76` uses base `0x03003680` plus offset 6; that base agrees with the independently bound global. Adding this store under `REGION_EU` changes the function from 544 to 560 bytes and gives its unique fixed-byte anchor at the correct EU address.

`sub_0813FF6C` starts at EU `0x08140024`. EU first fills VRAM `[0x06000000,0x06004000)` with zero halfwords, then `[0x0600F800,0x06010000)` with `0x01FF` halfwords. Two natural `CpuFill16_2` calls recover that behavior and grow the function from 336 to 384 bytes. Their size difference also explains the otherwise mismatching assembler-resolved local calls and callback addresses in this translation unit. No fixed-address branch instructions, register steering, or matcher changes were needed.

## Regional graphics payloads

The remaining `subgames.c` failures came from real EU graphics differences. Function-literal references establish these payload addresses; their LZ headers and stream boundaries agree with the next asset boundaries. Existing identical language payloads supply independent neighboring anchors.

| Source PNG suffix | EU address | USA compressed bytes | EU compressed bytes |
|---|---:|---:|---:|
| `crackity_hack/bg/main_tileset_eu.png` | `0x0836F600` |29396|29020|
| `crackity_hack/bg/game_ended/tileset_italian_eu.png` | `0x08376DE4` |1632|1636|
| `wave_ride/bg/game_ended/tileset_italian_eu.png` | `0x0837E99C` |960|960|
| `speed_eaters/bg/main_tileset_eu.png` | `0x083897D0` |12824|12468|
| `speed_eaters/bg/game_ended/tileset_italian_eu.png` | `0x0838CD60` |1204|1208|

Paths are below `graphics/`. Each PNG preserves the existing tile geometry and presentation palette. Its tile indices were reconstructed from the corresponding owned EU payload, then passed through the repository's ordinary PNG-to-4bpp and default LZ compression rules. Every resulting complete compressed payload equals the ROM bytes at the listed address, including alignment bytes. No arbitrary padding or raw ROM files were added. Spanish and all other existing language source assets remain unchanged; `REGION_EU` selects only these five variants. Source and generated payload hashes are in `EU_MINIGAME_RECOVERY.json`.

## Verification and limits

The strict isolated EU reconstruction verified 1,375,236 C bytes out of 1,427,032 executable bytes (96.3703687093%), versus 1,347,220 at this baseline: a 28,016-byte gain, with no pending functions left in either assigned translation unit. The complete 16 MiB reconstructed ROM compared byte-for-byte and had the expected SHA1. Raw pending gaps elsewhere remain uncredited.

The full gate used the existing matcher and an explicitly temporary metadata recipe adding `-DREGION_EU`; that recipe was restored and is not part of the source commits. Integrated published progress requires a fresh build using the official regional profile. The retained local receipt records the temporary recipe, rather than pretending it was the published configuration.

Separate pinned-compiler comparisons without `REGION_EU` confirmed that the complete `.text`, `.rodata`, `.data`, and text relocation records of both changed translation units equal their baseline USA objects. The six complete USA ROM checks were not run because an owned USA ROM was unavailable. No claim about their results follows from these object-level comparisons.

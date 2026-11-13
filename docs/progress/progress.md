# AmazingMirrorDecomp Europe (B8KP)

Verified C: **0.000%** (0 / 1,427,032 executable bytes).

ROM rebuild: **unverified; no C credit**.
Expected SHA1: `6f478a455383a2a12378f292581dfd7300300700`.

Mapped C function spans: 0; existing names: 0. The total European function count is unknown; raw gaps are pending code.

Current source evidence does not establish a verified multilingual ROM rebuild. Language-specific gameplay testing is separate.

Cartridge header: 188 excluded bytes. Data-format recovery is not measured. USA source metrics are a separate reference.

Verified source-backed local data: 0 unique bytes. C initializers and included assets remain distinct from audited semantic formats.

Owned local full-ROM rebuild receipt; CI validates current source evidence and does not obtain the ROM.

## Funciones por categoría

| Categoría | Total | C EU verificado | C pendiente EU | Borrador C | ASM pendiente | ASM conservado |
|---|---:|---:|---:|---:|---:|---:|
| Juego y motor | 5,646 | 0 | 5,644 | 2 | 0 | 0 |
| SDK / bibliotecas | 143 | 0 | 81 | 0 | 0 | 62 |
| Arranque | 2 | 0 | 0 | 0 | 0 | 2 |
| Total | 5,791 | 0 | 5,725 | 2 | 0 | 64 |

| Nombrado | Total | Nombre existente | Sin nombre descriptivo |
|---|---:|---:|---:|
| Juego y motor | 5,646 | 621 | 5,025 |
| SDK / bibliotecas | 143 | 132 | 11 |
| Arranque | 2 | 2 | 0 |
| Total | 5,791 | 755 | 5,036 |

Inventario de fuentes principales: excluye archivos de biblioteca del compilador (libc/libgcc) y programas multiboot auxiliares. No es el total definitivo de funciones de la ROM europea.
Borrador C significa definición alternativa legible; no recibe crédito C verificado. Los nombres existentes no equivalen a nombres auditados.
SDK agrupa SRAM, m4a, MultiSio, MultiBoot, Sio32MultiLoad y wrappers BIOS. Los adaptadores específicos del juego permanecen en juego/motor. Arranque contiene crt0.
Inventario completo: [functions.json](functions.json).

## Bibliotecas del compilador y auxiliares

**Total contabilizado: 6,960 funciones**, incluidas las copias de biblioteca de cada programa. No es un total europeo verificado.

| Programa | Funciones | C disponible | C EU verificado | ASM |
|---|---:|---:|---:|---:|
| Principal: libc/libgcc | 76 | 56 | 0 | 20 |
| multi_boot/subgame_loaders | 1 | 0 | 0 | 1 |
| multi_boot/subgame_loaders/payload | 47 | 0 | 0 | 47 |
| multi_boot/unk_8D94B9C | 344 | 1 | 0 | 343 |
| multi_boot/unk_8E1FE28 | 345 | 1 | 0 | 344 |
| multi_boot/unk_8E8490C | 356 | 1 | 0 | 355 |

Solo las instancias del programa principal con prueba regional reciben crédito C EU; las copias auxiliares no heredan esa prueba. Los aliases comparten una función. La entrada manual __start del cargador se cuenta una vez; no se cuentan etiquetas internas.

Nombre existente en todo el inventario: **1,248**; sin nombre descriptivo: **5,712**. Las propuestas externas sin revisar no se cuentan como nombres confirmados.


Current source inventory unavailable

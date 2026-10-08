# dsh-forecast-penalty — Registro de evaluación de la precisión de la predicción y verificación aritmética del cargo de evaluación

`dsh-forecast-penalty` lee un registro de evaluación de la precisión de la predicción —la cabecera más una fila por periodo de evaluación— y comprueba la completitud y la aritmética de ese mismo registro: que el periodo, el sujeto evaluado y el tipo de mercado estén identificados, que las cifras de predicción, valor real y precisión se puedan analizar como números, que la precisión registrada concuerde con la fórmula de definición que usted configure y el cargo de evaluación con la fórmula de cálculo que usted configure, que la moneda figure como código de tres letras, que no se repita ningún periodo y que no quede ningún marcador de plantilla en la columna de observaciones. Toda comprobación que no pueda ejecutarse se informa en `skipped` con su motivo.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| El registro no dice qué central ni qué mercado cubre, y una fila trae `--` como valor de predicción. | `FP-001` exige que el sujeto evaluado y el tipo de mercado estén identificados, y `FP-002` que el valor de predicción se pueda analizar como número, de modo que un `--` se informa. `FP-001` comprueba que ambos estén rellenados, no que el nombre de la central sea el correcto, y `FP-002` no decide si la predicción fue acertada. |
| La precisión que registro no coincide con la fórmula de definición de mi mercado, y el cargo tampoco con base por tarifa unitaria. | `FP-003` compara la cifra registrada con la fórmula de definición configurada en el paquete de reglas —la expresión de fábrica es una convención común y un ejemplo, no la regla de su mercado: sustituya `expression` o desactive la regla— con una tolerancia de 1,5 puntos. `FP-004` compara el cargo con `考核基数 × 考核单价` con una tolerancia de 0,01; la base la introduce usted. Ninguna de las dos decide si el método de evaluación es aplicable ni si el cargo debe cobrarse. |
| La columna de moneda está vacía en unas filas y en otras pone `元`. | `FP-005` exige un código de tres letras mayúsculas como CNY o USD, así que tanto la celda vacía como el `元` se informan; el límite de la regla es que juzga solo el formato y no decide qué código debe usar su institución para el renminbi. Tampoco decide si la moneda elegida es la correcta. |
| El mismo periodo de evaluación aparece en más de una fila. | `FP-006` informa de un periodo repetido, porque el duplicado hace que el cargo se acumule dos veces y deja sin saber si el periodo se registró dos veces o se evaluó dos veces; la comparación ignora los espacios. Un mismo periodo evaluado por franjas horarias y bloques produce legítimamente varias filas: distíngalas en la columna de observaciones o con otro identificador de periodo, o desactive la regla. No decide cuál de las filas es la duplicada. |
| La columna de observaciones todavía contiene `【】`, `XXX` o `TBD`. | `FP-007` informa de la fila cuando la columna de observaciones contiene uno de los marcadores configurados en el paquete de reglas, porque un registro copiado de una plantilla invita a suponer que la evaluación se realizó de verdad. La lista `terms` es suya para ajustarla, y la regla no decide si el texto de la observación es cierto. |
| Falta una columna entera en mi material, ¿la regla pasa en silencio? | No. Las reglas por columna (`FP-002`, `FP-005`, `FP-006`, `FP-007`) se informan a sí mismas en `skipped` con el motivo de que el material no trae esa columna, y el informe distingue ese caso del de una regla que sí se ejecutó y no halló ninguna fila con diferencias. Una comprobación que nunca se ejecutó no se presenta como superada. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
|---|---|---|
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为台账可追溯性） | FP-001 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为算术可行性） | FP-002 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为本机构配置的准确率定义式） | FP-003 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为本机构配置的考核算式） | FP-004 |
| 《表示货币的代码》 | GB/T 12406—2022（表示货币的代码；2022-12-30 发布并实施；全部代替 GB/T 12406—2008（该版名称为「表示货币和资金的代码」）——注意旧版名称含"资金"；修改采用 ISO 4217:2015，非等同采用；条号本次未取得） | FP-005 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为台账唯一性） | FP-006 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为台账真实性） | FP-007 |

**Boundary:** this plugin checks a **预测准确率考核台账** for arithmetic — that the period and subject are
identified, that forecast and actual figures parse, that the accuracy figure matches the definition formula
you configure, that the assessment charge matches your charge formula, that the currency follows its format,
that periods do not repeat, and that no placeholder survives. It does **not** decide whether a charge should be
levied, whether accuracy passes, or whether a waiver or appeal applies. **Those depend on the market rules, the
exemption cases and the dispute procedure.**

> ### ⚠️ This is a market rule, not a national standard — and the pack says so
>
> The accuracy definition, the exemption threshold, the unit rate and the settlement basis are set by **each
> power market's assessment rules and the grid-connection dispatch agreement**. Provinces differ sharply (some
> use `1 − deviation`, some use root-mean-square error, some assess by time block and band), and **no unified
> national standard exists**. So this pack does not fabricate a standard number: every rule's `excerpt` states
> plainly that its basis is arithmetic self-consistency or a locally configured convention and that **no
> citable clause exists**.
>
> **Two formulas ship as examples, and both are marked as such:**
>
> - `FP-003` **accuracy** defaults to `预测值 ÷ 实际值 × 100` with a 1.5-point tolerance. That is **one common
>   convention, not any market's rule**. Before use, replace `expression` with the formula from your market's
>   rules — or disable the rule. The note spells this out.
> - `FP-004` **charge** checks `考核费用 = 考核基数 × 考核单价`. The base is **entered by you** after working
>   it out under your market's rules, because the threshold, the bands and the volume basis are the market's
>   business and this plugin will not derive them. No unit rate is built in anywhere.
>
> A consequence worth knowing: the accuracy rule ships at `info` severity precisely because its formula is a
> deployment choice rather than a verified requirement.

## Compatibility

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-forecast-penalty
dsh --profile <name> --dump-config | grep 'dsh-forecast-penalty'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/forecast-penalty.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-forecast-penalty
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-forecast-penalty contributors.

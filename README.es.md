<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-forecast-penalty-hero-en-dark.webp">
  <img src="docs/assets/dsh-forecast-penalty-hero-en-light.webp" width="100%" alt="Banner de dsh-forecast-penalty: a la izquierda, el nombre y dos líneas de valor; a la derecha, arriba, una fila real del registro de evaluación (periodo 2026-03, predicción 966, real 1000, precisión 88.00, cargo 4000, moneda CNY) con la regla que se monta en cada columna (FP-002, FP-003, FP-004, FP-005, FP-006, FP-007) y FP-001 en la cabecera de sujeto y mercado; abajo, la tarjeta de hallazgo FP-003 —88.00 declarado frente a 96.6 según la fórmula configurada, 8,6 puntos porcentuales de diferencia, por encima de la tolerancia de 1,5— con una regla de tolerancia que dibuja ambos en un mismo eje; el informe es issues[] 1 · skipped[] 0 y el dictamen queda en manos humanas">
</picture>

# dsh-forecast-penalty

**Compruebe la completitud de un registro de evaluación de la precisión de la predicción y la aritmética del cargo de evaluación — obtiene una lista de qué fila, qué columna y qué corregir; el dictamen queda en manos del revisor.**

Plugin verificador de solo datos para DeepSeek Harness: lee un registro de evaluación de la precisión de la predicción (cabecera del sujeto más una fila por periodo de evaluación), aplica el paquete de reglas versionado que trae (FP-001..FP-007) y enumera solo las diferencias que puede señalar dentro del material: nunca un dictamen de cumplimiento, nunca una atribución de responsabilidad.

[Instalar](#instalación-en-tres-pasos) · [Configuración](#configuración) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidad)
[![npm](https://img.shields.io/npm/v/dsh-forecast-penalty?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-forecast-penalty)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-forecast-penalty/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-forecast-penalty/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidad)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-forecast-penalty?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-forecast-penalty/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-forecast-penalty?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-forecast-penalty)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-forecast-penalty?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-forecast-penalty?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-forecast-penalty/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-forecast-penalty)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-forecast-penalty)

```sh
dsh plugin --profile <name> add dsh-forecast-penalty
```

</div>

<sub>Plugin comunitario, no afiliado a DeepSeek. Repositorio canónico: <https://github.com/PerryLink/dsh-forecast-penalty> (Gitee es un espejo).</sub>

## Qué es

`dsh-forecast-penalty` lee un registro de evaluación de la precisión de la predicción —la cabecera del sujeto más una fila por periodo de evaluación— y comprueba la completitud y la aritmética de ese mismo registro: que el periodo, el sujeto y el mercado estén identificados, que las cifras de predicción, valor real y precisión se puedan analizar como números, que la precisión registrada concuerde con la fórmula de definición que usted configure y el cargo de evaluación con la fórmula de cálculo que usted configure, que la moneda figure como código de tres letras, que no se repita ningún periodo y que no quede ningún marcador de plantilla en la columna de observaciones. Toda comprobación que no pueda ejecutarse se informa en `skipped` con su motivo.

No decide si el método de evaluación es aplicable, si la precisión alcanza el umbral ni si el cargo debe cobrarse o puede eximirse.

- **Para quién es**: personal de contratación y de liquidación de evaluaciones; no hace falta saber usar la línea de comandos: entregue el material en el chat.
- **Qué le entrega**: el material de origen sobre el que trabaja la comprobación (una tabla, un registro o un documento); el original nunca se modifica. Excel puede convertirse antes a JSON/YAML, en el chat si la plataforma lo admite.
- **Qué recibe**: una lista de «qué fila, qué columna, qué falta y cómo corregirlo»; toda comprobación que no pudo ejecutarse se enumera en `skipped` con su motivo.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-forecast-penalty-flow-v5-dark.svg">
  <img src="docs/assets/dsh-forecast-penalty-flow-v5-light.svg" width="100%" alt="Estructura de dsh-forecast-penalty (marcador de reglas): dos entradas arriba —el material mediante parseMaterial, una fila y 12 columnas canónicas, y el paquete de siete reglas rules/forecast-penalty.yaml v2026.1 filtrado primero por only/disabled—; el panel de puntuación da por regla el campo, el tipo de comprobación, el tipo de fundamento hasta el límite de gravedad y la disposición de esta ejecución: FP-003 dibuja el 88.00 declarado frente al 96.6 esperado (±1,5 pp) en una regla de tolerancia, FP-004 cuadra 80 × 50 = 4000 con el 4000 declarado (tolerancia 0,01) y las otras cinco se ejecutan sin diferencias; abajo, dos salidas: issues[] con un hallazgo localizado (FP-003, fila 1, accuracy, info) y skipped[] vacío en esta ejecución, con los motivos por los que una regla puede acabar ahí; el dictamen queda en manos de la persona revisora">
</picture>

## Instalación en tres pasos

1. **Instalar** (elija un canal):

   ```sh
   # canal git (última main; equivale a git+https://github.com/PerryLink/dsh-forecast-penalty.git)
   dsh plugin --profile <name> add github:PerryLink/dsh-forecast-penalty
   # canal npm (versiones publicadas)
   dsh plugin --profile <name> add dsh-forecast-penalty
   # canal tarball: tras pnpm pack en este repositorio
   dsh plugin --profile <name> add ./dsh-forecast-penalty-<version>.tgz
   ```

2. **Configuración mínima** (los valores por defecto bastan; una fila de bundle sin `config` usa todos los valores por defecto y la ruta del paquete de reglas apunta al `rules/forecast-penalty.yaml` incluido):

   ```yaml
   - insert:
       - id: dsh-forecast-penalty
         name: dsh-forecast-penalty
   ```

3. **Verificar que se monta**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-forecast-penalty'
   ```

   Después entréguele un registro; por ejemplo, la muestra incluida (salida esperada en `samples/quickstart/expected/result.json`):

   ```text
   > Ejecuta esta comprobación con la muestra incluida y dime cuántos problemas encontró y de qué gravedad.
   forecast_penalty: 1 issue(s) — warn 1 (FP-001); skipped: 0
   ```

**Desinstalar**: `dsh plugin --profile <name> remove dsh-forecast-penalty` (o elimine la fila del patch del perfil).

<details>
<summary>Usarlo en WorkBuddy / Coze</summary>

Busque «Professional Document Check Suite» en WorkBuddy / Coze (el conjunto completo; esta comprobación es una de sus partes; disponibilidad según catálogo) para usar la misma capacidad de verificación sin línea de comandos.

</details>

<details>
<summary>Instalar desde el mercado de DSH Desktop</summary>

Todos los plugins de PerryLink están en el mercado integrado de DSH Desktop: **Mercado → Fuentes → Añadir fuente → pegar** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ seleccionar**. La instalación sigue requiriendo la verificación de identidad npm del mercado y su confirmación.

</details>

## Capacidades clave

`dsh-forecast-penalty` registra la herramienta `forecast_penalty`: lee un registro de evaluación, aplica un paquete de reglas versionado y devuelve un informe.

- **Siete reglas en un paquete de datos** — el paquete de reglas es datos, no código (`rules/forecast-penalty.yaml`); sustituirlo cambia todo el conjunto de reglas sin tocar una línea de TypeScript.
- **Solo lectura sobre el material** — acepta JSON o YAML y nunca modifica el original; ESM puro, sin peticiones de red y sin llamadas al modelo.
- **Sin citas inventadas** — cada regla lleva `document` / `number` / `clause` / `excerpt` / `kind` / `source`; `excerpt` debe ser una cita literal, y las reglas cuyo texto no se obtuvo en esta pasada lo dicen en el propio `excerpt` y quedan marcadas como `derived-from-principle`.
- **La gravedad sigue a la evidencia** — `derived-from-principle` tiene tope `warn`, la configuración institucional (`institutional-configuration`) tope `info`, y un test lo verifica.
- **Una lista vacía nunca es «no hay nada mal»** — toda comprobación que no pudo ejecutarse se informa en `skipped` con su motivo; una regla por columna que no encuentra su columna se declara en `skipped` en lugar de pasar en silencio.
- **Sin lenguaje que dictamine** — el informe enumera diferencias y nunca se pronuncia sobre cumplimiento, responsabilidad o corrección; un guardián de redacción (wording guard) lo impone y todo informe lleva el descargo.

| Regla | Comprobación | Gravedad | Tipo de base |
|---|---|---|---|
| `FP-001` | el registro identifica sujeto y mercado | warn | trazabilidad |
| `FP-002` | la cifra de predicción se analiza como número | warn | viabilidad aritmética |
| `FP-003` | la precisión coincide con su fórmula de definición | info | fórmula local |
| `FP-004` | el cargo coincide con su fórmula de cálculo | info | fórmula local |
| `FP-005` | la moneda es un código de tres letras | warn | GB/T 12406 |
| `FP-006` | los periodos de evaluación son únicos | warn | unicidad del registro |
| `FP-007` | la columna de observaciones no conserva marcadores sin sustituir | warn | integridad del registro |

### Ejemplos

Estos son los puntos de entrada reales del plugin; instálelo una vez y llame a uno.

**Ejemplo detallado** — herramienta `forecast_penalty`, entrada:

```json
{"rows":[{"考核期":"2026-03","预测值":"待补","实际值":"1000"}]}
```

Salida:

```json
{
  "id": "dsh-forecast-penalty.FP-002.de09b5a6",
  "ruleId": "FP-002",
  "severity": "warn",
  "locator": {
    "field": "forecastValue",
    "row": 1
  },
  "found": "第 1 行「forecastValue」的值「待补」无法解析为数字",
  "expected": "「forecastValue」应填写数字",
  "fix": "预测值应填写数字；本条只核对可解析性，不判断预测是否准确"
}
```

*Observed from `tests/fixtures/FP-002/FP-002-unsafe.json (cases.json expects FP-002 count 1); run via lib/index.mjs rules/forecast-penalty.yaml`*

### Qué preguntas

| Usted pregunta | Qué responde |
|---|---|
| El registro no dice qué central ni qué mercado cubre, y una fila trae `--` como valor de predicción. | `FP-001` exige que el sujeto evaluado y el tipo de mercado estén identificados, y `FP-002` que el valor de predicción se pueda analizar como número, de modo que un `--` se informa. `FP-001` comprueba que ambos estén rellenados, no que el nombre de la central sea el correcto, y `FP-002` no decide si la predicción fue acertada. |
| La precisión que registro no coincide con la fórmula de definición de mi mercado, y el cargo tampoco con base por tarifa unitaria. | `FP-003` compara la cifra registrada con la fórmula de definición configurada en el paquete de reglas —la expresión de fábrica es una convención común y un ejemplo, no la regla de su mercado: sustituya `expression` o desactive la regla— con una tolerancia de 1,5 puntos. `FP-004` compara el cargo con `penaltyBase × penaltyRate` con una tolerancia de 0,01; la base la introduce usted. Ninguna de las dos decide si el método de evaluación es aplicable ni si el cargo debe cobrarse. |
| La columna de moneda está vacía en unas filas y en otras pone la unidad local. | `FP-005` exige un código de tres letras mayúsculas como CNY o USD, así que tanto la celda vacía como la palabra de unidad local se informan; el límite de la regla es que juzga solo el formato y no decide qué código debe usar su institución para el renminbi. Tampoco decide si la moneda elegida es la correcta. |
| El mismo periodo de evaluación aparece en más de una fila. | `FP-006` informa de un periodo repetido, porque el duplicado hace que el cargo se acumule dos veces y deja sin saber si el periodo se registró dos veces o se evaluó dos veces; la comparación ignora los espacios. Un mismo periodo evaluado por franjas horarias y bloques produce legítimamente varias filas: distíngalas en la columna de observaciones o con otro identificador de periodo, o desactive la regla. No decide cuál de las filas es la duplicada. |
| La columna de observaciones todavía contiene marcadores de plantilla como corchetes vacíos, `XXX` o `TBD`. | `FP-007` informa de la fila cuando la columna de observaciones contiene uno de los marcadores configurados en el paquete de reglas, porque un registro copiado de una plantilla invita a suponer que la evaluación se realizó de verdad. La lista `terms` es suya para ajustarla, y la regla no decide si el texto de la observación es cierto. |
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

**Límite:** este plugin comprueba la aritmética de un **registro de evaluación de la precisión de la predicción**: que el periodo y el sujeto estén identificados, que las cifras de predicción y valor real se analicen, que la precisión coincida con la fórmula de definición que usted configure, que el cargo de evaluación coincida con su fórmula de cálculo, que la moneda siga su formato, que los periodos no se repitan y que no quede ningún marcador. **No** decide si un cargo debe cobrarse, si la precisión supera el umbral ni si procede una exención o apelación. **Eso depende de las reglas del mercado, los supuestos de exención y el procedimiento de disputa.**

> ### ⚠️ Esto es una regla de mercado, no una norma nacional — y el paquete lo dice
>
> La definición de precisión, el umbral de exención, la tarifa unitaria y la base de liquidación los fijan **las reglas de evaluación de cada mercado eléctrico y el acuerdo de despacho y conexión a la red**. Las provincias difieren mucho (unas usan `1 − deviation`, otras el error cuadrático medio, otras evalúan por franja y bloque), y **no existe una norma nacional unificada**. Por eso este paquete no inventa una cifra estándar: el `excerpt` de cada regla dice con claridad que su base es la coherencia aritmética o una convención configurada localmente y que **no existe una cláusula citable**.
>
> **Se incluyen dos fórmulas como ejemplos, y ambas están marcadas como tales:**
>
> - `FP-003` **precisión** usa por defecto `forecast ÷ actual × 100` con una tolerancia de 1,5 puntos. Esa es **una convención común, no la regla de ningún mercado**. Antes de usarla, sustituya `expression` por la fórmula de las reglas de su mercado — o desactive la regla. La nota lo explica.
> - `FP-004` **cargo** comprueba `charge = penaltyBase × penaltyRate`. La base **la introduce usted** tras calcularla con las reglas de su mercado, porque el umbral, los tramos y la base de volumen son competencia del mercado y este plugin no los deriva. No hay ninguna tarifa unitaria incorporada.
>
> Un detalle que conviene saber: la regla de precisión se distribuye con gravedad `info` precisamente porque su fórmula es una decisión de despliegue y no un requisito verificado.

## Configuración

Todos los parámetros ajustables son campos Schemastery `Config` de `src/config.ts` (modificables desde cordis.yml); los umbrales por regla viven en el paquete de reglas bajo `rules/`. Una sobrescritura dirigida por id reemplaza la fila entera: repita todas las claves que necesite.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/forecast-penalty.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

Parámetros de regla que conviene conocer:

- `FP-003` `expression` — la definición de precisión. `op` admite `divide`, `product`, `sum`, `subtract` (primer campo menos el resto) y `percent` (primer campo ÷ segundo × 100), con un multiplicador `scale` opcional. `tolerance` vale 1,5 puntos por defecto; ajústelo a su convención de redondeo.
- `FP-004` `expression` / `tolerance` — la fórmula del cargo, `penaltyBase × penaltyRate` por defecto con tolerancia 0,01.
- `FP-005` `pattern` — la forma de la moneda; tres letras mayúsculas por defecto.
- `FP-007` `terms` — los marcadores que se buscan.

Ejemplo de sobrescritura en el patch del perfil:

```yaml
- insert:
    - id: dsh-forecast-penalty
      name: dsh-forecast-penalty
      config:
        disabledRules: [FP-005]
        timeoutMs: 180000
```

## Formato del material

La herramienta acepta JSON o YAML:

```yaml
subject: 某某风电场
market: 省内现货
rows:
  - { 考核期: 2026-03, 预测值: '966', 实际值: '1000', 准确率: '96.60',
      考核门槛: '95', 考核基数: '80', 考核单价: '50', 考核费用: '4000', 币制: CNY }
```

Los nombres de columna se comparan sin distinguir mayúsculas y omitiendo espacios, guiones bajos y guiones; se conservan los nombres propios del registro, de modo que el hallazgo nombra la columna que realmente leyó. Las celdas numéricas pueden llevar separadores de millares y signo de porcentaje. Los campos son opcionales en la capa de lectura y los valida el motor, así que una exportación parcial produce hallazgos de «falta un elemento» en lugar de un fallo.

## Fuentes de las reglas

Los datos de las reglas están en `rules/forecast-penalty.yaml`, separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. Como el régimen de evaluación es una regla de mercado y no una norma, las entradas `basis` del paquete lo dicen explícitamente en lugar de citar una cláusula inexistente; la única referencia externa es la norma de códigos de moneda, cuyo extracto reconoce que el texto de la cláusula no se obtuvo.

El guardián de carga sigue exigiendo documento, cláusula, extracto y fuente por regla, y sigue prohibiendo que una comprobación configurada localmente se marque como `error`. `scripts/check-citations.mjs` y `rules/citations-baseline.json` registran las citas que siguen sin ser trazables en esta pasada: un nuevo extracto no trazable hace fallar la puerta, y también una entrada de la línea base que se haya vuelto trazable, de modo que la línea base solo puede encogerse. Un paquete que exagera su base falla al cargar en lugar de producir un informe de aspecto seguro.

## FAQ

<details>
<summary>¿Decide por nosotros si hay cumplimiento o no?</summary>

No. Solo enumera las diferencias que puede señalar dentro del material (qué fila, qué columna, qué falta y cómo corregirlo) y no decide hechos ni cumplimiento: la conclusión queda siempre en manos del revisor. Un guardián de redacción impone el texto del informe y todo informe lleva el descargo. Tampoco decide si la precisión supera el umbral ni si un cargo debe cobrarse o eximirse.

</details>

<details>
<summary>¿Se sube el material o se guarda en otro sitio?</summary>

No. Es un verificador sin conexión: solo lee el material que usted entrega a la herramienta, no hace peticiones de red, no llama a ningún modelo y no incluye telemetría, analítica ni informes en segundo plano. No escribe datos fuera del resultado de la herramienta y del almacenamiento de sesión/registro del propio host DSH; ese almacenamiento y su retención los controla el host, y este paquete no añade una segunda copia.

</details>

<details>
<summary>¿Una lista `issues` vacía se puede leer como «no hay nada mal»?</summary>

No. Toda comprobación que no pudo ejecutarse se enumera en `skipped` con su motivo (un material al que le falta una columna, una regla detenida por `disabledRules`). Las reglas por columna (`FP-002`, `FP-005`, `FP-006`, `FP-007`) se declaran en `skipped` cuando falta su columna en lugar de fingir que pasan. Lea `issues` y `skipped` juntos antes de sacar cualquier conclusión de un informe.

</details>

<details>
<summary>¿Las dos fórmulas incluidas sirven como regla de nuestro mercado?</summary>

No tal cual. La fórmula de precisión `FP-003` y la fórmula de cargo `FP-004` son **ejemplos**: la primera es una convención común, y en la segunda usted introduce la base de evaluación tras calcularla con las reglas de su mercado, sin ninguna tarifa unitaria incorporada. Sustituya `expression` por la convención de su institución antes de usarlas, o desactive la regla; `FP-003` se distribuye con `info` precisamente porque su fórmula es una decisión de despliegue.

</details>

<details>
<summary>¿Aguantará un trimestre entero de periodos a la vez?</summary>

La herramienta funciona en modo `native` y `ptc`; para trabajo por lotes (un trimestre de periodos o un directorio completo) use `ptc`, donde el coste de esquema se paga una vez. Las comprobaciones son comparación de columnas y aritmética locales: sin peticiones de red, sin llamadas al modelo; `timeoutMs` (120 s por defecto) es el presupuesto de tiempo de espera cooperativo.

</details>

## Solución de problemas

- **`FP-003` salta en todas las filas.** La precisión se calculó con una fórmula distinta de la configurada. Sustituya `expression` por la de su mercado o desactive la regla; no amplíe la tolerancia para ocultar una discrepancia de definición.
- **`FP-004` se declara `skipped`.** El registro no trae columna de base de evaluación o no trae cargo. La base la calcula y la registra usted; el plugin no la deriva.
- **`FP-005` salta con la palabra local de la moneda.** El patrón por defecto exige tres letras mayúsculas. Restrínjalo o amplíelo según la convención de sus documentos de liquidación.
- **`FP-006` salta dos veces en un mismo periodo.** Puede ser legítimo en la evaluación por franjas (punta/llano/valle). Distinga las filas en la columna de periodo o indíquelo en la observación.
- **Una regla nunca se ejecutó.** Revise el arreglo `skipped`; indica el id de la regla y el motivo.
- **El plugin se instala pero la herramienta no aparece.** Compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó; un `main` erróneo hace que el cargador omita la entrada en silencio.
- **`dsh plugin add` rechaza el paquete por incompatibilidad.** El rango de peers cubre `0.1.x` y `0.2.x`; si su runtime queda fuera, conceda una exención explícita: `dsh plugin --profile <name> allow-version dsh-forecast-penalty@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` informa `manifest-peers` como fallo.** El verificador estático compara con un rango de peers codificado que es anterior a la línea 0.2. El runtime aplica la compatibilidad de peers al instalar, así que el rango declarado es el correcto; es un problema conocido de `dsh-plugin-dev`.
- **Los horarios parecen desplazados.** Toda la aritmética es de hora local sobre las cadenas de entrada, sin conversión de zona horaria.

## Compatibilidad

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-rc.2`. `engines.dsh` se declara como `>=0.2.1-0 <0.3.0` y el host lo aplica desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native` y `ptc`; para un trimestre completo use `ptc` |

## Ecosistema y calidad

- [Espejo en Gitee](https://gitee.com/perrylink/dsh-forecast-penalty) (espejo sincronizado; GitHub es el canónico)
- [Página del plugin en dshfind](https://dshfind.com/plugins/PerryLink/dsh-forecast-penalty) (instalaciones y ranking)
- [Informe OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-forecast-penalty) (impulsado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (en catálogo)
- **Canal de la tienda 1024**: `npm i -g dsh1024` una vez y luego `dsh1024 plugin --profile <name> add dsh-forecast-penalty` (cuenta para el ranking de instalaciones de [deepseek1024.com](https://deepseek1024.com))
- [Base de conocimiento del ecosistema](https://perrylink.github.io/dsh-plugin-guide/) — guía de desarrollo de plugins · datos de selección medidos · criterios de mantenimiento

## Desarrollo

```sh
pnpm install                                        # node ^22.19 || >=24
pnpm run typecheck                                  # tsc --noEmit
pnpm test                                           # vitest: suite compartida de plugins de tabla + fixtures emparejados
pnpm run build                                      # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run verify:self-contained                      # las dependencias resuelven desde el registry
pnpm run check:lockfile                             # comprobación de deriva del lockfile
pnpm run check:readmes                              # consistencia de los README en cinco idiomas
pnpm run check:citations                            # línea base de citas del paquete de reglas
node ../scripts/sync-shared.mjs dsh-forecast-penalty   # refrescar src/shared desde ../_shared
pnpm pack                                           # el tarball publicado
```

El plugin es **de solo datos**: `src/model.ts` declara la forma de la tabla, el kit compartido aporta el lector y el motor de comprobación, y el paquete de reglas declara cada comprobación. Ejecución local de la muestra (requiere `pnpm run build` antes para producir `lib/`):

```sh
node samples/quickstart/run.mjs --json
# => {"tool":"forecast_penalty","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":0}
```

La entrada de la muestra está en `samples/quickstart/input/`, la salida esperada en `samples/quickstart/expected/result.json` y una captura en `docs/assets/quickstart.png`. Las imágenes del README se generan programáticamente con [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow) y se pueden volver a ejecutar; el diagrama de flujo antiguo de una sola variante y las imágenes de demostración permanecen en `docs/assets/` para enlaces externos, mientras que los README solo referencian el nuevo par claro/oscuro.

Topics: `deepseek-harness`, `dsh`, `dsh-plugin`, `cordis`, `forecast`, `penalty`

## Familia y agradecimientos

Este proyecto forma parte de la familia de plugins de DeepSeek Harness mantenida por [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Índice completo de la familia: [elegir un verificador por material](https://perrylink.github.io/zh/checkers/choose/) y [todos los plugins](https://github.com/PerryLink). Si le resulta útil, **una estrella ayuda a que la siguiente persona lo encuentre**: no desbloquea nada.

- [@PerryLink](https://github.com/PerryLink) — creador y mantenedor: el paquete de reglas de solo datos (FP-001..FP-007), la herramienta `forecast_penalty`, las notas sobre la base de regla de mercado y la documentación en cinco idiomas.

<details>
<summary>Expandir todos los plugins</summary>

| Plugin | Estado |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** |  |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** |  |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** |  |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** |  |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** |  |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** |  |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** |  |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** |  |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** |  |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** |  |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** |  |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** |  |
| **[dsh-github](https://github.com/PerryLink/dsh-github)** |  |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** |  |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** |  |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** |  |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** |  |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** |  |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** |  |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** |  |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** |  |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** |  |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** |  |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** |  |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** |  |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** |  |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** |  |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** |  |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** |  |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** |  |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** |  |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** |  |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** |  |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** |  |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** |  |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** |  |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** |  |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** |  |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** |  |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** |  |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** |  |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** |  |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** |  |
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** |  |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** |  |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** |  |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** |  |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** |  |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** |  |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** |  |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** |  |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** |  |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** |  |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** |  |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** |  |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** |  |
| **[dsh-skill-pack-security](https://github.com/PerryLink/dsh-skill-pack-security)** |  |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** |  |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** |  |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** |  |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** |  |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** |  |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** |  |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** |  |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** |  |
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRADO (repo archivado) |

</details>

## Licencia

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-forecast-penalty contributors

<p align="center"><sub>Apache-2.0 · Plugin comunitario, no afiliado a DeepSeek.</sub></p>

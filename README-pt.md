# dsh-forecast-penalty — Registo de avaliação da precisão da previsão e verificação aritmética do encargo de avaliação

`dsh-forecast-penalty` lê um registo de avaliação da precisão da previsão —o cabeçalho mais uma linha por período de avaliação— e verifica a completude e a aritmética desse mesmo registo: se o período, o sujeito avaliado e o tipo de mercado estão identificados, se os valores de previsão, valor real e precisão são analisáveis como números, se a precisão registada concorda com a fórmula de definição que você configurar e o encargo de avaliação com a fórmula de cálculo que você configurar, se a moeda está escrita como código de três letras, se não há períodos de avaliação repetidos e se não resta nenhum marcador de modelo na coluna de observações. Toda a verificação que não possa ser executada é reportada em `skipped` com o respetivo motivo.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| O registo não diz que central nem que mercado abrange, e uma linha traz `--` como valor de previsão. | `FP-001` exige que o sujeito avaliado e o tipo de mercado estejam identificados, e `FP-002` que o valor de previsão seja analisável como número, pelo que um `--` é reportado. `FP-001` verifica que ambos estão preenchidos, não que o nome da central seja o correto, e `FP-002` não decide se a previsão foi acertada. |
| A precisão que registo não coincide com a fórmula de definição do meu mercado, e o encargo também não com base vezes tarifa unitária. | `FP-003` compara o valor registado com a fórmula de definição configurada no pacote de regras —a expressão de fábrica é uma convenção comum e um exemplo, não a regra do seu mercado: substitua `expression` ou desative a regra— com uma tolerância de 1,5 pontos. `FP-004` compara o encargo com `考核基数 × 考核单价` com uma tolerância de 0,01; a base é introduzida por você. Nenhuma das duas decide se o método de avaliação é aplicável nem se o encargo deve ser cobrado. |
| A coluna da moeda está vazia em algumas linhas e noutras diz `元`. | `FP-005` exige um código de três letras maiúsculas como CNY ou USD, pelo que tanto a célula vazia como o `元` são reportados; o limite da regra é que avalia apenas o formato e não decide que código a sua instituição deve usar para o renminbi. Também não decide se a moeda escolhida é a correta. |
| O mesmo período de avaliação aparece em mais do que uma linha. | `FP-006` reporta um período repetido, porque a duplicação faz o encargo acumular duas vezes e deixa sem saber se o período foi registado duas vezes ou avaliado duas vezes; a comparação ignora os espaços. Um mesmo período avaliado por faixas horárias e blocos produz legitimamente várias linhas: distinga-as na coluna de observações ou com outro identificador de período, ou desative a regra. Não decide qual das linhas é a duplicada. |
| A coluna de observações ainda contém `【】`, `XXX` ou `TBD`. | `FP-007` reporta a linha quando a coluna de observações contém um dos marcadores configurados no pacote de regras, porque um registo copiado de um modelo leva a supor que a avaliação foi mesmo feita. A lista `terms` é sua para ajustar, e a regra não decide se o texto da observação é verdadeiro. |
| Falta uma coluna inteira no meu material — a regra passa em silêncio? | Não. As regras por coluna (`FP-002`, `FP-005`, `FP-006`, `FP-007`) reportam-se a si mesmas em `skipped` com o motivo de que o material não traz essa coluna, e o relatório distingue esse caso do de uma regra que foi executada e não encontrou nenhuma linha com diferenças. Uma verificação que nunca foi executada não é apresentada como superada. |

## Normas que segue

| Documento | Número | Regras que o citam |
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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-forecast-penalty
dsh --profile <name> --dump-config | grep 'dsh-forecast-penalty'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/forecast-penalty.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-forecast-penalty
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-forecast-penalty contributors.

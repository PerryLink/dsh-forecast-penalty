# dsh-forecast-penalty — 预测准确率考核台账与考核费用算术核对

`dsh-forecast-penalty` 读取一份预测准确率考核台账——表头加每个考核期一行——核对这份台账自身的齐备与算术：考核期、考核对象与市场类型是否写明，预测值、实际值与准确率是否可解析为数值，台账所填准确率是否与贵机构配置的定义式相符、考核费用是否与配置的算式相符，币制是否写成三位字母代码，考核期是否重复，备注栏是否残留未替换的占位符。凡是无法执行的检查，都会在 `skipped` 中逐条说明原因。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 台账没有写考核对象是哪个场站、属于哪个市场，其中一行预测值写的是 `--`。 | `FP-001` 要求写明考核对象与市场类型，`FP-002` 要求预测值能解析为数值，`--` 会被报出。`FP-001` 只核对这两项是否填写，不判断场站名称是否正确；`FP-002` 不判断预测是否准确。 |
| 台账里的准确率与贵市场考核办法的定义式算出来的不一致，考核费用也与基数乘单价对不上。 | `FP-003` 拿台账所填数与规则库配置的定义式相比——出厂式只是一种常见写法、是示例而非贵市场的考核公式，请先把 `expression` 换成贵市场的定义式，或停用本条——容差 1.5 个百分点。`FP-004` 以 0.01 的容差核对 `考核基数 × 考核单价`，考核基数由使用方算出后填入。两条都不判断考核办法适用是否正确、是否应当收取考核费用。 |
| 币制这一栏有的行空着，有的行写的是「元」。 | `FP-005` 要求写成三位大写字母代码（如 CNY、USD），所以留空与写「元」都会被报出；本条的限制是只判断格式，不替贵机构规定人民币该写哪一种，也不判断币制选择是否正确。 |
| 同一个考核期在台账里出现了两行。 | `FP-006` 会报出重复的考核期，因为重复会让费用累计两次，也让人分不清是重复登记还是确有两次考核；比较时忽略空白字符。同一考核期分时段分档考核确实可能产生多行——请在备注栏说明或使用不同的考核期标识，也可以停用本条。它不判断哪一行是重复的。 |
| 备注栏还留着 `【】`、`XXX`、`TBD` 这样的字样。 | `FP-007` 在备注栏命中规则库配置的占位符时逐行报出，因为照抄模板的台账会让人误以为已经核对了实际考核。`terms` 清单可按贵机构模板调整，本条不判断备注内容是否真实。 |
| 材料里整列缺失时，规则会不会静默通过？ | 不会。按列核对的规则（`FP-002`、`FP-005`、`FP-006`、`FP-007`）会在 `skipped` 中自报，并说明材料没有该列；报告把这种情形与「已执行但未发现差异行」分开列出。没有执行过的检查，不会被当成已经过。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
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

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-forecast-penalty
dsh --profile <name> --dump-config | grep 'dsh-forecast-penalty'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/forecast-penalty.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-forecast-penalty
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-forecast-penalty contributors.

# dsh-forecast-penalty — Forecast-accuracy assessment register and assessment-charge arithmetic verification

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-forecast-penalty` reads one forecast-accuracy assessment register — the subject header plus one row per assessment period — and verifies that register's own completeness and arithmetic: that the period, the subject and the market are identified, that the forecast, actual and accuracy figures parse as numbers, that the stored accuracy agrees with the definition formula you configure and the assessment charge with the charge formula you configure, that the currency is written as a three-letter code, that no assessment period repeats, and that no unreplaced placeholder survives in the remark column. Every check that cannot run is reported in `skipped` with its reason.

## Install

```sh
dsh plugin --profile <name> add dsh-forecast-penalty
dsh --profile <name> --dump-config | grep 'dsh-forecast-penalty'
```

## What it looks like

![Terminal demo of dsh-forecast-penalty: real output over its FP-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-forecast-penalty/main/docs/assets/dsh-forecast-penalty-hero.png)

![Animated terminal demo of dsh-forecast-penalty](https://raw.githubusercontent.com/PerryLink/dsh-forecast-penalty/main/docs/assets/dsh-forecast-penalty-demo.gif)

Real output from this plugin over its own `FP-002` test fixture — not a mock-up. The rule pack ships no invented quotations, so a finding names both the clause it applied and the fact that the clause text was not obtained.

## What it answers

| You ask | What it answers |
|---|---|
| The register never says which station or which market it covers, and one forecast figure reads `--`. | `FP-001` requires the subject and the market to be identified, and `FP-002` requires the forecast figure to parse as a number; a `--` is reported. `FP-001` checks that the two are filled in, not that the station name is the right one, and `FP-002` does not decide whether the forecast was accurate. |
| The accuracy I store differs from my own market's definition formula, and the charge differs from base times unit rate. | `FP-003` compares the stored figure with the definition formula configured in the rule pack — the shipped expression is one common convention and an example, not your market's rule, so replace `expression` or disable the rule — with a 1.5-point tolerance. `FP-004` compares the charge with `考核基数 × 考核单价` at a 0.01 tolerance; the base is entered by you. Neither decides whether the assessment method applies or whether a charge should be levied. |
| The currency column is blank on some rows and says `元` on others. | `FP-005` requires a three-letter uppercase code such as CNY or USD, so a blank and a `元` are both reported; the rule's limit is that it judges the format only and does not decide which code your institution should use for the renminbi. It also does not decide whether the currency chosen is the right one. |
| The same assessment period appears on more than one row. | `FP-006` reports a period that repeats, because a duplicate makes the charge accumulate twice and leaves it unclear whether the period was registered twice or assessed twice; the comparison ignores whitespace. One period assessed by time block and band legitimately produces several rows — distinguish those in the remark column or by a different period identifier, or disable the rule. It does not decide which row is the duplicate. |
| The remark column still holds `【】`, `XXX` or `TBD`. | `FP-007` reports the row when the remark column contains one of the placeholders configured in the rule pack, because a register copied from a template invites the reader to assume the assessment was actually carried out. The terms list is yours to adjust, and the rule does not decide whether the remark text is true. |
| A whole column is missing from my material — does the rule quietly pass? | No. The column-level rules (`FP-002`, `FP-005`, `FP-006`, `FP-007`) report themselves under `skipped` with the reason that the material carries no such column, and the report distinguishes that from a rule that ran and found no differing row. A check that never ran is never presented as a pass. |

## Standards it follows

| Document | Number | Cited by rules |
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

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-rc.2`. `engines.dsh` is declared as `>=0.2.1-0 <0.3.0` and is enforced by the host since 0.2.1 |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native` and `ptc`; for a year of periods use `ptc` |

## What it does

Registers the `forecast_penalty` tool. It reads one assessment register — the subject header plus one row per
period — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis |
|---|---|---|---|
| `FP-001` | the register names its subject and market | warn | traceability |
| `FP-002` | the forecast figure parses as a number | warn | arithmetic feasibility |
| `FP-003` | accuracy matches your definition formula | info | local formula |
| `FP-004` | the charge matches your charge formula | info | local formula |
| `FP-005` | the currency is a three-letter code | warn | GB/T 12406 |
| `FP-006` | assessment periods are unique | warn | register uniqueness |
| `FP-007` | the remark column holds no unreplaced placeholder | warn | register integrity |

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/forecast-penalty.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `FP-003` `expression` — the accuracy definition. Ops are `divide`, `product`, `sum`, `subtract` (first field
  minus the rest) and `percent` (first field ÷ second × 100), with an optional `scale` multiplier. `tolerance`
  defaults to 1.5 points; set it to your rounding convention.
- `FP-004` `expression` / `tolerance` — the charge formula, `考核基数 × 考核单价` by default with a 0.01
  tolerance.
- `FP-005` `pattern` — the currency shape; three upper-case letters by default.
- `FP-007` `terms` — the placeholders to look for.

## Material format

The tool accepts JSON or YAML:

```yaml
subject: 某某风电场
market: 省内现货
rows:
  - { 考核期: 2026-03, 预测值: '966', 实际值: '1000', 准确率: '96.60',
      考核门槛: '95', 考核基数: '80', 考核单价: '50', 考核费用: '4000', 币制: CNY }
```

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the register's own
column names are kept, so a finding names the column it read. Numeric cells may carry thousands separators and
a percent sign.

## Rule sources

Rule data lives in `rules/forecast-penalty.yaml`. Because the assessment regime is a market rule rather than a
standard, the pack's `basis` entries say so explicitly instead of citing one; the only external reference is
the currency-code standard, whose excerpt admits the clause text was not obtained. The load-time guard still
requires a document, clause, excerpt and source per rule, and still forbids a locally configured check from
being `error`.

## Troubleshooting

- **`FP-003` fires on every row.** The accuracy figure was computed under a different formula than the one
  configured. Replace `expression` with your market's, or disable the rule — do not widen the tolerance to
  hide a definition mismatch.
- **`FP-004` reports itself as skipped.** The register carries no 考核基数 column, or no charge. The base is
  yours to compute and record; the plugin will not derive it.
- **`FP-005` fires on `元`.** The default pattern wants three upper-case letters. Narrow or widen it to match
  your settlement documents' convention.
- **`FP-006` fires twice on one period.** That can be legitimate for time-block assessment (peak/flat/valley
  rows). Distinguish the rows in the period column or say so in the remark.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-forecast-penalty@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-forecast-penalty   # refresh src/shared from ../_shared
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and
the check engine, and the rule pack declares every check.

## PerryLink DSH Plugin Family

This project is part of the DeepSeek Harness plugin family from [PerryLink](https://github.com/PerryLink). The roster stays collapsed below so every README keeps a short first screen; expand it to see every row and its status.

<details>
<summary>Expand all plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** |  |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** |  |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** |  |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** |  |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** |  |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** |  |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** |  |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** |  |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** |  |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 FROZEN — see the repo README |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 FROZEN — see the repo README |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 FROZEN — see the repo README |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 FROZEN — see the repo README |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 FROZEN — see the repo README |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRED — see the repo README |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRED — see the repo README |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRED — see the repo README |

</details>## License

[Apache License 2.0](LICENSE) © 2026 dsh-forecast-penalty contributors.

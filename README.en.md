<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-forecast-penalty-hero-en-dark.webp">
  <img src="docs/assets/dsh-forecast-penalty-hero-en-light.webp" width="100%" alt="dsh-forecast-penalty banner: left, the plugin name and two value lines; right, above, one real assessment-ledger row (period 2026-03, forecast 966, actual 1000, accuracy 88.00, charge 4000, currency CNY) with the rule that mounts on each column (FP-002, FP-003, FP-004, FP-005, FP-006, FP-007) and FP-001 on the subject and market header; below, the FP-003 finding card — declared 88.00 against the 96.6 the configured formula yields, a gap of 8.6 percentage points beyond the 1.5 tolerance — with a tolerance ruler drawing both on one axis; the report is issues[] 1 · skipped[] 0 and the verdict stays human">
</picture>

# dsh-forecast-penalty

**Check a forecast-accuracy assessment register for completeness and assessment-charge arithmetic — you get a list of which row, which column, and what to fix; the verdict stays with the reviewer.**

A data-only checker plugin for DeepSeek Harness: it reads one forecast-accuracy assessment register (a subject header plus one row per assessment period), applies the versioned rule pack it ships (FP-001..FP-007), and lists only the differences it can point to inside the material — never a compliance verdict, never a liability finding.

[Install](#three-step-setup) · [Configuration](#configuration) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibility)
[![npm](https://img.shields.io/npm/v/dsh-forecast-penalty?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-forecast-penalty)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-forecast-penalty/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-forecast-penalty/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibility)

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

<sub>Community plugin, not affiliated with DeepSeek. Canonical repository: <https://github.com/PerryLink/dsh-forecast-penalty> (Gitee is a mirror).</sub>

## What it is

`dsh-forecast-penalty` reads one forecast-accuracy assessment register — the subject header plus one row per assessment period — and checks that register's own completeness and arithmetic: that the period, the subject and the market are identified, that the forecast, actual and accuracy figures parse as numbers, that the stored accuracy agrees with the definition formula you configure and the assessment charge with the charge formula you configure, that the currency is written as a three-letter code, that no assessment period repeats, and that no unreplaced placeholder survives in the remark column. Every check that cannot run is reported in `skipped` with its reason.

It does not decide whether the assessment method applies, whether accuracy passes, or whether a charge should be levied or waived.

- **Who it is for**: contract and settlement staff; no command line required — hand the material over in chat.
- **What you give it**: the source material the check works on (a table, register or document); the original is never modified. Excel can be converted to JSON/YAML first, in chat if the platform supports it.
- **What you get back**: a list of "which row, which column, what is missing, how to fix it"; every check that could not run is listed in `skipped` with its reason.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-forecast-penalty-flow-v5-dark.svg">
  <img src="docs/assets/dsh-forecast-penalty-flow-v5-light.svg" width="100%" alt="dsh-forecast-penalty structure (rule scoreboard): two inputs at the top — the material via parseMaterial, 1 row and 12 canonical columns, and the seven-rule pack rules/forecast-penalty.yaml v2026.1 filtered by only/disabled first; the scoring panel below gives, per rule, the field, the check kind, the basis kind to severity cap and this run's disposition: FP-003 draws the declared 88.00 against the expected 96.6 (±1.5 pp) on one tolerance ruler, FP-004 reconciles 80 × 50 = 4000 with the declared 4000 (tolerance 0.01), and the other five execute with 0 differences; two exits at the bottom: issues[] with one located finding (FP-003, row 1, accuracy, info) and skipped[] empty for this run, naming the reasons a rule can land there; the verdict stays with the reviewer">
</picture>

## Three-step setup

1. **Install** (pick one channel):

   ```sh
   # git channel (latest main; equivalent to git+https://github.com/PerryLink/dsh-forecast-penalty.git)
   dsh plugin --profile <name> add github:PerryLink/dsh-forecast-penalty
   # npm channel (published releases)
   dsh plugin --profile <name> add dsh-forecast-penalty
   # tarball channel: pnpm pack in this repo, then
   dsh plugin --profile <name> add ./dsh-forecast-penalty-<version>.tgz
   ```

2. **Minimal config** (sane defaults; a bundle row without `config` uses every default, with the rule-pack path pointing at the bundled `rules/forecast-penalty.yaml`):

   ```yaml
   - insert:
       - id: dsh-forecast-penalty
         name: dsh-forecast-penalty
   ```

3. **Verify it mounts**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-forecast-penalty'
   ```

   Then hand it a register — for example the bundled sample (expected output in `samples/quickstart/expected/result.json`):

   ```text
   > Run this check on the bundled sample and tell me how many issues it found and their severities.
   forecast_penalty: 1 issue(s) — warn 1 (FP-001); skipped: 0
   ```

**Uninstall**: `dsh plugin --profile <name> remove dsh-forecast-penalty` (or remove the row from the profile patch).

<details>
<summary>Use it in WorkBuddy / Coze</summary>

Search "Professional Document Check Suite" in WorkBuddy / Coze (the full set; this check is one part of it; availability as listed) to call the same checking capability without a command line.

</details>

<details>
<summary>Install from the DSH Desktop market</summary>

Every PerryLink plugin is listed in the built-in DSH Desktop market: **Market → Sources → Add source → paste** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ select**. Installation still requires the market's npm identity check and your confirmation.

</details>

## Core capabilities

`dsh-forecast-penalty` registers the `forecast_penalty` tool: it reads one assessment register, applies a versioned rule pack, and returns a report.

- **Seven rules in one data pack** — the rule pack is data, not code (`rules/forecast-penalty.yaml`); replacing it switches the whole rule set without touching a line of TypeScript.
- **Read-only on the material** — accepts JSON or YAML and never modifies the original; pure ESM, no network requests, no model calls.
- **No fabricated citations** — every rule carries `document` / `number` / `clause` / `excerpt` / `kind` / `source`; `excerpt` must be a verbatim quotation, and rules whose clause text could not be obtained this pass say so in the `excerpt` itself and stay marked `derived-from-principle`.
- **Severity follows the evidence** — `derived-from-principle` is capped at `warn`, institutional configuration (`institutional-configuration`) at `info`, and a test asserts it.
- **An empty issue list is never "nothing is wrong"** — every check that could not run is reported in `skipped` with its reason; a column-level rule that finds its column missing reports itself in `skipped` rather than passing silently.
- **No adjudicating wording** — the report lists differences and never pronounces on compliance, liability, or correctness; a wording guard enforces this and every report carries the disclaimer.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `FP-001` | the register names its subject and market | warn | traceability |
| `FP-002` | the forecast figure parses as a number | warn | arithmetic feasibility |
| `FP-003` | accuracy matches your definition formula | info | local formula |
| `FP-004` | the charge matches your charge formula | info | local formula |
| `FP-005` | the currency is a three-letter code | warn | GB/T 12406 |
| `FP-006` | assessment periods are unique | warn | register uniqueness |
| `FP-007` | the remark column holds no unreplaced placeholder | warn | register integrity |

### Examples

These are the plugin's real entry points; install once, then call one.

**Detailed example** — tool `forecast_penalty`, input:

```json
{"rows":[{"考核期":"2026-03","预测值":"待补","实际值":"1000"}]}
```

Output:

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

### What you ask

| You ask | What it answers |
|---|---|
| The register never says which station or which market it covers, and one forecast figure reads `--`. | `FP-001` requires the subject and the market to be identified, and `FP-002` requires the forecast figure to parse as a number; a `--` is reported. `FP-001` checks that the two are filled in, not that the station name is the right one, and `FP-002` does not decide whether the forecast was accurate. |
| The accuracy I store differs from my own market's definition formula, and the charge differs from base times unit rate. | `FP-003` compares the stored figure with the definition formula configured in the rule pack — the shipped expression is one common convention and an example, not your market's rule, so replace `expression` or disable the rule — with a 1.5-point tolerance. `FP-004` compares the charge with `penaltyBase × penaltyRate` at a 0.01 tolerance; the base is entered by you. Neither decides whether the assessment method applies or whether a charge should be levied. |
| The currency column is blank on some rows and says the local unit on others. | `FP-005` requires a three-letter uppercase code such as CNY or USD, so a blank and a local-unit word are both reported; the rule's limit is that it judges the format only and does not decide which code your institution should use for the renminbi. It also does not decide whether the currency chosen is the right one. |
| The same assessment period appears on more than one row. | `FP-006` reports a period that repeats, because a duplicate makes the charge accumulate twice and leaves it unclear whether the period was registered twice or assessed twice; the comparison ignores whitespace. One period assessed by time block and band legitimately produces several rows — distinguish those in the remark column or by a different period identifier, or disable the rule. It does not decide which row is the duplicate. |
| The remark column still holds template placeholders such as empty brackets, `XXX` or `TBD`. | `FP-007` reports the row when the remark column contains one of the placeholders configured in the rule pack, because a register copied from a template invites the reader to assume the assessment was actually carried out. The `terms` list is yours to adjust, and the rule does not decide whether the remark text is true. |
| A whole column is missing from my material — does the rule quietly pass? | No. The column-level rules (`FP-002`, `FP-005`, `FP-006`, `FP-007`) report themselves under `skipped` with the reason that the material carries no such column, and the report distinguishes that from a rule that ran and found no differing row. A check that never ran is never presented as a pass. |

## Standards it follows

| Document | Number | Cited by rules |
|---|---|---|
| Power market assessment measures and grid-connection dispatch agreement (no national standard; the canonical Chinese title lives in `rules/forecast-penalty.yaml`) | No unified standard (the basis is register traceability) | FP-001 |
| Power market assessment measures and grid-connection dispatch agreement (no national standard) | No unified standard (the basis is arithmetic feasibility) | FP-002 |
| Power market assessment measures and grid-connection dispatch agreement (no national standard) | No unified standard (the basis is the institution's configured accuracy formula) | FP-003 |
| Power market assessment measures and grid-connection dispatch agreement (no national standard) | No unified standard (the basis is the institution's configured charge formula) | FP-004 |
| Codes for the representation of currencies (canonical Chinese title lives in `rules/forecast-penalty.yaml`) | GB/T 12406—2022 (Codes for the representation of currencies; issued and effective 2022-12-30; fully replaces GB/T 12406—2008, whose title included "funds"; modified adoption of ISO 4217:2015, not identical; clause number not obtained this pass) | FP-005 |
| Power market assessment measures and grid-connection dispatch agreement (no national standard) | No unified standard (the basis is register uniqueness) | FP-006 |
| Power market assessment measures and grid-connection dispatch agreement (no national standard) | No unified standard (the basis is register integrity) | FP-007 |

**Boundary:** this plugin checks a **forecast-accuracy assessment register** for arithmetic — that the period and subject are identified, that forecast and actual figures parse, that the accuracy figure matches the definition formula you configure, that the assessment charge matches your charge formula, that the currency follows its format, that periods do not repeat, and that no placeholder survives. It does **not** decide whether a charge should be levied, whether accuracy passes, or whether a waiver or appeal applies. **Those depend on the market rules, the exemption cases and the dispute procedure.**

> ### ⚠️ This is a market rule, not a national standard — and the pack says so
>
> The accuracy definition, the exemption threshold, the unit rate and the settlement basis are set by **each power market's assessment rules and the grid-connection dispatch agreement**. Provinces differ sharply (some use `1 − deviation`, some use root-mean-square error, some assess by time block and band), and **no unified national standard exists**. So this pack does not fabricate a standard number: every rule's `excerpt` states plainly that its basis is arithmetic self-consistency or a locally configured convention and that **no citable clause exists**.
>
> **Two formulas ship as examples, and both are marked as such:**
>
> - `FP-003` **accuracy** defaults to `forecast ÷ actual × 100` with a 1.5-point tolerance. That is **one common convention, not any market's rule**. Before use, replace `expression` with the formula from your market's rules — or disable the rule. The note spells this out.
> - `FP-004` **charge** checks `charge = penaltyBase × penaltyRate`. The base is **entered by you** after working it out under your market's rules, because the threshold, the bands and the volume basis are the market's business and this plugin will not derive them. No unit rate is built in anywhere.
>
> A consequence worth knowing: the accuracy rule ships at `info` severity precisely because its formula is a deployment choice rather than a verified requirement.

## Configuration

All tunables are Schemastery `Config` fields in `src/config.ts` (changeable from cordis.yml); the per-rule thresholds live in the rule pack under `rules/`. An id-targeted override replaces the whole row — restate every key you need.

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/forecast-penalty.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `FP-003` `expression` — the accuracy definition. `op` supports `divide`, `product`, `sum`, `subtract` (first field minus the rest) and `percent` (first field ÷ second × 100), with an optional `scale` multiplier. `tolerance` defaults to 1.5 points; set it to your rounding convention.
- `FP-004` `expression` / `tolerance` — the charge formula, `penaltyBase × penaltyRate` by default with a 0.01 tolerance.
- `FP-005` `pattern` — the currency shape; three upper-case letters by default.
- `FP-007` `terms` — the placeholders to look for.

Example override in your profile patch:

```yaml
- insert:
    - id: dsh-forecast-penalty
      name: dsh-forecast-penalty
      config:
        disabledRules: [FP-005]
        timeoutMs: 180000
```

## Material format

The tool accepts JSON or YAML:

```yaml
subject: 某某风电场
market: 省内现货
rows:
  - { 考核期: 2026-03, 预测值: '966', 实际值: '1000', 准确率: '96.60',
      考核门槛: '95', 考核基数: '80', 考核单价: '50', 考核费用: '4000', 币制: CNY }
```

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the register's own column names are kept, so a finding names the column it read. Numeric cells may carry thousands separators and a percent sign. Fields are optional at the reader layer and validated by the check engine, so a partially exported register produces "missing item" findings instead of a crash.

## Rule sources

Rule data lives in `rules/forecast-penalty.yaml`, separated from the code: every rule carries document, number, clause in the source's own numbering, a verbatim excerpt, and a source URL. Because the assessment regime is a market rule rather than a standard, the pack's `basis` entries say so explicitly instead of citing a clause that does not exist; the only external reference is the currency-code standard, whose excerpt admits the clause text was not obtained.

The load-time guard still requires a document, clause, excerpt and source per rule, and still forbids a locally configured check from being `error`. `scripts/check-citations.mjs` and `rules/citations-baseline.json` record the citations that remain untraceable this pass: a new untraceable excerpt fails the gate, and so does a baseline entry that has become traceable, so the baseline can only shrink. A pack that overstates its basis fails at load time instead of producing a confident-looking report.

## FAQ

<details>
<summary>Does it decide compliance for us?</summary>

No. It lists only the differences it can point to inside the material (which row, which column, what is missing, how to fix it) and decides neither facts nor compliance — the conclusion always stays with the reviewer. A wording guard enforces the report's wording, and every report carries the disclaimer. It likewise does not decide whether accuracy passes or whether a charge should be levied or waived.

</details>

<details>
<summary>Is the material uploaded or kept anywhere else?</summary>

No. This is an offline checker: it reads only the material you hand the tool, makes no network requests, calls no model, and ships no telemetry, analytics, or background reporting. It writes no data outside the tool result and the DSH host's own session/log storage; that storage and its retention are controlled by the host, and this package does not add a second copy.

</details>

<details>
<summary>Can an empty `issues` list be read as "nothing is wrong"?</summary>

No. Every check that could not run is listed in `skipped` with its reason (a material missing a column, a rule stopped by `disabledRules`). The column-level rules (`FP-002`, `FP-005`, `FP-006`, `FP-007`) report themselves in `skipped` when their column is absent instead of pretending to pass. Read `issues` and `skipped` together before drawing any conclusion from a report.

</details>

<details>
<summary>Can the two bundled formulas be used as our market's rule?</summary>

Not as-is. The `FP-003` accuracy formula and the `FP-004` charge formula are both **examples**: the first is a common convention, and the second has you enter the assessment base after working it out under your market's rules, with no unit rate built in. Replace `expression` with your institution's convention before use, or disable the rule; `FP-003` ships at `info` precisely because its formula is a deployment choice.

</details>

<details>
<summary>Will it cope with a whole quarter of periods at once?</summary>

The tool works in both `native` and `ptc` modes; for batch work (a quarter of periods or a whole directory) use `ptc`, where the schema cost is paid once. The checks themselves are local column matching and arithmetic — no network requests, no model calls; `timeoutMs` (default 120 s) is the cooperative timeout budget.

</details>

## Troubleshooting

- **`FP-003` fires on every row.** The accuracy figure was computed under a different formula than the one configured. Replace `expression` with your market's, or disable the rule — do not widen the tolerance to hide a definition mismatch.
- **`FP-004` reports itself as skipped.** The register carries no assessment-base column, or no charge. The base is yours to compute and record; the plugin will not derive it.
- **`FP-005` fires on the local currency word.** The default pattern wants three upper-case letters. Narrow or widen it to match your settlement documents' convention.
- **`FP-006` fires twice on one period.** That can be legitimate for time-block assessment (peak/flat/valley rows). Distinguish the rows in the period column or say so in the remark.
- **A rule never ran.** Check the `skipped` array; it names the rule id and the reason.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if your runtime sits outside it, grant an explicit exemption: `dsh plugin --profile <name> allow-version dsh-forecast-penalty@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.
- **Times look shifted.** All arithmetic is wall-clock on the input strings, with no timezone conversion.

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-rc.2`. `engines.dsh` is declared as `>=0.2.1-0 <0.3.0` and is enforced by the host since 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native` and `ptc`; for a whole quarter use `ptc` |

## Ecosystem & quality

- [Gitee mirror](https://gitee.com/perrylink/dsh-forecast-penalty) (sync mirror; GitHub is canonical)
- [dshfind plugin page](https://dshfind.com/plugins/PerryLink/dsh-forecast-penalty) (installs and ranking)
- [OpenSSF Scorecard report](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-forecast-penalty) (driven by [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listed)
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile <name> add dsh-forecast-penalty` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking)
- [Ecosystem knowledge base](https://perrylink.github.io/dsh-plugin-guide/) — plugin development guide · measured selection data · maintenance criteria

## Development

```sh
pnpm install                                        # node ^22.19 || >=24
pnpm run typecheck                                  # tsc --noEmit
pnpm test                                           # vitest: shared table-plugin suite + paired fixtures
pnpm run build                                      # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run verify:self-contained                      # dependency specs resolve from the registry
pnpm run check:lockfile                             # lockfile drift check
pnpm run check:readmes                              # five-language README consistency
pnpm run check:citations                            # rule-pack citation baseline
node ../scripts/sync-shared.mjs dsh-forecast-penalty   # refresh src/shared from ../_shared
pnpm pack                                           # the published tarball
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and the check engine, and the rule pack declares every check. Local sample run (needs `pnpm run build` first to produce `lib/`):

```sh
node samples/quickstart/run.mjs --json
# => {"tool":"forecast_penalty","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":0}
```

The sample input lives in `samples/quickstart/input/`, the expected output in `samples/quickstart/expected/result.json`, and a screenshot in `docs/assets/quickstart.png`. The README images are generated programmatically by [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow) and are safe to re-run; the older single-skin flow diagram and demo images stay in `docs/assets/` for external deep links, while the READMEs reference only the new light/dark pair.

Topics: `deepseek-harness`, `dsh`, `dsh-plugin`, `cordis`, `forecast`, `penalty`

## Family & thanks

This project is part of the DeepSeek Harness plugin family from [PerryLink](https://github.com/PerryLink) (all Apache-2.0). Full family index: [choose a checker by material](https://perrylink.github.io/zh/checkers/choose/) and [all plugins](https://github.com/PerryLink). If it is useful, **a star helps the next person find it** — nothing is gated behind it.

- [@PerryLink](https://github.com/PerryLink) — creator and maintainer: the data-only rule pack (FP-001..FP-007), the `forecast_penalty` tool, the market-rule basis notes, and the five-language docs.

<details>
<summary>Expand all plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 FROZEN — see the repo README |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 FROZEN — see the repo README |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRED (repo archived) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRED (repo archived) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRED (repo archived) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRED (repo archived) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 FROZEN — see the repo README |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 FROZEN — see the repo README |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 FROZEN — see the repo README |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 FROZEN — see the repo README |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 FROZEN — see the repo README |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRED (repo archived) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRED (repo archived) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRED (repo archived) |

</details>

## License

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-forecast-penalty contributors

<p align="center"><sub>Apache-2.0 · Community plugin, not affiliated with DeepSeek.</sub></p>

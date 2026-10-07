# dsh-forecast-penalty

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
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a year of periods use `ptc` |

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

## Install

```sh
pnpm pack
dsh plugin --profile <name> add ./dsh-forecast-penalty-0.1.0.tgz
dsh --profile <name> --dump-config | grep 'dsh-forecast-penalty'
```

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

## License

[Apache License 2.0](LICENSE) © 2026 dsh-forecast-penalty contributors.

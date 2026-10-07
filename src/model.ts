/**
 * dsh-forecast-penalty — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'forecast_penalty'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  period: ['考核期', '期间', '月份', 'period'],
  forecastAt: ['预测日期', '预测时间', '申报日期', 'forecastAt'],
  forecastValue: ['预测值', '预测电量', '申报电量', 'forecastValue'],
  actualValue: ['实际值', '实际电量', '实际完成', 'actualValue'],
  unit: ['单位', '计量单位', 'unit'],
  accuracy: ['准确率', '预测准确率', '偏差率', 'accuracy'],
  threshold: ['考核门槛', '免考核门槛', '允许偏差', 'threshold'],
  penaltyRate: ['考核单价', '罚则单价', '考核标准', 'penaltyRate'],
  /**
   * The quantity the assessment charge is levied on.
   *
   * Deliberately not named for any one market: the base may be the shortfall
   * quantity, the settlement volume or a per-unit figure, and which one applies is
   * the market rule's business. The rule pack compares the charge against this times
   * the unit rate.
   */
  penaltyBase: ['考核基数', '考核电量', '计费基数', 'penaltyBase'],
  penalty: ['考核费用', '考核金额', '罚款金额', 'penalty'],
  currency: ['币制', '币种', 'currency'],
  note: ['备注', '说明', 'note', 'remark'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'periods', '考核期'],
  columns: COLUMNS,
  header: {
  subject: ['subject', '考核对象', '场站名称', '机组名称'],
  market: ['market', '市场类型', '交易品种'],
  ruleVersion: ['ruleVersion', '规则版本', '考核办法版本'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '考核期',
  'period',
  '预测值',
  'forecastValue',
  '实际值',
  'actualValue',
  '准确率',
  'accuracy',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }

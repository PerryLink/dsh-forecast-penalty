import { describeTablePlugin } from './table-plugin-suite.ts'
import { Config } from '../src/config.ts'
import { parseMaterial, runCheck, SPEC } from '../src/model.ts'
import { buildView } from '../src/view.ts'
import { inject, name, resolvePackageFile, TOOL_NAME } from '../src/index.ts'

describeTablePlugin({
  name,
  inject,
  TOOL_NAME,
  resolvePackageFile,
  Config,
  rulesFile: 'rules/forecast-penalty.yaml',
  parseMaterial,
  runCheck,
  buildView,
  columnNames: SPEC.columns,
  samples: {
    good: {
      subject: '某某风电场',
      market: '省内现货',
      rows: [
        {
          考核期: '2026-03',
          预测值: '966',
          实际值: '1000',
          准确率: '96.60',
          考核门槛: '95',
          考核基数: '80',
          考核单价: '50',
          考核费用: '4000',
          币制: 'CNY',
        },
      ],
    },
    unknownColumn: { rows: [{ 备注: '甲' }] },
  },
})

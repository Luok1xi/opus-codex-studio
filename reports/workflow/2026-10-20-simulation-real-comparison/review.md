# 2026-10-20-simulation-real-comparison 工作流复盘

完善现有小车仿真：本机导入实车S记录、同单位同时间对照，修正已确认的帧龄与退化拟合错误，并增加实际源码物理测试。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：Single shared website + per-project TeamHub + bounded native workers; workflow tool afe97f6d491815e0dfc552e713a1b489b20ee63b0fd8ddb951762aab69dbea95
- 验收状态：passed
- 开始：2026-10-20T07:37:53.781000+00:00
- 测量截止：2026-10-20T08:02:31.483000+00:00
- 墙钟秒数：1477.702
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| 观察窗口 | 1477.702 | seconds | 首次记录至功能验收截止；包括协调和部分复盘准备，不当成纯编码时间。 |
| 原生工作者 | 3 | workers | 输入契约/模型、外部物理研究、浏览器/数据模块三份明确范围；根代理集成。 |
| 新增外部模型调用 | 0 | calls | 向现有Opus数据库交接；原生工作者不是Opus。 |
| 物理研究窗口 | 406.112 | seconds | 该工作者有计时证据；不能与父任务墙钟相加。 |
| 浏览器验收后功能返工 | 1 | cycles | 首次版本存在输入失焦移动按钮，修复后重跑原鼠标路径。 |
| 全部工具失败数量 | 未知 | calls | 未可靠全量计数；已知CLI参数/输出结构错误和网页抓取失败逐项记观察。 |
| 复盘与归档自身净开销 | 未知 | seconds | 与浏览器验证并行，未能可靠拆分；归档阶段窗口另记回执。 |
| 实际token | 未知 | tokens | 无同口径提供方usage。 |
| 实际费用 | 未知 | currency | 无账单。 |

## 验收条件

- 接入现有网站和回放，真实采样时间/单位一致，错误输入明确拒绝，不操作设备。
- 导入、指标、导出、失败重试和手机布局经浏览器验证。
- 物理修复先复现原故障，使用实际源码回归，正常场景不变。

## 已完成

- 六信号本地导入、缺样保留、可见偏移、重叠时间统计、文件指纹及报告导出。
- 12项解析/对照测试、6组66项原回放指标与浏览器验收通过。
- 修复3项既有回放问题，并修复独立验收新发现的输入失焦导致点击落空。
- 实际源码帧龄边界回归、16次CLI、20项拟合检查、9项物理不变量通过。
- 既有网站重新构建；两个离线修复按原文件hash核对后集成。

## 未完成

- 无记录

## 收益与损耗观察

- 局部质量收益有证据：两人按实际DMA调用链确认帧龄错误；独立浏览器验收发现自动单测遗漏的真实鼠标问题。
- 没有相同任务/环境/验收的对照工作流，不能宣称净提效或节省比例。
- 三个工作者分工复用结果；输入契约由一人查清，另一人实现纯解析，根代理只实现页面集成。
- TeamHub categories/get参数与inbox输出结构猜测造成可避免的失败；先查一次help并保留结构化用法更省。
- GitHub网页抓取失败后用已连接的GitHub读取固定版本源码；未无限重试。
- 本轮保留CRLF、原文件hash和冻结回放，未覆盖并行生产固件；新功能首次浏览器验收未全过，已如实保留失败证据。
- 文件手动交接不等于Opus已接受；本轮没有收到新的Opus确认。

## 修改建议及下一轮验收

- **SIM-20261020-CONTRACT-FIRST [adopted]** 实车对照先固定采样时间、符号、缩放、字段来源；未经采集的字段显示缺失。；负责人：codex；下次检查：收到首份真实S记录后复核固件hash和单位，不能用模拟fixture代替。
- **SIM-20261020-BROWSER-BLUR [adopted]** 时间偏移在输入时更新，避免失焦改变按钮布局；浏览器验收保留普通鼠标和键盘各自证据。；负责人：codex；下次检查：下一次表单修改后连续点击不丢失，非法输入不恢复导出。
- **SIM-20261020-CLI-SCHEMA [proposed]** TeamHub常用命令先核对help及返回形状，记录在现有工具说明，减少参数和JSON结构猜测。；负责人：codex；下次检查：下一轮 get/categories/inbox 不发生同类参数错误，不为此新建一套CLI。
- **SIM-20261020-HOLDOUT [proposed]** 由实车操作方提供独立运行记录和工况，留出一整次运行验收；未校准前不自动改PID或换默认物理模型。；负责人：opus；下次检查：收到本人回执及真实记录，报告训练/验收分离和测量缺项。

## 证据

- evidence.json：脱敏聚合结果、公开来源和本地证据哈希。

## 限制

- Synthetic format fixtures are not physical measurements.
- No real dynamic S log, trajectory, voltage or suction calibration was available.
- Production firmware, serial ports and flashing were not touched.
- Offline simulator sources updated; existing default binary and historical web replay data not overwritten.
- No public website deployment or project-source upload.
- Opus新验收未收到；完整用量与成本未知。

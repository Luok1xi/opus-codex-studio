# 2026-11-12-visual-measurement09 工作流复盘

核查用户提出的三项视觉测量链缺陷；用实际C区分配对与预瞄、空间与时间滤波、保持与失效，提出分项修正策略。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + frozen-source probes + independent bounded geometry/control audits
- 验收状态：passed
- 开始：2026-11-12T06:47:14+00:00
- 测量截止：2026-11-12T07:08:39.737198+00:00
- 墙钟秒数：1285.737198
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Round wall clock to report cutoff | 1285.737 | seconds | UTC start to cutoff, includes coordination and read-only probes; excludes later remote verification. |
| Native contributors | 3 | agents | Geometry audit, control probes, bounded test plan; root consolidated. |
| Geometry actual C calls | 60 | calls | 10 grayscale inputs x2 modes x3 warmup frames. |
| Control diagnostic cases | 25 | cases | Signal/phase/filter combinations in saved real-C probe. |
| Production edits and target builds | 0 | operations | Frozen inputs and HEX reverified unchanged; variants live only in diagnostic harness. |
| Hardware operations | 0 | operations | No serial, flash or launch. |
| External model dispatch | 0 | calls | Native agents only. |
| Tokens | 未知 | tokens | No scoped usage evidence. |
| Cost | 未知 | currency | No billing evidence. |
| Review archive overhead | 未知 | seconds | Review overlaps task; remote verification occurs after cutoff. |

## 验收条件

- 逐项区分源码事实、可复现机制和未证明的实车因果。
- 使用冻结代码实际C回放与滤波诊断变体，不以未烧录版冒充现车。
- 保留原固件，记录限制和前轮参数文字更正。

## 已完成

- 10张灰度、60次实际六单元C调用，定位同带配对与预瞄跳变两个独立问题。
- 25组控制信号/相位/滤波变体，保持边界与cross失效检查；ASan/UBSan清洁。
- 跟踪真实include/init/参数写入链，确认250限幅和启动增益，纠正旧报告默认来源。
- 冻结08全部输入与HEX未改；没有串口、烧录或新固件。

## 未完成

- 无记录

## 收益与损耗观察

- Initial hypotheses were tested rather than simply affirmed: same-row pairing alone failed and corner-jump targets were on the correct outgoing band.
- A30px step saturated all variants, hiding delay. It was retained and supplemented with an unsaturated4px step and phase check.
- Local default macro inspection initially suggested no yaw cap; full include chain corrected that preliminary hypothesis before final conclusions.
- Previous report misidentified config values as startup gains. Actual assignment and override paths were traced and a separate correction recorded without rewriting frozen evidence.
- The bounded inbox returned historical handoffs; they were not treated as current runtime authorization or live hardware state.
- No matched workflow baseline exists; reduced synthetic signal variation is not an efficiency or physical stability claim.

## 修改建议及下一轮验收

- **ACTIVE-ASSIGNMENT-CHAIN [adopted]** 参数报告必须从启动赋值、宏include、运行写入口追到最终消费者，不能只读参数表。；负责人：codex；下次检查：下次生成固件摘要时对照实际初始化与无线回读口径。
- **UNSATURATED-FILTER-COMPARISON [adopted]** 滤波对照同时保留未饱和小阶跃、噪声和饱和大阶跃，分别记录P延迟与D尾。；负责人：codex；下次检查：后续候选不能以限幅后的首拍到位宣称没有时延。
- **GEOMETRY-CAUSE-SEPARATION [adopted]** 将白带配错、跨截面和预瞄位置跳变作为不同机制验证。；负责人：codex；下次检查：几何修改同时覆盖横向直角和同行双白带反例。

## 证据

- evidence.json

## 限制

- No current vehicle firmware identity, runtime parameter readback or physical telemetry captured.
- Synthetic input/output probes, not closed-loop vehicle acceptance or a new deployable firmware.
- Hypotheses about latest physical run remain unproven; no speedup claim.

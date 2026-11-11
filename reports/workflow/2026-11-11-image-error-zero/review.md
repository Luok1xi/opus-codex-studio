# 2026-11-11-image-error-zero 工作流复盘

直接诊断前方直角存在但图像偏差很小直到丢线，明确观测盲区与无效零值，给出修复边界。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + current source identity + bounded telemetry evidence
- 验收状态：passed
- 开始：2026-11-11T14:27:44+00:00
- 测量截止：2026-11-11T14:36:15.471091+00:00
- 墙钟秒数：511.471091
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native contributors | 2 | agents | Bounded identity recovery and independent actual-function checks. |
| Owner questions | 1 | questions | Distinguished approaching-straight from already-turning observation; no repeat drive requested. |
| Hardware changes | 0 | operations | No serial, flash or runtime writes. |
| External dispatch | 0 | calls | No DSH or Opus handoff. |
| Usage | 未知 | tokens | No scoped provider usage. |
| Cost | 未知 | currency | No billing evidence. |
| Review overhead | 未知 | seconds | Not separately measured; final archive after cutoff. |

## 验收条件

- 绑定最新完整记录的实际参数及最后烧录来源，不沿用下午候选。
- 用实际函数区分有效零、保持旧值和无效零。
- 明确解决方案与未验证范围，不越权改车。

## 已完成

- 16项原函数测试通过；6项输入与当前目标回执匹配。
- 核实直角接管关闭、局部采样窗盲区、失效100ms后替代零。
- 发现重复导出的旧记录曾贴新参数标签，按时间与hash区分。
- Owner确认前方弯时仍直走，报告提供最小视觉与交接修复顺序。

## 未完成

- 无记录

## 收益与损耗观察

- An actual five-hour firmware/config change made the earlier same-day candidate stale; refreshed identity before concluding.
- The GUI zero value is ambiguous without validity/age; original C reproduced both legitimate and missing-data zeros.
- Bounded extraction excluded reasoning and did not execute recovered commands.
- The inbox query again returned oldest historical bodies; no old hardware statement was used as current evidence.

## 修改建议及下一轮验收

- **IMAGE-VALIDITY [proposed]** 下一轮实现将新鲜、保持、无效分开记录和显示，缺失图像不要画成居中。；负责人：codex；下次检查：同一固定图像序列验证零值与失效在图上可区分。
- **CAPTURE-IDENTITY [adopted]** 新运行参数只绑定新记录；同hash的手动导出仍归原试跑。；负责人：codex；下次检查：相邻K参数比较必须同时核cap hash和实际回读。

## 证据

- evidence.json

## 限制

- 没有同步现场原图，不能证明每一帧爬线失败细节。
- 本轮提供定位与解决方案，未实现或烧录视觉修复。
- 无同条件效率基线，不宣称提速。

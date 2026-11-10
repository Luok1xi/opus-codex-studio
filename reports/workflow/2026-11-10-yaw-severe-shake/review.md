# 2026-11-10-yaw-severe-shake 工作流复盘

Separate recurring oscillation, intermittent feedback bursts and actuator saturation in saved controller tests.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-11-10T20:36:48+08:00
- 测量截止：2026-11-10T20:40:31.7966645+08:00
- 墙钟秒数：223.796664
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Actual model usage | 未知 | tokens | Provider usage unavailable |
| Independent reviewers | 2 | agents | Separate firmware and record reviews |
| Physical operations | 0 | operations | Saved data analysis only |
| Coordination and review overhead | 未知 | seconds | Not separately metered |

## 验收条件

- Validate current run metadata and match frozen source
- Quantify the distinct signatures and their diagnostic limits

## 已完成

- Recomputed key windows and validated a synchronized comparison chart
- Reviewed controller and acquisition paths independently
- Included a newly saved comparison at the analysis cutoff

## 未完成

- 无记录

## 收益与损耗观察

- The same displayed build name identified two different profiles, so matching the saved profile to frozen source and the flash path prevented a mistaken comparison.
- Comparing constant wheel commands, feedback, and actuator limits separated recurring roughness from a transient spike. A newly saved contrasting record materially affected the diagnostic confidence.

## 修改建议及下一轮验收


## 证据

- Local controller source, flash receipt and saved captures
- Local synchronized plot and independent cross-check

## 限制

- No new physical diagnostic performed
- Decimated measurements cannot establish raw-signal ordering
- No matched workflow baseline

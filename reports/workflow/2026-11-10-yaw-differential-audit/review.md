# 2026-11-10-yaw-differential-audit 工作流复盘

Audit wheel differential, measured angular rate, and the most recent unstable control run.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-11-10T15:37:51+08:00
- 测量截止：2026-11-10T15:41:00.9564204+08:00
- 墙钟秒数：189.95642
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Actual model usage | 未知 | tokens | Provider usage unavailable |
| Complete recordings independently audited | 3 | runs | Sample index and closing record verified |
| Independent reviewers | 1 | agent | Read-only source and capture cross-check |
| Physical operations | 0 | operations | Saved evidence only |
| Coordination and review overhead | 未知 | seconds | Not separately metered |

## 验收条件

- Check recorded field mapping and scale, differential signs, and gain encoding
- Separate display errors from actual tracking and physical calibration

## 已完成

- Recomputed three complete recordings from their board field layout
- Found a second mismatch between reported configuration and the actual phase target
- Verified signed targets and measured wheel difference, counted sample clipping, and rendered a side-by-side comparison

## 未完成

- 无记录

## 收益与损耗观察

- A current-phase target and a stored configuration are different signals. Verifying the wire fields against their assignments avoids treating one as the other.
- Measured and commanded differential traces separate channel-sign concerns from controller output clipping.

## 修改建议及下一轮验收


## 证据

- Board source, three complete saved captures and visually checked comparison

## 限制

- Gyroscope absolute physical scale and wheel slip were not independently measured
- No matched workflow baseline

# 2026-11-10-brushed125-dsh-frame 工作流复盘

Use existing real camera captures and the measured height to separate launch failure from first-corner recognition.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-11-10T23:17:37+08:00
- 测量截止：2026-11-10T23:22:15+08:00
- 墙钟秒数：278.0
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Validated historical camera payloads | 4 | frames | Header, full payload, terminator and local hash |
| Synthetic controls | 2 | frames | Reused prior idealized controls at both heights |
| Independent evidence inspections | 1 | agents | Native subagent located the comparable archived incident |
| Actual model usage | 未知 | tokens | Provider usage unavailable |
| Review overhead | 未知 | seconds | Not separately measured |

## 验收条件

- Validate archived raw payloads
- Compare both calibrated-height assumptions in the frozen matcher
- Replay the reported pre-corner view separately from the verified launch view

## 已完成

- Verified four complete recorded camera payloads
- Reproduced the historical launch rejection in identical navigation sources
- Applied the reported distance at plausible map poses and independently replayed the original image-line branch

## 未完成

- 无记录

## 收益与损耗观察

- The correction supplied by the operator changed the interpretation of the pre-corner frame; the historical launch frame was kept independent.
- Correcting only camera height did not meet the historical launch threshold.
- The original line detector could identify the corner under repeated-frame offline replay, which does not demonstrate on-vehicle route admission.

## 修改建议及下一轮验收


## 证据

- Complete camera payload checks and executable matcher results
- Prior source equality check
- Separate source-based image-line replay
- Reference route and measured height

## 限制

- No matched workflow baseline
- No new live vehicle measurement
- The exact physical reference point of the reported distance and the full camera projection are unverified

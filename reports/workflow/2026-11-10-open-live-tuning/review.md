# 2026-11-10-open-live-tuning 工作流复盘

Compare open-source serial tuning tools and document the existing vehicle live-setpoint workflow.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-11-10T12:47:17+08:00
- 测量截止：2026-11-10T12:51:41.0153665+08:00
- 墙钟秒数：264.015366
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Actual model usage | 未知 | tokens | No provider usage report |
| Research assignments | 3 | agents | Independent serial tools, motor tools, and local implementation |
| Synthesis assignments | 1 | agent | Report writer consumed the three note files |
| Physical operations | 0 | operations | Source and saved evidence only |
| Coordination and review overhead | 未知 | seconds | Not separately metered |
| Rework | 未知 | retries | Research iterations were not separately counted |

## 验收条件

- Give an actionable firmware-specific procedure and distinguish wheel target and yaw target
- Compare verified primary sources for command writes, readback, and plotting

## 已完成

- Checked saved physical evidence, firmware command paths and the current webpage capability checks
- Separated runtime setpoint, parameter readback, and chart sampling across upstream projects
- Delivered a local sourced comparison

## 未完成

- 无记录

## 收益与损耗观察

- Separate checking of serial send capability and vehicle firmware semantics avoided classifying telemetry-only viewers as equivalent to live control.
- Comparisons are stronger when a repository license, the send path, and the readback path are recorded separately.

## 修改建议及下一轮验收


## 证据

- Three focused source notes and one reviewed report
- Official upstream repositories and documentation
- Local frontend and firmware source plus saved flash and build evidence

## 限制

- No matched workflow baseline
- Tools were not installed or tested on the vehicle
- Current physical firmware identity was not queried

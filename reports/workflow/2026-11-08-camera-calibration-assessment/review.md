# 2026-11-08-camera-calibration-assessment 工作流复盘

Assess glare, reported field-of-view change and a minimal physical calibration plan before further vehicle work.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; owner-limited assessment
- 验收状态：passed
- 开始：2026-11-08T08:10:34.916952+00:00
- 测量截止：2026-11-08T08:16:05.107792+00:00
- 墙钟秒数：330.19084
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| camera_source_files_compared | 4 | files across three versions | Current SHA comparison |
| new_vehicle_commands | 0 | commands | Read-only local and web investigation only |
| agents_dispatched | 0 | agents | No delegation |
| model_usage | 未知 | tokens | Provider usage unavailable |
| cost | 未知 | currency | No billing receipt |
| review_archive_overhead | 未知 | seconds | Final archive receipt supplies measured transfer duration |

## 验收条件

- Honor assessment-only scope
- Separate optical hypotheses, source defaults and live measurements
- Give staged calibration plan and minimal owner preparation

## 已完成

- Owner confirmed same-camera historical comparison and unchanged installation
- Camera default/driver parity verified across three frozen versions
- Primary manufacturer documentation checked for optics, sensor windows and calibration
- Owner height incorporated; model discrepancy explicitly identified
- Plan distinguishes light control, effective field of view, ground mapping and later control fix

## 未完成

- 无记录

## 收益与损耗观察

- Recorded timing starts at assessment folder creation; initial contextual reads and clarification preceded it.
- Equal firmware defaults do not prove equal active camera registers or physical field of view.
- The two saved real frames were not a controlled same-pose comparison; saturation percentages were not used as proof of optical change.
- A user-provided measurement superseded the proposed repeated height measurement.
- The physical-camera height differs from the model; pitch/intrinsics remain unknown.

## 修改建议及下一轮验收

- **CRAZY-CIRCUIT-PHYSICAL-CAMERA-BASELINE-20261108 [proposed]** Freeze actual camera configuration and fit physical geometry before tuning navigation against a simulated camera model.；负责人：codex；下次检查：Read back effective sensor window and use held-out ground markers at owner-provided height before a new candidate is accepted.

## 证据

- Source camera parity and model geometry
- Explicit owner clarification
- Manufacturer optics and sensor references
- Local staged assessment plan; project handoff

## 限制

- Assessment completed; physical calibration and firmware correction intentionally deferred per owner.
- Reported height is owner-provided, not independently measured by this agent.
- No proof yet that optical angle actually changed; no active camera register snapshot in this round.
- No matched workflow baseline or speedup claim.
- No raw images, logs, source code, firmware or credentials uploaded.

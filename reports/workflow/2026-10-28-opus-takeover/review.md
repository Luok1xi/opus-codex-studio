# 2026-10-28-opus-takeover 工作流复盘

Take over production speed-loop diagnosis, recover direct serial capture, audit current changes, and pause parameter changes for owner-requested right-drivetrain inspection.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-28T09:54:47Z
- 测量截止：2026-10-28T10:19:24.202019+00:00
- 墙钟秒数：1477.202019
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native worker tasks | 2 | tasks | One independent audit completed and answered a narrow follow-up; website worker interrupted on owner instruction. |
| Complete owner-started physical runs | 1 | runs | Original two-wheel baseline; coordinator configured and captured, owner pressed physical start. |
| Coordinator flashes | 0 | flashes | Existing flash evidence was inspected only. |
| Experimental gain candidates applied | 0 | candidates | Only original baseline gains were sent. |
| External inference calls | 0 | calls | Opus evidence read and project handoff recorded; no new external model consultation. |
| Provider usage | 未知 | tokens | Unavailable; no estimates substituted. |
| Cost | 未知 | currency | Unavailable. |
| Coordination and review overhead | 未知 | seconds | Interleaved with physical waits; archive starts at measurement cutoff. |
| Rework count | 未知 | iterations | No predefined accepted-cycle denominator; interrupted scope is documented separately. |

## 验收条件

- Verify current source and existing flash evidence, capture a complete owner-started baseline, and identify the next evidence-driven physical test without claiming unresolved speed-loop acceptance.

## 已完成

- Independently audited actual speed-mode C paths: 9708 backend assertions and 41 control checks passed; these are software checks, not physical scenarios.
- Corrected stale not-flashed handoff using an existing verified flash log; no flash was performed by this coordinator.
- Preserved old capture files, stopped only the identified old serial collector, and verified fresh stopped-state parameters before inviting a physical button start.
- Collected one complete two-wheel target40 baseline with original gains, 500 rows, normal timed stop, and separately computed startup and steady-state metrics.
- Proved a capture-header consumer incompatibility; stopped website work when the owner explicitly paused it.
- Recorded project handoff376 and asked for a fully unpowered hand-spin comparison before changing right-wheel output.

## 未完成

- Await physical hand-spin observation; mechanical drag, electrical loading and encoder effects remain hypotheses.
- Establish intended competition target and repeat matched physical runs after diagnosis; speed-loop acceptance is not complete.
- Angular-rate telemetry/display semantics and physical acceptance remain pending; website work is paused.

## 收益与损耗观察

- Fresh serial state showed race mode after a reset despite an older configured collector; the production restart was not recognized by the old helper.
- The collector prompt was corrected locally from two button presses to one; actual command readback, stopped state, IMU readiness and battery state were checked before the owner start.
- The right wheel had larger steady-state variation and higher mean output, but this does not isolate a mechanical fault.
- Feedback is slew-limited before capture, so raw encoder integrity is not established by this log.
- Worker software review found a real consumer regression, but the owner prioritized manual physical tuning; the website candidate was not installed.
- A late unfiltered inbox read returned old and excessive context; future refreshes should select only new IDs and fetch full bodies selectively.
- No matched quality-controlled workflow baseline exists; net efficiency is unproven.

## 修改建议及下一轮验收

- **WF-LIVE-REBOOT-READBACK-20261028 [adopted]** After any reset or serial takeover, verify fresh mode, exact gain values and stopped state before inviting the physical start; extend restart detection only when the helper is next maintained.；负责人：codex；下次检查：Next live run records a fresh matching readback after reset; helper restart support remains unimplemented.
- **WF-TUNE-HEADER-CONTRACT-20261028 [proposed]** For firmware telemetry changes, check an export from the actual C function against its existing consumer before release.；负责人：codex+opus；下次检查：When website work resumes, the optional angle metadata is accepted without weakening malformed or truncated capture checks.

## 证据

- evidence.json; local source-audit outputs and complete physical capture; project handoff376.

## 限制

- No production source edits or flashing by coordinator; runtime parameters and serial capture were used, and the owner physically started one ground run.
- Physical diagnosis and competition-speed acceptance are pending, so no mechanical repair or speed-loop pass is claimed.
- No raw captures, source, live databases, process command lines, credentials or conversations are uploaded.

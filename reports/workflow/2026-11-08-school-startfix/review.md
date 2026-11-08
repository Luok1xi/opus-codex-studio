# 2026-11-08-school-startfix 工作流复盘

Correct and deploy the isolated startup candidate, then diagnose four failed owner-operated starts against live telemetry, saved real images and exact source.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + manifest-only MCU build and real-input replay
- 验收状态：partial
- 开始：2026-11-08T07:28:03.485688+00:00
- 测量截止：2026-11-08T08:05:17.714372+00:00
- 墙钟秒数：2234.228684
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| source_files | 688 | files | Frozen manifest and build-input comparison |
| full_build_wall | 6.08 | seconds | MCU build log |
| flash_wall | 4.075 | seconds | Official flasher output |
| agents_dispatched | 0 | agents | Coordinator performed this bounded task |
| confirmed_helper_failures | 2 | failures | Host stub omission and release helper path assertion corrected |
| safety_test_detected_source_defects | 1 | defects | Manual fan cap absent on one path; corrected |
| total_tool_errors | 未知 | errors | No complete instrumented count; other access/policy errors described |
| usage | 未知 | tokens | Provider usage unavailable |
| cost | 未知 | currency | Billing unavailable |
| review_archive_overhead | 未知 | seconds | Archive receipt records actual timing after report cutoff |
| observed_failed_owner_starts | 4 | starts | Complete closed capture with no resets |
| diagnostic_flash_actions | 0 | actions | Only read-only queries and offline analysis |
| initial_archive_wall | 17.294888 | seconds | Earlier verified archive receipt |
| diagnostic_initial_snapshot_to_cutoff | 554.841626 | seconds | Measured diagnostic snapshot interval; earlier request/context work excluded |

## 验收条件

- Real-frame admission without weakening invalid/stale-image rejection
- Launch timing, clean build, exact firmware readback and continuous capture
- Owner-operated physical start and lap validation

## 已完成

- Isolated manifest-only source copy and six reviewed source changes; historical source preserved
- Real input admission plus invalid-input and stale-frame rejection checked with unchanged matching limit
- Previously successful ESC launch sequence restored and checked using extracted actual functions
- Manual fan maximum clamp regression found and corrected before building
- Eight full-route cases and terminal stop passed; route tests use zero fan
- Fresh MCU build, tested-source parity, payload identity and warning parity verified
- Owner-confirmed physical setup; one verified flash with zero byte differences
- Live wired readback of expected identity, requested settings, stationary output and camera 150 fps
- Live wireless identity and settings verified after reconnection
- Read-only continuous capture opened and fresh data confirmed
- Four complete owner-operated failed starts preserved with no restart in capture
- Calibration and fan prefill progression distinguished from navigation acceptance failure
- Complete stopped-state onboard record, identity and camera image read back
- Exact released navigator rejected the newly captured input in offline replay
- Observed zero mean forward target with nonzero counter-rotating wheel targets traced to readiness/control coupling

## 未完成

- Physical starting acceptance FAILED in all four attempts; no further corrected firmware deployed
- Real-image/model alignment and unified forward/steering admission need correction
- Line following, early turns, corner speed and full-lap behavior still unvalidated

## 收益与损耗观察

- Measurement window starts at isolated staging; initial task/context preparation is outside this measured interval.
- Real captured image reproduced the rejection; bright-floor contamination was corrected before deployment.
- Alternate offline threshold/component probes did not meet the admission gate and were excluded from firmware.
- Launch tests caught a manual-output limit defect and a missing host stub; both corrected before final checks.
- Release verification initially assumed separate host source directories; assertion caught the shared-source layout and was corrected.
- WSL required the approved local execution context; build child script required process-scoped policy permission, with no system policy change.
- No model delegation or external independent review was claimed.
- User physical confirmation arrived after the candidate was concretely frozen; no repeated flash authorization was requested.
- The prior single real frame passed but did not represent later real inputs; synthetic brightness variants were insufficient.
- Three attempts had no sampled wheel command; one briefly drove and then commanded opposing wheel directions. These outcomes must be separated.
- The stop field remains latched across new starts and cannot alone identify the current active fault.
- Excluding a manually identified bright-floor region lowered error but still failed admission; that diagnostic crop is not a deployable rule.
- A valid localization flag alone does not authorize wheel drive when the forward request is zero; the inner yaw state can remain active.
- The post-stop frame does not reconstruct the exact moving frame or internal pose that caused the short driven attempt.
- After stopped-state queries, read-only recording was reopened but no fresh complete wireless telemetry arrived by the final check.

## 修改建议及下一轮验收

- **REAL-SENSOR-STARTUP-ADMISSION-20261108 [adopted]** Use captured real input and rejected-input cases as a deployment gate alongside simulation; retain separate physical acceptance.；负责人：codex；下次检查：Next owner-operated start must establish valid localization and wheel command; complete lap still needs physical evidence.
- **CRAZY-CIRCUIT-REAL-ADMISSION-CORPUS-20261108 [proposed]** Expand admission regressions with every distinct real failure and jointly check forward, yaw and wheel inhibition; passing one frame is insufficient.；负责人：codex；下次检查：Next candidate passes both saved real inputs, invalid/stale input rejection, and zero-forward wheel inhibition before owner-operated acceptance.

## 证据

- Frozen source and release manifests
- Exact-source real-frame and startup regression summaries
- Route and finish-stop summaries
- Verified flash receipt
- Live query and capture receipts
- Closed four-attempt capture summary
- Complete last-attempt onboard dump summary
- Current-frame rejection and bounded diagnostic ablation
- Actual zero-forward counter-rotation telemetry and source call path

## 限制

- Two post-stop real frames differ; neither reconstructs the short driven attempt frame by frame.
- Full-route tests use zero fan; fan30 timing is validated separately with stubbed hardware.
- No physical turn timing, line adhesion or complete-lap success claimed.
- No matched workflow quality/timing baseline, no speedup claim.
- No raw source, serial records, images, firmware, live databases or credentials uploaded.
- Physical acceptance failed; calibration/prefill success cannot be reported as a successful launch.

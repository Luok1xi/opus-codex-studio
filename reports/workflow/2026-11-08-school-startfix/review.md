# 2026-11-08-school-startfix 工作流复盘

Correct real-frame startup rejection while preserving requested settings and route, then clean-build and deploy after current physical preparation.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + manifest-only MCU build and real-input replay
- 验收状态：partial
- 开始：2026-11-08T07:28:03.485688+00:00
- 测量截止：2026-11-08T07:48:49.037386+00:00
- 墙钟秒数：1245.551698
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

## 未完成

- Owner-operated physical launch and line-following/early-turn/corner-speed acceptance remain pending

## 收益与损耗观察

- Measurement window starts at isolated staging; initial task/context preparation is outside this measured interval.
- Real captured image reproduced the rejection; bright-floor contamination was corrected before deployment.
- Alternate offline threshold/component probes did not meet the admission gate and were excluded from firmware.
- Launch tests caught a manual-output limit defect and a missing host stub; both corrected before final checks.
- Release verification initially assumed separate host source directories; assertion caught the shared-source layout and was corrected.
- WSL required the approved local execution context; build child script required process-scoped policy permission, with no system policy change.
- No model delegation or external independent review was claimed.
- User physical confirmation arrived after the candidate was concretely frozen; no repeated flash authorization was requested.

## 修改建议及下一轮验收

- **REAL-SENSOR-STARTUP-ADMISSION-20261108 [adopted]** Use captured real input and rejected-input cases as a deployment gate alongside simulation; retain separate physical acceptance.；负责人：codex；下次检查：Next owner-operated start must establish valid localization and wheel command; complete lap still needs physical evidence.

## 证据

- Frozen source and release manifests
- Exact-source real-frame and startup regression summaries
- Route and finish-stop summaries
- Verified flash receipt
- Live query and capture receipts

## 限制

- One post-stop real frame plus deterministic variants does not cover all real track images.
- Full-route tests use zero fan; fan30 timing is validated separately with stubbed hardware.
- No physical turn timing, line adhesion or complete-lap success claimed.
- No matched workflow quality/timing baseline, no speedup claim.
- No raw source, serial records, images, firmware, live databases or credentials uploaded.

# 2026-11-08-real125-fan30-bringup 工作流复盘

Deliver the explicitly requested isolated firmware, capture owner-operated starts, and diagnose failure against the proven starting baseline and real sensor input.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + project-specific build/flash receipts
- 验收状态：partial
- 开始：2026-11-08T06:51:25+00:00
- 测量截止：2026-11-08T07:22:54.592987+00:00
- 墙钟秒数：1889.592987
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| source_files_verified | 688 | files | Frozen candidate manifest checked before copying |
| full_build_wall | 6.553 | seconds | ADS full-build log |
| flash_wall | 4.121 | seconds | Official flasher reported overall time |
| flash_attempts | 1 | attempts | One official burn receipt |
| failed_device_open | 1 | attempts | Stale wireless port absent before live device enumeration |
| script_policy_build_failure | 1 | attempts | First child PowerShell blocked script; temporary process permission then approved |
| agents_dispatched | 0 | agents | No delegation occurred |
| model_usage | 未知 | tokens | Provider usage unavailable |
| cost | 未知 | currency | No billing receipt |
| review_archive_overhead | 未知 | seconds | Archive not completed at cutoff |
| observed_failed_starts | 5 | starts | Closed capture, complete running transitions |
| onboard_record_samples | 17 | samples | Complete indexed dump with terminator |
| offline_real_frame_replay | 1 | experiment | Unmodified navigator and saved frame |
| diagnostic_flash_actions | 0 | actions | Only serial queries and offline work |
| initial_archive_wall | 16.075637 | seconds | Verified initial archive receipt |
| diagnostic_evidence_helper_rework | 2 | assertion failures | Later starts and manifest path-separator normalization |
| total_tool_errors | 未知 | errors | No complete instrumented count; observed query and helper issues described |

## 验收条件

- Isolated source provenance and fresh MCU build
- Explicit flash authorization and physical preparation
- Verified flash and live readback of requested settings
- Continuous capture established; actual run diagnosis follows observed run
- Real-device start succeeds after calibration; failing starts must be diagnosed with preserved evidence

## 已完成

- Source hashes verified, empty build output directory, fresh complete build
- One verified flash with zero byte differences
- Both wired and wireless readback matched new identity and requested settings
- Read-only recorder confirmed fresh and growing
- Three startup segments separated; latest stationary output remained zero over ten seconds
- Five failed owner-operated starts preserved separately from restart segments
- Complete onboard record and real camera frame retrieved with read-only commands
- Unmodified current navigator rejected the real input in an isolated offline replay
- Current and historically successful source manifests verified; inherited control difference identified

## 未完成

- Physical starting acceptance failed; no corrected firmware has been deployed
- Real input/projection and readiness integration require correction and validation
- Line-following, turn timing, corner speed and full lap remain unvalidated

## 收益与损耗观察

- Owner clarified that a new flash was required; source-only readiness was not the intended result.
- Device enumeration must occur in the actual device-access context; initial limited-context view was stale.
- Current build identity and source candidate identity were unified before freezing.
- Restart-separated sensor readings prevented treating improved bias as resolved prematurely.
- Successful synthetic simulation and byte-identical clean build did not validate real-image startup admission.
- The integration made map localization a wheel-release prerequisite without first validating real sensor frames.
- Five starts failed before a nonzero sampled wheel command; a complete onboard record and unchanged-source replay supported a software readiness rejection.
- The same navigator existed in the immediate predecessor; the proven starting baseline used a different control path.
- One missing identity response was preserved, followed by a successful bounded read-only query.
- Evidence helper assertions caught later attempts and inconsistent path separators; corrected before reporting.
- First workflow archive preceded the failed runs; this amended report preserves that earlier history and records failed acceptance.

## 修改建议及下一轮验收

- **CRAZY-CIRCUIT-DEVICE-CONTEXT-20261108 [adopted]** Enumerate and open hardware in the same execution context, then confirm continuous data before declaring capture ready.；负责人：codex；下次检查：Next device task has one consistent enumeration/readback receipt.
- **REAL-SENSOR-STARTUP-ADMISSION-20261108 [proposed]** Before accepting a simulation-derived control path for deployment, replay a real parked start frame and verify that readiness and nonzero target can be established while loss-of-line protection still rejects invalid input.；负责人：codex；下次检查：Next corrected candidate passes real-frame admission plus invalid-frame rejection and a user-operated launch; model-only completion does not count.

## 证据

- Frozen-source manifest receipt
- Fresh full build and normalized warning comparison
- Official flash receipt with zero difference verification
- Wired/wireless query receipts and capture status
- Restart-segment stationary sensor summary
- Closed run transition summary
- Complete indexed onboard record summary
- Real camera frame replay result with exact-source hashes
- Historical/current source comparison and local project handoff

## 限制

- Diagnosis complete at integration-path level; no corrected physical start or lap is claimed.
- Post-stop replay input was not recorded at the exact failure instant.
- Physical geometry and contributions to image/model mismatch are uncalibrated.
- No matched workflow baseline, usage or billing evidence; no efficiency claim.
- Raw source, images, serial data, firmware, device identifiers and private paths excluded from upload.

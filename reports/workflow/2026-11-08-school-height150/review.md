# 2026-11-08-school-height150 工作流复盘

Apply owner-supplied camera height in an isolated candidate, improve bright-floor filtering and stop residual steering when forward motion is rejected; retain failed route regression and withhold deployment.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + manifest-only candidate + unchanged route acceptance
- 验收状态：partial
- 开始：2026-11-08T08:24:14.827293+00:00
- 测量截止：2026-11-08T08:45:50.546001+00:00
- 墙钟秒数：1295.718708
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| source_files | 688 | files | Manifest-only staging and final hash comparison |
| changed_files | 7 | files | Reviewed source delta from frozen baseline |
| route_passed | 7 | cases | Final eight-case C and physics regression |
| route_failed | 1 | cases | Right-offset physics case stops3 at node11 |
| sanitized_image_cases | 36 | cases | Actual candidate parser and navigator under address/undefined-behavior sanitizers |
| motion_gate_checks | 19 | checks | Full candidate control loop with hardware stubs |
| final_build_wall | 5.675 | seconds | MCU full-build log |
| measured_task_wall | 1295.718708 | seconds | Staging-to-cutoff; includes waits and analysis, excludes earlier context retrieval |
| agents_dispatched | 0 | agents | Coordinator-only implementation; handoff does not imply independent review |
| flash_actions | 0 | actions | No flasher invoked |
| read_only_device_queries | 3 | queries | Parked-state guard before each identity/record/image request |
| total_tool_errors | 未知 | errors | No complete instrumented count; helper failures described separately |
| usage | 未知 | tokens | Provider accounting unavailable |
| cost | 未知 | currency | Billing unavailable |
| review_archive_overhead | 未知 | seconds | Measured archive receipt is recorded after report cutoff |

## 验收条件

- Consistent owner-supplied height and clean provenance
- Real-input admission and invalid/stale-input protection
- Common forward/yaw/wheel inhibition
- Unchanged full-route criteria before deployment

## 已完成

- Staged only 688 manifest-listed source files from the frozen on-car baseline; seven reviewed files changed.
- Updated forward/inverse camera projections consistently to owner-supplied 150mm; route and distance atlas byte-identical.
- Separated height-only replay evidence from threshold and motion-gate changes; map acceptance stays below15.
- Two saved real frames and deterministic variants checked: 36 cases, 842 checks; sanitizer run passed.
- One clipped-brightness variant remains rejected by design; this is not full glare robustness.
- Actual motion-control gate passed19 checks; zero-forward requests clear inner-controller state and both outputs.
- Actual extracted launch functions passed15 cases and374963 checks; fan30 startup remains unchanged.
- Final unchanged-criteria route matrix passed7 of8; right-offset physics case stops safely at node11.
- Paired old/new thresholds reproduce identical failing route behavior; threshold is not the cause in that fixture.
- Extended terminal run covers all47 nodes and stop26 at81.184mm past finish, wheels and fan off.
- Clean final MCU build has0 errors and14 inherited warnings, no new warnings; tested/built source parity and payload checks passed.
- Read-only wireless query reverified on-car baseline, speed125, fan30 and47 nodes; captured original-lens frame.
- New candidate is frozen with an explicit offline-only/do-not-flash status; no remote start, parameter write or flash.

## 未完成

- Resolve right-offset route localization loss without weakening the matching/out-of-line/stale-input gates.
- Obtain a clear original-lens image at the normal starting pose; current holdout contains foreground objects.
- Physical glare robustness, line following, turn timing and complete-lap acceptance remain unvalidated.

## 收益与损耗观察

- Height-only change improved both real-frame scores but did not admit the newer saved scene; stricter paint extraction was separately tested.
- Failed route trace shows localization loss before the motion gate disables outputs; confirmed branch observations existed. Exact root of longitudinal pose divergence is unresolved.
- Historical source and binary identity, current candidate source, and live firmware identity are recorded separately.
- Offline test clones contain diagnostic instrumentation; none of their source is copied into the MCU manifest.
- Preparation encountered a newline-sensitive assertion, CRLF shell-script error and stale version expectation; corrected in local helpers.
- An int-to-byte conversion warning was removed by keeping the Boolean local as int, followed by clean rebuild and final regression.
- Extended terminal fixture originally rejected the post-stop route-index reset; acceptance now checks full sequential coverage before a trailing reset with launch off and stop26. Original scored route criteria remain unchanged.
- One IDE launcher exited before building; a fresh isolated IDE workspace recovered. A duplicate encoding marker in the new helper was corrected before the successful build.
- Optional Python serial/image packages were absent; used the existing serial reader and standard-library image decoding instead of installing packages.
- User restored the original lens; requested foreground cleanup before another calibration capture. No answer by this cutoff.
- No independent agent review or workflow speed improvement claimed.

## 修改建议及下一轮验收

- **CC-150MM-REAL-AND-ROUTE-GATE-20261108 [adopted]** Require real-input admission, common motion inhibition and the unchanged full-route regression together before deployment; preserve failures as evidence.；负责人：codex；下次检查：Next candidate must pass the same eight route cases and clear original-lens holdout before physical trial.
- **CC-BUILD-HELPER-FAILFAST-20261108 [proposed]** Check the IDE process after launch and preserve full helper error output to avoid repeated dead-process menu waits.；负责人：codex；下次检查：Future builder fails promptly on a simulated exited process and still completes a clean build.

## 证据

- Source/HEX manifest and candidate diff
- Height-only and final exact-source real replays
- Actual gate and launch regressions
- Paired threshold route probes and final route summaries
- Extended finish-stop evidence
- Read-only identity and original-lens capture receipt

## 限制

- Height150 is owner supplied; pitch46/focal94/ahead40 remain inherited, not physically calibrated.
- Full-route tests use zero fan; fan30 timing is tested separately with hardware stubs.
- Current scene has foreground objects; camera saturation count alone does not distinguish track from glare.
- One route failure remains; build success is not physical acceptance.
- No matched workflow quality/timing baseline and no speedup claim.
- Only sanitized aggregate reports are uploaded; no source, firmware, images, raw logs, databases or credentials.

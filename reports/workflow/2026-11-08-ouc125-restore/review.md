# 2026-11-08-ouc125-restore 工作流复盘

Restore OUC primary control after multi-run diagnosis, isolate auxiliary navigation and withhold the candidate after route regression failure.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + source authority tests + immutable builds + unchanged acceptance
- 验收状态：partial
- 开始：2026-11-08T18:14:36.406661+08:00
- 测量截止：2026-11-08T10:45:28.628432+00:00
- 墙钟秒数：1852.221771
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| measured_wall | 1852.221771 | seconds | Initial multi-run investigation timestamp to cutoff; includes steering and tool recovery |
| captured_launch_intervals | 17 | runs | Boot-aware parser of7 frozen recorder files |
| source_files | 688 | files | Immutable input manifests |
| changed_source_files | 9 | files | Final source diff against08 |
| control_checks | 426 | checks | Actual PID/vision linked test |
| startup_cases | 15 | cases | Actual extracted functions |
| full_route_passed | 0 | cases | Final two-model regression |
| full_route_total | 8 | cases | Same course and acceptance boundaries |
| final_clean_build_wall | 4.756 | seconds | ADS full C build log |
| flash_actions | 0 | actions | No flasher invoked |
| remote_starts | 0 | actions | No launch commands |
| agents_dispatched | 0 | agents | Single coordinator |
| usage | 未知 | tokens | No provider usage accounting |
| cost | 未知 | currency | No billing |
| tool_failures | 未知 | failures | Not instrumented end-to-end |
| review_archive_overhead | 未知 | seconds | Will be measured in archive receipt |

## 验收条件

- OUC owns control; auxiliary photo cannot command motion
- Clean build and startup/control regression
- Full-course and physical acceptance

## 已完成

- Reviewed17 complete manual launch intervals across3 boot epochs; all stopped with code3, without assigning unrecorded physical element positions.
- Implemented isolated OUC primary control and removed all photo motion/route authority; retained125/30,47 events and existing hardware/startup calibration.
- Verified426 control checks and15 actual-function startup cases; replayed4 real images with temporal warm-up.
- Preserved immutable historical manifests and completed a full C-source build with0 errors and no new warnings.
- Ran unchanged route acceptance, retained failed experiments separately, and explicitly withheld the candidate after0/8 complete-route passes.

## 未完成

- Correct OUC turn entry/exit on the current course and pass the unchanged full-route regression.
- Validate resistor/dash traversal and body stability physically; no candidate flash performed.

## 收益与损耗观察

- A visual module being present did not make it the active control path; call-path audit was necessary.
- Restoring the prior controller did not restore full-course acceptance under the new course/camera conditions.
- Several local parameter changes progressed farther but failed the common acceptance criteria and were rejected.
- Cold-only image replay initially suggested invalid resistor detection; temporal warm-up changed the result and was added before reporting.
- An ADS close request left a process holding the workspace. New startup then waited; only verified current-workspace processes were closed.
- Removing object files alone only reran assembly; generated assembly must also be invalidated for a full source rebuild.
- No matched workflow baseline; no speedup claim.

## 修改建议及下一轮验收

- **CC-OUC-AUTHORITY-20261108 [adopted]** Test that auxiliary navigation cannot write motion or route state, and run real images with temporal initialization.；负责人：codex；下次检查：Future candidates pass the same authority and warm-up regressions; full-route quality still required.
- **CC-ADS-CLEAN-20261108 [proposed]** Treat close as a request until process exit and invalidate compiler-generated assembly as well as objects for a full build.；负责人：codex；下次检查：A later isolated build starts without workspace lock conflict and emits full C compilation evidence.

## 证据

- Versioned source/diff and manifest
- Controller and startup test logs
- Temporal static-image replay
- Unchanged eight-case route regression
- Boot-aware multi-run aggregate

## 限制

- Candidate is not approved for flashing.
- Full route and physical stability remain unaccepted.
- Static frames and fixed-pitch simulation do not prove physical nose-over prevention.
- Only sanitized aggregate reports are uploaded.

# 2026-10-30-vision-ipm-turn 工作流复盘

Implement and evaluate frame-bound two-dimensional turn geometry, motion compensation and an early visual steering candidate.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md and TEAMHUB.md
- 验收状态：partial
- 开始：2026-10-30T04:30:45Z
- 测量截止：2026-10-30T05:43:21.793284+00:00
- 墙钟秒数：4356.793284
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Wall time to delivery cutoff | 4356.793 | seconds | UTC task start through integration, verification and handoffs; parallel work overlaps, archive follows. |
| Simulation and diagnostic executions | 65 | runs | 18 initial +2 speed-switch diagnostics +1 exact replay +6 source regressions +6 new-arm development +32 frozen validation. |
| Final validation elapsed | 56.440244 | seconds | Observed runner wall time, not simulated lap time. |
| Final validation passes | 1 | of 32 | New arm1/8; all other arms0/8; no55mm engineering-margin passes. |
| Largest held-out fallback output jump | 209.6 | degrees/second | Early-control arm, same stage and route at exit to original controller; absence of immediate sign reversal does not mean smooth handover. |
| Current independent C assertions | 702 | assertions | 101 motion+132 geometry+285 control+132 phase2+52 PID; includes repeated setup and coverage overlap, not702 independent scenarios. |
| Exact source regression runs | 6 | runs | All pre-existing control columns matched; disabled-arm new diagnostic counters intentionally become zero. |
| Worker scopes | 3 | agents | Geometry, simulation and independent review; no recursive dispatch. |
| Successful host build invocations | 12 | builds | Each produces C and PyBullet binaries; includes4 prepared unused builds. |
| Unused prepared host builds | 4 | builds | Replaced by same-tick shadow instrumentation before any run. |
| Full target builds | 2 | builds | Initial-off and optimized default-off;180C units each. |
| Default-off target build log time | 4.356 | seconds | Compiler log; excludes setup and verification. |
| Default-off CPU1 memory recovered | 4600 | bytes | Relative to initial isolated build; not an active-controller runtime saving. |
| Hardware operations | 0 | operations | No flash, serial or vehicle command. |
| Exclusive review overhead | 未知 | seconds | Review overlaps implementation and simulation. |
| Exclusive coordination wait | 未知 | seconds | Not separately instrumented. |
| Total tool failure count | 未知 | operations | No complete census; recorded UTF8 preparation failure and corrected frozen-manifest lookup. |
| Provider token usage | 未知 | tokens | No complete provider usage evidence. |
| Actual cost | 未知 | currency | No billing evidence. |
| Archive overhead | 未知 | seconds | Measured after delivery cutoff in archive receipt. |

## 验收条件

- Test a bounded image-derived 2D branch controller at committed turns without simulator truth inputs
- Preserve prior results,60mm out threshold,inner loops and current hardware state
- Use matched development then new frozen validation cases; report any baseline modeling failures
- Deliver reviewed source and measured evidence to Opus and archive sanitized workflow report

## 已完成

- Implemented bounded two-sided turn targets and anchor extraction, encoder/IMU capture-time interpolation, and guarded visual turn modes in isolated firmware.
- Diagnosed a precise observation-lifetime expiry and an independent geometric anchor rejection using identical replay and original image processing.
- Preserved original arms, prospectively declared one early-control extension, completed exact-column regressions and32 frozen validation runs.
- Independent C, integration and target checks passed; default-off compile removed unused workspace and restored4600 bytes.
- Delivered all outcomes and explicit non-promotion decision through the project database.

## 未完成

- No robust cross-model or held-out improvement; new arm passes only1/8 validation conditions and fails55mm margin.
- No matched passing baseline supports a lap-time speedup claim.
- Actual hardware calibration, CPU processing time, complete stack high-water and physical performance remain unverified.
- External Opus acceptance and artifact-ledger acknowledgement remain pending.

## 收益与损耗观察

- A passing development run did not generalize to the same model validation cases; opposite-model regressions were retained.
- Merged fallback reasons initially prevented diagnosis; one logging-only replay with exact legacy-column parity resolved lifetime expiry before changing thresholds.
- Independent frame reprocessing found a second blocking condition; moving the expiry check alone would not refresh the rejected anchor.
- Default-disabled control still reserved geometry memory; compile-time removal recovered memory without changing legacy control traces.
- Shadow diagnostics were added after4 prepared host builds; specifying required counters before freezing would reduce rework.
- A host preparation failure came from implicit Windows encoding; explicit UTF8 corrected it before simulation.
- The coordinator first chose a research-source manifest to compare against production, then switched to the actual production freeze; no production files were changed.

## 修改建议及下一轮验收

- **TURN-OBSERVABILITY [adopted]** Specify first-loss subreason, capture/current odometry and same-tick pre-override output before freezing comparison builds.；负责人：codex；下次检查：Future traces must distinguish geometry rejection, identity loss, age and distance expiry.
- **TURN-HOLDOUT [adopted]** Preserve cross-model failures and require an explicit new validation set after further development.；负责人：codex；下次检查：A single completed route never promotes the candidate; retain engineering margin separately.
- **TURN-ANCHOR [proposed]** Review anchor extrapolation constraints against measured turn shape and study fallback transitions separately from turn-entry timing.；负责人：opus；下次检查：New bounded design and independent tests before any changed-threshold simulation.
- **TURN-BUDGET [proposed]** Measure active per-core geometry timing and stack high-water before enabling on hardware; default-off must remove its scratch memory.；负责人：opus；下次检查：Separate default-off memory savings from active-controller timing.

## 证据

- Aggregate evidence and cryptographic fingerprints retained in evidence.json; full source, images, runs and detailed reviews remain local.

## 限制

- No matched workflow-quality baseline; no workflow speedup claim.
- Simulation latency is configured, not measured target runtime.
- Development and final held-out outcomes are reported separately.
- No new threshold or gain tuning after final validation.
- Target artifact defaults to disabled visual control and uncalibrated projection.
- Archive verification occurs after the measurement cutoff.

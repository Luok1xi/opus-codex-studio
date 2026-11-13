# 2026-11-13-nov1-turn-handoff 工作流复盘

Owner paused tuning and requested a new-chat handoff. Preserve the successful quiet physical launch, incomplete legacy-turn adaptation, failed row sweeps, and unvalidated combined routing changes without claiming a stable release.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：Single root hardware owner; bounded native implementation, review and isolated sweep; stop request terminates further optimisation. Sanitized stage archive only.
- 验收状态：partial
- 开始：None
- 测量截止：2026-11-13T08:17:29Z
- 墙钟秒数：None
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| measured_checkpoint_interval | 2388 | seconds | 07:37:41Z to owner stop08:17:29Z; includes human wait, not whole-task development duration. |
| whole_task_duration | 未知 | seconds | True task start and earlier work not bounded by this checkpoint. |
| physical_runs_saved | 3 | runs | Closed capture manifest; complete P/I/S exports for each. |
| verified_configuration_runs | 1 | runs | Only first run had fresh fullQ plus matchingM2 at launch. |
| unknown_configuration_runs | 2 | runs | Later launches lacked fresh completeQ/matchingM2. Remain unknown. |
| first_run_board_samples | 225 | samples | Complete S export;20ms samples, not2ms. |
| first_run_board_span | 4.48 | seconds | (225-1)*20ms, first-to-last saved sample. |
| nominal_two_model_passes | 0 | passes_of_2 | Saved csim/PyBullet first-corner failures with main row70. |
| isolated_row_full_passes | 0 | passes_of_5 | Rows62,52,42,47,32, fixed frozen nov1-v2; original model/controller. |
| route_synthetic_assertions | 19 | assertions | Three actual-C cases4+7+8; does not establish full integration. |
| first_corner_metric_corrections | 1 | corrections | Row52 initially reported route_k0 max42.95; corrected complete corner+exit peak59.85. |
| sweep_restricted_WSL_retry | 1 | retries | Restricted launch refused; existing compiler invoked through authorized elevated execution. |
| total_rework | 未知 | reworks | No complete whole-task coding/review event ledger. |
| tokens | 未知 | tokens | Provider whole-scope usage unavailable. |
| cost | 未知 | currency | No billing evidence. |
| review_wait | 未知 | seconds | Not independently timed. |
| archive_overhead | 未知 | seconds | Archive is after owner-stop cutoff; its final receipt records a separate checkpoint. |

## 验收条件

- Verify quiet startup reaches wheel control with a correctly bound configuration.
- Adapt legacy turn behavior and routing with explicit same-source model acceptance before deploying.
- Honor stop request, preserve all completed trials and hand off known gaps.

## 已完成

- First quiet physical start reached wheel drive after calibration/pre-spin; 225 board samples at20ms, 4.48s first-to-last span, then stop3.
- Saved capture contains three runs; all P/I/S exports complete. Only run001 has verified launch-time configuration binding.
- Two-model nominal smoke of the restored legacy turn failed at the first corner; failures retained.
- Five isolated row candidates preserved exact build/source receipts; zero full-course passes; row47 was not merged and main remains70.
- Actual C routing counterexample reproduced premature route consumption; one-line fix passed19 synthetic assertions.
- Collector closed naturally with exit0 and zero manifest faults. No further tests or optimisation after owner pause.

## 未完成

- Next chat should first inspect saved run002(94 samples) and run003(228 samples); both remain unknown configuration binding and cannot be used as matched-parameter comparisons.
- Combined route fix, legacy turning and any alternative row require joint simulation and target ADS build; these were not performed.
- No stable course-completion result for the new candidate; no new candidate deployment.

## 收益与损耗观察

- Physical first-start success is new evidence; the prior quiet-build report correctly said unverified at its own cutoff and is not rewritten.
- Owner clarified the failure was a left fork before the dashed section. A stop3 code alone does not establish that the car traversed the dashes correctly.
- Legacy parameters cannot be independently transplanted without actuator, sensing and phase checks: both nominal models failed despite the historically stable controller.
- First-corner completion and exit peak are different metrics. Row52 rose from42.95mm before route advance to59.85mm when exit was included.
- Rows42/47 met the first-corner-plus-exit50mm criterion but failed near k8; local success does not establish course stability.
- Later saved runs exist but have unknown configuration binding and were not analysed in this stage.
- Bounded summaries avoid large nested telemetry output. Preserve detailed data locally rather than printing whole manifests.
- No matched-quality workflow baseline; elapsed checkpoint time cannot establish efficiency gains.

## 修改建议及下一轮验收

- **NOV1-FIRST-CORNER-EXIT-WINDOW [adopted]** Report first-corner error through exit up to the next turn, not only until route index advances; publish the interval definition.；负责人：codex；下次检查：Future turn comparisons include exit peaks and exact event boundaries.
- **NOV1-LEGACY-TWO-MODEL-SMOKE [adopted]** After legacy controller or parameter migration, start with same-source nominal smoke in both models before a wider sweep or deployment.；负责人：codex；下次检查：Next combined candidate must pass both smoke runs before broader claims.
- **NOV1-BOUNDED-TELEMETRY-SUMMARY [adopted]** Print selected scalar facts and artifact links; keep nested telemetry and complete raw evidence in files.；负责人：codex；下次检查：Next review extraction emits only selected metrics and counts.

## 证据

- evidence.json aggregates saved run bindings, sample periods, nominal failures, sweep results and19 assertion boundary.
- Root owns full local project handoff; this report does not replace it or modify project state.
- Prior quiet-build archive bee0f540 remains unchanged.

## 限制

- Execution paused at owner request; no new simulation, tests, flashing or serial connection performed by archive worker.
- Startup phase timestamps come from asynchronous telemetry; their10ms overlap is not evidence of source phase-order failure.
- Unknown configuration on runs002/003 remains unknown; no retrospective parameter backfill.
- All five sweep results use the frozen pre-route-fix snapshot; they cannot validate the later one-line routing change.
- Actual-C synthetic routing cases do not prove camera perception or whole-track correctness.
- Full-stage start, total usage/cost and total review/coordination overhead unknown.
- Only sanitized reports and aggregate evidence are uploaded.

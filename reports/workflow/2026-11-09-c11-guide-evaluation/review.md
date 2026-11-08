# 2026-11-09-c11-guide-evaluation 工作流复盘

Evaluate an isolated guide-to-task handoff and bounded turn-exit repair, incorporate the requested reviewer consultation, and reject promotion when full-course acceptance fails.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; isolated implementation, explicit state contract, unchanged acceptance limits
- 验收状态：partial
- 开始：2026-11-08T15:22:53.543547+00:00
- 测量截止：2026-11-08T16:19:34.125360+00:00
- 墙钟秒数：3400.581813
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| claim_to_review_cutoff_wall | 3400.581813 | seconds | Task-claim timestamp to report preparation; includes owner steering and local testing; later archive excluded |
| final_unit_scenarios | 44 | scenarios | Actual sanitizer-enabled host run |
| final_unit_assertions | 167 | assertions | Actual host test output |
| final_segment_passed | 10 | runs | Ten normal segment completion records |
| final_fault_stops_passed | 4 | runs | Output-zero and300ms post-stop coast evidence |
| final_full_course_passed | 3 | runs | Unchanged quality thresholds; eight final cases |
| final_full_course_total | 8 | runs | Four conditions in two models |
| external_model_calls_completed | 1 | calls | Verified reviewer reply; abstract minimal payload only |
| external_model_elapsed | 38.422 | seconds | Consultation receipt; not token or cost usage |
| external_detailed_payload_rejections | 1 | attempts | Automatic approval rejected detailed payload; it was not sent |
| target_native_build_failed | 1 | attempts | IDE-only compiler license rejected standalone invocation; no target HEX |
| frozen_source_files_checked_each | 688 | files | Two independent frozen trees |
| modified_source_files | 9 | files | Frozen baseline source diff |
| hardware_actions | 0 | actions | No serial, flashing or remote launch |
| child_agents_dispatched | 0 | agents | One direct reviewer consult, no recursive delegation |
| usage | 未知 | tokens | Not fully instrumented; archive interval is recorded separately |
| cost | 未知 | currency | Not fully instrumented; archive interval is recorded separately |
| total_tool_failures | 未知 | failures | Not fully instrumented; archive interval is recorded separately |
| review_archive_overhead | 未知 | seconds | Not fully instrumented; archive interval is recorded separately |
| full_round_wall | 未知 | seconds | Not fully instrumented; archive interval is recorded separately |

## 验收条件

- Preserve frozen sources and vehicle
- Separate physical guide from task counter with verified handoff
- Pass segment and full-course acceptance before promotion
- Keep reviewer advice and measured results distinct

## 已完成

- Rechecked frozen historical and deployed-source identities and created a source-only isolated evaluation.
- Compared planned-side admission and restored bounded turn-exit supervision with explicit failure reasons.
- Consulted the requested reviewer through one verified abstract model call and reviewed its separate local handoff; corrected unsupported historical and symbol assumptions.
- Implemented the owner-approved lead-in guide separately from task numbering while retaining one turn state machine and its distance datum.
- Passed44 unit scenarios with167 assertions, ten normal segments and four fail-closed injected segments.
- Ran all eight final full-course conditions under unchanged quality limits; three passed and five failed. No flash approval or physical actions.
- Detected and fixed a physics replay schema mismatch and a far-line optical false-proof case; retained original failed evidence.

## 未完成

- Repair full-course exit-lock and dense-turn quality failures; do not promote current evaluation.
- Complete target compilation in the licensed IDE and verify RAM/timing only when preparing a viable candidate.
- Physical odometry/camera calibration and vehicle acceptance remain separate later stages.

## 收益与损耗观察

- Segment success did not predict full-course acceptance; the unrepaired evaluation remains explicitly unapproved.
- Several iterative control revisions and full runs were needed; no matched baseline supports a speedup claim.
- A duplicated replay header caused malformed physics CSV interpretation; both writers now share one schema function.
- A synthetic distant-line counterexample exposed ambiguity between small image pixels and large physical displacement; an inherited-model ground intercept check was added, with physical calibration still pending.
- Detailed external consultation was rejected by automatic review; the completed consultation used only abstract design information. Full project evidence remained local.
- The reviewer response contained a wrong symbol assumption; consultation did not replace source/image verification or acceptance.
- Standalone target compilation hit the existing IDE-only licensing restriction; no workaround was attempted and no target artifact was claimed.
- Some command/path assumptions and quoting errors caused avoidable retries. Known recipe and schema checks should precede broad validation.

## 修改建议及下一轮验收

- **CC-REPLAY-SCHEMA-SINGLE-20261109 [adopted]** Use one replay schema emitter for both host models and assert column count before evaluating quality.；负责人：codex；下次检查：Every model trace must retain finite fields, continuous timestamps and correct fan/speed columns.
- **CC-GUIDE-TASK-CONTRACT-20261109 [adopted]** Keep physical guide execution, task progress and distance datum separate, and fail closed when the guide was not admitted.；负责人：codex；下次检查：Future changes retain missed-guide and datum-preservation tests; full-course failures remain failures.
- **CC-CONSULT-MINIMUM-20261109 [adopted]** Start reviewer consultation with the minimum abstract question, then add only explicitly authorized evidence where needed.；负责人：codex；下次检查：Review call receipts and ensure project evidence is not included implicitly.

## 证据

- Local frozen manifests and source diff
- Verified abstract reviewer response and local handoff
- Final unit, segment, fault and full-course summaries
- No target artifact and explicit no-flash manifest

## 限制

- No physical repair or acceptance claim.
- Final full-course acceptance failed; target build and RAM/timing are unverified.
- Historical turn settings were evaluated, not blindly restored.
- No matched quality baseline or measured workflow speedup.
- No raw sessions, reasoning, source, photos, telemetry or databases uploaded.

# 2026-11-03-school-dash-position 工作流复盘

Move the provisional school-course dashed section to the adjacent segment above and refresh the local simulation bench.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：passed
- 开始：None
- 测量截止：2026-11-03T15:56:55.424308+08:00
- 墙钟秒数：None
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| observed_work_interval | 506.465 | seconds | First local clock to cutoff; excludes pre-clock work and later archive. |
| focused_tests_passed | 10 | tests | Node output. |
| browser_check_groups | 5 | groups | Rendered position, old solid, map digest, displayed result and exact camera pixels. |
| actual_c_baseline_runs | 1 | runs | Existing result reused on camera-check retry. |
| native_workers | 1 | workers | Read-only geometry and route-coverage review. |
| actual_opus_calls | 0 | calls | Database handoff only. |
| observed_check_retries | 2 | retries | Full-frame comparison replaced by relevant near-field comparison; stray browser-script parenthesis fixed. |
| tokens | 未知 | tokens | Unavailable. |
| cost | 未知 | currency | Unavailable. |
| coordination_wait | 未知 | seconds | Not separately timed. |
| review_archive_overhead | 未知 | seconds | Later receipt records archive interval; earlier report preparation not separately timed. |
| archive_approval_failures | 3 | attempts | Two shared-database requests and one private GitHub upload rejected by review service at capacity; commands not executed. |
| report_validation_retries | 1 | retries | Future performance limits moved out of unmet acceptance for this completed position correction. |

## 验收条件

- Move only the dashed segment; preserve hexagon, base course and controller.
- Verify live website geometry and refreshed camera replay.

## 已完成

- Six flat-ended dashes moved; original lower segment restored.
- One independent geometry review confirms other tape geometry and route unchanged.
- 10 focused tests and production build passed;5 browser assertions passed with no page errors.
- One actual C baseline and camera probes saved; historical evidence preserved.

## 未完成

- 无记录

## 收益与损耗观察

- New baseline ends out of bounds at5.642s and5.54m; not a lap time or evidence of improved control.
- Camera at the new dash position is invalid while original solid-line comparator is valid.
- Old-position full images differ because far rows see the moved upper segment; the restored near-field rows match exactly.
- No serial, firmware, vehicle movement, public deployment, new server or dependency installation.
- Independent review found zero route coverage over the moved section; limitation included in replay metadata.

## 修改建议及下一轮验收

- **LUOKIXI-WEB-school-map-coverage [adopted]** Check route coverage explicitly after moving an element and avoid claiming a full-course run tested an unvisited element.；负责人：codex；下次检查：Retain coverage evidence for the next map change.
- **LUOKIXI-WEB-small-map-correction [adopted]** Reuse deterministic evidence and keep position-only tasks to a narrow geometry/browser check; constrain camera comparisons to the intended region.；负责人：codex；下次检查：No speedup claim without a matched quality baseline.

## 证据

- engine-evidence.json
- browser-evidence.json
- school-dash-move-worker-evidence.json
- tests.log
- build.log

## 限制

- No matched baseline for workflow efficiency.
- Local simulation evidence only; no actual race completion.
- Reference route does not traverse the moved dashes; complete-lap and dashed-traversal performance unproven.
- Dimensions remain provisional.
- Shared-database registration and private-repository upload pending: automatic approval service returned model-at-capacity before execution; no writes were attempted through another route. Local review and worker evidence retained.

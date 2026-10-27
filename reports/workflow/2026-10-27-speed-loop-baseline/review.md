# 2026-10-27-speed-loop-baseline 工作流复盘

Prepare real-car low-speed-loop baseline, independently assess saved evidence, and prevent incomplete captures from misleading tuning.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md and WORKFLOW_DATABASE.md read 2026-10-27
- 验收状态：partial
- 开始：2026-10-27T14:19:25Z
- 测量截止：2026-10-27T14:29:44Z
- 墙钟秒数：619.0
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native reviewers | 1 | agents | One existing native reviewer completed a bounded source and synthetic-data check. |
| External model invocations | 0 | calls | Project handoffs only; no paid model dispatch. |
| Validator tests passed | 10 | tests | Unit tests plus integration with existing metrics. |
| New real-device tuning runs | 0 | runs | Owner not ready; no hardware action issued. |
| Firmware modifications | 0 | files | Local analysis wrapper only; current Opus firmware/tool preserved. |
| Observed historical test fragments | 6 | fragments | Three normal endings, two manual stops, one trailing truncation; first normal ending lacks start marker. |
| Analysis corrections | 1 | events | Boundary assertion revealed an initial fragment and final unfinished test; summary corrected rather than discarded. |
| Read-only query errors | 1 | events | Task query used a nonexistent schema column; task was resolved from verified handoffs instead. |
| Raw usage | 未知 | tokens | Provider usage unavailable. |
| Actual cost | 未知 | currency | No billing evidence. |
| Review/archive overhead | 未知 | seconds | Review overlapped preparation; archive interval separately recorded in receipt. |

## 验收条件

- Identify the currently flashed tuning firmware and owner readiness.
- Prepare baseline commands and validate measurement interpretation.
- Acquire repeated baseline tests before choosing a parameter change.

## 已完成

- Current tuning firmware flash receipt and boot parameters checked.
- Owner reports hardware not ready; all work remained offline.
- Independent source review reproduced a missing-sample timing error in the existing reporting path.
- Added a local validation layer reusing existing metric calculation; ten tests passed.
- Recomputed previous sparse logs and identified incomplete run boundaries.
- Initial and completed preparation handoffs355/356 sent to the project reviewer.

## 未完成

- Owner setup and repeated real-device baseline captures.
- Choose and verify one gain adjustment against a matched baseline.
- Opus coordination acknowledgement and serial operator confirmation.

## 收益与损耗观察

- Measured source/build status differs from physical readiness; owner response prevented interpreting preparation as an executed test.
- Dropping sample indices can reward damaged records with falsely short response time. Rejecting incomplete records is needed before parameter comparisons.
- A reused metrics implementation plus a narrow integrity gate avoided changing the live firmware during parallel hardware work.
- No matched workflow quality/timing baseline exists; net efficiency improvement remains unproven.

## 修改建议及下一轮验收

- **WF-CRAZY-SPEED-20261027-INTEGRITY [adopted]** Require complete ordered sample indices and normal completion before scoring tuning captures.；负责人：codex；下次检查：Next real capture is validated before any gain recommendation.
- **WF-CRAZY-SPEED-20261027-METADATA [proposed]** Freeze acquisition parameters in firmware capture metadata, or retain automatic dump before any subsequent parameter change.；负责人：opus；下次检查：Re-exporting an old capture cannot label it with newer settings.

## 证据

- Saved flash/boot evidence; current source and original analysis tool were read only.
- Local checked_step_report.py and ten passing tests; synthetic timing-error reproduction.
- Project handoffs354 read,355/356 created; older baseline summary remains local.

## 限制

- No real-device tuning improvement was demonstrated.
- Saved status telemetry is sparse and averaged; it does not establish high-rate oscillation or ISR timing.
- New capture windows cover only the first0.4s of each step and use conditioned feedback.
- The wrapper cannot prove firmware metadata provenance after a later parameter change; automatic dump workflow is still required.
- Raw logs, source and project tools are not uploaded in the workflow archive.


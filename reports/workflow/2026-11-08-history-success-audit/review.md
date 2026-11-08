# 2026-11-08-history-success-audit 工作流复盘

Audit historical successful controller against current early-turn failures, verify owner-authoritative track geometry, and defer physical calibration.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; frozen evidence and effective-source comparison
- 验收状态：passed
- 开始：2026-11-08T15:01:01.364720+00:00
- 测量截止：2026-11-08T15:15:44.919596+00:00
- 墙钟秒数：883.554876
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| claim_to_cutoff_wall | 883.554876 | seconds | Task-claim timestamp to review preparation; initial context lookup and later archive excluded |
| historical_source_files_each | 684 | files | Two historical trees checked against historical manifest plus documented profile difference |
| frozen_source_files_each | 688 | files | Frozen reference and deployed diagnostic checked against release manifests |
| historical_rows_decoded | 932 | rows | Strict count and continuous index with END delimiter |
| historical_planned_turns_matched | 15 | turns | Measured state3 direction sequence matches old route |
| current_rows_rechecked | 234 | rows | Complete latest saved diagnostic record |
| drawing_checks | 31 | checks | 25 dimension relations and6 regular-hex derived sides |
| route_distances_checked | 47 | entries | Route geometry sum equals frozen table entry |
| hardware_actions | 0 | actions | No serial, flash, commands or launches |
| agents_dispatched | 0 | agents | Single coordinator; historical reports treated as historical evidence |
| owner_clarifications | 1 | answers | Actual midpoint start confirmation |
| usage | 未知 | tokens | Not fully instrumented; archive interval reported separately in verified receipt |
| cost | 未知 | currency | Not fully instrumented; archive interval reported separately in verified receipt |
| total_tool_failures | 未知 | failures | Not fully instrumented; archive interval reported separately in verified receipt |
| coordination_wait | 未知 | seconds | Not fully instrumented; archive interval reported separately in verified receipt |
| review_archive_overhead | 未知 | seconds | Not fully instrumented; archive interval reported separately in verified receipt |
| full_round_wall | 未知 | seconds | Not fully instrumented; archive interval reported separately in verified receipt |

## 验收条件

- Identify successful historical version from original evidence
- Separate map, parameters, observations and causal hypotheses
- Preserve frozen source and car state
- Verify authoritative drawing and defer calibration

## 已完成

- Verified historical successful baseline against frozen source and HEX evidence, separating later reference labels from deployed identity.
- Re-decoded complete historical record and compared its state transitions with saved current failure telemetry.
- Compared effective control, geometry and route settings; distinguished observed missing admission from unrecorded rejection causes.
- Recorded owner clarification and excluded an inconsistent start-location hypothesis as the actual cause.
- Checked authoritative dimensioned drawing against frozen topology and all47 cumulative route distances.
- Verified frozen and deployed source inventories unchanged; no firmware edits, serial access, flash or launch.
- Produced local source diff, evidence manifest, geometry check and bounded diagnosis report.

## 未完成

- 无记录

## 收益与损耗观察

- Static website firmware label was not a live vehicle identity and its displayed number was a replay sector rather than a physical junction identifier.
- Observed state-machine non-admission is stronger evidence than attributing every stop to the previously suspected hold exit.
- Direct owner clarification ruled out using the battery-centre start alternative as an actual explanation.
- Some combined searches exceeded output budgets and several assumed metadata paths were absent; subsequent checks used exact files and structured summaries.
- Existing control initialization contains later overrides; final values were checked instead of reading the first assignment.
- No independent new reviewer was dispatched; original author attribution was retained for historical reports.

## 修改建议及下一轮验收

- **CC-HISTORY-STATE-CONTRACT-20261108 [adopted]** Compare actual state transitions and effective overrides before labelling a controller as restored to a successful baseline.；负责人：codex；下次检查：Future isolated revision links every changed control behavior to its baseline and matching segment evidence.
- **CC-NODE-ADMISSION-EVIDENCE-20261108 [proposed]** Preserve raw and filtered turn observations, distance residual, confirmation count and explicit rejection reason in a later isolated diagnostic.；负责人：codex；下次检查：First-corner segment distinguishes classifier, geometry and rate rejection before changes are promoted.

## 证据

- Historical source and HEX hash inventory
- Strict old-record parsing and saved diagnostic comparison
- Owner-confirmed start and authoritative drawing
- Dimension and cumulative route-distance checks
- Local read-only source diff

## 限制

- Physical failure remains unresolved; this audit is not a repair or a flash approval.
- No new full-lap simulation or hardware acceptance performed.
- Historical completion did not measure current physical55/60mm limits.
- No matched quality baseline; no speedup claim.
- No raw sessions, source, photos, telemetry or databases uploaded.

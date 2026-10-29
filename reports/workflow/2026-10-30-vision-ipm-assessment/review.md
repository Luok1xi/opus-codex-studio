# 2026-10-30-vision-ipm-assessment 工作流复盘

Review latest saved vehicle versions and assess sparse inverse perspective mapping, without changing the running firmware.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + TEAMHUB.md, read 2026-10-30
- 验收状态：partial
- 开始：2026-10-29T23:43:39Z
- 测量截止：2026-10-29T23:52:24.460351+00:00
- 墙钟秒数：525.460351
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Observed wall time to assessment cutoff | 525.46 | seconds | UTC timestamps; includes native reviews, coordination and report preparation; remote archive is later. |
| Native reviewers completed | 2 | agents | Two distinct read-only scopes returned saved evidence reports; coordinator consolidated. |
| Parser boundary checks | 3 | checks | Binary prefix, malformed row, empty valid capture checks passed. |
| Initial database permission failures | 6 | operations | Five acknowledgements and one handoff returned readonly; authorized retry succeeded. |
| Worker compiler probe failure | 1 | operations | One WSL probe denied; no retry. Reference formula evaluation explicitly not claimed as compiled C. |
| Workflow validation correction | 1 | operations | Validator rejected passed status with pending hardware acceptance; corrected to partial while assessment remains completed. |
| Production firmware modifications | 0 | files | Read-only review; pre/post hash comparison of 612 source files unchanged. |
| Peer review elapsed exclusive time | 未知 | seconds | Work overlapped coordinator; no complete same-clock exclusive interval attribution. |
| Coordination wait exclusive time | 未知 | seconds | No isolated wait accounting. |
| Token usage | 未知 | tokens | Provider usage for parent and children unavailable. |
| Actual cost | 未知 | currency | No billing evidence. |
| Review and archive overhead | 未知 | seconds | Not isolated from assessment; archive duration will be saved in receipt. |

## 验收条件

- Pin latest local source and saved run evidence
- Identify calibrated versus borrowed camera geometry
- Deliver concrete IPM integration and validation plan to Opus

## 已完成

- Pinned current source and saved artifact identities, and checked available run records.
- Separated partial distance compensation from full planar calibration; identified unit and planner integration constraints.
- Received two independent read-only reports; delivered the consolidated assessment to the project handoff database.

## 未完成

- Physical calibration, implementation, board timing, and real-car A/B are subsequent work, not completed by this assessment.
- Opus has not acknowledged the new final handoff in this round.

## 收益与损耗观察

- The latest live tree had advanced beyond the last design handoff. File/script and saved-run verification prevented a stale version assessment.
- A complete route status is not a certified lap time; an empty export is not evidence of a whole-lap recording.
- Two reviewers covered source contracts and calibration provenance separately; their findings were consolidated without duplicate firmware changes.
- Initial database writes required authorized escalation; no production rework occurred because this was an assessment.
- No matched task/quality baseline exists, so net workflow speedup remains unproven.

## 修改建议及下一轮验收

- **CRAZY-CIRCUIT-IPM-20261030-EVIDENCE [adopted]** Before geometry changes, pin the newest source and distinguish raw run evidence, author reports, and calibration provenance.；负责人：codex；下次检查：Next candidate report references the exact source snapshot and held-out physical calibration error.
- **CRAZY-CIRCUIT-IPM-20261030-SHADOW [proposed]** Evaluate new geometry on identical image frames before changing control units or speed policy; record bounded timing separately.；负责人：opus；下次检查：Receive actual peer review and same-input shadow comparison before claiming acceptance.

## 证据

- Local assessment and two independent audit artifacts (hashes in evidence.json).
- Aggregate parser/source freeze evidence.
- CRAZY-CIRCUIT handoffs 466 and 467.

## 限制

- Source-to-HEX rebuild equivalence and current hardware firmware identity were not verified.
- No new physical calibration, simulation, flash, serial control, or live test was performed.
- Report archive is not complete until private visibility and remote exact content are verified.

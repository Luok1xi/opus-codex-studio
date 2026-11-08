# 2026-11-08-ouc09-photo-runs 工作流复盘

Diagnose three photographed09R2 stops using preserved telemetry and a frozen-controller reproduction.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + evidence-first physical diagnosis
- 验收状态：partial
- 开始：2026-11-08T13:07:14.528986+00:00
- 测量截止：2026-11-08T13:16:36.964382+00:00
- 墙钟秒数：562.435396
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| measured_analysis_wall | 562.435396 | seconds | First saved analysis timestamp to cutoff; initial capture preparation preceded it |
| photo_runs | 3 | runs | Owner order and complete wireless intervals |
| board_samples | 194 | samples | Header, contiguous indices and END |
| software_reproductions | 1 | cases | Frozen actual controller binary and route code |
| unchanged_source_files | 688 | files | Release hash manifest |
| firmware_edits | 0 | files | No firmware writes |
| flash_actions | 0 | actions | No flasher invocation |
| remote_starts | 0 | actions | No launch command |
| readonly_queries | 3 | queries | Parked S/P/I intent log |
| agents_dispatched | 0 | agents | Single coordinator |
| usage | 未知 | tokens | No provider accounting |
| cost | 未知 | currency | Unavailable |
| tool_failures | 未知 | failures | Not instrumented |
| archive_overhead | 未知 | seconds | Measured in archive receipt |

## 验收条件

- Preserve latest record and identify actual run intervals
- Separate observed facts from root-cause hypotheses
- Do not alter the running baseline while collecting evidence

## 已完成

- Preserved the last run onboard record before reboot:194 contiguous20ms samples with terminator.
- Aligned three owner photos in order to three complete wireless launch/stop intervals; all stopped with code3.
- Separated observed photo location from internal route progress and inferred wrong-branch trajectory.
- Reproduced the dash hold boundary handing a large fresh line error to saturated steering in the frozen controller.
- Verified688 source inputs unchanged and restored passive capture; no firmware/parameter change or flash.

## 未完成

- Implement guarded lane reacquisition and straight-junction route isolation in a separate candidate, then rerun full-course acceptance.
- Physical acceptance remains open; no claimed repair or full-lap success.

## 收益与损耗观察

- The last run record was saved before another start; earlier two onboard records had already been overwritten and were not reconstructed as originals.
- Photos locate a different physical branch from the planned first-pass route; internal node index is not ground-truth position.
- A finite bridge timeout alone is insufficient if it hands off immediately to a large but nominally valid line error.
- Full-course simulation passed but did not cover the photographed real branch-entry and interrupted-line conditions.
- No matched efficiency baseline; no speedup claim.

## 修改建议及下一轮验收

- **CC-DASH-REACQUIRE-20261108 [proposed]** Gate dash-to-line handoff on reliable own-lane reacquisition and preserve finite failure limits; add the recorded large-error boundary case before integration.；负责人：codex；下次检查：A new candidate rejects the reproduced saturated handoff and passes the unchanged full-route suite.

## 证据

- Three owner-labeled photos and source hashes
- Three boot-consistent wireless intervals
- Complete194-row onboard record
- Unchanged source/binary hashes and diagnostic output

## 限制

- Exact moving path and actual timeout sub-branch were not recorded.
- No new firmware was implemented or flashed in this analysis round.
- No physical full-lap acceptance.
- Only sanitized aggregate workflow records are uploaded.

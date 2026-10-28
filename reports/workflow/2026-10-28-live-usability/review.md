# 2026-10-28-live-usability 工作流复盘

Improve the real-car tuning interface, preserve received data, and measure browser rendering under matched synthetic input.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-10-28T06:09:39Z
- 测量截止：2026-10-28T06:48:13+00:00
- 墙钟秒数：2314.0
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native workers | 4 | agents | Performance, official-source research/review, baseline/browser preparation, and browser continuation after interruption. |
| External Opus calls | 0 | calls | Project database handoff only; no acceptance reply claimed. |
| Provider usage | 未知 | tokens | Not exposed by runtime. |
| Model cost | 未知 | currency | No billing record. |
| Interruption duration | 未知 | seconds | A user-side interruption stopped workers/services; total wall interval includes it. |
| Review/coordination overhead | 未知 | seconds | Interleaved with tests/publication; archive receipt records subsequent archive interval. |
| After browser performance run | 32.069 | seconds | Browser report timestamps; same two viewport workloads. |
| Final browser interactions | 7.425 | seconds | 34 checks, after two test-only timing/locator corrections. |
| Interaction executions | 3 | runs | Two failing test assertions were corrected; no product code changed between these runs. |

## 验收条件

- Practical task-focused controls, correctly scaled parameter forms, no automatic hardware commands, complete recorded/exported data, responsive layout, measured browser comparison and existing-site publication.

## 已完成

- Added speed/vision/all views, named gain inputs, draft-safe readback, freeze-with-reception and log search.
- Removed offscreen/background visual work, bounded battery SVG output, cached chart preparation and reduced repeated log formatting.
- 38 unit tests and 34 mock browser checks passed; same 21000 records retained at both widths.
- Published original site with unchanged public audience and preserved replay data.

## 未完成

- 无记录

## 收益与损耗观察

- Official Serial Studio and PlotJuggler workflows informed task-focused controls; installed Playwright and native browser observers sufficed. Plugin discovery found no specific missing capability worth adding.
- Independent review caught camera/PID selector collision and draft-status inconsistency; both fixed and covered in browser checks before publication.
- Full synthetic browser comparison while watching curves: desktop long tasks 9 to 0, narrow viewport 25 to 0; same input and record totals. These are product measurements, not a matched multi-agent workflow baseline.
- Chart microbenchmark improved static hover/statistics but slightly slowed changing-window preparation (0.598 to 0.656ms); do not claim a universal speedup.
- Initial browser baseline was extended to include actually watching curves; first top-only result retained separately.
- Connection-refused runs produced no valid samples. Existing service was restored using the project launcher, local backups and migration plan.
- Interaction reruns corrected test timing/locator assumptions for throttled offscreen logs, not product defects.
- No matched single-agent workflow baseline or provider usage; net coordination efficiency is unknown.

## 修改建议及下一轮验收

- **WF-WEB-PERF-20261028 [adopted]** Collect top-of-page and visible-chart workloads plus recording/export integrity in the initial browser plan; use condition waits for throttled UI.；负责人：codex；下次检查：Next dashboard change reuses fixed synthetic inputs and verifies equal retained data before reporting rendering improvement.

## 证据

- evidence.json; source hashes, local browser reports/screenshots, unit logs, build and publication receipts.

## 限制

- One machine and one matched rendering pair; no generalized performance claim.
- No physical serial throughput measurement, flashing or motor action.
- No cloud-browser or chart-library dependency added.
- Local database backups remain local and excluded from publication/archive.

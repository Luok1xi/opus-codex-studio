# 2026-10-30-control-rate 工作流复盘

Preserve paused vision research, diagnose real archived yaw-rate overshoot and repair a separate tuning-state saturation defect.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md / TEAMHUB.md
- 验收状态：partial
- 开始：2026-10-30T07:57:47Z
- 测量截止：2026-10-30T08:15:53.384379+00:00
- 墙钟秒数：1086.384379
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Wall time to analysis delivery | 1086.384379 | seconds | Includes checkpoint, coordination, analysis and patch; overlaps native workers. |
| Primary archived records | 2 | captures | Two complete 1000-row diagnostic captures; cadence validated against versioned source. |
| Extracted-C assertions | 6523 | assertions | Repeated per-tick assertions and setup; not distinct cases. |
| Candidate added lines | 2 | lines | One guard/clamp plus one explanatory comment; tuning branch only. |
| Target builds | 0 | builds | Target compilation is pending; host verification only. |
| Hardware operations | 0 | actions | No serial, flash or vehicle motion. |
| Actual model usage | 未知 | tokens | No provider usage evidence. |
| Actual cost | 未知 | currency | No billing evidence. |
| Exclusive coordination and review overhead | 未知 | seconds | Overlaps analysis; no exclusive measurement. |

## 验收条件

- Preserve interrupted IPM work
- Analyze actual 2026-10-29 logs against matched source
- Prepare bounded control fixes and useful tuning steps based on evidence

## 已完成

- Preserved interrupted work in a verified checkpoint.
- Matched actual archived samples and cadence to reconstructed source, corrected reported peak values and separated command-transition effects.
- Prepared a two-line tuning-only saturation fix with actual-C regression and sanitizer checks; preserved production files.
- Prepared a bounded current-load test sequence using the existing full-firmware tuning entry.

## 未完成

- Full ADS build, hardware runs and independent external acceptance are pending.
- Exact cause attribution among PI gains, feedback delay, wheel response and switching needs new measurements.
- No claim that competition-loop stability is fixed.

## 收益与损耗观察

- The initial file search and unfiltered database output were too broad; bounded saved JSON summaries were more usable.
- The official source tree was older than the experimental tree used on the vehicle; version ledger and reconstructed-source hashes resolved the mismatch.
- Raw capture cadence differed between diagnostic and whole-lap versions; assuming current cadence would corrupt timing estimates.
- A real tuning-only state saturation issue is separate from race-mode overshoot.
- One synthetic regression fixture initially did not reach its intended output range; stimulus was corrected without changing the production fix.
- The two-line change affects no race-mode gain or formula; twelve test trajectories are injected feedback, not physical validation.

## 修改建议及下一轮验收

- **CRAZY-RATE-VERSION-CADENCE [adopted]** Bind every waveform to firmware version, sample interval and raw row index before comparing control responses.；负责人：codex；下次检查：Next capture must retain target, feedback and versioned cadence.
- **CRAZY-RATE-LIMIT-STATE [adopted]** Match tuning-controller state to the downstream applied limit and independently verify normal-mode equivalence.；负责人：codex；下次检查：Target build and paired physical test remain necessary.
- **CRAZY-RATE-SEPARATE-SWITCH [proposed]** Tune fixed-target response before changing state-transition output handling.；负责人：opus；下次检查：Compare signed step responses before changing the turn-exit command.

## 证据

- Sanitized evidence.json retains capture and patch checksums; full records and source stay local.

## 限制

- No matched quality baseline establishes workflow speedup.
- Model tests use injected feedback and do not establish physical stability.
- Source/host, archived data and new physical testing are distinct evidence levels.
- No new physical run or target binary was produced.

# 2026-10-28-speed-loop-plan 工作流复盘

Recompute current production speed-loop runs and coordinate the owner decision to tune wheels independently before angular-rate and outer-loop work.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-10-28T09:38:55Z
- 测量截止：2026-10-28T09:51:04.525122+00:00
- 墙钟秒数：729.525122
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native independent analysts | 1 | agents | Source and four-capture independent review. |
| Complete captures | 4 | captures | Each n999/stride2 with500 rows. |
| External inference calls | 0 | calls | Actual Opus project updates read; current priority sent by database. |
| Provider usage | 未知 | tokens | Unavailable. |
| Cost | 未知 | currency | Unavailable. |
| Coordination/review overhead | 未知 | seconds | Interleaved; archive interval starts at cutoff. |

## 验收条件

- Use current production captures and controller source; distinguish measured stability from hypotheses; provide a single-variable next-run plan and synchronize owner priority.

## 已完成

- Independently recomputed four complete production captures with one common 500ms steady-state window.
- Confirmed original gains remain the current baseline; target80 has good steady-state tracking but left startup overshoot remains about39%; target40 oscillates.
- Recorded a right-wheel-first A/B/A proposal with left gains fixed and a clear rollback; no parameter was sent.
- Read Opus file-ownership and angle-entry handoffs; synchronized the owner instruction to finish speed-loop stability before other loops.
- Clarified angular-rate inner loop, angle/vision outer loop, and underlying wheel-speed loops from actual code.

## 未完成

- 无记录

## 收益与损耗观察

- Latest project evidence showed physical tests already existed; reusing them avoided restarting diagnosis or modifying the controller without data.
- Unified measurement windows explain differences from earlier reported standard deviations.
- Mean target tracking alone concealed low-speed oscillation; startup and steady-state metrics were separated.
- Encoder counts are limited before capture, runs are single trials, battery voltage differs, and one gain candidate also changed right Ki; causal confidence is limited.
- The owner explicitly prioritized speed-loop stability while Opus was preparing an angular-rate entry; synchronized that priority without overwriting concurrent code.
- Some initial reads were broader than necessary; subsequent inspection used exact capture files and controller sections.
- No matched quality-controlled workflow baseline; net efficiency remains unproven.

## 修改建议及下一轮验收

- **WF-WHEEL-SINGLE-FACTOR-20261028 [proposed]** Keep the other wheel gains and physical test conditions fixed; compare one gain change against repeated baselines before adopting it.；负责人：opus；下次检查：New paired physical captures show repeatable benefit without worsening the other wheel or startup behavior.
- **WF-LOOP-PRIORITY-20261028 [proposed]** Finish repeatable wheel-speed acceptance before switching physical tests to angular-rate or outer-loop tuning.；负责人：codex+opus；下次检查：Recipient acknowledges priority and records speed-loop acceptance against agreed criteria.

## 证据

- evidence.json; local peer results and source review; project handoffs371/373/375.

## 限制

- Planning and evidence review are complete; the proposed gain candidate and stable speed-loop acceptance are not physically verified.
- No flashing, serial access, parameter writes or motor starts.
- No promise of faster-than-simulation lap time; comparison requires matched course and timing rules.
- No raw captures, project source, live databases, credentials or conversations are uploaded.

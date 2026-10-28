# 2026-10-28-real-tune-direction 工作流复盘

Participate in physical-car tuning by auditing saved evidence and coordinating reverse-motion and drift diagnosis.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-28T06:52:01Z
- 测量截止：2026-10-28T07:02:35.620640+00:00
- 墙钟秒数：634.62064
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native audit workers | 1 | agents | One read-only source/capture reviewer. |
| External Opus inference calls | 0 | calls | CLI doctor reported login required; used project DB handoff instead. |
| Project handoffs | 2 | records | Records 360 and 361; no recipient acknowledgement at cutoff. |
| Provider usage | 未知 | tokens | Unavailable. |
| Model cost | 未知 | currency | No billing data. |
| Coordination and review overhead | 未知 | seconds | Interleaved; archive timing recorded separately in receipt. |
| Firmware edits by this round | 0 | files | Preserved actively shared firmware pending physical mapping. |
| Test rework | 未知 | runs | No new firmware implementation or acceptance run. |

## 验收条件

- Resolve direction mapping before gain changes; verify current real evidence and coordinate edits with the active operator.

## 已完成

- Read the latest saved floor captures and current firmware call paths; independently reproduced step metrics.
- Distinguished the corrected gyro bias in the latest run from the earlier contaminated calibration.
- Owner confirmed camera-facing end is forward; positive test targets currently move physically backward.
- Sent source-specific coupled drive/encoder mapping advice and validation order through two project database handoffs.

## 未完成

- Opus acknowledgement and agreement on edit ownership are pending.
- Physical wheel/channel and manual gyro sign checks, firmware integration and real-car acceptance remain pending.

## 收益与损耗观察

- A fresh capture superseded the earlier bad gyro calibration during this round; current and previous conditions were kept separate.
- Positive encoder feedback does not prove physical forward motion; owner observation was necessary.
- One directory listing and context output were too broad/truncated; later reads used bounded fields. A broad file search hit unrelated denied directories and yielded no useful test harness.
- Initial non-elevated GitHub read failed due to restricted network, then the authorized scoped read succeeded.
- Native independent audit is separate from actual Opus; current Opus findings were read but no response to these handoffs was received.
- No matched workflow baseline; net efficiency is unproven.

## 修改建议及下一轮验收

- **WF-REAL-MAPPING-20261028 [proposed]** Record physical front, wheel/channel identity, encoder sign and gyro sign before accepting a speed-loop trace.；负责人：codex+opus；下次检查：Next real run must attach verified mapping, stopped calibration, selected profile and firmware identity.

## 证据

- evidence.json; local audit and project handoffs 360/361.

## 限制

- Saved capture analysis only; no direct serial access, flashing or motor start by this round.
- No raw captures, sessions, firmware or project database uploaded.
- Gain candidates and physical forward mapping have not been accepted on the car.

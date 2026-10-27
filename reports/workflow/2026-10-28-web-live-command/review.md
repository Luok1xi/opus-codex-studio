# 2026-10-28-web-live-command 工作流复盘

Add sending and device replies to the existing real-car website using its current serial connection.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-10-27T16:07:32Z
- 测量截止：2026-10-27T16:32:14+00:00
- 墙钟秒数：1482.0
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native subagents | 2 | agents | Protocol/browser review and publication preparation, bounded separate scopes. |
| External Opus calls | 0 | calls | Only project database handoff; no current Opus response. |
| Raw model usage | 未知 | tokens | Provider usage unavailable. |
| Model cost | 未知 | currency | No billing record. |
| Coordination wait | 未知 | seconds | Overlapped work, not instrumented. |
| Review and archive overhead | 未知 | seconds | Archive receipt will record its actual subsequent interval; reading workflow rules and preparing review interleaved with task. |
| Source correction passes | 1 | passes | Self-review strengthened own-property validation before tests; no test failure. |
| Observed infrastructure failures | 3 | operations | Canonical Git read denied; localhost socket denied; first publish helper TLS handshake failed. Retried with scoped authorization / certificate-validating OpenSSL. |

## 验收条件

- Visible command controls in existing page, exact newline encoding, valid bounds, visible replies/errors, no automatic command, local build and public deployment.

## 已完成

- Added bounded hwtest commands and independent device-reply view.
- 30 unit tests, ESLint, build and 22 mock browser checks passed.
- Published to the existing public site; preserved replay data and prior audience.

## 未完成

- 无记录

## 收益与损耗观察

- Reused existing writer and parser; no dependencies, firmware changes or extra serial connection.
- Subagent protocol review identified hidden/paused-log risk; independent reply panel addresses it.
- Publishing helper initially failed Windows TLS handshake; process-local OpenSSL preserved certificate verification and succeeded.
- Browser checks repeated once for close-up screenshots, an avoidable verification overhead.
- No matched workflow baseline; no speedup claim.
- Review schema rejected placing out-of-scope physical follow-up under unmet acceptance; moved it to existing limits. No acceptance criterion was removed.

## 修改建议及下一轮验收

- **WF-WEB-SERIAL-SEND-20261028 [adopted]** Combine serial writer assertions, viewport coverage and close-up screenshots in one browser run.；负责人：codex；下次检查：Next serial UI change should collect all evidence in one run unless a failure requires a repeat.

## 证据

- evidence.json; local source manifest, mock browser results, build log, package and deployment receipts.

## 限制

- No physical serial, flashing or motor actions.
- Fresh status gating is a UI precaution, not a hardware interlock.
- No Opus response or acceptance claimed.

# 2026-10-30-prelim-yaw-tune 工作流复盘

Build and flash full yaw-tuning firmware, verify idle startup, and prepare the physical test without remote launch.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md and TEAMHUB.md
- 验收状态：partial
- 开始：2026-10-30T10:11:51Z
- 测量截止：2026-10-30T10:30:34.709913+00:00
- 墙钟秒数：1123.709913
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Wall time to verified flash and idle check | 1123.709913 | seconds | Includes source drift review, ADS setup, flash wrapper recovery and connection loss. |
| Target compiled C units | 173 | units | Fresh isolated ADS workspace build log. |
| Build log elapsed | 5.168 | seconds | Compiler-reported elapsed; excludes setup. |
| Target errors | 0 | errors | Build log. |
| Existing warnings | 11 | warnings | Same warning classes as base. |
| Flash executions | 1 | executions | One programmer log, programming and verification pass. |
| Serial commands sent | 0 | commands | First read-only capture; later setup failed before port open. |
| Remote vehicle starts | 0 | commands | No start command or physical S5 operation by agent. |
| Actual usage | 未知 | tokens | No provider accounting. |
| Actual cost | 未知 | currency | No billing evidence. |
| Exclusive review overhead | 未知 | seconds | Overlapping review, no isolated measure. |

## 验收条件

- Build full existing firmware with reviewed tuning-state clamp only
- Check startup and tuning gates
- Flash only after current stopped/downloader-ready confirmation and successful target validation
- Verify flash receipt and idle startup; no remote vehicle launch

## 已完成

- Verified source drift is limited to preserved comments, then built the reviewed two-line change in an isolated full-firmware workspace.
- Independent startup, mode, timeout and export-gate review passed for this bounded test.
- One target programming and verification succeeded; recovered the receipt after the wrapper remained waiting.
- Read idle startup telemetry showing healthy IMU, battery and zero wheel output.

## 未完成

- Owner disconnected downloader to switch to wireless, then deferred hardware work until the battery is charged; tuning mode has not been acknowledged.
- Physical step test and stability improvement remain unverified.
- A new black-display report has only a source-level pin-mapping review; actual cause is unknown.

## 收益与损耗观察

- Fresh source verification detected three preserved comment-only changes instead of silently overwriting parallel work.
- The programmer completed while its wrapper remained waiting; independent log verification allowed receipt recovery without repeated flash.
- Serial preparation refused to proceed after the port disappeared; owner later confirmed physically unplugging the downloader.
- An unavailable optional Python serial dependency was avoided by using the installed .NET serial interface.
- A local report helper needed one encoding-name correction; one inbox command needed argument correction.
- One native reviewer independently audited startup/test gates and later the screen path. Opus received file/database handoffs; no new Opus review response was received.
- Further device work and questions stopped at the owner request to wait for charging.

## 修改建议及下一轮验收

- **CRAZY-FLASH-WAIT-RECOVERY [proposed]** Review bounded programmer-process waiting and durable log-first receipt recovery in the shared burn wrapper.；负责人：dsh；下次检查：Investigate a replayable process-wait test without reflashing hardware.
- **CRAZY-RATE-READBACK [adopted]** Require fresh stopped-mode readback after every reset or reconnect before the operator presses S5.；负责人：codex；下次检查：Next physical run must have a matching current side/target/gain acknowledgement.

## 证据

- Sanitized aggregate evidence and artifact hashes in evidence.json; source and raw telemetry remain local.

## 限制

- No new driving trial, no PI optimization or physical stability claim.
- No matched workflow quality baseline; speedup not established.
- Receipt recovery is disclosed and is not a second flash.
- Display hardware mapping and the black-screen cause remain unverified.

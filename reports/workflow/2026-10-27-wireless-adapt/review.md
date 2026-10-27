# 2026-10-27-wireless-adapt 工作流复盘

Adapt low-throughput wireless tuning with a tested nonblocking candidate and evidence-based transport plan.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md and WORKFLOW_DATABASE.md read2026-10-27
- 验收状态：partial
- 开始：2026-10-27T14:42:54Z
- 测量截止：2026-10-27T15:49:16.912862+00:00
- 墙钟秒数：3982.912862
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native agents | 3 | agents | Firmware audit/patch, protocol validator, isolated build; consolidated by coordinator. |
| External model calls | 0 | calls | One CLI readiness probe reported login unavailable; project database handoffs only. |
| Firmware test groups | 7 | groups | Actual extracted functions, 736 checks; baseline negative control failed as expected. |
| Capture validator tests | 16 | tests | Synthetic v4/v5 boundary tests and real saved five-run input. |
| Saved records verified | 8600 | records | Five complete historical captures, not newly acquired device data. |
| ADS build duration | 5.874 | seconds | Compiler-reported build time; excludes import, setup, review and archive. |
| Hardware actions | 0 | actions | No serial connection, flashing or motor command. |
| Observed inter-turn tool gap | 2581 | seconds | Last pre-interruption timestamp14:52:48Z to first resumed timestamp15:35:49Z; not a precise measure of pause or active work. |
| Source version refresh | 1 | events | Detected v4 to v5 change after user resumed; reused new queue instead of implementing stale plan. |
| Coordinator read-only command failures | 2 | events | Unsupported query option and absent old build-script filename; corrected from actual help and paths. |
| Validator test environment rework | 1 | events | Worker reported temp-directory permission failure; replaced CLI test with in-memory invocation. |
| Raw usage | 未知 | tokens | Provider usage unavailable. |
| Actual cost | 未知 | currency | Billing evidence unavailable. |
| Review overhead | 未知 | seconds | Review overlaps implementation; archive interval recorded separately in receipt. |

## 验收条件

- Preserve local control/capture rate while bounding wireless foreground work.
- Reuse current peer changes and provide reproducible tests and target build.
- Distinguish implemented candidate, protocol proposal, and real-device validation.

## 已完成

- Audited actual tuning build and separate production library; identified blocking UART path and ignored unsent bytes.
- Detected live source advancement, preserved active files and reused its queue in a three-site candidate patch.
- Candidate yields on RTS busy or full FIFO, sends at most16 bytes per service, and restricts reinitialization to parked states.
- Seven native C test groups passed; original code failed the same nonblocking contract as expected.
- Full isolated ADS build passed with zero errors and warnings; source hashes stable and output hash verified.
- Added v4/v5 capture integrity gate with original sample indices;16 tests passed and8600 saved records accepted.
- Offline packing experiment preserved every value in five captures and quantified byte savings without claiming radio throughput.
- Concrete proposal and tested candidate delivered through project handoffs358/359; recipient acknowledgement pending.

## 未完成

- Opus independent review and integration into the actively edited firmware.
- Hardware validation of UART FIFO/RTS interaction, actual radio throughput, losses and control ISR timing.
- Compact binary live protocol and complete per-block reliable wireless export remain proposals, not deployed features.
- Existing mutable capture metadata and command validation weaknesses require a separate coordinated fix.

## 收益与损耗观察

- Wall-clock interval includes an interrupted turn; it is not continuous active work time.
- Refresh of source identity prevented implementing against a stale version.
- Existing queue was reused; only sender, service placement and retry guard changed.
- Capture validation prevents a changed row format or stride from receiving a falsely favorable zero score.
- No matched quality-controlled workflow timing baseline exists; net efficiency remains unproven.

## 修改建议及下一轮验收

- **WF-CRAZY-WIRELESS-20261027-REFRESH [adopted]** Refresh source hashes after an interrupted turn before continuing an implementation plan.；负责人：codex；下次检查：Next resumed peer-edit task records source identity and preserves concurrent changes.
- **WF-CRAZY-WIRELESS-20261027-LAYERS [adopted]** Report build, host tests, wire-format experiments and physical link validation as separate acceptance levels.；负责人：codex；下次检查：Hardware follow-up adds measured throughput and timing without reusing offline claims.
- **WF-CRAZY-WIRELESS-20261027-CAPTURE [proposed]** Freeze capture metadata and coordinate a compact CRC/sequence-based block export with the receiver.；负责人：opus；下次检查：Peer acknowledgement and tests for corruption, missing blocks and interrupted runs before integration.

## 证据

- Local source manifest, candidate patch, seven-group C test receipt and negative control.
- Isolated ADS build log, map,649 stable source hashes and artifact digest.
- Sixteen-test capture validator and five-run integrity output.
- Local byte-budget experiment and project handoff readback; raw records remain local.

## 限制

- No current-task Opus reply or independent approval received.
- No live-device action or radio performance improvement demonstrated.
- Source-level periodic status budget excludes events and capture export.
- Existing live status is averaged;250Hz export skips alternate500Hz samples.
- ASCII has no CRC and cannot prove numeric integrity or capture-parameter provenance.
- Only sanitized workflow reports and aggregate evidence are archived; no project source or raw logs uploaded.

# 2026-11-01-live-recording-start 工作流复盘

Consolidated manual-tuning diagnosis, including post-reboot telemetry, zero-offset inspection and a peer-acquired original camera frame.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md / TEAMHUB.md
- 验收状态：partial
- 开始：2026-11-01T06:21:54.764339+00:00
- 测量截止：2026-11-01T08:13:45.999672+00:00
- 墙钟秒数：6711.235333
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Wall time from first recorded check | 6711.235 | seconds | Includes owner wait, capture, diagnosis and review preparation; not exclusive agent work. |
| Geometry fixture executions | 9 | cases | Frozen vision sources with runtime undefined/bounds/float-conversion checks; synthetic only. |
| Stopped-status guard checks | 6 | cases | One valid stopped input and five incomplete or non-stopped inputs. |
| Coordinator read-only serial commands | 1 | commands | One earlier stopped log export; zero new commands by the coordinator during this reboot check. |
| Export rows expected and received | 175 | rows | Contiguous zero-based indices; complete terminator; no missing or malformed rows. |
| Firmware flashes | 0 | flashes | No production build or flash; host-only diagnostic compilation. |
| Motion parameter changes | 0 | changes | No gains, camera settings, route thresholds or launch commands changed. |
| Model usage | 未知 | tokens | No provider accounting. |
| Cost | 未知 | currency | No billing data. |
| Exclusive review overhead | 未知 | seconds | Not timed separately. |
| Peer read-only requests in reboot check | 3 | commands | Peer handoff reports one register query and two image requests; not coordinator commands. |
| Verified original image payload | 22560 | bytes | 188x120 dimensions, exact frame terminator and byte-for-byte saved raw match. |

## 验收条件

- Preserve received data and exclusive port ownership.
- Separate source, synthetic experiments, sampled telemetry and physical validation.
- Obtain evidence before changing motion parameters.

## 已完成

- Closed receiver segments and fresh resumed heartbeats were verified through bounded exclusive handovers.
- Driver-disabled starts were separated from later tracking failures.
- Nine direct-source geometry fixtures and six stopped-status guard cases were checked.
- One stopped-only log-read command returned all 175 indexed rows without missing or malformed rows.
- An independent reviewer checked state decoding; the owner located the manual sweep beyond the power symbol.
- The collaborating reviewer supplied camera calibration references, checked against old raw images.
- Fresh uptime, mode and camera counters confirmed data after the owner rebooted.
- A persistent stationary-rate discrepancy was separated from IMU communication readiness; source confirms boot calibration already occurs.
- A real peer acquired a full original image; payload length, terminator and exported raw bytes matched independently.

## 未完成

- Physical camera calibration and a stationary reboot zero check remain pending at cutoff.
- The exact cause of the earlier missed turn remains unproven; no new driven-lap acceptance.
- Firmware identity is based on the ledger, not a chip readback.

## 收益与损耗观察

- Same round and objective as startup; this report supersedes the startup snapshot and consolidates later evidence.
- One native reviewer was reused for bounded independent checks; the real collaborating reviewer provided a separate project handoff, not a fabricated response.
- Width rejection was a tentative hypothesis corrected by source inspection before a firmware edit.
- The owner clarified that the manual sweep ended beyond the element near the later switch/corner; a latched stop code was not treated as a new stop.
- A status-label correction was needed in the startup review. Two earlier approval timeouts blocked archive receipts; later normal approval succeeded and receipts were stored.
- Capture rotations were exclusive but had documented gaps; no uninterrupted recording claim.
- The bounded WSL check required normal approval after access denial; local parser diagnostics corrected one mistaken database column name.
- The compact retained-run export succeeded over wireless; earlier full-image transport limitations were not generalized to all read-only diagnostics.
- Same ongoing tuning objective; this is a new evidence revision, not a recursively opened review round.
- An incoming port-intent message overlapped a newly started receiver. The peer used graceful stop and resume; the coordinator subsequently read shared files without opening a competing port.
- A failed image request lacked a header; a later request returned a complete frame. Prior wireless transport concerns must not be promoted into a categorical impossibility claim.
- The source performs boot zero averaging without a stillness-quality gate. Prelaunch calibration has a variability gate but then launches the vehicle, so it was not offered as a harmless standalone calibration command.
- The new image supports a camera-view mismatch; numerical pitch estimates still depend on camera-model assumptions.

## 修改建议及下一轮验收

- **CRAZY-PASSIVE-RECORD-DURABILITY [adopted]** Preserve raw capture, heartbeat, closure receipts and explicit serial ownership through diagnostic handovers.；负责人：codex；下次检查：Continue reconciling closed-file counts and declared gaps.
- **CRAZY-STOPPED-LOG-BEFORE-RESET [adopted]** Read and validate the retained run before a new launch or power cycle when that evidence is relevant.；负责人：codex；下次检查：Verify complete row indices and use sampled-state limits in conclusions.
- **CRAZY-PORT-OWNERSHIP-REFRESH [adopted]** Refresh both shared receiver heartbeat and newest project intent before opening the port; preserve graceful handover and distinguish partial images from validated frames.；负责人：codex；下次检查：Confirm no overlapping open attempts on the next coordinated capture.

## 证据

- Sanitized aggregate checks in evidence.json.
- Raw photographs, serial data and firmware source remain local; shared project handoff retains their locations.

## 限制

- No matched quality baseline; efficiency benefit is unproven.
- Photographs are not original camera frames.
- Retained-run association depends on continuity, because the legacy log has no run identifier.
- Twenty-millisecond samples may miss brief preparatory states; absence of sustained turn activation does not identify the failed gate.

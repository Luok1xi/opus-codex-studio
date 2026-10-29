# 2026-10-29-prelim-car-port 工作流复盘

Accept owner-observed overcorrection, identify the missing T-junction port, and prepare the finalized preliminary-map simulation algorithm for physical tuning.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-28T14:37:30Z
- 测量截止：2026-10-29T00:57:57.137675+00:00
- 墙钟秒数：37227.137675
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Independent native workers | 3 | workers | Two bounded workers before interruption and one independent verifier after resumption. |
| Low-speed-table host assertions | 614 | assertions | ActualPID_Init baseline/candidate comparison. |
| Preliminary-port host assertions | 25827 | assertions | 34 plus25793 actual-C assertions; source hashes stable on final run. |
| Coordinator flashes | 0 | flashes | No flasher was launched. |
| Coordinator serial opens | 0 | opens | Read-only OS device inventory only in this round. |
| Token usage | 未知 | tokens | Provider usage unavailable. |
| Cost | 未知 | currency | Unavailable. |
| Active work duration | 未知 | seconds | The observed interval includes an explicit overnight interruption; wall time is not active time. |
| Coordination and review overhead | 未知 | seconds | Interleaved; not independently timed. |
| Matched workflow speedup | 未知 | percent | No same-input same-quality baseline. |

## 验收条件

- Use owner observations without repeated confirmation; preserve current hardware fixes; build and check the preliminary algorithm; flash only an available device.

## 已完成

- Integrated a five-line low-speed gain ramp into the canonical PID initialization, preserving concurrent uncommitted work;614 actual-C assertions passed.
- Located the finalized preliminary robust source and reused its real pixel-based fork detector and24-item route controller, rather than designing a duplicate detector.
- Prepared an isolated fullADS hardware port preserving current physical direction/encoder mapping, serial protocols andS5 controls; default target40. Incorporated Opus review388 and measured parameter33: physical encoder scale and latest tuned yaw/direction gains.
- Added explicit vehicle-side final-exit and whole-run stops to replace the simulator-only endpoint break.
- Actual-C vision/route/gate tests passed34 assertions; profile/stop tests passed25793 assertions with stable hashes and sanitizers. ADS built with0errors; full build had13warnings.
- Checked current hardware availability read-only; no matching downloader or serial device was present. No port opened, flash attempted or motion commanded.

## 未完成

- Physical flashing and on-map tuning await device reconnection. The fullP15 candidate remains isolated; its expected start must match the physical course.
- Full-route regression at the currently reported50 processed frames/s, speed40 and physical yaw gains is pending; the8-second simulation used490 frames/s.
- Real camera geometry, grip, route completion and an8-second physical lap remain unverified.

## 收益与损耗观察

- Owner explicitly requested fewer repeated confirmations; the correction and port used their observations as inputs.
- The original function was ordinary-corner-only; a mature simulated fork detector had not been integrated into production.
- An old mixed-encoding source prevented the first preparation attempt; nonASCII legacy comments were omitted while preserving executable bytes.
- A newline normalization overlapped one independent test; its assertions passed but the frozen-source result was discarded and rerun.
- Initial restricted ADS import andWSL/Git access required normal execution permissions. One test fixture needed a volatile declaration correction. Serial-library import was unavailable; OS device inventory was used instead.
- Opus review388 confirmed hardware preservation and required the measured encoder scale plus latest runtime tuning; these were adopted and independently rechecked. Review390 reported successful fork recognition on two realT snapshots and identified current parked processing around50fps versus the archived490fps simulation. Full low-speed regression remains pending; the historical490 observation was not denied. No external inference call was made.
- No matched baseline supports an efficiency improvement claim.

## 修改建议及下一轮验收

- **WF-OWNER-OBSERVATION-TO-PATCH-20261029 [adopted]** Accept reported vehicle behavior as an input and ask only for missing information that changes implementation, such as the required junction exit.；负责人：codex；下次检查：Next tuning round makes a bounded correction without asking the owner to reproduce an already reported symptom.
- **WF-SIM-TO-HARDWARE-ENTRY-20261029 [adopted]** Before promising a simulator feature on the car, verify its route loader, physical start point and terminal stop exist in the actual hardware build.；负责人：codex；下次检查：The next physical handoff includes source/profile identity, tested startup loading and a vehicle-side stop.

## 证据

- evidence.json; local source freezes, build logs, independent reports, project handoffs385-391 and measured parameter33.

## 限制

- Sanitized aggregate report only; no raw sessions, credentials, telemetry, source or live databases uploaded.
- Synthetic host checks and anADS build do not establish a physical lap time.
- First observed round timestamp is used; the interval includes overnight interruption and inactive time.

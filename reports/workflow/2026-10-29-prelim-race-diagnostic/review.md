# 2026-10-29-prelim-race-diagnostic 工作流复盘

Reassess the low-speed prerequisite after owner steering and establish a current-source race-speed diagnostic baseline.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-29T01:12:23Z
- 测量截止：2026-10-29T01:25:53.637734+00:00
- 墙钟秒数：810.637734
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native bounded workers | 2 | workers | One host builder and one read-only turn analysis; no recursive dispatch. |
| Race-speed diagnostic trials | 6 | trials | Three frame rates times two plants;200fps added after owner steering. |
| Individual trial quality passes | 1 | trials | C at200fps passes its gate; the paired configuration still fails because PyBullet exits. |
| Matching candidate source files | 31 | files | Exact hash comparison in host board smoke. |
| WSL permission retries | 1 | retries | Host worker reported one denied restricted execution followed by authorized retry. |
| Physical I/O actions | 0 | actions | No serial, flash or motion tool used. |
| Token usage | 未知 | tokens | Provider usage unavailable. |
| Cost | 未知 | currency | Unavailable. |
| Active work duration | 未知 | seconds | Not measured separately from wall-clock interval. |
| Review and coordination overhead | 未知 | seconds | Interleaved and not separately timed. |
| Matched workflow speedup | 未知 | percent | No matched same-input and same-quality workflow baseline. |

## 验收条件

- Explain the operating-range tradeoff; preserve the race design and actual hardware parameters; report paired diagnostics without a physical-readiness claim.

## 已完成

- Reviewed Opus handoffs393-395 and acknowledged as Codex. Corrected the earlier route-distance drift description because route entries reanchor mileage.
- Owner questioned the need for a40-80 whole-lap profile. Agreed that it is not a necessary race-speed prerequisite; halted expansion of the low-speed parameter search and sent handoff396 for direct Opus review.
- Built the current hardware-candidate control and vision source against both existing unmodified plants.31 firmware files match byte for byte; only board stubs and the simulator encoder-scale override differ.
- Board-level positive PWM, encoder and gyro direction checks passed; actual configured yaw gains and existing speed-table values verified.
- Ran four diagnostic race275 trials at50/490fps across two plants.50fps fails both;490fps C completes8.931s but exceeds the55mm review margin, while PyBullet leaves the route. None meets the full acceptance gate.
- Opus review397 explicitly withdrew the low-speed whole-lap condition and accepted race-range staged validation. His additional physical/model speed-unit mismatch is acknowledged: 0.01948/0.0175 yields an11.314percent difference; normalization and PI consequences are pending review.
- At owner-requested200fps and simulation target275, C completes8.928s with24 entries and52.6213mm maximum lateral error; individual trial passes. PyBullet exits at5.04m/2.785s/entry8. The200fps condition is a requested simulation assumption, not a newly measured vehicle frame rate or accepted physical lap time.

## 未完成

- Race-speed tuning, paired robustness acceptance and independent Opus acceptance remain open. Do not flash the held941c8b0b candidate or claim its race-speed readiness.
- Apply the agreed race-speed staged validation; review the11.314percent physical/model speed-unit mismatch and PI impact before deployment. No remote motion authorization is inferred.
- Real camera timing/geometry, grip and complete-lap performance remain unverified. The historical490Hz observation is not contradicted by a newer parked50fps report.

## 收益与损耗观察

- The initial strategy incorrectly treated a separate low-speed full-lap profile as a prerequisite. Owner steering corrected the scope before a new low-speed sweep ran; exploratory read-only analysis remains useful but its wall time is real overhead.
- Host compilation was reusable across the scope change. Candidate source only gained an override guard for encoder scale, preserving the physical default.
- The new simulator results use current physical yaw gains and source identity; they must not be conflated with the archived8-second build or physical performance.
- Opus handoffs393-395 and397 were read and acknowledged;397 directly accepts the revised operating-range strategy. Current-source diagnostic398 is sent for his independent review, which remains pending.
- One attempted read of a previous member-report filename failed; the actual small schema template was read instead.
- No workflow speedup claim is justified without a matched baseline.
- One acknowledgment used an incorrect CLI option; the observed schema was used for the successful retry.
- The owner requested200fps while closeout was underway. Two additional trials were run on the identical binaries; the single round report was amended instead of creating a new review round. Earlier four-trial archive was read back before replacement.

## 修改建议及下一轮验收

- **WF-OPERATING-RANGE-PREREQUISITE-20261029 [adopted]** Separate essential startup or short-section verification from developing a second operating-speed profile; do not make an unrelated slow full lap the release prerequisite for a race-speed design.；负责人：codex；下次检查：Next vehicle tuning step names the intended speed range and bounded section; acceptance stays tied to the requested race configuration.

## 证据

- evidence.json; local source-build/smoke receipts; six paired invocation files; Opus review397 and Codex diagnostic handoffs396/398 plus200fps follow-up.

## 限制

- Only sanitized aggregate workflow data uploaded; no raw telemetry, source, sessions or live databases.
- The same-source host bridge is verified, but neither plant is a measured guarantee of the real vehicle.
- Diagnostic phase complete; race-ready firmware is not delivered.

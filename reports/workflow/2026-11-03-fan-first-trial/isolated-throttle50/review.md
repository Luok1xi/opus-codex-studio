# 2026-11-03-fan-first-trial 工作流复盘

Measure the actual 50-percent command waveform with actuators isolated, then restore zero target and verify stopped state.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：partial
- 开始：2026-11-03T14:36:19+00:00
- 测量截止：2026-11-03T14:52:43.096558+00:00
- 墙钟秒数：984.096558
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| native_review_workers | 1 | workers | Actual saved evidence and coordinator action record; null means not separately available. |
| actual_opus_consultations | 0 | consultations | Actual saved evidence and coordinator action record; null means not separately available. |
| remote_start_commands | 0 | commands | Actual saved evidence and coordinator action record; null means not separately available. |
| firmware_flashes | 0 | flashes | Actual saved evidence and coordinator action record; null means not separately available. |
| parameter_writes | 2 | writes | Actual saved evidence and coordinator action record; null means not separately available. |
| cleanup_zero_replies | 7 | replies | Actual saved evidence and coordinator action record; null means not separately available. |
| measured_positive_pulses | 50 | pulses | Actual saved evidence and coordinator action record; null means not separately available. |
| nonzero_wheel_telemetry_rows | 8 | rows | Actual saved evidence and coordinator action record; null means not separately available. |
| tokens | 未知 | tokens | Actual saved evidence and coordinator action record; null means not separately available. |
| cost | 未知 | currency | Actual saved evidence and coordinator action record; null means not separately available. |
| review_overhead | 未知 | seconds | Actual saved evidence and coordinator action record; null means not separately available. |
| coordination_wait | 未知 | seconds | Actual saved evidence and coordinator action record; null means not separately available. |

## 验收条件

- Confirm operator isolation and stopped readback before setting the target.
- Measure actual nonzero waveform and independently cross-check source and telemetry.
- Restore zero target with fresh readback before allowing later reconnection.

## 已完成

- Operator confirmed ESC power and control disconnected, wheel driver off and LA1010 connected; COM6 was reconnected for parameter access.
- Authoritative flashed candidate b2fc907f was reviewed; #F only configures while stopped, and S5 starts a roughly 0.625-second fan ramp independently of launch delay.
- 50-percent target was independently read back before the operator performed the S5 test and manually saved a fresh one-second capture.
- Physical digital waveform has 100 edges: 49 positive widths of 1500 us and one of 1501 us; rising periods are 20000 us (45) and 20001 us (4), at nominal 1 MHz sampling.
- Software telemetry includes output50/pulse1500/run1. Ordinary race control later issued wheel PWM8500; operator-reported physical wheel disable was essential.
- Final independent read-only session returned seven target0/output0/run0 replies; final telemetry has zero wheel PWM and encoder values. All serial sessions closed.
- One native reviewer independently re-read source, waveform and raw telemetry.

## 未完成

- Historical humming/nonrotation root cause is unresolved. ESC reception/arming, analog amplitude, power delivery, phases and mechanics remain unverified.
- Owner has only LA1010, no multimeter. Next step is powered-off visual inspection of the actual ESC-to-motor wiring.
- No same-capture CSV cross-check or independent timebase calibration; kvdat parsing remains narrowly based on third-party reverse engineering.

## 收益与损耗观察

- Initial project context output was too broad; subsequent reads used explicit limits and full targeted handoff 572. A wrong get argument form and an incorrect filename were corrected.
- Both setting helpers failed their immediate confirmation gate. The nonzero setting and subsequent zero cleanup were accepted only after separate read-only sessions supplied fresh replies; no missing acknowledgement was treated as success.
- The intended short manual window was exceeded: telemetry contains 22 running rows at 250 ms intervals and eight nonzero wheel-command rows. Isolation, not estimated delay or automatic protection, bounded physical actuation.
- S5 toggles state, so the operator was told not to press it again if already stopped. Ordinary stopping does not erase the prepared target; zero cleanup was explicitly required.
- No same-condition quality baseline exists; parallel review or manual fallback does not establish a speedup.

## 修改建议及下一轮验收

- **fresh-setting-readback [adopted]** Separate setting delivery from acceptance; if immediate confirmation is missing, query fresh state without repeating a start action.；负责人：codex；下次检查：Only report successful setting or cleanup after independent fresh target and run-state replies.
- **isolate-before-command-test [adopted]** Keep physical actuator isolation mandatory for manual nonzero signal checks; do not rely on operator timing or zero-encoder protection.；负责人：codex；下次检查：Before a later powered spin, use a dedicated bounded test path or another established limit, rather than this full-race manual procedure.

## 证据

- Firmware artifact b2fc907f; reviewer matched source hashes to saved manifest and flash receipt.
- Waveform SHA256 69a35c59278759efb8e284ad99518c2df6221daffc4f3028f487cbacb1b95e55, 1752 bytes; raw capture stays local.
- Run log: 720 complete telemetry rows, 177 fan replies; 179 query commands across about 180 seconds.
- Cleanup query: 9 queries, 8 fan replies, first target50 followed by 7 target0; final stopped/zero-wheel state.
- Local source-timing-review.json and measurement-review.json retain original reviewer evidence.

## 限制

- Digital timing only, under operator-reported isolation; no claim that the fan or ESC works.
- Final 1000 us pulse is software readback, not an additional post-cleanup physical LA capture.
- 1.50 V is the input threshold setting, not measured signal amplitude; one microsecond is nominal sample spacing.
- No raw captures, serial logs, full transition lists, screenshots, private source or live databases are uploaded.
- Unknown usage and itemized overhead stay null; no efficiency gain claimed.

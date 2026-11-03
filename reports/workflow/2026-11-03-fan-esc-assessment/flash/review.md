# 2026-11-03-fan-esc-assessment 工作流复盘

Flash the explicitly authorized fan ESC firmware and verify parked startup telemetry without commanding movement or fan activation.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：passed
- 开始：2026-11-03T11:09:02+00:00
- 测量截止：2026-11-03T11:18:28.326376+00:00
- 墙钟秒数：566.326376
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| observed_interval | 566.326 | seconds | Flash-stage start to cutoff, including owner power-state clarification and independent review; candidate preparation excluded. |
| flash_attempts | 1 | attempts | Official programmer log. |
| flash_tool_duration | 1.847 | seconds | Programmer log reports 1847 milliseconds; not total task time. |
| verified_differing_bytes | 0 | bytes | Official memory readback result. |
| serial_captures | 2 | captures | Two separately preserved 8-second captures, query only; both ports closed. |
| fan_setting_commands | 0 | commands | Only #F query was transmitted. |
| vehicle_start_commands | 0 | commands | No launch command was sent. |
| native_review_workers | 1 | workers | One independent reviewer, no hardware access. |
| opus_calls | 0 | calls | Database handoff only; no Opus response claimed. |
| capture_setup_failures | 1 | attempts | Initial Python capture failed before opening port because pyserial was unavailable; switched to built-in .NET SerialPort. |
| firmware_rebuilds | 0 | builds | Approved binary was unchanged. |
| tokens | 未知 | tokens | Unavailable. |
| cost | 未知 | currency | Unavailable. |
| coordination_wait | 未知 | seconds | Not separately measured. |
| review_overhead | 未知 | seconds | Not separately measured; archive receipt records only post-cutoff interval. |

## 验收条件

- Flash the exact approved artifact with official readback verification.
- Read startup status without issuing throttle changes or vehicle start commands.
- Preserve evidence and distinguish MCU telemetry from physical fan validation.

## 已完成

- Exact approved artifact flashed once; readback PASS with zero differing bytes.
- Parked query confirmed zero fan target/output and zero wheel PWM.
- Initial camera failure and low ADC report occurred with owner-confirmed main power off; later powered capture shows camera at 150 fps with advancing sequence.
- Independent native reviewer checked the original flash log and both raw captures.

## 未完成

- 无记录

## 收益与损耗观察

- USB programmer enumeration did not prove that main board power was switched on.
- Separate captures preserved the before/after power-state evidence instead of overwriting the initial record.
- The aggregate hardware-ready telemetry value is only initialized at startup and is not refreshed after camera retry; live camera flag and frame progression established acquisition recovery. It is not used as a launch gate in this snapshot.
- No repeat build or flash was needed when camera acquisition recovered under main power.

## 修改建议及下一轮验收

- **capture-with-existing-runtime [adopted]** Use the available operating-system serial implementation for this bounded query rather than assuming an optional Python package is installed.；负责人：codex；下次检查：Next capture starts without a dependency setup failure.
- **refresh-ready-telemetry [proposed]** Update the combined readiness telemetry after camera retry in the next reviewed firmware change, preserving current launch gates.；负责人：codex；下次检查：A startup-failure then successful-retry test makes live cam, imu and combined status agree.

## 证据

- flash-receipt.json
- flash.log
- post-flash-summary.json
- power-check-summary.json
- independent-review.json
- manifest.json

## 限制

- Waveform, ESC arming, physical fan direction, suction, current and response remain unmeasured.
- Battery numbers are ADC-reported values, not a calibrated terminal measurement.
- Camera activity and parked zero-output telemetry do not establish track-following readiness.
- No matched workflow baseline; no efficiency improvement claimed.

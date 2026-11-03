# 2026-11-03-fan-first-trial 工作流复盘

Carry out owner-controlled fan trials, implement the explicitly requested 50-percent limit, and analyze installation-fault evidence without claiming an unmeasured physical diagnosis.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：partial
- 开始：2026-11-03T11:21:49+00:00
- 测量截止：2026-11-03T12:00:31.479894+00:00
- 墙钟秒数：2322.479894
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| observed_interval | 2322.48 | seconds | First recorded clock to cutoff; includes owner actions, waiting, three trial levels, firmware build and diagnostic review. |
| native_workers | 2 | workers | One independent reviewer and one host-test implementer; no actual Opus call. |
| firmware_changed_files | 1 | files | Compared with exact flashed baseline; maximum trial throttle definition only. |
| host_groups | 12 | groups | Real extracted C functions with hardware stubs. |
| host_assertions | 919 | assertions | Accepted sanitized execution. |
| host_test_interval | 5.034 | seconds | Recorded compile and execution interval. |
| static_checks | 9 | checks | Separate from execution tests. |
| target_build | 5.065 | seconds | Official ADS log; excludes IDE startup/import. |
| flash_attempts | 1 | attempts | Official programmer readback PASS. |
| flash_duration | 1.786 | seconds | Programmer log, not total workflow duration. |
| verification_differing_bytes | 0 | bytes | Official readback. |
| vehicle_start_commands | 0 | commands | Owner used the physical S5 button; agent sent configuration and query commands only. |
| capture_gap | 39.715947 | seconds | Between the two 10-percent capture windows; not continuous coverage. |
| tokens | 未知 | tokens | Unavailable. |
| cost | 未知 | currency | Unavailable. |
| coordination_wait | 未知 | seconds | Not separately measured. |
| review_overhead | 未知 | seconds | Not separately measured; archive receipt measures only the post-cutoff interval. |

## 验收条件

- Use parked confirmed settings and keep vehicle activation with the owner.
- For the requested higher limit, preserve the exact previous source and verify the new binary before authorized flashing.
- Correlate raw records and owner observations, then clear the temporary target and distinguish findings from hypotheses.

## 已完成

- 10 and 15 percent settings were acknowledged; owner reported no physical rotation.
- Owner-requested 50 percent firmware changed one definition; host tests, official build, independent review and memory readback passed.
- 50 percent produced owner-observed shudder or abnormal noise; further upward trials stopped.
- Actual record contained an approximately 33-second 50-percent request interval, exceeding the planned two-second manual test.
- Final setting and output both zero, run flag zero, acknowledged twice; serial connection closed.
- Low voltage observation was reconciled with owner-confirmed manual power removal; no causal supply-fault claim.

## 未完成

- Physical cause of failed fan startup remains unresolved; requires installation inspection and actual electrical measurements.

## 收益与损耗观察

- Current serial transport changed from downloader to wireless; one attempted stale COM6 open failed before sending anything.
- Mixed binary telemetry prefixed a valid fan reply; line-start anchoring incorrectly missed it. Local parser now recognizes the literal fan token regardless of prefix.
- One guarded setup query received no acknowledgement; no setting was sent in that attempt.
- One cleanup attempt sent zero but lacked a successful acknowledgement; fresh readback and an idempotent retry subsequently verified zero.
- Host tests first encountered a WSL access denial before compilation; the same authorized execution then passed.
- The three physical trials were not matched conditions: wheel-drive state differed and a timer reset occurred in the 15-percent capture.
- A long IMU calibration interval also occurred with zero fan output, so it cannot independently establish vibration from faulty installation.
- Manual timing did not enforce the intended two-second powered trial; software request duration must be reported honestly.

## 修改建议及下一轮验收

- **bounded-fan-only-test [proposed]** Before further powered diagnosis, provide a dedicated fan-only test with MCU-enforced timeout and wheel-output inhibition instead of relying on the full launch workflow and manual timing.；负责人：codex；下次检查：Test expiry and cancellation independently clear fan output and cannot launch the wheels.
- **capture-current-transport-and-epochs [adopted]** Use the actually enumerated transport, parse mixed binary/text tokens, and separate device-time resets and capture gaps.；负责人：codex；下次检查：Next analysis does not merge rebooted camera rows or infer continuous coverage across gaps.
- **verify-cleanup-ack [adopted]** Treat a zero-setting command as incomplete until its target, output and launch-state readback all confirm the stopped state.；负责人：codex；下次检查：Final handoff cites the successful fresh acknowledgement, retaining failed attempts separately.

## 证据

- source-changes.json
- manifest.json
- test-results.json
- ads-build-results.json
- reviewer.json
- flash-receipt.json
- hardware-log-review.json
- installation-log-analysis.json
- reset-fifty-zero-retry-summary.json
- https://blog.csdn.net/longqiu_LQ/article/details/160896921

## 限制

- No measured control waveform at the ESC, phase current, tachometer, impeller-clearance or connector-continuity evidence.
- Firmware output is a command, not measured power or physical rotation.
- Software and programming checks passed; physical fan startup did not.
- No matched workflow baseline; net efficiency remains unproven.

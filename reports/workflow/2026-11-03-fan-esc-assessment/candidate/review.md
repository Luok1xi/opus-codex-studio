# 2026-11-03-fan-esc-assessment 工作流复盘

Prepare and verify the complete vehicle firmware for the owner-confirmed Longqiu STC32G mini ESC and mainboard control header; flashing awaits explicit approval.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：passed
- 开始：None
- 测量截止：2026-11-03T11:06:31.685556+00:00
- 墙钟秒数：None
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| implementation_observed_interval | 988.686 | seconds | First clock of this continuation to cutoff, includes research and approval request; earlier assessments excluded. |
| native_workers | 3 | workers | One hardware-source researcher, one independent software reviewer, one C test implementer. |
| host_test_groups | 11 | groups | Exact candidate source functions and headers with hardware stubs. |
| host_assertions | 619 | assertions | One accepted execution. |
| host_test_seconds | 3.957 | seconds | Test report measured compile and run interval. |
| target_build_seconds | 4.989 | seconds | ADS build log; excludes startup/import. |
| code_review_fixes | 1 | fixes | Volatile qualification for shared launch flag. |
| timing_claim_corrections | 1 | corrections | Separate 5ms software request from 50Hz register and mechanical response. |
| standalone_build_failures | 1 | attempts | IDE-only compiler license; official ADS build succeeded. |
| hardware_commands | 0 | commands | No serial, flashing or actuation. |
| tokens | 未知 | tokens | Unavailable. |
| cost | 未知 | currency | Unavailable. |
| coordination_wait | 未知 | seconds | Not separately measured. |
| review_overhead | 未知 | seconds | Not separately measured; archive receipt records only post-cutoff interval. |

## 验收条件

- Use the documented flashed snapshot, not a divergent working tree.
- Implement bounded fan setting, query, startup and stop semantics without changing driving parameters.
- Verify actual C behavior, full target build and independent review before presenting a concrete flash candidate.

## 已完成

- Four source files changed; original snapshot preserved.
- Manufacturer family interface and board header checked against official sources.
- 11 real-C test groups, 619 assertions and 9 separate static checks passed with sanitizers.
- Official ADS build: zero errors and 11 unchanged warnings; ROM grew 452 bytes and RAM did not grow.
- Independent software findings resolved; source, test and candidate hashes agree.

## 未完成

- 无记录

## 收益与损耗观察

- Power and control wire terminology was resolved by owner clarification in the preceding continuation.
- Manufacturer name supplied during work enabled direct official product-family documentation; the exact physical board revision remains unverified.
- The first direct build repeated an existing IDE-only license limitation; the established official IDE workflow then completed.
- No extra full-car simulation was needed for this bounded interface change; offline tests do not establish suction or track performance.
- Flashing is a separate explicit owner decision under the project burn script; candidate preparation is complete.

## 修改建议及下一轮验收

- **reuse-verified-ide-build [adopted]** Start with the last successful official IDE build recipe for this toolchain instead of retrying its unsupported standalone compiler mode.；负责人：codex；下次检查：Next firmware candidate goes directly through the recorded IDE path.
- **separate-pwm-response-stages [adopted]** Document requested throttle, pulse width, register update boundary and measured mechanical response as separate quantities.；负责人：codex；下次检查：First powered fan validation records actual signal and response separately.

## 证据

- manifest.json
- ads-build-results.json
- test-results.json
- reviewer.json
- hardware-review-v2.json
- https://blog.csdn.net/longqiu_LQ/article/details/160896921

## 限制

- Not flashed or tested on the physical car.
- No measured waveform, current, suction, rotation or ESC startup behavior.
- 30 percent is a trial throttle cap, not a measured electrical safety threshold.
- No matched workflow baseline; no efficiency improvement claimed.

# 2026-11-08-hold-exit-target 工作流复盘

Build and deploy isolated hold-exit diagnostics, verify stationary identity, and prepare owner-controlled segment trials.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md plus isolated target/flash/readback gates
- 验收状态：partial
- 开始：2026-11-08T13:50:22.136674+00:00
- 测量截止：2026-11-08T14:14:51.217175+00:00
- 墙钟秒数：1469.080501
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| measured_wall | 1469.080501 | seconds | Target directory creation to review cutoff, includes rebuild and connection waits; excludes earlier reading |
| native_build_attempts | 2 | builds | One compile-time record padding failure, one successful clean build |
| native_compile_units | 174 | units | Final compiler log |
| native_new_warnings | 0 | warnings | Normalized comparison against frozen baseline |
| controller_scenarios | 23 | scenarios | Sanitizer harness |
| controller_assertions | 126 | assertions | Sanitizer harness |
| flash_attempts | 2 | actions | First failed at DAS initialization before erase; second verifiedPASS |
| flash_successes | 1 | actions | Official receipt |
| successful_flash_time | 4008 | milliseconds | Flasher log |
| serial_queries | 5 | commands | Per-capture intent receipts |
| remote_launches | 0 | actions | Only readback queries |
| agents_dispatched | 0 | agents | Single coordinator |
| tool_failure_count | 未知 | failures | Not globally instrumented; concrete rework listed below |
| usage | 未知 | tokens | No authoritative provider usage |
| cost | 未知 | currency | Unavailable |
| review_archive_overhead | 未知 | seconds | Archive duration in final readback receipt |

## 验收条件

- Preserve frozen baseline
- Clean native build and verified HEX identity
- Owner-confirmed flash preparation and live stopped readback
- Physical traversal remains separate

## 已完成

- Preserved frozen09R2 source and release; copied688 inputs into an isolated target tree.
- Clean174-unit native build passed with0 errors and12 unchanged warnings; CPU0 link headroom3559bytes after reserved stacks/CSA.
- 23 host controller scenarios/126 assertions and LOG2 roundtrip passed; stop28 keeps unsafe56px exit out of normal PID.
- Official diagnostic flash verified after owner-confirmed reconnect; live wired identity125/fan30/OUC/47 nodes matches frozen HEX.
- Stationary30s timing showed no new lateness or execution overruns;2ms/5ms measured maxima45/18us in that window.
- Empty prelaunch LOG2 record accepted only for count0/start0/period0; nonempty invalid-period records remain rejected.
- Wireless identity and stopped settings verified after owner restored module; passive run capture prepared.
- Owner ran the car; passive wireless recorded a stop28 and later stop3. Owner located the failure at dashed line. First-run timing reached74/49us with no overrun or late count.

## 未完成

- Dashed-line traversal has not passed. Detailed failure diagnosis awaits a stopped, unrestarted board-record export; repeated launches prevented three guarded queries.
- No physical route or segment quality acceptance; no real stack high-water result.
- C27 evaluation deferred by owner until current diagnostic tests; reference reads only.

## 收益与损耗观察

- Host record18-byte layout became20bytes on target; compile assertion caught it before flash. Separate16-byte record andint16 array preserved18KB.
- Own ADS process lingered after window close; replacement could not acquire workspace. Process paths verified and only this stage processes stopped before clean rebuild.
- First flash failed in downloader initialization. Owner reconnected and confirmed powered screen; retry passed before any test run.
- Boot system_start resets the relative timer after interrupts start, producing one spurious late count; later30s counters did not grow. This diagnostic flaw remains in deployed D01.
- Timing enqueue can drop lines under pressure; longer stationary sample captured30 rows. Running timing remains pending.
- Readback initially rejected the empty prelaunch record period0. Local decoder fixed without rewriting deployed firmware.
- Owner requested C27 evaluation then deferred it; no C27 implementation or firmware change occurred.
- Physical trials started during capture setup. Repeated launch and a reboot prevented preservation of the firststop28 board record; sparse telemetry cannot prove its specific exit cause. Queries correctly refused while running. Passive capture remains active for the next stopped handoff.
- No matched workflow baseline; no speedup claim.

## 修改建议及下一轮验收

- **CC-NATIVE-RECORD-LAYOUT-20261108 [adopted]** Keep target size assertions and clean compiler audit before flash; host layout alone is insufficient.；负责人：codex；下次检查：New diagnostic fields must fit the native memory map and pass wire-schema tests.
- **CC-TIMING-BOOT-ANCHOR-20261108 [proposed]** In a later isolated diagnostic revision, use a stable timer baseline and retry status enqueue; preserve current test HEX for comparability.；负责人：codex；下次检查：Reset/reboot produces no artificial lateness; active loop execution and queued telemetry remain bounded.

## 证据

- Frozen source/HEX manifest and native compiler/map
- Official flash receipts and live serial readbacks
- Controller tests and strict record decoder
- Local deployment handoff

## 限制

- No active physical acceptance.
- Static timing and link headroom do not prove active-loop timing or stack high-water.
- Only sanitized aggregate reports uploaded.

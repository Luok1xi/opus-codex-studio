# 2026-11-08-d01-final-capture 工作流复盘

Preserve one owner-operated vehicle run and analyze turn-state failure without changing firmware.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; live identity and stopped-only readback
- 验收状态：partial
- 开始：2026-11-08T22:45:16+08:00
- 测量截止：2026-11-08T14:55:28.314105+00:00
- 墙钟秒数：612.314105
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| measured_capture_analysis_wall | 612.314105 | seconds | Recorder start to analysis/review cutoff; excludes initial source/context preparation |
| owner_runs | 1 | runs | Single owner launch captured before logger failure; recovered board interval overlaps same run |
| board_records | 234 | rows | Strict LOG2 count/index/time/END decode |
| serial_read_queries | 4 | commands | P before run, then S/P/I parked recovery |
| wireless_stream_complete | 0 | boolean | Host status file sharing error interrupted passive log |
| board_record_complete | 1 | boolean | Saved full stopped board buffer |
| firmware_writes | 0 | actions | No build or flash |
| parameter_writes | 0 | actions | Read-only command allowlist |
| remote_launches | 0 | actions | Owner physical S5 only |
| agents_dispatched | 0 | agents | Single coordinator |
| logger_lock_regression_passed | 1 | tests | Exclusive file lock fixture; no serial open |
| usage | 未知 | tokens | Not authoritatively instrumented; archive timing kept in receipt |
| cost | 未知 | currency | Not authoritatively instrumented; archive timing kept in receipt |
| total_tool_failures | 未知 | failures | Not authoritatively instrumented; archive timing kept in receipt |
| review_archive_overhead | 未知 | seconds | Not authoritatively instrumented; archive timing kept in receipt |

## 验收条件

- Current identity and owner-controlled run
- Preserved complete onboard data before reuse
- Separate observed fields from hypotheses
- No vehicle state changes

## 已完成

- Verified current firmware tag and125/fan30/47 over live wireless before owner launch.
- Saved raw wireless bytes and host byte timestamps; recovered complete234-row onboard log after host-side status-file sharing failure.
- Read-only stopped identity/image export completed; owner confirmed unchanged stopped pose.
- Compared two real records: ordinary-following conflict repeats around1s while route progress stays0; separated observed state from missing admission evidence.
- Corrected effective first-node window interpretation to200mm from actual enabled macros; left firmware untouched.
- Fixed advisory heartbeat failure handling and verified it under an exclusive file lock without hardware.
- Saved hashed local evidence, waveform plot and limitations; kept deployed sources/HEX unchanged.

## 未完成

- Physical route failure remains unresolved; no repair or acceptance claimed.
- Raw/filtered corner, route-distance rejection and ra_seen were not recorded, so exact gate remains uncertain.
- Stationary snapshot is later than motion failure; passive wireless stream has a documented gap.

## 收益与损耗观察

- Initial runtime lacked optional serial module; reused established system serial interface without installation.
- Logger stopped when an advisory status write collided with a concurrent reader; parked recovery preserved the same-run complete board record, but wireless continuity was lost.
- Status-write errors now leave primary recording alive; explicit lock fixture passed. No unearned claim of uninterrupted automatic capture.
- CLI task creation verb and one quoted analysis snippet needed correction; exact total tool failure count not instrumented.
- Measured yaw supports physical turning while recorded planning state stays0; exact early rejection is still not observable.
- Source comments and older summary understated enabled first-node distance window; effective macros were checked before proposing changes.

## 修改建议及下一轮验收

- **CC-HEARTBEAT-NONFATAL-20261108 [adopted]** Keep advisory status write failure nonfatal; use durable raw evidence as primary recorder output.；负责人：codex；下次检查：Concurrent live reader cannot interrupt a later recorded run.
- **CC-NODE-ADMISSION-EVIDENCE-20261108 [proposed]** Include raw/filtered corner, confirmation count and explicit admission rejection reason in a later isolated diagnostic revision.；负责人：codex；下次检查：Recorded segment resolves classifier versus distance/direction/rate gate; no widened acceptance.

## 证据

- Local hash-manifest aggregate
- Strict board-record decoding and same-run timestamp overlap
- Live identity and read-only command receipts
- Source gate inspection and actual telemetry plot
- Offline file-lock regression

## 限制

- No raw telemetry, images, code, sessions or databases uploaded.
- No matched quality baseline; no speedup claim.
- Derived yaw/odometry uses20ms samples, not the firmware2ms state.

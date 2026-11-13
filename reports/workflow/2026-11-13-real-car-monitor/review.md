# 2026-11-13-real-car-monitor 工作流复盘

Build a local real-car evidence monitor: run segmentation, loop plots, stopped images, position-photo pairing and observation-only firmware.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：Project database with scoped native implementers and independent review
- 验收状态：passed
- 开始：2026-11-13T04:49:46.021Z
- 测量截止：2026-11-13T05:26:19.326768+00:00
- 墙钟秒数：2193.305768
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| native_child_contributors | 3 | agents | Three native contributors returned scoped evidence; no impersonated external review. |
| external_studio_calls | 0 | calls | DSH file handoff was read; no external Opus/DSH invocation. |
| unit_tests | 58 | tests | Final unittest receipt. |
| target_build_seconds | 8.39100000000326 | seconds | Final coherent observer target build receipt. |
| hardware_operations | 0 | operations | No live serial open, firmware flash, gain write or remote launch. |
| tokens | 未知 | tokens | No reliable complete measurement available. |
| cost | 未知 | currency | No reliable complete measurement available. |
| coordination_wait | 未知 | seconds | No reliable complete measurement available. |
| review_overhead | 未知 | seconds | No reliable complete measurement available. |
| archive_overhead | 未知 | seconds | No reliable complete measurement available. |
| total_rework | 未知 | events | No reliable complete measurement available. |

## 验收条件

- Offline real-log replay with honest time and run association.
- Stop-only read capture, immutable provenance and local waveform/photo review.
- Observation firmware compiles; existing control source remains unchanged.

## 已完成

- 58 unit tests passed; two real-log reports generated; desktop/mobile rendering and photo export checked.
- Actual UART-export timing and partial image framing audited against saved evidence.
- Firmware compiled with 0 errors and 13 inherited warnings; exact-C CRC/FIFO mocks passed.
- Independent review corrected mixed image timestamp/frame provenance and several reader/assembly defects.

## 未完成

- 无记录

## 收益与损耗观察

- Reused existing chart/store code instead of a second website or server.
- Real inputs exposed CRCRLF splitting and EOF image terminator differences absent from initial synthetic fixtures; these were fixed with regression tests.
- Independent review found an observer camera timestamp/frame mismatch; the candidate was rebuilt and old hash removed from active automatic-export profiles.
- Report assembly was hardened for path confinement, snapshot hashes, stop byte bounds and invalid export associations.
- Browser startup first failed from missing cached executable and local restrictions; installed Edge completed final validation.
- No matched quality/time workflow baseline exists; no efficiency speedup claimed.

## 修改建议及下一轮验收

- **REALMON-C-FIXTURE [adopted]** Keep exact C-generated frames and real truncated/mixed-newline logs in local protocol regression tests.；负责人：codex；下次检查：Next telemetry change must pass the parser contract before field use.
- **REALMON-OBSERVED-ID [adopted]** Separate observed controller route position, human photo annotation, retained export and live device identity in every report.；负责人：codex；下次检查：First supervised capture must preserve one complete run and photo without cross-run association.

## 证据

- evidence.json contains sanitized aggregates only.
- Full source, raw logs and photographs remain local; project task145 contains the handoff.

## 限制

- This round delivers offline tooling and an unflashed observer candidate; no real-car lap or wireless throughput acceptance.
- Physical corner/element position still needs external confirmation; route counters are not ground truth.
- 50Hz full-run telemetry cannot replace 2ms short capture for high-frequency speed-loop analysis.
- Stop images are requested after stopping, not synchronized fault-trigger frames.
- Two nominal plant trajectory hashes match for the earlier observer revision; final camera-provenance-only fix was rebuilt/mock-tested, not rerun as a full matrix.
- Measurement cutoff precedes remote archive verification; unknown usage and overhead remain null.

# 2026-11-08-real125-fan30-bringup 工作流复盘

Build and flash the explicitly requested isolated route candidate, verify identity and requested settings, establish wireless capture and inspect restart-related stationary sensor readings.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + project-specific build/flash receipts
- 验收状态：partial
- 开始：2026-11-08T06:51:25+00:00
- 测量截止：2026-11-08T07:09:04.410713+00:00
- 墙钟秒数：1059.410713
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| source_files_verified | 688 | files | Frozen candidate manifest checked before copying |
| full_build_wall | 6.553 | seconds | ADS full-build log |
| flash_wall | 4.121 | seconds | Official flasher reported overall time |
| flash_attempts | 1 | attempts | One official burn receipt |
| failed_device_open | 1 | attempts | Stale wireless port absent before live device enumeration |
| script_policy_build_failure | 1 | attempts | First child PowerShell blocked script; temporary process permission then approved |
| agents_dispatched | 0 | agents | No delegation occurred |
| model_usage | 未知 | tokens | Provider usage unavailable |
| cost | 未知 | currency | No billing receipt |
| review_archive_overhead | 未知 | seconds | Archive not completed at cutoff |

## 验收条件

- Isolated source provenance and fresh MCU build
- Explicit flash authorization and physical preparation
- Verified flash and live readback of requested settings
- Continuous capture established; actual run diagnosis follows observed run

## 已完成

- Source hashes verified, empty build output directory, fresh complete build
- One verified flash with zero byte differences
- Both wired and wireless readback matched new identity and requested settings
- Read-only recorder confirmed fresh and growing
- Three startup segments separated; latest stationary output remained zero over ten seconds

## 未完成

- Owner-run lap and symptom diagnosis are pending

## 收益与损耗观察

- Owner clarified that a new flash was required; source-only readiness was not the intended result.
- Device enumeration must occur in the actual device-access context; initial limited-context view was stale.
- Current build identity and source candidate identity were unified before freezing.
- Restart-separated sensor readings prevented treating improved bias as resolved prematurely.

## 修改建议及下一轮验收

- **CRAZY-CIRCUIT-DEVICE-CONTEXT-20261108 [adopted]** Enumerate and open hardware in the same execution context, then confirm continuous data before declaring capture ready.；负责人：codex；下次检查：Next device task has one consistent enumeration/readback receipt.

## 证据

- Frozen-source manifest receipt
- Fresh full build and normalized warning comparison
- Official flash receipt with zero difference verification
- Wired/wireless query receipts and capture status
- Restart-segment stationary sensor summary

## 限制

- No physical lap or tracking-fix claim yet.
- Filtered deadband telemetry is not raw sensor-noise evidence.
- No matched workflow baseline; no efficiency claim.
- Raw source, serial streams, firmware and device identifiers excluded from upload.

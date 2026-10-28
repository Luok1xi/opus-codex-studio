# 2026-10-28-screen-serial 工作流复盘

Diagnose black display and serial/IMU status confusion; integrate display repair and coordinate the concurrent wireless fix.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-28T08:36:43Z
- 测量截止：2026-10-28T09:26:31.781459+00:00
- 墙钟秒数：2988.781459
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native workers | 2 | agents | Independent display/control and website/serial audits. |
| External Opus calls | 0 | calls | Database handoffs and direct source observations; no inference call claimed. |
| Display host assertions | 501 | checks | Strict compiler and ASan/UBSan passed. |
| Static checks | 16 | checks | Includes shared-pin release and unchanged control path. |
| Default website checks | 14 | checks | Existing canonical parser/model; no source patch needed. |
| Saved capture chunk modes | 4 | modes | Each recovered 217 status and voltage samples. |
| ADS final compile | 4.291 | seconds | Final isolated full build only. |
| Provider usage | 未知 | tokens | Unavailable. |
| Cost | 未知 | currency | Unavailable. |
| Review and coordination overhead | 未知 | seconds | Interleaved; archive interval begins at measurement cutoff. |

## 验收条件

- Identify current source and physical-evidence boundaries; repair production display without overwriting concurrent work; verify source/build; hand off wireless evidence.

## 已完成

- Found disabled display initialization; enabled early SPI landscape startup and bounded S5/state text; preserved motion-time full-image guard.
- Reused the established board-specific P15.4 input restoration after display initialization.
- 501 source-derived host assertions and 16 static checks passed; final full ADS build had zero errors and eleven unchanged-code warnings.
- Installed three display files with hash checks and a scoped local commit; preserved Opus wireless changes.
- Owner confirmed COM6 connection resumed after closing duplicate connections; no particular occupying process was proved.
- Fourteen default-status checks and four chunk modes of a saved real capture proved the existing website can ingest production voltage/status.
- Independent audit identified wrong wireless RTS pin; observed Opus correcting it and delivered initialization failure-path findings in handoffs 369/370.

## 未完成

- Physical screen illumination, IMU state and current wireless reception require final integrated firmware and hardware acceptance by Opus/Owner.
- Opus final acknowledgement of this round is pending.

## 收益与损耗观察

- Initial software-only pin review missed a physical shared-pin constraint; reading the previously validated board adaptation corrected this before installation.
- Disabled screen initialization does not by itself explain no backlight on a board with direct backlight power; explicitly corrected that inference.
- Repeated bounded handle scans timed out without identifying an owner; device enumeration was not presented as proof of occupancy or disconnection.
- A strict host compile detected potential display-format truncation; shortened padding then reran all relevant checks.
- Deleting isolated generated build files exposed an ADS resource-cache failure; refresh was insufficient and a fresh isolated workspace restored a verified build.
- Staging the contextual patch failed because S5 was an existing unstaged change; a scoped zero-context patch committed only this round changes.
- Several broad reads produced unnecessary output and wildcard-path mistakes; routine diagnosis should begin with exact paths and bounded records.
- Concurrent wireless source changes made the isolated display HEX unsuitable for deployment; only source was integrated and Opus retains the final combined build/flash responsibility.
- No matched quality baseline exists; elapsed time and multiple workers do not establish efficiency.

## 修改建议及下一轮验收

- **WF-BOARD-ADAPTATION-FIRST-20261028 [adopted]** Compare board-level pin macros and established hardware adaptations before integrating a driver-dependent feature.；负责人：codex；下次检查：Trace each enabled GPIO to the actual board mapping, including pins unused by software interrupt configuration.
- **WF-ARTIFACT-CURRENT-TREE-20261028 [proposed]** Final hardware coordinator rebuilds from the combined current working tree and records the artifact identity before flashing.；负责人：opus；下次检查：Recipient acknowledgement and current combined source/build/hardware evidence.

## 证据

- evidence.json; local source hashes, test reports, build logs, installation receipt and project handoffs.

## 限制

- This round did not open serial ports, flash firmware or move motors.
- No raw capture, project source, live database, process dump, credentials or conversations are uploaded.
- The isolated display HEX excludes concurrent wireless changes and must not be flashed.
- Current live voltage/IMU state was not observed by Codex.

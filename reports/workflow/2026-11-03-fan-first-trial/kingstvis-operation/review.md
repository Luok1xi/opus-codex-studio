# 2026-11-03-fan-first-trial 工作流复盘

Operate KingstVIS with LA1010, preserve off/on control captures, and measure the isolated parked fan-control waveform without vehicle or fan actuation.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：partial
- 开始：2026-11-03T13:43:23+00:00
- 测量截止：2026-11-03T14:09:35.752588+00:00
- 墙钟秒数：1572.752588
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| configured_single_captures | 2 | captures | 已记录两段配置明确的单次采样；不将前期出现的被动连续采样混入此数量。 |
| saved_raw_files | 2 | files | 本地核验两个实际存在的 kvdat 文件；保存成功按实际文件名认定。 |
| saved_raw_bytes | 3004 | bytes | 两份原件长度 1252 + 1752 字节，已直接读取文件元数据。 |
| analyzer_outputs_enabled_by_agent | 0 | outputs | 协调者动作记录：未启用分析仪输出。既有 PWM1 被关闭，不能写成分析仪全程没有输出。 |
| existing_analyzer_outputs_disabled | 1 | outputs | 已关闭既有 PWM1；PWM2 原本未启用。 |
| vehicle_serial_commands | 0 | commands | 本阶段没有车辆串口查询或调参命令。 |
| vehicle_or_fan_start_commands | 0 | commands | 本阶段没有 S5、远程发车或风机油门指令。 |
| firmware_flashes | 0 | flashes | 本阶段没有烧录。 |
| native_review_workers | 2 | workers | 实际分派 diagnostic_review 做方法及测量复核，operation_review 仅整理工作流草稿；不等于真实 Opus 回复。 |
| real_opus_consultations | 0 | consultations | 本阶段没有真实 Opus CLI 或云端会诊回执。 |
| documented_rework_episodes | 5 | episodes | 按五类已记录返工计数：旧坐标/窗口变化、通道设置未确认即切换、错误判断进程退出、长文件名输入不完整、另存实际默认文件名与计划名不一致；不是所有失败调用总数。 |
| tool_failures_total | 未知 | calls | 未从完整执行记录逐项核算，不把已知返工类别数当作失败调用总数。 |
| tokens | 未知 | tokens | 没有同口径真实用量数据。 |
| cost | 未知 | currency | 没有实际账单数据。 |
| review_overhead | 未知 | seconds | 独立复核与报告编写的完整专属耗时未单独测量。 |
| coordination_wait | 未知 | seconds | 用户接线/上电及成员回复等待没有完整独立计时。 |
| archive_overhead | 未知 | seconds | 本草稿没有执行上传、远端回读或数据库登记。 |
| elapsed_to_measurement_cutoff | 1572.753 | seconds | Wall time including user replies, GUI rework, review and approval waits; not pure compute time. |
| powered_positive_pulses | 50 | pulses | All 50 complete positive widths are 1000 samples at recorded 1 MHz. |
| powered_period_min | 20000 | microseconds | 44 of 49 rising-edge periods. |
| powered_period_max | 20001 | microseconds | 5 of 49 rising-edge periods; one nominal sampling step of difference. |
| csv_export_approval_timeouts | 2 | calls | Both calls were rejected before execution; one allowed retry was attempted. |

## 验收条件

- 在真实 LA1010 已连接的 KingstVIS 实例中配置被动单次采样，保留原始数据及实际采样条件。
- 将未供电对照与主板单独供电后的测量分开，使用实际数据核对停车脉冲的周期及高电平宽度。
- 保持电调隔离，不发送车辆启动或风机加油门指令，不把数字脉冲观察扩展为整套电调或动力系统正常。
- 如实记录 GUI 返工、证据限制及未知开销，完成协调者最终核验后再登记并验证私人归档。

## 已完成

- 已确认 KingstVIS 3.6.6 安装且真实 LA1010 连接；配置 CH0、1 MHz、1 MSa、自定义阈值 1.50 V，无触发条件，毛刺过滤均未勾选。
- 发现分析仪既有 PWM1 输出处于启用状态后将其关闭；PWM2 原本关闭。本轮未启用分析仪输出。
- 第一段单次采样显示平低，随后用户确认当时 S1 关闭；对照原件 fan-ch0-s1-off-20261103.kvdat 已保存，实测文件长度 1252 字节。
- 用户明确报告主板单独上电、电调保持断开、车轮驱动关闭后，第二段单次采样出现规律脉冲；原件实际保存为 2026-11-03_21-57-30.kvdat，实测文件长度 1752 字节。
- 对软件退出的错误判断已向用户更正；原连接实例保持运行，多开的未连接演示实例已关闭。
- Independent file review and coordinator rerun agree: powered CH0 has 100 transitions, 50 complete 1000 us positive pulses and 49 rising periods of 20000–20001 us. The recorded 1 MHz sample rate agrees with the GUI. Candidate firmware specifies 50 Hz and 1000 us stop.

## 未完成

- Same-capture CSV comparison remains incomplete: opening the export menu was rejected twice because automatic approval review exceeded its deadline, including the permitted single retry. No unsafe-action determination was reported.
- The kvdat reader is based on a third-party reverse-engineered format, narrowly validated for these two files; no manufacturer format specification or independent timebase calibration was obtained.
- Loaded signal, ESC arming, power supply, phases and mechanical behavior remain untested. The historical non-spinning fan root cause is not established.

## 收益与损耗观察

- 主板供电条件解释了两段观察差异。第一次平低不能作为 MCU 无输出或硬件损坏证据；用户确认供电条件后才采集第二段。
- 早期窗口几何发生变化后，旧坐标用于新窗口，随后见到被动连续采样；协调者停止采样并增加窗口句柄、进程及前台验证。不能据此声称初次操作即通过。
- 通道选择曾因未确认即进入更多设置而丢失，已重新选择并确认 CH0。
- 使用受限进程视图未找到软件，被误解为软件退出；重新打开了一个未连接演示窗口。后续在正确权限上下文确认原连接实例始终存在，关闭额外演示实例并更正用户说明。
- 长 SendKeys 输入只填入部分路径；改为定位原生保存对话框控件并读回文本。第二份原件仍以默认时间戳名称保存，文件名读回不等于最终保存路径已验证。
- 原件保存、截图观察及输入条件已经形成可复核证据，但 GUI 操作产生了多次返工。本轮没有合格同条件基线，不能判断净提效。
- 截图和原始 kvdat 保留本地；私人归档仅允许脱敏流程报告、聚合指标和必要工作流变更。
- The default timestamp-named powered capture was retained and independently parsed rather than discarded because the intended output name was absent.
- The CSV export could not proceed after two automatic approval timeouts. Existing files provided a non-device alternative for timing analysis; there was no further GUI retry.
- Earlier research only finding a changelog note about decoded-result export did not establish that the application TCP API was export-only. Independent source review found broader command documentation; it was not enabled or executed during this phase.

## 修改建议及下一轮验收

- **bind-instrument-window [adopted]** 已在 ui.ps1 中加入指定进程、预期窗口句柄和前台窗口验证；继续把同句柄下的几何变化也纳入输入前核对，任何不一致先重新观察。；负责人：codex；下次检查：下一次窗口切换后确认输入前校验拦截失效句柄，并用新截图验证实际目标；同句柄几何验证仍需补强。
- **verify-process-in-desktop-context [proposed]** 判断桌面程序退出或设备断连前，使用与 GUI 操作一致的权限和桌面上下文核对目标实例；无法枚举时记录未知，避免再开实例。；负责人：codex；下次检查：下一次进程查询异常时，先核对原 PID/窗口及设备状态，不因受限枚举为空而宣布退出。
- **verify-saved-artifact [adopted]** 保存后读取实际目录、文件大小和内容标识，核对最终文件名；控件文本读回只作为中间检查。优先保留已经成功保存的默认文件名，再建立清楚的证据索引。；负责人：codex；下次检查：每次测量保存后，在开始下一次采样前确认原件存在并记录哈希；不要只检查计划文件名或无限重试焦点。
- **prefer-bounded-acquisition-path [proposed]** Before future instrument sessions verify official acquisition/export automation capabilities and persistence behavior; avoid long keyboard paths and duplicate application instances. Keep a GUI fallback and explicit device identity checks.；负责人：codex；下次检查：Verify the vendor API documentation and a passive read/export capability before any later automation change; no socket server was enabled in this round.

## 证据

- 本地原件：fan-ch0-s1-off-20261103.kvdat，1252 字节；SHA256 A6E731926CE81C8F7BAD62F673C4524984F8544438C1DBFC261067C178F05187；不上传原件。
- 本地原件：2026-11-03_21-57-30.kvdat，1752 字节；SHA256 88EEFAB1A0B58ED31B049C62ED917666A0B5937E68D80358CDC38CEA90D646AE；不上传原件。
- 本地截图：single-result、powered-result、outputs-off-applied、filter-dialog；不上传。
- 本地实现检查：ui.ps1 包含进程、窗口句柄及前台验证；save-dialog.ps1 包含控件与文本读回检查。
- 用户在当前阶段明确报告 S1 关闭，以及随后主板单独上电、电调隔离和轮驱关闭；属于现场状态报告，不等同于独立电气测量。
- Independent kvdat review plus coordinator rerun agree on both file hashes, complete byte consumption, increasing edges, terminal sample markers and measured timing.
- https://github.com/andy-qingcai/KintstvisMcp/blob/main/kingstvis_mcp/kformats.py#L71-L128

## 限制

- Only the isolated parked digital waveform was measured. Physical connection and power states are operator reports.
- 1.50 V is a threshold setting, not a measured signal voltage; nominal 1 us timing resolution is not calibrated absolute accuracy.
- The format parser is based on open-source reverse engineering. Same-capture CSV comparison remains incomplete because automatic approval review timed out twice.
- No vehicle commands, actuator launch, firmware changes or analyzer output enablement occurred. Previously enabled PWM1 was disabled.
- Raw captures, full transitions, screenshots and private source stay local; only sanitized workflow reports and aggregates are archived.
- Unknown usage, cost, total failure count and itemized review/wait overhead remain null. No matched baseline or efficiency gain is claimed.

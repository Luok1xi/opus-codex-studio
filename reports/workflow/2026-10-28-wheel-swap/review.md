# 2026-10-28-wheel-swap 工作流复盘

Compare wheel swaps and speed80, verify the live camera and full-control boundary, collect a failed low-speed line-following trial, and coordinate independent review with the returning Opus operator.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-28T10:22:54Z
- 测量截止：2026-10-28T14:26:43.419494+00:00
- 墙钟秒数：14629.419494
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native independent worker threads | 2 | threads | Distinct read-only scopes with bounded follow-ups; one coordinator consolidates evidence. |
| Complete new speed captures | 3 | captures | Two target40 wheel-swap runs and one target80 run; all500 rows validated. |
| Complete race high-frequency captures | 0 | captures | Strict index/order/length verification rejected the raw LOG export. |
| Observed race start segments | 4 | minimum segments | Sparse complete state transitions; not four fully measured tracks. |
| Actual camera frames verified | 2 | frames | Raw bytes decoded with frame sequence and payload validation, then processed by actual C vision code. |
| Coordinator production flashes | 0 | flashes | All source candidates stayed local; runtime serial configuration was used. |
| New external inference calls | 0 | calls | Doctor probes only; actual Opus collaboration was through the shared project handoffs and independently produced artifacts. |
| Provider usage | 未知 | tokens | Unavailable; no character or tool-output estimate substituted. |
| Cost | 未知 | currency | Unavailable. |
| Active work duration | 未知 | seconds | Wall interval includes operator waits and a long observed timestamp gap; no active-work estimate inferred. |
| Review and coordination overhead | 未知 | seconds | Interleaved; archival interval starts at the measurement cutoff. |
| Total tool failures | 未知 | events | Not counted exhaustively; important failures and their resolution are described. |

## 验收条件

- Preserve actual hardware evidence, distinguish stable wheel speed from stable steering, verify camera and command semantics, and coordinate one serial owner before further changes.

## 已完成

- Captured three complete owner-started speed runs: two wheel-swap target40 trials and one target80 trial; each had500 rows and a normal timed stop.
- Recorded the owner-observed right-left-right drift after tire/hub-only swaps without declaring a unique mechanical cause.
- Verified target80 steady wheel tracking while identifying that most net measured heading change occurred during startup; no275 acceptance was claimed.
- Built an isolated80-to275 input-limit candidate:2665 host assertions passed; full ADS build had0 errors and11 warnings in unchanged files. Candidate was not installed or flashed.
- Read two actual camera frames with increasing sequence numbers; current production vision replay recognized the white guide line in both. Fresh live state showed50 processed/valid frames per interval and about2.7ms processing.
- Verified screen images are limited to5fps while stopped and disabled while running; wireless raw-image export blocks foreground processing. Complete simulation route/hexagonal-ring behavior is not present in this production firmware.
- Validated the existing stopped-only ValuePack configuration with837 actual-C assertions; configured race base40, verified real target readback, and recorded owner-operated line-following attempts.
- Rejected the race high-frequency export as incomplete despite its END marker; strict states demonstrate large alternating corrections but do not establish full-run integrals or a unique faulty loop.
- Read and acknowledged Opus handoffs377-382, transferred serial ownership per382, and sent evidence/limitations in383. Independently verified the Opus speed-header compatibility fix with the actual web consumer.
- Independently inspected the Opus-labeled Kp3 snapshot: sampled correction was milder, but a fresh run-to-lost-line-stop transition remained. Returned the limited conclusion and compatibility review to Opus.

## 未完成

- Opus owns the live car; the Kp3 sampled run still lost the line. Angular-rate/outer-loop stability acceptance remains pending.
- Wheel assembly consistency, angular-rate tuning, reliable race high-frequency export and target275 physical validation remain unfinished.
- The isolated275 candidate predates the Opus webcompat change and must not overwrite it; no new candidate was deployed.

## 收益与损耗观察

- A default inbox result showed old items and concealed new Opus handoffs. A later limit200 query exposed the current owner transfer; the coordinator corrected its misleading inference from CLI login state.
- Automatic review rejected an old binary zero-target payload because zero float fields could alter direction gains. It was not executed; an alternative no-gain ASCII command could not open the port and was not sent. Serial operations stopped after ownership was clarified.
- The first map configuration was guarded out when no fresh state arrived. A later stopped configuration succeeded, but malformed trailing text required strict complete-state parsing; real checksum-valid target readback was retained.
- An END marker alone incorrectly looked promising for the raw race export; independent index checks exposed missing, duplicate and backward rows. No complete-run metrics were claimed from that export.
- Local helper reuse avoided a new telemetry implementation. One shell quoting attempt failed without changing the collector and was replaced by direct file copying and a small reviewed patch.
- The275 host-test first compile failed on a test signedness warning, then passed after correcting the test; production source was not changed to satisfy it.
- No same-task, same-quality workflow baseline exists, so net efficiency is unproven.

## 修改建议及下一轮验收

- **WF-TEAMHUB-FRESH-INBOX-20261028 [adopted]** Query a sufficient bounded inbox and filter by the last seen ID before hardware ownership decisions; read and acknowledge full new handoffs.；负责人：codex；下次检查：Next physical round observes the current ownership handoff before opening a port; use source state rather than CLI login as evidence of another active session.
- **WF-RACE-CAPTURE-INTEGRITY-20261028 [proposed]** Make race exports use the existing bounded transmit queue and validate declared count plus ordered indices before accepting capture completion.；负责人：opus+codex；下次检查：A new race capture contains every declared index exactly once under the actual wireless link; truncated/repeated fixtures are rejected.
- **WF-LOW-SPEED-OUTER-GAIN-20261028 [proposed]** Treat low-speed direction-gain changes as single-variable physical comparisons, keeping inner-loop and wheel gains fixed and recording mechanical setup.；负责人：opus；下次检查：Fresh paired evidence supports reduced correction without interpreting a filename, an END marker or longer motion alone as stability acceptance.

## 证据

- evidence.json; local validated captures, camera replay and protocol tests; project handoffs377-383.

## 限制

- Real car motion was initiated by the owner; the coordinator configured and captured but did not remotely start or flash it.
- The latest serial owner is Opus. The coordinator cannot claim the current target is zero after the rejected/unexecuted cleanup attempts.
- Build/source, live camera, sparse race telemetry and full speed captures have different evidence boundaries.
- Only sanitized aggregate workflow reports are uploaded; no raw captures, live databases, credentials, conversations or project source.

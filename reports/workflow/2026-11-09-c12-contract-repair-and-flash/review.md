# 2026-11-09-c12-contract-repair-and-flash 工作流复盘

Repair first-turn admission and safe steering handoff in an isolated candidate, validate it and flash after renewed owner authorization.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; transition-contract audit
- 验收状态：partial
- 开始：2026-11-08T17:18:32+00:00
- 测量截止：2026-11-09T02:57:46.605060+00:00
- 墙钟秒数：34754.60506
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| round_wall_including_owner_pause | 34754.60506 | seconds | Task start to measurement cutoff; includes overnight pause requested by owner, not active work time |
| review_local_packaging_so_far | 34.906315 | seconds | Local packaging start to cutoff; upload and later monitoring excluded |
| full_sim_executions | 98 | cases | Saved experiment summaries; includes rejected experiments |
| accepted_full_cases | 8 | cases | Four conditions times two engines |
| accepted_segments | 10 | cases | Saved segment results |
| accepted_fault_stops | 4 | cases | Saved fault and coast checks |
| external_model_calls | 0 | calls | No model delegation during this implementation round |
| subagents | 0 | agents | Coordinator only |
| flash_operations | 1 | actions | Official verified receipt |
| remote_launches | 0 | actions | Serial write allowlist contains read-only queries only |
| active_work | 未知 | seconds | No complete matched measurement available |
| owner_wait | 未知 | seconds | No complete matched measurement available |
| usage | 未知 | tokens | No complete matched measurement available |
| cost | 未知 | currency | No complete matched measurement available |
| all_tool_failures | 未知 | calls | No complete matched measurement available |
| physical_runs_observed | 2 | runs | Two distinct board record starts and complete exported blocks; both stopped30 |

## 验收条件

- Frozen baselines remain unchanged
- Fixed quality and out-of-route limits
- Segment, full-lap and handoff validation
- Verified target build, flash and stationary configuration

## 已完成

- Isolated repair preserves frozen baselines and separates build, flash and live identities.
- Passed segmented/fault checks, eight full-lap cases and all state-handoff audits under unchanged limits.
- Completed clean official target build, verified official flash and stationary wired/wireless identity.
- Saved and attributed both first physical trials; identified repeated outgoing-lane relock timeout without changing protections.
- Reproduced the outgoing recovery/speed coupling defect in an unchanged host controller; recorded incomplete restoration of stable turning parameters.
- Rejected an unpowered manual distance sample and stopped measurement after the owner reported a rollback to an old stable version.

## 未完成

- Physical acceptance failed twice; fixes for the demonstrated controller regression are not implemented.
- Current owner-restored firmware identity is unverified; powered odometry and camera distance calibration are not completed.

## 收益与损耗观察

- A candidate that completed eight laps still had unsafe steering handoffs; state-transition auditing prevented its release.
- Intermediate relock designs rejected correct lanes or missed adjacent corners; bounded raw optical evidence and explicit controller ownership resolved the tested cases.
- A GUI-dependent auxiliary project builder blocked official headless compilation; isolated metadata-only correction enabled the licensed build.
- Owner deferred flashing overnight; wall-clock duration must not be interpreted as active implementation time.
- One coordinator prepared local handoffs; no peer acceptance is claimed.
- Both physical runs stopped at the first-turn exit despite correct target heading; passing modeled laps did not establish physical lane alignment.
- Owner reports old firmware turns normally on the old map. This raises software-regression priority but is not a controlled software-only A/B because the map also changed.
- Reading an open capture file directory length as zero incorrectly led to repeated serial reconnects despite existing raw bytes. A later device disappearance is a separate event.
- Successful historical turn behavior was not completely restored: changed turn gain and ceiling survived while strict exit relock was added without matching low-speed recovery.

## 修改建议及下一轮验收

- **CC-STATE-HANDOFF-C12 [adopted]** Keep per-transition safety audits alongside lap completion metrics, including initial admission and fault/coast checks.；负责人：codex；下次检查：Compare the first physical turn and exit with saved diagnostic evidence without relaxing acceptance limits.
- **CC-HEADLESS-METADATA-C12 [adopted]** Preflight auxiliary GUI-dependent builders before clean official headless builds; preserve compiler options and record metadata diff.；负责人：codex；下次检查：Apply only when the same builder is present; confirm a fresh full source compilation.
- **CC-CONTRACT-PARTIAL-C12 [adopted]** Validate diagnostic decoders on short and saturated records, isolate textual record envelopes from multiplexed binary data, and attribute record completion before later launches.；负责人：codex；下次检查：Use the saved two short physical records and the saturated fixture as capture/decoder regression inputs.
- **CC-STABLE-CONTROL-DIFF-C12 [proposed]** Treat the successful effective controller profile as a regression baseline; separate hardware, route and safety changes and replay real failed exits before broad simulation.；负责人：codex；下次检查：Demonstrate low-speed bounded recovery and safe handoff on both recorded failure states without weakening quality or protection limits.
- **CC-CAPTURE-BYTE-TRUTH-C12 [adopted]** Use bytes actually read and timestamped parsed samples for connection status; distinguish telemetry omission from device disappearance and require a powered stationary cumulative baseline before manual pushes.；负责人：codex；下次检查：When measurement resumes, obtain a valid baseline with main power on before instructing movement; do not integrate sparse velocity telemetry as exact totals.

## 证据

- Frozen source hashes and clean-build manifest
- Segment, fault and full-lap summaries with handoff audit
- Official flash receipt and stationary wired/wireless readback
- Rejected experiments retained locally
- Two separately attributable physical records and owner-confirmed unmoved parked image
- Ten host diagnostic assertions and two preserved failed probe attempts
- Historical effective controller source comparison and local regression review
- Rejected manual sample, capture heartbeat/raw-byte evidence and owner-reported rollback

## 限制

- Simulation does not establish physical completion or calibrated distance accuracy.
- Physical trial results and sensor/odometry calibration remain separate work.
- No measured target camera processing time or stack high-water result.
- No independent peer review or matched workflow baseline; no speedup claim.
- Only sanitized aggregate workflow reports uploaded, no project sources, images, raw serial logs or databases.
- Current physical outcome is two stop30 failures; do not repeat trials or label the candidate physically accepted.
- No new repair or flash after the failed physical trials; the rollback version was reported by the owner and not independently identified.

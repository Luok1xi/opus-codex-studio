# 2026-10-29-prelim-exit-camera-fix 工作流复盘

Repair nominal simulated route exits, then prioritize the owner-reported physical camera half-rate problem with isolated comparison and screen diagnostics candidates.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-29T04:34:59Z
- 测量截止：2026-10-29T05:39:48.825003+00:00
- 墙钟秒数：3889.825003
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native bounded workers | 4 | workers | Read-only trace diagnosis, unit review, camera implementation, independent review; no recursive delegation. |
| Paired-model exploratory and final trials | 68 | trials | Six saved result groups, including all failed variants. |
| Final200fps trials passed | 10 | trials | 12 executed; both lower-grip trials failed. |
| Actual-C camera handoff assertions | 33 | assertions | DMA/VSYNC arrival, invalid/error/repeat paths; old source reproduces failures. |
| OUC snapshot equivalent images | 4 | images | Identical real algorithm output for external versus internal snapshot input. |
| Camera meter checks | 11 | checks | Counters,init,DMAerror,recovery,wrap and worsttext length under sanitizers. |
| Instrumented camera FPS builds | 3 | builds | 100/150/200 requests; eachsource-frozen684files,0errors13warnings. These are not measured frame rates. |
| Race candidate changed source files | 4 | files | Full frozen input/final hash comparison. |
| Camera-only changed source files | 2 | files | Separate frozen input/final hash comparison. |
| Camera worker observed duration | 518 | seconds | Worker-reported observed interval for first patch/testing task; excludes later camera-only build. |
| Codex physical I/O actions | 0 | actions | No serial/flasher/motion tool used by coordinator or native workers. |
| Provider token usage | 未知 | tokens | Unavailable; no output-size substitution. |
| Cost | 未知 | currency | Unavailable. |
| Active work duration | 未知 | seconds | Only observed round wall-clock start/cutoff recorded. |
| Coordination and review overhead | 未知 | seconds | Interleaved; not separately measured. |
| Matched workflow speedup | 未知 | percent | No same-input same-quality workflow baseline. |
| Screen diagnostic candidate checks | 52 | checks | 18 driver, 26 statistics/display, 8 DMA-init checks pass. The unchanged baseline has 4 expected failed assertions in 8 checks. Stubs do not prove physical timing. |
| Additional frozen camera builds | 2 | builds | A 400 configuration-only comparison and separate 200 screen diagnostics. Both 0 errors / 13 existing warnings. |
| Screen worker observed duration | 570 | seconds | Worker reported 05:28:04 to 05:37:34 UTC; includes source, checks and build. Overlaps other work and is not additive wall time. |
| 400 ADS compiler duration | 4.713 | seconds | Saved ADS Build Finished duration; excludes setup and review. |
| Screen ADS compiler duration | 4.527 | seconds | Saved ADS Build Finished duration; excludes setup and review. |

## 验收条件

- Locate the observed simulation failure, implement narrow fixes, retest both plants and communicate remaining physical/deployment limits directly to Opus.

## 已完成

- Used the existing current-source200fps failed trace and Opus gain sweep instead of repeating a broad initial search. Original PB5.04m exit follows post-turn oscillation; turn-entry yaw was740.8deg/s versus4.2 with intermediate gains. This is simulator evidence, not a measured physical root cause.
- Found a second failure under10mm start offset: reconstructed encoder position moved the first-corner observation outside the capture window. Halving acceleration increments restored paired offset completion without loosening any line-loss or track gate.
- Selected only four source-file changes: yawPI.2/.012, launch/later acceleration branch increments5/10, stable camera snapshot with early DMA-buffer release and preserved frame metadata. Rejected offset, earlier-turn, extra-brake and map-brake experiments that caused failures elsewhere.
- Final source-identical paired200fps checks pass10/12: nominal C8.796s/PB9.095s, speed248/303, seed2 and10mm lateral offset all finish24entries. Bothmu1.2 cases still fail.
- Camera snapshot concurrency fix passed33 actual-C assertions and4 OUC image-equivalence cases under sanitizers. Independent source review found no new blocking race, image-consumer issue or interference with standalone wheel/yaw test modes.
- ADS compiled the race candidate with0errors13existingwarnings; sourcefreeze684files is stable. At the owner camera-first steering relayed in Opus405, built a separate two-file camera-only candidate that retains the existing control gains/ramp for stationary measurement.
- Kept Opus as exclusive hardware operator, sent direct project handoffs and preserved active firmware paths. No Codex serial, flash or motion action occurred.
- Delivered separate 100/150/200 instrumented camera HEX variants with VSYNC-total and buffer-owned-skip counters; 11 additional sanitized checks and independent review pass. Original control settings retained. Physical results subsequently showed about 50 processed fps at 100 configured and about 95 at 200 configured; the earlier buffering hypothesis did not explain the result by itself.
- Built the owner-requested 400 configuration-only comparison. All 684 source files remain frozen; exactly one macro differs from the delivered 200 baseline. Actual 400-configuration performance is not inferred from compilation.
- Opus reports flashing the 400 comparison (handoff 423); the saved log independently ends with content-verification PASS. Its measured frame rate has not yet been reported at this cutoff. Codex did not read serial or operate the hardware.
- Built a separate 200 diagnostic candidate with the corrected DMA initialization handle, per-second VSYNC/skip/capture/error/IRQ screen counters and elapsed-time-normalized processing FPS. Control parameters and capture architecture remain unchanged; physical acceptance is pending.

## 未完成

- No full race release: lower-grip robustness failed. The simulation assumes 200 fps; the owner reports about 95 processed fps with the 200 configuration. The earlier 100 configuration still processed about 50 fps after the snapshot patch. The physical half-rate problem remains unresolved.
- Physical yaw response and the11.314percent raw encoder speed-unit difference are not yet aligned. The reviewed normalization design was not mixed into this root-cause patch.
- Opus flashed the camera-only 100 and instrumented 200 candidates; saved flasher logs end in verification PASS. Subsequent observation is screen-only at the owner request. Boot target 40 is a bring-up default, not a newly validated full-map profile.
- One rejected map-brake experiment reached entry24 but terminal stop26 preceded the simulator lap endpoint; this is retained as a separate end-distance observation, not hidden by modifying the validator.
- The first diagnostic window can include startup counts; interpret the second complete window onward. Screen diagnostics localize symptoms but do not yet prove the sensor clock, VSYNC edge reliability or physical DMA timing.
- The five additional LCD text rows incur display overhead whose effect on processed FPS has not been measured. They do not add serial traffic. The diagnostic build is an observation aid, not a claimed performance release.

## 收益与损耗观察

- Independent trace diagnosis corrected an initial simplistic weak-turn interpretation: the oscillation begins on the preceding exit. A35mm fallback-offset assumption was also corrected to the actual28mm table.
- A camera test fixture initially fabricated a DMA completion before DMA was active; it was corrected, then tests were refreshed after the memory-barrier addition. Production source was not weakened to satisfy the fixture.
- One exploratory matrix was launched after its compiler returned a running session but before the final completion receipt was read. All resulting binary fingerprints matched the completed builds; final acceptance was launched only after explicit build completion. Avoid that orchestration ordering in future.
- An existing launch_time equality boundary can retain the initial5-count increment longer; it was recorded rather than mixed into this fix. Acceleration descriptions use actual branches and caps.
- Owner steering via Opus405 changed immediate delivery to a camera-only build, preserving motor-control settings during stationary frame-rate measurement. The tested race patch remains available separately.
- Opus408 accepted the snapshot patch;410 requested150/200 alternatives plus acquisition counters. Delivered separately named100/150/200 instrumented builds. A second native review checked counter semantics,trigger edge,status capacity and parser compatibility.
- Opus411 reports the firstcamera-only build flashed; the savedflashlog contains verificationPASS. He also reported that absent-wireless busy gating suppresses visual status and that gyro bias needs checking. Those live issues were not silently folded into the frozen camera variants.
- The camera-only ADS window was initially not ready for menu discovery; the worker retried once and completed. Its observed follow-up interval was138seconds, excluding later instrumented builds.
- No paired workflow baseline exists, so improved technical test outcomes do not establish net workflow speedup.
- Do not equate a configured camera rate with sensor output. Without VSYNC, completed-frame and error counts, half-rate processing can arise from either acquisition loss or sensor timing. The sensor-clock hypothesis is unmeasured, and the historical owner measurement is not disproved.
- The original status sender busy guard returns only from the sender; it does not suppress the outer processed-frame counter update. Moving sampling earlier and normalizing elapsed time improves reporting, but is not evidence that the old busy guard caused the half-rate result.
- Independent source review confirmed that DMA initialization cleared a service request using an uninitialized channel object instead of the initialized local handle. Its contribution to the measured half-rate remains unproven.
- Owner steering via Opus 418 requested a configuration-only 400 comparison. The later diagnostic candidate remains separately named at 200; no ISR-copy or CPU1 architecture rewrite was attempted without acquisition measurements.
- A proposed diagnostic row below the display was corrected before delivery after checking the actual 320 by 240 landscape initialization. The existing 188 by 120 image leaves space on its right for counters without covering S5 instructions.
- Two isolated ADS windows were serialized for build-menu actions to avoid shared-focus interference. The 400 import needed one bounded permission recovery; no source rework was needed for that comparison.
- The screen worker corrected two auxiliary-command issues (function-pattern spacing and PowerShell/Python quoting) before evidence collection; the source compiled once successfully. Independent review confirmed the first-window caveat and no new blocking source defect.

## 修改建议及下一轮验收

- **WF-FAILED-TRACE-BEFORE-MATRIX-20261029 [adopted]** Compare the failed and passing trace around the preceding state transition, then run a bounded perturbation set before declaring a gain successful.；负责人：codex；下次检查：Next tuning handoff includes the onset of divergence and failed perturbations, not only the final exit location.
- **WF-ONE-PHYSICAL-FACTOR-20261029 [adopted]** Package the acquisition fix separately when the immediate physical question is frame rate, preserving unrelated control settings for that measurement.；负责人：codex；下次检查：Opus reports before/after physical acquisition and processed rates with the camera-only build identity.
- **WF-CAMERA-COUNTS-BEFORE-ARCHITECTURE-20261029 [adopted]** Show sensor-event, capture-completion, deliberate-skip and DMA-error counts together before choosing a buffering or sensor-timing fix.；负责人：codex；下次检查：Compare screen counter rates and processed FPS under the same frozen firmware and scene.

## 证据

- evidence.json; local paired-model results, actual-C checks, frozen ADS receipts, independent reviews and project handoffs 401 onward. Physical observations are attributed separately from local tests.

## 限制

- Sanitized aggregate workflow report only: no raw telemetry, private source, sessions or live databases uploaded.
- Two uncalibrated physical models and synthetic DMA scheduling do not prove real-car speed, frame rate or grip.
- Higher-speed full-lap readiness remains unaccepted despite fixing the nominal200fps failure.

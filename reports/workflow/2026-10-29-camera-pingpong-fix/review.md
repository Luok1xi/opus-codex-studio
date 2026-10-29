# 2026-10-29-camera-pingpong-fix 工作流复盘

Repair the camera acquisition ownership guard after measured counters confirmed its dominant frame loss, preserving the control and route code.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-29T09:52:36Z
- 测量截止：2026-10-29T10:30:06.765446+00:00
- 墙钟秒数：2250.765446
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native workers | 3 | workers | One implementation/build worker, one DMA and memory design reviewer, one ownership reviewer; no recursive delegation. |
| Saved-recording intervals independently checked | 11 | intervals | Complete status windows from one saved recording, no serial access. |
| Frozen firmware candidates | 2 | builds | ADS compiler logs and frozen-source receipts; not physical acceptance. |
| Final actual-C assertions passed | 338 | assertions | 265 ownership/DMA/copy checks plus 44 timing and 29 serial-gating regressions, all zero failures. |
| Product defects found by the new checks and repaired | 1 | defects | One latched DMA error was counted repeatedly while reset was pending; acknowledge once before reset, then rerun successfully. |
| Worker test harness compile failures | 1 | attempts | Implementation worker reported one mock type/constants/indentation correction; not a product compiler failure. |
| Implementation worker observed elapsed time | 1907 | seconds | Worker observed 09:55:05 to 10:26:52 UTC; includes overlapping reviews and is not additive coordinator wall time. |
| ADS compiler runs | 3 | runs | Initial 200, error-counter-corrected 200 and matched 400; all zero errors and 13 existing warnings. |
| Final 200 compiler duration | 4.62 | seconds | Saved ADS build summary; excludes setup, tests and review. |
| Final 400 compiler duration | 4.534 | seconds | Saved ADS build summary; excludes setup, tests and review. |
| Codex hardware operations | 0 | operations | No serial port open, flash or motor command by this coordinator or its workers. |
| Provider-reported token usage | 未知 | tokens | No complete provider usage ledger for this stage. |
| Provider cost | 未知 | currency | Billing evidence unavailable. |
| Coordination and review active time | 未知 | seconds | Activity overlaps; no complete mutually exclusive timing ledger. |
| Total tool failures | 未知 | failures | No complete audited tool ledger across workers. |
| Acceptance rework count | 未知 | iterations | Physical acceptance remains pending; design clarifications are not counted as failed deliveries. |
| Archive duration | 未知 | seconds | Measured separately in the archive receipt after remote verification. |

## 验收条件

- Independently reproduce the handoff's aggregate rates from the saved recording without opening hardware.
- Two DMA capture buffers and the existing stable algorithm snapshot; correct metadata ownership, latest-ready overwrite counting and bounded abnormal recovery.
- Actual-C scheduling, image integrity, linked descriptor and regression checks; independent state-machine and memory review.
- Frozen ADS 200 and 400 candidates, hashes, source differences and memory budget; only FPS configuration differs between the paired variants.
- Deliver firmware and measured acceptance instructions to Opus; distinguish offline evidence from later flash and live results.

## 已完成

- Independently reproduced the receiver's aggregate counter diagnosis from complete saved records before changing the acquisition architecture.
- Implemented two capture buffers with a stable algorithm snapshot, frame-specific sequence/time metadata, latest-ready replacement accounting and protected foreground copying.
- Checked the actual linker memory banks before allocating the additional frame; reviewed descriptor switching and bounded abnormal capture recovery.
- Built and froze matched diagnostic candidates while preserving existing control and route behavior; independent review and implementation checks are recorded locally.
- Delivered firmware, four driver source files and a configuration-preserving patch to the receiver, separating software validation from flashing and physical frame-rate verification.
- Audited the newly requested core partition: the second core is idle in this baseline. Recommended a complete vision pipeline there, with control and route decisions retained on the first core. The receiver confirmed this split and independently owns the port.

## 未完成

- The firmware candidates have not been physically accepted by this coordinator. Actual acquisition/processing rates, image integrity and timing under track lighting still require receiver verification.
- Host-side interrupt and register models cannot prove the physical waveform, DMA bus timing or absence of hardware faults.
- Integration with the receiver's independently owned second-core port awaits its frozen source. These two delivered binaries remain first-core reference builds; no second-core performance claim is made.

## 收益与损耗观察

- Live evidence was already collected by the hardware owner. Independent parsing of the saved recording avoided another port session and repeated owner questions.
- Independent design review identified an insufficient default SRAM bank and the risk of joining incomplete frames before implementation was finalized.
- Source implementation and two bounded read-only reviews were separated; build GUI and hardware ownership remained exclusive.
- No matched single-agent baseline exists. These local defect-prevention observations do not establish net speedup.
- The final-state source review also corrected a misleading vector-table assumption and a preprocessor enum trap in memory placement; both were communicated before the independent second-core port was frozen.
- A newer receiver handoff superseded the earlier request for this coordinator to move the core. Ownership was reconciled rather than writing competing ports. Additional sensor configurations are deferred to the integrated port instead of multiplying obsolete reference binaries.

## 修改建议及下一轮验收

- **WF-LINKER-BANK-BEFORE-FRAME-ALLOCATION [adopted]** Check contiguous capacity in the actual linker bank before adding a frame buffer.；负责人：codex；下次检查：Verify the new symbol address and remaining stack/CSA reservations in each frozen build map.
- **WF-SAVED-COUNTERS-BEFORE-HARDWARE-REPEAT [adopted]** Use complete saved status windows to cross-check a receiver diagnosis before asking for another measurement.；负责人：codex；下次检查：Record valid-window count, corruption filters and limitations for the next diagnostic handoff.
- **WF-FRAME-OWNERSHIP-FAULT-TESTS [adopted]** Keep completion, foreground copying, skipped acquisition and ready replacement distinct in tests and diagnostics.；负责人：codex；下次检查：Receiver compares capture, processing, replacement and abnormal-recovery rates with timing under one frozen firmware.
- **WF-EARLY-REVIEWABLE-PATCH [proposed]** Expose the smallest reviewable implementation before completing all harness work, allowing bounded reviewers to inspect real code sooner.；负责人：codex；下次检查：Record time from assignment to first reviewable source and compare quality-matched tasks; no speedup assumed.

## 证据

- evidence.json; local frozen compiler receipts, actual-C checks, two independent reviews and verified project handoffs.

## 限制

- Sanitized workflow aggregates only; raw source, telemetry, sessions and databases remain local.
- No claimed real-car performance gain or causal workflow speedup.

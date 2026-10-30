# 2026-10-30-vision-ipm-research 工作流复盘

Study suitable GitHub smart-car vision code, test inverse-perspective limitations, assess core placement and prepare an evidence-based ground-path fusion design.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + TEAMHUB.md, read 2026-10-30
- 验收状态：partial
- 开始：2026-10-30T01:53:43Z
- 测量截止：2026-10-30T02:18:58.130624+00:00
- 墙钟秒数：1515.130624
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Wall time to research delivery cutoff | 1515.131 | seconds | UTC start/cutoff; includes research, tests, independent review, prototype repair and handoff. Archive follows. |
| Received native worker scopes | 3 | agents | Source study, unchanged-module stress tests, architecture and prototype review; coordinator consolidated. |
| Source study worker observed interval | 1106.782 | seconds | Worker supplied same-clock start/end; overlaps coordinator and other workers, not additional elapsed time. |
| Actual C prototype assertions passed | 27 | checks | Known circle, hidden bump, horizontal turn, duplicates, cusp, gap, nonfinite input and capacity cases; ASan/UBSan. |
| Prototype complete test invocations | 2 | runs | Initial implementation, then reviewer-found cusp correction; separate narrow negative-control review also executed. |
| Prototype behavioral defects fixed | 1 | defects | Independent real-C reproduction of backtrack summarized as straight; pre-sampling cusp rejection and focused retest. |
| External component semantic comparison modes | 3 | modes | Original C executed with common input; outputs differed so performance comparison was rejected. |
| External component three-mode runs | 2 | runs | Worker normalized extra terminal newline to match Git blob and repeated semantic regression; no throughput claim. |
| Projection stress execution rounds | 2 | runs | Second run added forward-distance markers to expose a missed calibration sensitivity metric; unchanged tested module. |
| Source study product rework | 0 | changes | Worker reported no product source edits; only local source normalization/harness compilation. |
| Hardware actions | 0 | operations | No serial, flashing or motor control; production manifest reverified unchanged. |
| Total tool failures | 未知 | operations | Read-only Git permission failures, one GitHub transport failure, an encoding probe and premature report reads occurred; no complete counter. |
| Exclusive coordination wait | 未知 | seconds | No isolated wait attribution; work overlapped. |
| Exclusive review overhead | 未知 | seconds | Not separately instrumented from research/prototype changes. |
| Provider token usage | 未知 | tokens | No complete parent/children provider usage evidence. |
| Actual cost | 未知 | currency | No billing evidence. |
| Archive overhead | 未知 | seconds | Separate archive completion receipt records time after this cutoff. |

## 验收条件

- Read concrete GitHub smart-car source and distinguish verified techniques from unverified ranking claims
- Assess CPU placement from current source and saved timing, not assumptions
- Extend actual-C geometry/failure tests and compare useful implementation options
- Deliver a source-linked fusion design and any evidence-supported isolated improvement, preserving live firmware

## 已完成

- Read pinned public source and licenses; separated same-track embedded systems, servo-car techniques and isolated table benchmarks.
- Verified current production source identity and core ownership, memory, time-base limitations, historical timing and control units.
- Ran actual unchanged C on curve/topology/gap/noise/calibration cases and rejected an external optimization comparison with unequal outputs.
- Implemented and independently reviewed an isolated bounded multi-point geometry prototype after research; repaired a reproduced cusp defect.
- Delivered detailed fusion design and evidence to Opus through the project database.

## 未完成

- Current-pose physical calibration, full board latency measurement, production integration and matched driving acceptance remain pending.
- The final Opus handoff has not received acceptance; no vehicle performance improvement is claimed.

## 收益与损耗观察

- Real source inspection showed mature projects connect geometry to spatial filtering, ordered paths, route selection and preview; a two-point projection alone omits internal curves.
- A nominally optimized remap component produced different values for the same out-of-bounds query across modes; checking semantics prevented a misleading speedup transfer.
- Forward-distance markers exposed calibration errors hidden by tests that measured only line heading and lateral deviation.
- Independent architecture review prevented cross-core time origins and nominal encoder units from being confused with synchronized timestamps and measured vehicle speed.
- Prototype review found a cusp case missed by initial tests; it was fixed before delivery, with memory claims limited to the actual buffers counted.
- No matched workflow baseline exists; useful defect discoveries do not quantify net speedup.

## 修改建议及下一轮验收

- **VISION-RESEARCH-EQUIVALENCE-20261030 [adopted]** Before adopting an optimization benchmark, run equal inputs including invalid-domain cases and compare observable outputs.；负责人：codex；下次检查：Future remap or geometry changes retain the negative-control fixtures and do not compare mismatched semantics.
- **VISION-RESEARCH-GEOMETRY-20261030 [adopted]** Keep calibration accuracy, route topology, local path shape, compute cost and closed-loop results as separate acceptance gates.；负责人：codex；下次检查：The next production candidate reports each gate, retaining hidden-bump, cusp and mismatched-branch cases.
- **VISION-RESEARCH-BOARD-20261030 [proposed]** Measure a common-timestamp vision-to-control chain under the actual suction working pose before accepting dynamic preview/control fusion.；负责人：opus；下次检查：Receive real calibration and board timing plus independent integration acceptance.

## 证据

- Pinned public-source report and actual original-C semantic regression.
- Unchanged-module stress results, current-core audit, prototype C results and independent review.
- Aggregate artifact hashes and project handoff IDs in evidence.json.

## 限制

- Offline prototype correctness does not establish real driving improvement.
- Historical sampled timing does not bound the current version worst-case execution time.
- Native parallel work has no measured causal workflow speedup.
- Private remote archive completion is verified separately.

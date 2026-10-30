# 2026-10-30-vision-autop-ab 工作流复盘

Implement an AuTop-style sparse inverse-perspective path pipeline on CPU1 and compare it fairly with the existing lightweight geometry.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + TEAMHUB.md read 2026-10-30
- 验收状态：partial
- 开始：2026-10-30T02:24:10Z
- 测量截止：2026-10-30T03:07:30.108519+00:00
- 墙钟秒数：2600.108519
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Wall time to implementation delivery cutoff | 2600.109 | seconds | UTC start to cutoff; includes parallel module work, tests, evaluation, review, integration, target builds and handoff. Archive follows. |
| Native worker scopes completed | 3 | agents | Module, fixed-input evaluation, independent review; coordinator integrated and consolidated. |
| Module elapsed time to ready | 1119 | seconds | 02:27:25 to 02:46:04 UTC supplied by worker; overlaps other work. |
| Module complete test script runs | 3 | runs | Worker evidence; final 190 module and 114 legacy assertions passed. |
| Independent targeted assertions passed | 75 | assertions | ASan/UBSan, signed normals, bad spans, endpoints, discontinuity, cusp and projection domain. |
| Original visual same-output comparisons | 120 | comparisons | 40 fixed images times 3; scalar fields, whole binary image and full boundary arrays matched. |
| Formal performance sessions | 1 | sessions | After isolated ADS exited; 21 alternating pairs for each of two scopes. No favorable rerun. |
| Formal performance elapsed time | 15.631 | seconds | Evaluator start/end includes the final functional and timing execution. |
| Successful target configurations | 3 | configurations | Independent artifacts and source manifests for A, B and default OFF; all 0 errors. |
| Observed target build recovery events | 2 | events | New file omitted before Eclipse refresh caused unresolved symbol; a later external-header change gave a no-op build. Both corrected before saving accepted artifacts. |
| Geometry design revisions recorded | 3 | revisions | Normal estimation moved after edge sampling; added centre resampling; restored a bounded physical-distance window after observed quantization failure. |
| Test harness integration corrections | 3 | events | ABI size guard caught evolving summary layout; full-struct equality initially compared unspecified padding; clean-build parser initially expected a banner absent from this builder. Corrected before claiming passes. |
| Clean target rebuilds matching prior HEX | 3 | builds | New Opus evidence raised header-dependency concerns. All generated objects were removed inside the verified isolated Debug directory; 175 sources rebuilt per variant and all three HEX hashes matched. |
| Total tool failures | 未知 | operations | Some metadata/path/CLI probes failed; no complete per-call inventory was maintained. |
| Exclusive coordination wait | 未知 | seconds | Overlapping work, no separate wait instrumentation. |
| Exclusive review overhead | 未知 | seconds | Independent review overlapped implementation, test and target build work. |
| Provider token usage | 未知 | tokens | No complete provider usage records for parent and children. |
| Actual cost | 未知 | currency | No billing evidence. |
| Archive overhead | 未知 | seconds | Separate remote verification receipt records completion after this cutoff. |

## 验收条件

- Implement an AuTop-style sparse point IPM/filter/resampling/geometry B variant in an isolated TC264 candidate
- Retain existing A two-section geometry for same-input comparisons
- Compare correctness, useful path information, timing and memory with identical tests and expose failures
- Build reviewable target artifacts and hand off to Opus without overwriting live work or touching hardware

## 已完成

- Implemented bounded sparse projection, smoothing, edge and centre arc resampling, normal offset and local geometry in an isolated candidate.
- Integrated CPU1 shadow computation and CPU0 coherent diagnostic snapshots without changing existing pixel-based control parameters.
- Passed module and regression suites, independent targeted review, real ISR copy and shared-frame-reader checks.
- Retained both early and revised B results on fixed input; reported geometry benefits, quantization noise, rejected noisy samples and range truncation.
- Built A_MODEL, B_MODEL and B_OFF with matching source/config/HEX records; inspected target memory and visible call-chain stack estimates.
- Rechecked frozen live files and sent a concrete delivery to Opus through the project database.

## 未完成

- Current-car lens/pose/stripe calibration, route-confirmed branch selection, robust curvature and adequate forward coverage remain prerequisites for control integration.
- Board latency, whole-runtime stack high-water, closed-loop driving benefit and final Opus acceptance remain unverified.

## 收益与损耗观察

- The first B version exposed quantized normals and false curvature; checking the reference call sites identified a missing physical-distance window. The correction was explicitly data-informed, not a blind validation win.
- A six-case normal-width addendum was declared before B results because inherited horizontal-width fixtures did not match the centre-offset assumption.
- More geometry information and stronger rejection rules do not imply universally higher quality: some noisy inputs and S-curve range cases remained worse or unavailable.
- Eclipse cached external source/header edits. Forced refresh plus artifact freshness checks and different memory maps prevented a stale binary from being labeled as a new variant.
- Host benchmarks were serialized after ADS exited. Different functionality and target architecture prevent interpreting the cost ratio as a general speedup or board FPS claim.
- Visible target CPU1 stack estimates differ from host sanitizer frames; recursive global metadata prevents a full worst-case stack guarantee.
- A small number of premature artifact/metadata probes were avoidable; future reads should use worker ready notices and known paths.

## 修改建议及下一轮验收

- **AUTOP-API-20261030 [adopted]** Freeze the C API layout before independent wrappers, and retain ABI assertions and full-field comparisons that exclude C padding.；负责人：codex；下次检查：Further summary changes update the versioned wrapper before any benchmark executes.
- **AUTOP-BUILD-20261030 [adopted]** Refresh externally edited Eclipse resources before building, then bind HEX files to source/config manifests and linker-map differences.；负责人：codex；下次检查：Future variants fail delivery when the accepted artifact predates changed source.
- **AUTOP-QUALITY-20261030 [adopted]** Separate shape recovery, calibrated accuracy, continuity/range, route trust and real board budget instead of declaring an overall winner from one metric.；负责人：codex；下次检查：Preserve all failed noise and S-range cases in the next declared revision.
- **AUTOP-HARDWARE-20261030 [proposed]** Opus reviews the isolated delivery and obtains current calibration, matched board latency and route identity before using ground geometry in control.；负责人：opus；下次检查：Receive explicit hardware evidence and final acceptance.

## 证据

- Fixed-input actual-C report with original and revised B evidence, including all failures.
- Module, independent review and target build records; aggregate hashes and handoff IDs in evidence.json.

## 限制

- No matched workflow-quality baseline exists; parallel work does not prove workflow acceleration.
- Host CPU cost is not target runtime or measured camera FPS.
- The physical-distance-window change used observed evaluation data and has no independent holdout.
- Physical calibration, control integration and real driving improvement are not established.
- Remote archive verification is recorded after this report cutoff.

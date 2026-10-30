# 2026-10-30-vision-ipm-closedloop 工作流复盘

Optimize sparse inverse perspective geometry and test whether fixed or velocity-scaled preview improves closed-loop smart-car tracking.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md and TEAMHUB.md
- 验收状态：partial
- 开始：2026-10-30T03:12:47Z
- 测量截止：2026-10-30T04:26:50.805176+00:00
- 墙钟秒数：4443.805176
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Wall time to delivery cutoff | 4443.805 | seconds | UTC start through delivery, review, target build and handoffs; archive follows. Parallel work overlaps. |
| Simulation executions | 113 | runs | 4 baseline +72 development +36 frozen validation +1 exact replay for frame capture. |
| Frozen validation elapsed | 53.907572 | seconds | Observed runner start/end; not simulated lap time. |
| Frozen validation primary passes | 0 | of 36 | All failures retained:35 off-track and1 protection stop. No lap improvement established. |
| Independent geometry holdout passes | 41 | of 52 | All11 failures retained;2pixel noise remains limited. |
| Independent C checks passed | 173 | checks | Geometry/controller/PID/protection suites; preserved negative controls reproduced3 prior failures. |
| Native worker scopes completed | 3 | agents | Geometry, simulation, independent review. No recursive delegation. |
| Host build invocations | 10 | builds | Simulation-worker evidence, two executables per invocation. |
| Clean target build configurations | 1 | configurations | 177 C units;0 errors and11 prior warnings; default control OFF. |
| Target compiler-reported build time | 4.345 | seconds | Build-log elapsed only, excludes setup and verification. |
| Development revisions | 3 | stages | Initial integration, strict timestamp gate, then final clamp and common guard experiment; all72 runs preserved. |
| Additional geometry revision | 1 | revision | Independent review required full2D segment gap and minimum5-point support. |
| Hardware operations | 0 | operations | No serial, flash or movement. |
| Exclusive review overhead | 未知 | seconds | Review overlapped implementation and simulations. |
| Exclusive coordination wait | 未知 | seconds | Not separately instrumented. |
| Complete tool-failure count | 未知 | operations | Several path/schema/permission probes failed; no complete census. |
| Provider token usage | 未知 | tokens | No complete provider usage record across coordinator/children. |
| Actual cost | 未知 | currency | No billing evidence. |
| Archive overhead | 未知 | seconds | Recorded separately after cutoff. |

## 验收条件

- Integrate image-derived IPM geometry into a real closed-loop simulation controller
- Use existing C and PyBullet plants with explicit camera, route and baseline provenance
- Compare fixed conditions and report failures, coverage, stability, error and completion time
- Deliver tested bounded C changes and artifacts to Opus, preserving live firmware and hardware boundaries

## 已完成

- Implemented bounded C3 geometry, coherent frame publication and guarded pure-pursuit integration in isolated source.
- Fixed stale-frame admission and final-rate-clamp defects; reproduced and isolated a protection quantization issue.
- Ran two physical models with real camera-to-CPU1-to-controller glue and retained all development and validation failures.
- Independent geometry holdout and C review completed; target build and memory/visible stack inspected.
- Delivered explicit negative whole-route result, local gains, source manifests and a concrete branch-binding proposal through the project database.

## 未完成

- No validated whole-route speed/stability gain; all36 held-out runs failed the complete-route criterion.
- Online junction identity and complete2D branch control remain unimplemented and unvalidated.
- Real camera calibration, board timing, interrupt-stack high-water and physical driving benefits remain unverified.
- Final external Opus acceptance and artifact-ledger acknowledgement were not received.

## 收益与损耗观察

- Correcting a stale simulator entry was essential: an earlier wrapper never executed the new CPU1 path. Event-to-controller glue and binary/source fingerprints were checked before comparison.
- Ordinary-track local gains did not transfer to route completion; adaptive preview also increased arc peak error. A reference algorithm did not imply a universal win.
- A proposed exit blend had zero eligible plain frames and was rejected before implementation. Full2D paths provide an observational basis, but no online branch-binding proof.
- Review corrected an overstatement: the first selected frame had common near targets, not an already-wrong250mm target. Later branch divergence occurred after route state pointed right.
- Target memory improved relative to priorB, but visible CPU1 stack increased. An existing abnormal ISR call path already exceeded allocated stack numerically; local fit size cannot prove whole-stack safety.
- Existing frozen-tree drift was three comment translations, with matching noncomment tokens. It was preserved and reported rather than overwritten.
- New connector probes repeated argument-schema errors; retaining verified invocation contracts would reduce avoidable coordination overhead.

## 修改建议及下一轮验收

- **IPM-GLUE-20261030 [adopted]** Bind simulator callbacks, actual active-controller counters and source/binary fingerprints before spending runs on algorithm comparison.；负责人：codex；下次检查：A new integration must demonstrate CPU1 execution and controller use before performance claims.
- **IPM-VALIDATION-20261030 [adopted]** Separate development corrections from a frozen independent validation and retain every failure and adverse peak.；负责人：codex；下次检查：Future optimization uses a new declared validation set; these36 results cannot be recycled as blind success.
- **IPM-BRANCH-20261030 [proposed]** Review a frame-versioned junction/route binding before using full2D paths inside gyro turns.；负责人：opus；下次检查：No simulator ground-truth branch choice; adjacent and same-direction junctions tested with explicit tokens.
- **IPM-BUDGET-20261030 [proposed]** Measure per-core runtime and ISR stack high-water before enabling the new controller on the car.；负责人：opus；下次检查：Separate CPU1 projection cost, CPU0 fitting cost and existing abnormal call paths.

## 证据

- Hashes and aggregate counts in evidence.json; full local outcomes and source-bound target receipts retained.

## 限制

- No matched workflow-quality baseline exists; no workflow speedup claimed.
- Local tracking-error changes are development diagnostics, not complete-lap gains.
- Model calibration and declared processing delay are not measured MCU performance.
- Target construction defaults to disabled IPM control and uncalibrated/OFF projection.
- Independent geometry holdout is synthetic point noise, not measured camera-image noise.
- Archive verification completes after this cutoff.

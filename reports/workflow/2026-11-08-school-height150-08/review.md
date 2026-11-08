# 2026-11-08-school-height150-08 工作流复盘

Deploy isolated08 after offline regression, compare the supplied control source, and diagnose physical visual-stop failures without confusing simulation with real acceptance.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + immutable source freeze + active-path audit + physical evidence separation
- 验收状态：partial
- 开始：2026-11-08T09:11:58.681307+00:00
- 测量截止：2026-11-08T09:53:41.843045+00:00
- 墙钟秒数：2503.161738
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| source_files | 688 | files | Frozen source manifest rehashed after deployment |
| changed_from07 | 4 | files | Reviewed source delta |
| route_passed | 8 | cases | Two engines, same eight conditions and criteria |
| real_input_cases | 37 | cases | 37cases852checks and sanitizer validation |
| motion_gate_checks | 19 | checks | Actual controller with hardware stubs |
| launch_cases | 15 | cases | 374963checks using extracted actual functions |
| clean_build_wall | 6.342 | seconds | Build log |
| flash_wall | 4.031 | seconds | Official flasher log |
| flash_actions | 1 | actions | Official verification receipt |
| remote_starts | 0 | actions | Only read-only device queries; recorder sends no commands |
| read_only_queries | 14 | queries | Initial3,wired1,wireless1,diagnostic3+3,image retries1+1,pre-resistor1; failed replies retained |
| captured_start_intervals | 4 | attempts | Three intervals in first recorder, one in second; not all linked to owner-reported three attempts |
| measured_task_wall | 2503.161738 | seconds | Initial clear-scene work timestamp through cutoff; includes user waits and analysis |
| agents_dispatched | 0 | agents | Coordinator only; no independent reviewer claimed |
| total_tool_errors | 未知 | errors | Not fully instrumented |
| usage | 未知 | tokens | Provider accounting unavailable |
| cost | 未知 | currency | Billing unavailable |
| review_archive_overhead | 未知 | seconds | Archive timing will be stored in its receipt |

## 验收条件

- Clean identified deployment
- Effective control-source comparison
- Physical resistor and route completion

## 已完成

- Preserved688 manifest-listed source files and isolated the08 candidate; four changes from07, seven from06.
- Added a small-residual pose-correction deadband after reproducing07 longitudinal localization drift; kept matching/out-of-line/stale criteria unchanged.
- Eight of eight unchanged route cases passed in two simulation engines; real-frame and motion/launch checks passed; no claim of physical acceptance.
- Clean build passed with zero errors and14 inherited warnings; tested/built source identity and historical snapshots verified.
- User authorized deployment and confirmed actual download preparation. One official flash verified; wired and wireless readbacks matched125/30/47.
- Read-only record spans several start/stop attempts across two boot epochs; user reports three starts repeatedly stopping at the shown location. Per-attempt correspondence is not assumed.
- A captured run shows matching error rising above admission threshold before drive inhibition and stop3. User reports stopping at a resistor.
- Verified six Ningxia reference files against original extraction manifest; checked actual initialization and active125 control path.
- Documented missing dedicated resistor handling, bypassed legacy route/control path, inherited symbol geometry and limited diagnostic coverage.
- Preserved two complete board records of55 and60 samples and complete post-stop/pre-resistor images with owner-specified scene context.
- Later explicit identity readback succeeded. A missing image reply and a one-item array helper bug were retained as failed attempts; corrected helper obtained complete images and recording resumed.
- Exact frozen vision code accepts some offline pose hypotheses for both resistor and sparse post-stop images; this does not establish true pose or dynamic reliability.

## 未完成

- Obtain a continuous resistor entry/body/exit sequence and per-frame pose/rejection evidence; current static frames do not isolate the dynamic cause.
- Implement and validate the evidence-supported visual correction in a new isolated candidate, without relaxing stop protection.
- Accept physical125/fan30 resistor crossing, first corner and repeated complete laps; current08 has failed physical trials.

## 收益与损耗观察

- Offline route success did not predict physical resistor passage; missing corresponding failure-scene evidence is an acceptance gap.
- The source contains legacy visual modules, but the active125 path uses a different navigator; auditing call paths prevents ineffective gain changes.
- Effective yaw gains equal the reference after profile initialization; an older report based on earlier assignments is inapplicable.
- Map symbols exist but their placement/shape is inherited; no dedicated resistor crossing state machine is connected to the active path.
- Recorder began after the initial failure; later attempts were captured. Latched stop codes and boot resets were separated from new stop events.
- Helper exploration included missing-path reads and oversized output; no exact failure count was measured.
- Parked diagnostic returned valid log/image data but no explicit identity response; retained the failed receipt rather than claiming complete query success.
- No matched workflow baseline or independent reviewer; no workflow speedup claim.
- Single-item PowerShell array expansion caused one image-helper wait failure; corrected in the local helper only. Source/vehicle remained unchanged.
- Both supplied real frames admit some offline pose hypotheses, demonstrating that a low match residual alone cannot certify true localization.

## 修改建议及下一轮验收

- **CC-08-ACTIVE-PATH-ELEMENT-ACCEPTANCE [proposed]** Require an active-call-path feature inventory and real element entry/body/exit evidence before describing a visual port as complete.；负责人：codex；下次检查：Next candidate documents which element outputs drive steering and passes the captured resistor sequence.
- **CC-08-FAILURE-EVIDENCE-CAPTURE [proposed]** Preserve concrete navigation rejection reason and pre-stop visual evidence; begin recording before manual launch.；负责人：codex；下次检查：A physical failure can be tied to an exact reason, frame and route state without inference from a latched stop code.

## 证据

- Immutable source/HEX manifests and clean-build log
- Eight-case route regression and exact-source image/control/launch checks
- Official flash and wired/wireless readback receipts
- Read-only serial record with boot-separated start/stop transitions
- Six-file reference hash audit and executed effective initialization
- Partial parked diagnostic receipt, complete board log and current image
- Two owner-contextualized static images, two complete board records and offline multi-pose fit diagnostics

## 限制

- Only height150 is owner supplied; other projection values remain inherited.
- Full-route tests use fan0; fan30 startup tested separately with stubs.
- No physical full-lap acceptance;08 stops3 in local trials.
- No raw source, firmware, images, logs, chats, databases or credentials uploaded.
- No matched timing-quality baseline; unknown metrics remain null.
- Image scene context is owner-confirmed, but exact metric pose and failure-time frames are absent; grid optima are hypotheses only.

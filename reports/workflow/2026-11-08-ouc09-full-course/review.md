# 2026-11-08-ouc09-full-course 工作流复盘

Refine OUC09 corner tracking against the archived125 baseline, pass the exact school course, and prepare125/30 firmware for physical deployment.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + frozen simulation inputs + full ADS source rebuild
- 验收状态：partial
- 开始：2026-11-08T20:06:53.114201+08:00
- 测量截止：2026-11-08T12:53:50.899233+00:00
- 墙钟秒数：2817.785032
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| measured_wall | 2817.785032 | seconds | Recorded round start to cutoff, including build recovery and physical-preparation wait |
| source_files | 688 | files | Frozen tested/built input manifest |
| changed_from08 | 12 | files | Hashed source comparison |
| full_route_passed | 8 | cases | Final frozen inputs in both plants |
| full_route_total | 8 | cases | Four conditions per plant |
| max_lateral | 50.6957 | mm | Full1ms traces |
| control_checks | 447 | checks | Actual controller regression |
| startup_cases | 15 | cases | 19 extracted hardware-control functions |
| startup_checks | 374963 | checks | Startup regression log |
| full_c_compilations | 174 | units | Final ADS build log |
| final_native_build | 4.517 | seconds | Final ADS timing |
| build_errors | 0 | errors | Final native log |
| new_warnings | 0 | warnings | Normalized comparison with frozen baseline |
| completed_experiment_batches | 20 | batches | Retained batch summaries; not all early runs had immutable binary snapshots |
| flash_actions | 0 | actions | Official receipt or no flasher invocation |
| remote_starts | 0 | actions | No launch commands |
| agents_dispatched | 0 | agents | Single coordinator; no independent reviewer claimed |
| usage | 未知 | tokens | Provider accounting unavailable |
| cost | 未知 | currency | No billing data |
| tool_failures | 未知 | failures | Not counted end to end |
| review_archive_overhead | 未知 | seconds | Archive receipt measures its own interval |

## 验收条件

- OUC primary125/30 control with separated identities
- Full precise-course regression before deployment
- Verified native build and physical readback

## 已完成

- Verified all684 archived stable125 source hashes and the historical HEX identity before adapting its controller to the current47-node course.
- Retained OUC primary steering and element state control; auxiliary photo observes only. Default speed125 and fan30 remain fixed.
- Corrected near-line heading holds, close-junction confirmation and speed continuity, symbol gap fill, and polygon heading/mileage handoff.
- Passed8/8 final full-course cases across two plants with the unchanged55mm quality and60mm out-of-line rules; maximum lateral error50.6957mm.
- Verified447 control checks and15 startup cases with374963 assertions; replayed4 stored real frames with temporal warm-up.
- Built174 C units from source in a clean ADS directory,0 errors and12 inherited warnings, no new warnings; bound tests, frozen simulation inputs and HEX to the same688 hashes.
- Preserved old08, MIN01 and initial09 identities separately; final release identifier is09R2.

## 未完成

- Connect downloader and verify current physical preparation, then flash and read back the frozen09R2 identity and125/30.
- Validate physical line following, resistor/dash traversal and body stability with owner-controlled launches.

## 收益与损耗观察

- Old physical125 success was limited evidence on a different route; copying its trigger/gains alone failed the precise current map.
- A heading hold needed lateral correction from fresh near-line edges; polygon correction also needed an aligned-stem gate to reject neighboring roads.
- An old static fan0 simulation could not validate the requested fan30 trial; this round sets and checks actual fan output30 in both plants.
- Early simulations referenced mutable host binaries; later batches froze their binary and source inputs before launch. Only the final frozen batch supports release.
- Several isolated changes progressed farther but failed the same quality threshold; the threshold was never widened.
- Standalone compiler licensing rejected command-line make; headless IDE mode stalled on workbench creation. The established isolated ADS build succeeded.
- Four new pixel conversion warnings were made explicit; final tests and full builds were repeated on that exact source.
- Failed experiments are retained as evidence outside the release firmware; no old object/assembly/HEX was reused.
- No matched workflow baseline exists; no speedup claim.

## 修改建议及下一轮验收

- **CC-SIM-FROZEN-INPUTS-20261108 [adopted]** Freeze per-batch source and host binaries before parallel route tests and bind their hashes to the native release.；负责人：codex；下次检查：Future release verification rejects mutated source or host binaries.
- **CC-SIM-ACTUAL-FAN-20261108 [adopted]** Assert actual speed and fan outputs in route traces, alongside unchanged course quality limits.；负责人：codex；下次检查：Future125/30 route batches cannot pass with fan0 or output speed above125.
- **CC-ADS-ENTRY-20261108 [adopted]** Use the established isolated ADS build for this non-standalone compiler license and verify full source compilation counts.；负责人：codex；下次检查：Next build avoids repeated unsupported standalone/headless trials.

## 证据

- Historical source and HEX hash audit
- Final controller/startup logs and static-frame replay
- Frozen two-plant eight-case route regression
- Full ADS build and688-input release manifest

## 限制

- Passing fixed-pitch flat-ground simulations does not establish physical stability over obstacles or glare robustness.
- Camera pitch/focal parameters and fan thrust remain inherited model assumptions; only150mm height is owner supplied.
- Archived stable125 success is not a matched physical A/B baseline for the new course.
- No independent Opus review was performed; this is coordinator implementation and self-review.
- Only sanitized aggregate workflow records are uploaded.

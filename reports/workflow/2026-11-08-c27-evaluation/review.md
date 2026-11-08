# 2026-11-08-c27-evaluation 工作流复盘

Evaluate national-team visual reconstruction ideas offline after diagnostic physical failure; reject promotion when route acceptance fails.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; isolated input/target and separate safety/completion gates
- 验收状态：partial
- 开始：2026-11-08T14:23:38.575984+00:00
- 测量截止：2026-11-08T14:40:02.313559+00:00
- 墙钟秒数：983.737575
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| measured_wall | 983.737575 | seconds | Isolated evaluation directory creation to review cutoff; includes context recovery and report preparation; excludes earlier physical capture |
| controller_scenarios | 36 | scenarios | Sanitizer test output |
| controller_assertions | 138 | assertions | Actual PID and wire record tests |
| full_laps_attempted | 8 | runs | Four conditions, two engines |
| full_laps_passed | 0 | runs | All stopped at relock guard |
| normal_segments_passed | 6 | runs | Centered and offset straight/dash/fork |
| fault_safe_stops | 4 | runs | Synthetic fault cases; physical acceptance separate |
| fill_cases | 35 | inputs | Eleven geometry, two stationary real, twenty-two development replay |
| native_compile_units | 174 | units | Clean native build log |
| native_new_warnings | 0 | warnings | Normalized comparison with frozen baseline |
| native_build_attempts | 1 | builds | One clean target build succeeded |
| flash_actions | 0 | actions | Offline evaluation scope |
| serial_commands | 0 | commands | Offline evaluation scope |
| remote_launches | 0 | actions | No vehicle control |
| agents_dispatched | 0 | agents | Single coordinator; existing research handoff only |
| usage | 未知 | tokens | Provider accounting unavailable |
| cost | 未知 | currency | Billing unavailable |
| tool_failure_count | 未知 | failures | Not globally instrumented; known rework described |
| review_archive_overhead | 未知 | seconds | Report creation and archive timing recorded separately; full overhead not instrumented |

## 验收条件

- Isolated immutable baseline
- Real/synthetic provenance separation
- Fixed55mm quality/60mm out gates
- Eight full-lap attempts and no promotion on failure

## 已完成

- Preserved frozen historical sources/artifacts and deployed diagnostic source/HEX; identities kept separate.
- Complete saved physical record exposes ordinary-following deviation conflict while route index stays0; missing raw corner/distance prevents exact first-node cause attribution.
- Implemented independently derived restricted near-gap fill, bounded ordinary-line conflict stop, and versioned full-sequence/yaw diagnostics in isolated offline source.
- Actual-C fill comparison completed on35 inputs across4 modes; static and development sources labeled separately from synchronized moving evidence.
- Six simple segments and four injected safe-stop cases passed;36 controller scenarios/138 assertions and actual record roundtrip passed.
- All8 full laps failed completion with stop28. No quality/out limit relaxation, no promotion, no physical retry request.
- Native174-unit build passed with0 errors and12 inherited warnings;3559bytes static CPU0 headroom. Source/host parity and artifact identity audited.

## 未完成

- The physical vehicle is not fixed or accepted. No synchronized moving camera frames or exact rejected-node evidence available.
- No target cycle or stack high-water measurements for the evaluation. Host timing includes Python/ctypes/copy overhead.
- No qualified firmware candidate: full-lap completion0/8.

## 收益与损耗观察

- Two host build attempts failed due to private fill-header coupling; moved the public mode constant into the adapter interface, then both engines built.
- Initial replay window incorrectly used launch-relative times against absolute replay timestamps and selected0frames. Corrected using the recorded3500ms launch offset and asserted nonempty input.
- Benchmark added actual V|GAP dash mode after inspecting trace flags; retained HV only as a labeled sensitivity group.
- Restricted AUTO filled synthetic small gaps but changed none of the available real/development camera inputs; combining it with prior route fill retained false synthetic opening joins.
- Physical record lacks exact heading: a sensitivity sweep stops early at0/+/-8deg assumptions but does not at+/-12deg. This is a limit, not a claimed physical repair.
- Native clean build and source matching avoided mixing old object files. No independent agent review was claimed.
- No matched quality-passing workflow baseline exists; no efficiency or speedup claim.

## 修改建议及下一轮验收

- **CC-NODE-ADMISSION-EVIDENCE-20261108 [proposed]** Record raw prefilter corner, route-distance window and rejection reason before another first-node tuning cycle.；负责人：codex；下次检查：One synchronized segment distinguishes classifier miss from admission rejection.
- **CC-EVAL-INPUT-CLOCK-20261108 [adopted]** Use explicit replay clock origin and nonempty selection assertion; label synthetic, static real and development replay separately.；负责人：codex；下次检查：Future replay exports include launch origin and exact selected frame IDs.
- **CC-NATIVE-RECORD-LAYOUT-20261108 [adopted]** Retain clean native compilation, source parity and bounded wire-schema checks for added diagnostic fields.；负责人：codex；下次检查：Target map and actual formatter roundtrip remain required.

## 证据

- Sanitized source-freeze/native-build summary
- Actual-C host comparison aggregates
- Segment and full-lap result aggregates
- Wire schema roundtrip and bounded physical-record sensitivity

## 限制

- Raw code, logs, camera frames, sessions and databases stay local.
- Simulation safety stop is not completed-lap quality or physical acceptance.
- Only one of repeated physical starts has a complete saved detailed record.

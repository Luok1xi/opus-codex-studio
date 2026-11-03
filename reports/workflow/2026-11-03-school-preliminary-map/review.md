# 2026-11-03-school-preliminary-map 工作流复盘

Add a provisional school course with dashed track and a hexagonal roundabout to the existing preliminary-map simulation and local tuning bench.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：partial
- 开始：None
- 测量截止：2026-11-03T15:15:44.160402+08:00
- 墙钟秒数：None
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| observed_work_interval | 1112.535 | seconds | First recorded local clock14:57:11.626 to verification cutoff15:15:44.160; excludes pre-clock work and final archive. |
| frontend_tests_passed | 26 | tests | Final Node test suite. |
| backend_tests_passed | 31 | tests | Worker final Django suites,1.174s. |
| browser_check_groups | 8 | groups | Final browser-evidence.json; no page errors. |
| actual_c_runs | 4 | runs | One initial map baseline, one final-cap baseline, two UI request checks using realC. |
| native_workers | 2 | workers | Exclusive backend and frontend file ownership; root geometry/integration. |
| actual_opus_calls | 0 | calls | TeamHub handoff only; no reply claimed. |
| hardware_actions | 0 | actions | No serial, flash or motion calls. |
| tokens | 未知 | tokens | No provider usage meter. |
| cost | 未知 | currency | No billing evidence. |
| review_archive_overhead | 未知 | seconds | Archive not finished at measurement cutoff. |

## 验收条件

- Keep original preliminary map unchanged.
- Use identical new geometry in C camera, legal-course checks and web visualization.
- Permit school selection, simulation and replay without misidentifying it as preliminary.
- Record actual results and provisional placement without claiming a finished lap.

## 已完成

- Registered a fixed school scenario with map digest, route validation and per-run map snapshot.
- Preserved original elements; added six 30mm dash marks separated by 20mm gaps and a160mm-side hexagon, with32 route entries.
- 57 focused unit tests passed; production build passed.
- Eight rendered-browser check groups passed at1440px and390px; camera pixels match exported C frames.
- Rendered review found and fixed missed primary-button text, route action labels and flat-end rendering.
- Real125-speed C baseline stopped with STOP3 after3.31s and3.43m; it is explicitly not a lap time.
- Existing website and Hub ports reused; no firmware/serial/vehicle operation.

## 未完成

- Owner has not confirmed provisional element positions and dimensions.
- Complete-lap and hexagon traversal performance remains unproven; dashed-section vision needs follow-up tuning.

## 收益与损耗观察

- Backend/frontend work ran independently; root verified scene and browser boundary.
- Map geometry check confirmed all nonstraight route actions,8 sixty-degree entries, legal route continuity and camera-invisible dash gaps.
- Actual camera probes distinguish school dashes/hexagon from original straight segments; dash pose invalid while original straight pose valid.
- Browser controlled-submit check used an authorization fixture with realC computation; anonymous live backend protection verified separately. No live owner login or credentials copied.
- Discovery had oversized/truncated output and Git permission failures; read scope and execution permissions were then narrowed.
- No plotting package was installed: after two missing-library probes, an existing browser rendered SVG geometry.
- Rework included map segment-count assertion, flat boundary caps, browser label selector, missing primary-button label, route label formatting and a normalized-path guard before second Hub reload.
- No public deployment or unrelated-source commit.

## 修改建议及下一轮验收

- **school-rendered-boundary [adopted]** Keep the final screenshot review after catalog and backend integration; test the primary visible action and readable route labels in addition to API success.；负责人：codex；下次检查：Retain these assertions for future map variants.
- **school-bounded-discovery [proposed]** Read project categories before choosing one, bound data extraction, and use the installed browser for geometry preview instead of probing plotting packages.；负责人：codex；下次检查：Measure comparable future map tasks before claiming less time or fewer retries.

## 证据

- school-backend-geometry-check.json
- school-route-label-check.json
- engine-evidence.json
- browser-evidence.json
- school-backend-worker-evidence.json
- school-bench-ui worker-report.json
- map_sha256=e1422a2dd25b91e4a1f2318905faf8f7b211e6d093402dc36cb571855c06e112

## 限制

- Positions are a visible provisional layout, not surveyed school-track dimensions.
- No complete-lap success or real-car validation.
- No matched quality baseline; workflow speedup unproven.


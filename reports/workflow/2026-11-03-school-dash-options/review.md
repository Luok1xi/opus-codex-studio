# 2026-11-03-school-dash-options 工作流复盘

Display three candidate dashed-track positions, integrate separate original/line-fill configurations, and begin controlled school-course simulation tuning.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：passed
- 开始：None
- 测量截止：2026-11-03T17:17:54.401446+08:00
- 墙钟秒数：None
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| observed_work_interval | 1006.947 | seconds | First recorded clock through verification cutoff; excludes pre-clock work and later archive. |
| actual_c_runs | 14 | runs | 3 original baselines +8 isolated strategy/parameter trials +3 final API exports. |
| native_workers | 3 | workers | Separate backend/frontend/offline experiment ownership. |
| actual_opus_calls | 0 | calls | Project handoff only; no acceptance claimed. |
| final_backend_tests | 18 | tests | Worker unittest evidence. |
| final_frontend_tests | 5 | tests | Focused identity/parameter suite after fill IDs. |
| browser_groups | 10 | groups | Two suites of5; includes checks repeated for distinct strategy set. |
| tokens | 未知 | tokens | Provider usage unavailable. |
| cost | 未知 | currency | Billing unavailable. |
| coordination_wait | 未知 | seconds | Not separately timed. |
| review_archive_overhead | 未知 | seconds | Later receipt records post-cutoff archive time; initial preparation not isolated. |

## 验收条件

- Preserve confirmed hexagon and original maps.
- Show three candidate positions and keep strategies separately selectable.
- Run actual controller experiments and retain unsuccessful results.
- Verify rendered website, camera and selected-map requests.

## 已完成

- Three candidate maps and six replay configurations delivered to existing local site.
- All original configurations stop near dashes; existing image line-fill lets all three pass dashes and upper capacitor gap.
- All final candidates fail at hexagon entrance; two parameter changes rejected as ineffective.
- Fixed allowlist, independent route fingerprints,18 backend tests and5 final frontend tests passed;27 frontend tests had passed before adding fill IDs.
- Both sets of browser checks passed at1440/390px; camera pixels match exported C frames.

## 未完成

- 无记录

## 收益与损耗观察

- Worker reused all3 root baselines; final3 reruns were deliberate canonical API replay exports.
- Review caught extra line-fill flags in proposed baseline before any C baseline ran; separated original and treatment strategies.
- Browser script first targeted hidden index buttons; corrected to the user-visible configuration library.
- Request-payload fixture used authentic saved C outputs; it did not claim an owner-authenticated live submission.
- No controller source, firmware, out-of-line threshold, serial or vehicle operation changed.

## 修改建议及下一轮验收

- **LUOKIXI-WEB-school-strategy-isolation [adopted]** Keep route/image-processing changes in separate map IDs and condition fingerprints; do not describe them as same-condition PID gains.；负责人：codex；下次检查：Retain for the next hexagon-entry experiment.
- **LUOKIXI-WEB-school-test-frontier [adopted]** Stop parameter sweeps when distinct settings fail at the same structural handoff; retain traces and target the handoff in the next controlled experiment.；负责人：codex；下次检查：Test ordinary-straight to60-degree handoff without removing route entries or relaxing bounds.

## 证据

- backend-worker.json
- frontend-worker.json
- experiment/worker-evidence.json
- experiment/camera-comparison.json
- experiment/hex-entry-handoff.json
- browser-evidence.json
- browser-fill-evidence.json
- baseline-summaries.json
- fill-summaries.json

## 限制

- User has confirmed ring position, but exact dash position is still optional input pending.
- Outer-circle validation only, not full-element competition route or real-car validation.
- No completed loop;6.85s is a failure termination time.
- No matched workflow baseline; net speedup unproven.

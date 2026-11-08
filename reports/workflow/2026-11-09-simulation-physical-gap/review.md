# 2026-11-09-simulation-physical-gap 工作流复盘

Explain why saved website laps and earlier physical success do not establish acceptance of the current control revision.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; evidence identity comparison
- 验收状态：passed
- 开始：2026-11-08T17:09:44+00:00
- 测量截止：2026-11-08T17:12:42.351529+00:00
- 墙钟秒数：178.351529
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| observed_review_interval | 178.351529 | seconds | Known clock sample after initial read to cutoff; initial read excluded |
| firmware_edits | 0 | actions | Read-only evidence comparison |
| website_edits | 0 | actions | Read-only evidence comparison |
| hardware_actions | 0 | actions | Read-only evidence comparison |
| new_simulations | 0 | actions | Read-only evidence comparison |
| external_model_calls | 0 | actions | Read-only evidence comparison |
| full_round_wall | 未知 | seconds | Not instrumented for full interval; archive receipt separately measures upload |
| usage | 未知 | tokens | Not instrumented for full interval; archive receipt separately measures upload |
| cost | 未知 | currency | Not instrumented for full interval; archive receipt separately measures upload |
| review_archive_overhead | 未知 | seconds | Not instrumented for full interval; archive receipt separately measures upload |

## 验收条件

- Check replay configuration and control identity
- Separate historical success from current regression
- Do not change hardware or firmware

## 已完成

- Inspected two saved website replay payloads and their exact controller branch.
- Compared historical successful physical control with later deployed-source behavior.
- Recounted existing camera mismatch acceptance evidence; separated observation from root-cause hypotheses.

## 未完成

- 无记录

## 收益与损耗观察

- Saved replays and current implementation use different geometry, controllers and operating conditions.
- A successful historical physical state sequence was not preserved in the failing later revision.
- Known sensor-model mismatch tests already expose failure outside the displayed nominal case.
- One guessed simulation source path was absent; switched to manifest-backed controller paths without further guessing.

## 修改建议及下一轮验收

- **CC-COMPARE-IDENTITY-20261109 [proposed]** Bind every displayed result to controller, map, camera and operating settings; preserve proven state handoffs when changing maps.；负责人：codex；下次检查：Future comparisons must show identical inputs or explicitly list differences; source facts precede proposed repair.

## 证据

- Saved replay metadata and exact controller branches
- Historical successful-run audit and later source settings
- Recorded camera sensitivity matrix

## 限制

- No new simulation or physical result.
- No live website deployment or vehicle identity check.
- Original repair remains unfinished.
- No matched workflow baseline or speedup claim.
- No source, raw logs, images, sessions or databases uploaded.

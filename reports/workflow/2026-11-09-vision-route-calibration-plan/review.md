# 2026-11-09-vision-route-calibration-plan 工作流复盘

Explain visual and route calibration after wheel/yaw tuning and how to diagnose early turning.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-11-09T17:13:55+08:00
- 测量截止：2026-11-09T09:15:54.255512+00:00
- 墙钟秒数：119.255512
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| round_wall | 119.255512 | seconds | First read to local cutoff; exact active and review timing unavailable |
| vehicle_actions | 0 | actions | Read-only design clarification; no serial access |
| code_changes | 0 | changes | No implementation requested in this phase |
| external_model_calls | 0 | calls | No dispatch |
| usage | 未知 | tokens | Unavailable |
| review_overhead | 未知 | seconds | Not separately measured |

## 验收条件

- Separate visual and actuator loops
- Preserve coordinate, controller and safety constraints
- Provide a staged diagnosis for early turns

## 已完成

- Read current saved OUC sampling and turn-state code alongside project vision/route references.
- Separated actuator inner-loop tuning, image geometry, visual steering and route execution acceptance.
- Defined staged validation that preserves quality limits and does not confuse detecting a corner with turning.

## 未完成

- 无记录

## 收益与损耗观察

- The visual outer loop depends on image geometry and cannot be treated as fully tuned before visual calibration.
- Both preview contamination and premature state-machine triggers can appear as early turning.
- Finite-radius turning requires a measured lead distance, so forcing turn onset exactly at a map vertex is not a valid universal fix.

## 修改建议及下一轮验收

- **VISION-ROUTE-STATE-POSITION [proposed]** Record physical reference, frame evidence, controller state, target yaw and observed yaw together for single-corner acceptance before full laps.；负责人：codex；下次检查：On the next authorized segment, identify which transition deviates before changing thresholds.

## 证据

- Saved OUC weighted-row implementation
- Saved route admission, direct trigger and fallback source
- Previously confirmed outgoing-lane recovery failure
- Existing image geometry and route strategy references

## 限制

- No physical validation or new tuning values.
- No current-car firmware or fresh run claim.
- No matched workflow baseline or speedup claim.
- No raw code, private messages, telemetry, images or databases in archive.

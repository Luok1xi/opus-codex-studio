# 2026-11-08-noseover-light-diagnosis 工作流复盘

Explain repeated first-resistor nose-over after lighting changes and distinguish real visual control, simulation limitations and post-tip evidence.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + source-path verification + temporal causal separation
- 验收状态：partial
- 开始：2026-11-08T09:59:04.409567+00:00
- 测量截止：2026-11-08T10:08:44.714296+00:00
- 墙钟秒数：580.304729
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| measured_wall | 580.304729 | seconds | Initial telemetry snapshot to cutoff; includes user clarification waits |
| board_samples | 109 | samples | LOG109 with complete sequential records and END |
| read_only_device_queries | 3 | queries | P/S/I parked queries with receipt |
| flash_actions | 0 | actions | No flasher invoked |
| remote_starts | 0 | actions | Only read-only commands |
| firmware_changes | 0 | files | Source inspection only |
| agents_dispatched | 0 | agents | Single coordinator |
| tool_failures | 未知 | failures | Not instrumented end-to-end |
| usage | 未知 | tokens | Provider accounting absent |
| cost | 未知 | currency | No billing available |
| review_archive_overhead | 未知 | seconds | Archive duration will be recorded separately |

## 验收条件

- Explain source and simulation behavior accurately
- Identify observed failure sequence without claiming an unmeasured cause

## 已完成

- Confirmed actual forward nose-over and separated post-tip/stuck motor data from normal grounded tuning.
- Read firmware identity and preserved109 complete20ms board samples plus complete current camera frame.
- Found a zero-output interval followed by resumed low target and negative wheel outputs; correlated source gate/reset/restart behavior.
- Verified the simulation uses image-based control but its virtual camera ignores chassis pitch/roll; floor is a plane and tested routes used fan0.
- Verified two frozen historical control/vision files and contrasted their local visual control with current125 map navigation.
- Retained causal uncertainty and advised no further repeated starts before the protection and failure evidence gaps are addressed.

## 未完成

- Establish the order of forward tip, visual loss and control transitions with synchronized body attitude and visual evidence.
- Implement and verify a justified isolated protection/control correction before another physical trial.

## 收益与损耗观察

- User clarification changed the failure class from possible line loss to actual forward tip.
- Initial generic visual-stop explanation was insufficient; latest board log contains a materially different opposed-saturation regime after a reported tip/stuck event.
- Source proves non-latched permission can resume during the same launch; a captured resume commands reverse PWM at both wheels, consistent with braking but without a measured torque. Exact onset of body tip is missing.
- Simulation has real image processing but a fixed-pitch virtual camera, which excludes the camera consequences of chassis pitch.
- No matched workflow baseline or performance claim.

## 修改建议及下一轮验收

- **CC-NOSEOVER-TEMPORAL-EVIDENCE-20261108 [proposed]** Record body attitude and the first control-permission loss, and distinguish pre-tip behavior from post-tip saturation before tuning gains.；负责人：codex；下次检查：A repeated failure has a synchronized attitude/control/image timeline before further physical testing.

## 证据

- Owner failure clarification
- Read-only identity and109-sample board record
- Current camera frame and offline fit diagnostic
- Frozen historical source hashes and current gate/reset/control code
- Simulator camera, collision-plane and invocation source

## 限制

- Root cause of the initial nose-over remains unproved.
- Lighting comparison is not matched by pose/time.
- Electrical coast/brake behavior at PWM0 is not inferred.
- Only aggregate workflow reports uploaded; no images, raw logs, source, databases or credentials.

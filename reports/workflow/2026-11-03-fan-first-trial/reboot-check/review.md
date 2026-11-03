# 2026-11-03-fan-first-trial 工作流复盘

Distinguish a zero fan target after reboot from the unresolved earlier audible startup failure.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW-2026-10-18
- 验收状态：partial
- 开始：2026-11-03T12:28:48+00:00
- 测量截止：2026-11-03T12:32:21.612467+00:00
- 墙钟秒数：213.612467
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| serial_query_commands | 5 | commands | Local capture summary; only #F queries. |
| actuator_commands | 0 | commands | No target-setting or launch commands. |
| received_bytes | 0 | bytes | Ten-second query-only capture. |
| native_review_workers | 1 | workers | Received independent source review. |
| tokens | 未知 | tokens | Unavailable. |
| cost | 未知 | currency | Unavailable. |
| review_overhead | 未知 | seconds | Not separately measured. |
| coordination_wait | 未知 | seconds | Not separately measured. |

## 验收条件

- Verify target initialization and S5 semantics against the flashed snapshot.
- Separate expected software behavior from current device state.
- Do not increase throttle or remotely start the vehicle.

## 已完成

- Flashed snapshot initializes the target to zero and does not persist the earlier throttle; S5 changes launch state without setting a target.
- Owner reported an impeller that can be turned unpowered and no fan response after reboot and S5.
- A bounded query-only serial attempt completed with zero bytes and closed its port.

## 未完成

- Current target, output and launch state were not received.
- The earlier audible startup failure remains unresolved.

## 收益与损耗观察

- Do not conflate a launch-enable button with a nonzero fan target.
- A source-level zero default is not a measurement of current target or proof of healthy hardware.
- Impeller hand rotation excludes only an obvious stationary jam, not every loaded mechanical or electrical fault.
- Initial system port enumeration failed under restricted access; an authorized retry exposed one port. It opened but yielded no reply.

## 修改建议及下一轮验收

- **show-reset-target-separately [adopted]** During future fan diagnostics explicitly distinguish configured target, run gate, requested output and observed rotation.；负责人：codex；下次检查：Use a successful status reply or stopped signal capture before diagnosing post-reset silence.

## 证据

- Flashed snapshot control.c:24,142; cpu0_main.c:122,132; vision_link.c:194,218; wireless.c:102.
- Bounded query capture aggregate: five queries, zero received bytes, serial closed.
- Independent source review received; no Opus response claimed.

## 限制

- No current telemetry reply or measured PWM.
- Prior startup fault not repaired.
- No matched workflow baseline; no efficiency gain claimed.

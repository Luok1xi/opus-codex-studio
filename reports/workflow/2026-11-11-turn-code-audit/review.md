# 2026-11-11-turn-code-audit 工作流复盘

Codex直接对照旧稳定源码审计转弯异常；按Owner后续要求准备保持250行驶基速的离线候选。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + source-bound deterministic tests
- 验收状态：passed
- 开始：2026-11-11T09:16:40+00:00
- 测量截止：2026-11-11T09:32:20.402264+00:00
- 墙钟秒数：940.402264
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native contributors | 2 | agents | Bounded source provenance and independent C review; no recursive agents. |
| External model dispatch | 0 | calls | No DSH or Opus dispatch. |
| Hardware or runtime changes | 0 | operations | Offline artifacts only. |
| Model usage | 未知 | tokens | No reliable scoped usage supplied. |
| Cost | 未知 | currency | No billing data. |
| Coordination and archive overhead | 未知 | seconds | Not separately measured; coordination in total wall time, final archive after cutoff. |

## 验收条件

- 找到与指定旧HEX对应的真实工程并核来源。
- 区分旧缺口、新模式冲突和实车未证实因果。
- 保持250候选通过离线与目标编译，原冻结版不被覆盖。

## 已完成

- 三份旧HEX相同，683文件来源快照匹配。
- 真实C当前221、旧5断言通过；发现原route0重触发和固定图像增益交接冲突。
- 独立恒速候选854断言通过，官方ADS零错误；未使用串口或烧录。
- 未向DSH再次交接；原生只读辅助用于证据定位与复核，Codex承担结论与实现。

## 未完成

- 无记录

## 收益与损耗观察

- Owner narrowed responsibility to Codex; no new DSH handoff was sent.
- Original test harness constants differed from hardware constants; new reproducer extracted actual macros and did not reuse that mismatch.
- Exact baseline artifact discovery prevented calling an inherited defect a new regression.
- Initial ADS run could not write its Eclipse configuration; authorized compiler-only retry succeeded.
- Early listing of not-yet-created helper output and an invalid task-help verb added avoidable tool errors.
- Owner requested constant250 during audit; isolated candidate changed the drive target without also changing legacy steering gain scheduling.

## 修改建议及下一轮验收

- **TURN-REAL-CONSTANTS [adopted]** 针对切换边界测试使用实际宏与函数，并绑定编译输入哈希。；负责人：codex；下次检查：后续修复验证必须覆盖route0旧角释放与正负指令交接。
- **TURN-GAIN-SEPARATION [adopted]** 速度策略变更与方向增益变更分开；恒速候选不得冒称交接缺陷已修好。；负责人：codex；下次检查：未来实车验收分别保留速度设定、角速目标、轮差速与元素状态。

## 证据

- evidence.json

## 限制

- 没有同质量时间基线，不能宣称协作加速。
- 离线状态复现不是完整仿真或实车验证。
- 没有同步翻转时刻与角点原图，不判定唯一翻车原因。
- 恒250指行驶基速，左右轮仍差速；转弯交接修复及实车试跑尚未实施。

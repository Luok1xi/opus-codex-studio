# 2026-11-13-old125-250-fan-stable 工作流复盘

沿用旧125视觉顺序路线实现250速度上限的负压候选，提高合理弯速，定位连续路口漏判，完成离线稳定验收与目标冻结。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：Project database, scoped native agents, frozen shared-source evidence
- 验收状态：passed
- 开始：2026-11-13T03:47:43.395Z
- 测量截止：2026-11-13T04:45:24.003175+00:00
- 墙钟秒数：3460.608175
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| native_child_contributors | 3 | agents | Three native assistants returned scoped evidence. |
| external_opus_or_dsh_calls | 0 | calls | No external studio worker was invoked; handoff does not imply acceptance. |
| matrix_wall_seconds | 173.20542274699983 | seconds | Final runner interval, not sum of parallel trials. |
| host_build_seconds | 13.209329743000126 | seconds | Final host build receipt. |
| target_build_seconds | 8.078000000008615 | seconds | Final successful official ADS invocation only. |
| final_passes | 24 | of24 | Both plants, four conditions, three repeats, event identity audit. |
| known_test_drift_rework | 1 | events | Shared configuration changed during one test run; discarded and rerun. |
| known_missing_metadata_build_failure | 1 | events | Missing ADS settings prevented compilation; restored original project metadata. |
| hardware_operations | 0 | operations | No serial, flashing or actuator operation. |
| total_tokens | 未知 | tokens | No complete trustworthy provider usage receipt. |
| total_cost | 未知 | currency | No billing receipt. |
| coordination_wait | 未知 | seconds | Not independently timed. |
| review_overhead | 未知 | seconds | Review interleaved with implementation. |
| total_rework_count | 未知 | events | Known examples recorded; exhaustive total unavailable. |
| exclusive_archive_overhead | 未知 | seconds | Archive segment separately timed; not isolated exclusive effort. |

## 验收条件

- 旧视觉、2ms速度环、视觉触发顺序选路，无全局节点门槛。
- 双模型四工况三重复全圈、完整路线事件，沿用60mm开发门槛。
- 同源TC264目标编译和冻结，不串口、不烧录。

## 已完成

- 复现旧125八工况基线；最终24/24与路线物理身份核验通过。
- 修复直行锚点覆盖、转后释放、前路延续漏判和普通保持超时；真实源码反例回归通过。
- 尝试并保存多个较高弯速与较缓减速失败，最终保留80/70；负压敏感性完成。
- 官方ADS0错误13原警告；36共享输入一致、RAM/栈静态审查、可重建源和HEX已冻结。

## 未完成

- 无记录

## 收益与损耗观察

- 先读取已登记任务、历史经验和实际源码，复现旧基线后开始增量。引用实际采用的经验包359bd0b7：CC-F143、R124、GEOMETRY-ACCEPTANCE、R109。
- 三个成员分别做来源与目标审计、图像故障定位、提速和物理敏感性；没有冒充真实Opus或DSH验收。
- 一次A基线重复运行和一次测试期间配置漂移造成可避免返工；原始失败保留。
- 最终独立审查在V1验收后发现200ms保持遗漏，形成V2并重跑24项；这是发现真实边界后的必要复验。
- 将单工况成功扩展为八工况揭示95和85档不稳，拒绝只挑成功轨迹。
- 部分工具输出过大及参数调用错误带来开销；仅记录已知事件，不伪造全量计数。
- 没有匹配的同质量工作流耗时基线，不能将圈时提升或多人并行解释为开发效率提升。

## 修改建议及下一轮验收

- **STABLE250-REVIEW-BEFORE-FREEZE [adopted]** 冻结完整矩阵前先审计保持/失效边界，源冻结期间测试者与写配置者互斥。；负责人：codex；下次检查：下一轮确认无因并行写入造成的验收漂移，并在完整矩阵前运行空帧与超时反例。
- **STABLE250-PHOTO-TOPOLOGY [adopted]** 遇到漏路口先逐帧核对爬线和原语，再改单个判断；每项保留不应识别的反例。；负责人：codex；下次检查：新地图故障需原图复现与完整事件身份核验，不能仅调速度让失败位置消失。

## 证据

- evidence.json contains sanitized aggregates and fingerprints only.
- Project task144; complete source and evidence remain local.

## 限制

- Recorded start covers this development round; prior days are not included.
- Cutoff includes interleaved review; later remote upload/verification is reported separately.
- Unknown usage/cost/wait stay null; no claimed workflow speedup.
- Physical readiness is not established by simulation or linking.
- 实物相机/负压/编码器标定、HIL、实车完赛与2ms最坏耗时不属本轮离线完成范围。
- 严格行驶50mm仅6/24达到；急转目标跳变未完全消除，不能声称完美或恒250。

# 2026-11-12-ouc-alignment 工作流复盘

按海大main实际源码逐段核对视觉移植，列已接、替代、未实现和未消费；Owner明确要求仅审计，不改变现有转弯。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + upstream call-chain matrix + bounded real-C probes + frozen-source verification
- 验收状态：passed
- 开始：2026-11-12T01:46:41+00:00
- 测量截止：2026-11-12T02:01:19.350416+00:00
- 墙钟秒数：878.350416
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native contributors | 3 | agents | Call-chain/state audit, image primitive audit, CPU bridge audit; root consolidated. |
| User scope clarifications | 2 | messages | Owner emphasized preserving turning behavior and a source-alignment checklist. No candidate had been modified. |
| Firmware edits | 0 | files | Final 626-input hashes and frozen HEX unchanged. |
| Target builds | 0 | builds | No firmware change; prior build is provenance, not claimed as this-round compilation. |
| Hardware operations | 0 | operations | No serial, parameter writes, flashing or launch. |
| External model dispatch | 0 | calls | Native helper agents only. |
| Tokens | 未知 | tokens | No scoped provider usage available. |
| Cost | 未知 | currency | No billing evidence. |
| Review/archive overhead | 未知 | seconds | Review is the requested work and overlaps coordination; remote verification follows cutoff. |

## 验收条件

- 绑定海大main来源和冻结07，按实际调用而非函数名对齐。
- 列清缺失功能、刻意替代和原版自身行为，定位源码与证据。
- 按用户收窄不改固件，核对全部冻结输入及HEX未变。

## 已完成

- 22阶段对齐矩阵、8项原状态子功能与复位/有效性清单。
- 确认角态共同预瞄、fork预瞄/选边、十字重建未移植；补线函数已接但mode0关闭。
- 复现状态显示旧偏差、诊断不同帧和停车抓图超时风险；未误称其导致转弯。
- 核对15个图像/11个爬线共同函数体，38次灰度及86帧分支公式对比，11项桥函数检查。
- 626个冻结输入和HEX未变，无串口、烧录或新候选。

## 未完成

- 无记录

## 收益与损耗观察

- Owner required source alignment rather than another control experiment; the frozen candidate stayed unchanged throughout.
- A function existing without a current caller was not sufficient proof of a bug: one upstream function was also unused, and legacy angle output was intentionally replaced by pixel output.
- The upstream angle-state selection was distinct from a fixed-heading takeover, but depended on state/route/IMU lifecycle; isolated branch arithmetic cannot establish actual upstream turning timing.
- Two minimal grayscale issues reproduced with the original maze replacement; they were classified as inherited limitations, not port regressions.
- Bounded probes supported specific claims, but the functional matrix was the main deliverable; optional experiments should not lead the next audit.
- WSL access required authorized test escalation; no hardware or firmware authority was inferred from it.

## 修改建议及下一轮验收

- **UPSTREAM-CALLCHAIN-FIRST [adopted]** 移植审计先交原入口→原调用→本车调用→缺失功能矩阵；逐一标刻意替代，不先围绕新算法扩展实验。；负责人：codex；下次检查：后续补齐工作必须引用矩阵行并更新函数调用和依赖验收。
- **VISUAL-STATE-NOT-HEADING-TAKEOVER [adopted]** 区分图像目标选择状态、路线决策和目标航向接管；恢复一个函数前列明所有状态输入与退出条件。；负责人：codex；下次检查：若获准恢复angle选点，单独验证状态生命周期、单位及单边丢失。
- **DIAGNOSTIC-FIELD-CONTRACT [proposed]** 后续修正状态输出时分别表达最新图像有效性和控制保持值；统一同帧诊断字段，不把旧显示当控制失效。；负责人：codex；下次检查：未来经Owner确认后修改，复现有效→失效→超时全过程；本轮没有实施。

## 证据

- evidence.json

## 限制

- 静态审计与小型host测试；没有整套海大状态机、实车或全圈验收。
- 审计发现已登记但按Owner要求未修改；不能报告为已修复。
- 本地main来源已核对，不宣称远端最新；无匹配效率基线，不宣称提速。

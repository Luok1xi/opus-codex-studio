# 2026-11-11-rectangle-outerloop 工作流复盘

按Owner收窄后的范围，完成正式固件的图像外环调参入口、编译复核、授权烧录和DSH交接；后续Owner与DSH实测，Codex分析问题。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + project TeamHub + independent native review
- 验收状态：passed
- 开始：2026-11-11T08:09:20+00:00
- 测量截止：2026-11-11T08:36:41.037103+00:00
- 墙钟秒数：1641.037103
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native child workers | 3 | agents | Source/archive recovery, implementation, independent review; no recursive delegation. |
| External model consultations | 0 | calls | No Opus or DeepSeek CLI invocation this round; DSH received a database handoff only. |
| Selected actual C checks passed | 4808 | assertions | Component harness with host stubs; not 4808 independent hardware scenarios. |
| Target build elapsed | 8.89 | seconds | Final successful build receipt; excludes earlier permission failure. |
| Target warnings | 13 | warnings | Exact match to baseline warning lines. |
| Authorized flash operations | 1 | operations | Established burn entry and complete verification receipt. |
| Remote start commands | 0 | commands | Only parked parameter queries were sent; user will conduct later trials. |
| Measured model tokens | 未知 | tokens | No comparable provider usage available. |
| Measured model cost | 未知 | currency | No billing evidence available. |
| Coordination and review overhead | 未知 | seconds | Not separately instrumented; included in wall time. |
| Tool and administrative rework total | 未知 | events | Observed failures described below; no complete normalized event count. |

## 验收条件

- 保留正式程序，隔离图像纠偏与自动直角触发以支持调参。
- 实际源码组件检查、目标编译和独立复核通过。
- 获得实际烧录准备确认后写入冻结HEX，完整校验并只读核对实机。
- 交接完整配置与边界，不自行继续试跑或改其他环。

## 已完成

- 仅5个源文件改动，冻结626个构建输入、HEX/ELF及回退HEX。
- 4808项组件断言通过；目标0错误，13条既存警告；复核无阻断项。
- 烧录与校验通过，实机身份及默认参数回读一致，停车输出为零。
- 完整操作说明已入项目库H774，任务133完成；命令须逐条回读，矩形必须退出校赛路线。

## 未完成

- 无记录

## 收益与损耗观察

- 发现历史存档、同名候选、真实烧录版本及当前RAM设置并不等价，按构建清单和现场读回建立版本边界。
- Owner中途把目标收窄为写入口并烧录，后续调车交DSH；执行范围随之收窄。
- 三名原生子代理分别恢复证据、实施和复核；复核与实现不共享写入范围。未声称获得Opus/DSH的实时审稿回复。
- 默认权限下串口/系统枚举及ADS配置访问失败后，使用已有授权执行明确范围的硬件和构建操作；一次task-update命令拼写错误改用实际CLI update-task。
- 实现后补齐最终初始化覆盖链的已定内环参数，并将主机测试移到目标源码目录之外；原测试.txt本身并未被证明会参与ADS编译。
- 两次停车读回设置不同，来源未确定；交接分别记录烧录前临时值和烧录后默认值，不归因于某个代理。
- 动态提前转弯是否改善仍待后续实车波形；本轮通过的是调参工具交付，不是完赛验收。
- 交付后Owner纠正为只有大直角提前、小角正常：撤销此前小角隔离试验建议，核对J1/O0仍走原自动直角/分档PD路径并更新H775。没有改源码、串口设置、烧录或追加实跑。固定图像PD不覆盖航向/直角PD，不能误称一项参数控制全程。

## 修改建议及下一轮验收

- **RECT04-READBACK [adopted]** 维持源码、冻结HEX、烧录凭据、现场参数四者独立核对；本轮交付清单和DSH说明已实施。；负责人：codex；下次检查：下次实跑导出必须关联同趟参数回读和版本，检查是否仍有混用。
- **RECT04-SEQUENTIAL [adopted]** 调参协议逐条发命令并等完整回显；禁止整段批量粘贴，以免队列繁忙时命令未生效。；负责人：codex；下次检查：由DSH下一次设置时逐条核对，未收到其执行回执前不声称收益验证。
- **RECT04-SCOPE-CORRECTION [adopted]** 最新现场描述覆盖旧诊断分支，交接首屏标记被撤销的测试，保留历史以免另一代理继续旧流程。；负责人：codex；下次检查：DSH按H775仅复核大直角；尚未收到执行回执。

## 证据

- evidence.json
- 本地发布、组件测试、独立复核、烧录与实机只读凭据的摘要和哈希见evidence.json；原始项目数据未上传。

## 限制

- 没有同输入同验收的时间基线，不能声称并行或新流程提速。
- 后续矩形试跑、无线新命令实车交付和动态性能未验收；不保证已经消除提前转弯。
- 实际token、费用和单独复核/协调开销未知；截止之后归档时间不计入当前墙钟。
- DSH交接已入库，不代表对方已读取或接受。
- 上述同目标补充不另开复盘轮；原测量截止及墙钟保留为固件交付阶段，补充说明和归档独立开销未计量。

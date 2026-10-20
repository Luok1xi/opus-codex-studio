# 2026-10-20-live-log-power 工作流复盘

实际接收车辆日志，对比关电源、原电池上电闪灯、换电池后三种状态；确认当前运行恢复。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：Per-project TeamHub, one live serial reader at a time, one native offline review.
- 验收状态：partial
- 开始：2026-10-20T09:52:08.573Z
- 测量截止：2026-10-20T10:09:38.166Z
- 墙钟秒数：1049.593
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| 观察区间 | 1049.593 | seconds | 开始至完成OFF/ON诊断及交接，包含Owner中途改变供电状态。 |
| 被动串口采集 | 3 | sessions | 每次12秒，结束即关闭；有实际开始结束记录。 |
| 完整状态行 | 36 | rows | 三段各12完整行，分别保存OFF、原电池ON、换电池；未完整尾行排除。 |
| 串口写入 | 0 | bytes | 采集脚本无write调用。 |
| 烧录及主动复位 | 0 | operations | 本轮未执行。 |
| 生产文件修改 | 0 | files | 仅本地采集和审核材料。 |
| 原生独立审核者 | 1 | workers | 复用同一审核者，先读旧日志，后追加新状态与ADC复核。 |
| 新增外部模型调用 | 0 | calls | 使用已有Opus共享数据库交接。 |
| 已记录工具失败 | 1 | calls | 普通进程查询权限拒绝，获授权只读查询后成功。 |
| 模型用量 | 未知 | tokens | 无一致提供方usage。 |
| 费用 | 未知 | currency | 无账单。 |
| 协调等待和重复工作 | 未知 | seconds | 未分离计算；反复更新结论由供电状态变化触发。 |
| 归档开销 | 未知 | seconds | 完成后记入归档回执。 |

## 验收条件

- 实际读取日志而非猜测；不发送车辆控制指令。
- 把供电状态、缓存帧与真正新帧分开解释。
- 将未确定根因与下一步区分测量交给现场操作者。

## 已完成

- 读取实际同伴日志并确认抓图成功可能只是重复缓存。
- 两次各12秒被动接收；OFF和ON闪灯状态各12条完整记录，均没有时间回退，摄像头没有新帧。
- 结合Owner确认的开关状态，区分电池实际端电压与开关后电源ADC估计。
- 对照原图和ADC代码，未发现明显换算倍数错误；保留测量链误差可能。
- 结果正文已入项目库handoff90；采集前通知88已被同伴确认，串口已释放。
- 换电池后又被动接收12秒：电源估计约11.68V、49～50fps、帧号增长；Owner确认灯已稳定。
- 三个状态各自保留固定名称原始记录，避免通用文件名指向新采样引起误读。

## 未完成

- 具体属于原电池电量、内阻、保护或接头接触，尚无直接测量区分。
- 仅完成静态短时观察，未做带电机/风机负载验收；整体就绪标记仍未成立。
- 新结果handoff91待Opus回执；独立接口问题未在本轮修改。

## 收益与损耗观察

- 局部质量收益：Owner确认开关OFF避免把低ADC错误诊断为电池损坏；ON对照进一步把排查重点指向供电/检测链。
- 计时连续只能说明观察窗口内主控未反复启动，USB可能掩盖主板供电跌落。
- 没有相同质量条件的对照基线，不能宣称净提效。
- Owner中途更换电池，固件未改即恢复新帧与灯稳定，形成供电侧的对照证据；换电池包含重新插拔，不能将确切故障独归电芯。
- 先前归档草稿已入库但未发布时收到新实测，追加数据库版本并在GitHub发布最终版，避免旧结论覆盖新事实。

## 修改建议及下一轮验收

- **LIVELOG-20261020-POWERSTATE [proposed]** 日志记录时同时记电池、总开关、USB状态和改变时间，不把vbat字段直接当电池插头电压。；负责人：opus；下次检查：下一次供电实验有同步的测量和连接状态记录。
- **LIVELOG-20261020-FRESHNESS [proposed]** 图像页按帧号和时间显示新帧/缓存状态；解析成功与采集健康分别验收。；负责人：opus；下次检查：断开摄像头供电后旧缓存不再被显示为实时新帧。

## 证据

- evidence.json: three-state aggregates and provenance; raw data remains local.

## 限制

- Blinking stopped per owner and capture recovered; exact old-battery/connector failure mechanism unmeasured.
- Short stationary observation only; no motor or fan load validation.
- No commands sent, firmware edits or reboot. Raw logs and live databases excluded.

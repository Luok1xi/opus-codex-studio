# 2026-10-20-exposure-disconnected 工作流复盘

核查实际曝光是否已调整并尝试实车接入；Owner确认尚未重新连接，实测被设备缺席阻断。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：Reuse existing candidate, bounded native review, one serial connection attempt.
- 验收状态：partial
- 开始：2026-10-20T10:46:42.297Z
- 测量截止：2026-10-20T10:50:54.742Z
- 墙钟秒数：252.445
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| 开始至截止 | 252.445 | seconds | 实际时钟，含Owner答复等待。 |
| 实车连接尝试 | 1 | attempts | COM6不存在，未重试。 |
| 实车曝光写入 | 0 | operations | 未建立串口连接。 |
| 固件修改或烧录 | 0 | operations | 本轮只检查候选和准备最小适配建议。 |
| 原生独立审核 | 1 | workers | 复用现有审核者，无递归派发。 |
| 模型用量及费用 | 未知 | unknown | 无提供方账单或同口径usage。 |
| 协调及复盘开销 | 未知 | seconds | 未分离测量。 |

## 验收条件

- 实际调整曝光并用同场景图像及寄存器验证，不能把工具已发送当作已生效。

## 已完成

- 确认最近上车旧版本没有运行时曝光命令；磁盘新版本不能冒充车上版本。
- 一次COM6连接返回设备不存在，Owner明确确认未接回。
- 独立审核给出最小曝光及读回适配范围，发现停车保护缺口；未擅自混入其他相机配置。

## 未完成

- 尚未调整曝光，黑图未解决。
- 等待硬件重新接回；之后绑定可调曝光固件并完成前后图像和寄存器验证。

## 收益与损耗观察

- Owner强调实际修复优先；本轮明确没有调曝光，不把审查或报告算作修复。
- 设备不存在且Owner确认未接回，停止重复尝试。
- 没有同质量基线，不宣称提效。

## 修改建议及下一轮验收

- **EXPOSURE-20261020-ACTUAL-STATE [adopted]** 改参数前先核对在线固件功能与设备连接；以寄存器/画面变化验收，明确requested与verified区别。；负责人：codex；下次检查：重新连接后保存同场景曝光前后读数和图像；设备缺席时不继续循环连接。

## 证据

- evidence.json

## 限制

- Exposure not adjusted; hardware absent confirmed by owner.
- Review suggests a minimal patch, not an applied or hardware-tested fix.

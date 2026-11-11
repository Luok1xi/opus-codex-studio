# 2026-11-11-corner-record-analysis 工作流复盘

按Owner要求分析最新转角记录，并按其补充优先解释开启自动直角却未完成的前趟；调参仍由Owner与DSH执行。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + project evidence binding + native source review
- 验收状态：passed
- 开始：2026-11-11T08:46:24+00:00
- 测量截止：2026-11-11T08:56:02.138931+00:00
- 墙钟秒数：578.138931
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native contributors | 2 | agents | One recovered timestamped settings, one independently traced actual source; no recursive dispatch. |
| Actual trial records analyzed | 3 | records | Existing recordings only, not new experiments. |
| New firmware or runtime mutations | 0 | operations | No firmware, tuning or hardware writes. |
| Clarification questions | 1 | questions | Asked only whether the earlier failed turn retained normal contact; no rerun requested. |
| External model consultation | 0 | calls | No CLI consultation; database handoff only. |
| Model tokens | 未知 | tokens | No comparable usage evidence. |
| Model cost | 未知 | currency | No billing evidence. |
| Coordination/review overhead | 未知 | seconds | Included in wall time, not separately measured. |

## 验收条件

- 读取完整实际试跑，绑定版本和同趟参数，分清前后配置。
- 核对停机与控制状态源码，区分日志事实、现场观察和原因推断。
- 交付波形、数据和共享分析，不抢串口或代改参数。

## 已完成

- 三趟完整采集与实际回读已分别绑定；不是同配置重复试验。
- 前趟RA接管后急减速/反向制动与差速累积、超时链已核对，后两趟纯图像丢线单列。
- 用户合并姿态观察仅按原意记录，无俯仰/同步图像时不宣称唯一机械原因。
- 生成未平滑图和CSV/JSON，独立核对源码参数及状态，发DSH共享交接。

## 未完成

- 无记录

## 收益与损耗观察

- 将后趟失败归因于前趟自动直角会混淆配置；实际后两趟关闭元素，且固定P/D有变化。
- Owner强调前一趟同样失败后，分析重点即时转向RA接管后的制动和接地异常，不以后一趟取消状态机解释全部。
- 新增试跑在分析期间到达，仅做一次增量绑定；不抢占DSH串口。
- 一份早期TeamHub inbox输出虽有限条数仍含旧正文，后续用具体ID读取，避免扩大与本轮无关的材料。
- 先有采集事实与源码积分量相符，再结合Owner观察；未把Z轴角速度误称俯仰测量。

## 修改建议及下一轮验收

- **CORNER-BIND-CONFIG [adopted]** 每趟将实际回读与capture一起绑定；固定图像和分档图像、元素开关分别标注。；负责人：codex；下次检查：下一趟数据审核不得把表内kp字段误认成固定模式有效增益。
- **CORNER-CONTACT-FIRST [proposed]** Owner确认接地或姿态异常的片段单列，不用于继续增大角速PI；恢复正常工况后再单变量调参。；负责人：dsh；下次检查：需Owner与DSH的下一次正常接地证据及同趟配置；未代执行或代确认。

## 证据

- evidence.json
- Local frozen capture/config/source review hashes; public archive excludes project raw data.

## 限制

- 原因链部分定位不等于已修复；减速是否唯一诱因仍未证实。
- 40ms导出不能确定5ms控制相位或精确物理提前距离；没有同步图像/俯仰/触地传感。
- DSH交接已入库，未声称对方已接受；未产生新实车验证。
- 无同条件效率基线，不宣称提速；截止之后归档开销不在当前墙钟内。

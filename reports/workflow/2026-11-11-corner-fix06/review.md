# 2026-11-11-corner-fix06 工作流复盘

修复矩形直角已被视觉识别但局部偏差接近零时未接管的问题，参考已有海大与国二代码，形成不烧录的独立候选。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + bounded reference review + isolated implementation + actual C regression + ADS build
- 验收状态：passed
- 开始：2026-11-11T14:39:28+00:00
- 测量截止：2026-11-11T15:00:00.171387+00:00
- 墙钟秒数：1232.171387
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native contributors | 2 | agents | One source-reference and independent-review worker, one image/bridge verification worker; root implemented and integrated. |
| Source review findings closed | 4 | findings | Unbounded handover, mismatched frame validity, route0 residual fill, cold-start route restore; fixed with targeted tests. |
| Target builds | 2 | successful builds | Initial and final ADS runs; final receipt matches frozen sources. |
| Root control harness compile correction | 1 | failures | Initial Werror misleading-indentation in two test loops; braces corrected. |
| Hardware changes | 0 | operations | No serial opening, runtime writes, flashing, or starting. |
| External model dispatch | 0 | calls | Native workers only; no DSH/Opus delegation. |
| Tokens | 未知 | tokens | No scoped provider usage supplied. |
| Cost | 未知 | currency | No billing evidence. |
| Coordination wait | 未知 | seconds | Overlapped with implementation; not independently measured. |
| Review/archive overhead | 未知 | seconds | Review overlapped implementation; archive verification occurs after cutoff. |

## 验收条件

- 从当前已记录烧录来源隔离，不覆盖其他工作。
- 现有视觉实际灰度回放与控制/桥接真实C回归通过。
- 源码与官方目标构建绑定，保留未实车验证边界。

## 已完成

- 保留已识别角点通路，默认自动直角；三帧新线确认、同帧有效性、防旧角重入、有界交回。
- 修正无路线时残留校赛补线与冷启动路线恢复；保留用户选择的250基础轮速。
- 新增有效/保持/丢失状态及伴随记录，原采集协议保留。
- 475张合成灰度、5700次实际流水线、2645图像检查；419控制及140接口检查，内存检查通过。
- 官方TC264编译0错误13警告；冻结HEX与全部输入哈希。

## 未完成

- 无记录

## 收益与损耗观察

- Independent review found four concrete integration errors after the first passing unit suite; fresh integration tests closed them.
- Existing OUC already detects standard long-arm corners even when Gaussian deviation is zero or invalid; a new vision rewrite was not justified by the replay.
- A local national-second-prize reference uses a different navigation task; source mechanisms and physical units were compared instead of copying gains.
- Frozen current-flash lineage avoided replacing active DSH work.

## 修改建议及下一轮验收

- **CORNER-SNAPSHOT [adopted]** 控制状态切换只接受同一视觉帧的方向、有效性和采集时间；新增交回策略同时测试下一弯是否可重入。；负责人：codex；下次检查：下一次真实连续图像回放复核同帧记录与相邻弯。
- **GEOMETRY-ACCEPTANCE [adopted]** 基础速度与角速上限同时做半径检查，不把状态机测试通过当作高速贴线通过。；负责人：codex；下次检查：实测轮速换算与角速度跟踪后再定高速弯触发位置。

## 证据

- evidence.json

## 限制

- 未烧录、未接串口；没有整圈闭环或8/8工况验收。
- 相机俯角、轮速标度、抓地未重新标定；250基础速度的物理过弯能力未证实。
- 同条件效率基线不存在，不宣称协作提速。

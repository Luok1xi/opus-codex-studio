# 2026-11-12-visual-outer 工作流复盘

纠正上一轮自动直角接管的错误方向，修复纯图像方向外环在弯前偏差不变的问题；核对指定疯狂电路国二与海大源码，完成隔离候选和编译，不接车。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + image-observation contract + source-reference audit + actual C regression + isolated ADS build
- 验收状态：passed
- 开始：2026-11-12T01:08:12+00:00
- 测量截止：2026-11-12T01:41:57.231164+00:00
- 墙钟秒数：2025.231164
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native contributors | 2 | agents | One source audit/review worker, one full-image testing worker; root implemented/integrated. |
| Target builds | 2 | successful builds | Initial candidate and final candidate after visibility/record fixes; final source hashes bound. |
| Post-initial candidate defects fixed | 2 | issues | Short occluded centered stub incorrectly valid; interrupt-interleaved record snapshot. |
| Prior-round scope correction | 1 | rounds | Owner rejected automatic corner takeover; isolated prior candidate preserved, new candidate rebuilt from flashed lineage. |
| Optional diagnostic exceptions | 19 | cases | Nonactive fill2 interpolation/noise cases retained as failures; not counted in required pass total. |
| Hardware operations | 0 | operations | No serial, parameter writes, flashing or launch. |
| External model dispatch | 0 | calls | Native workers only; no Opus/DSH consultation. |
| Tokens | 未知 | tokens | No scoped provider usage available. |
| Cost | 未知 | currency | No billing evidence. |
| Coordination wait | 未知 | seconds | Overlapped implementation; not separately measured. |
| Review/archive overhead | 未知 | seconds | Review overlapped work; remote archive verification follows measurement cutoff. |

## 验收条件

- 纯图像偏差产生转向需求，正常接口不能开启自动直角或路线。
- 同灰度输入复现旧窗口零偏差并验证新输出，当前候选范围回归通过。
- 真实C控制和目标编译与冻结源码绑定，明确未实车验证。

## 已完成

- 接回OUC前方爬线选点，输出右正像素，保持现有内环公式。
- 修正遮挡短直段误报有效居中，保留无效/保持/失线区分。
- 修正中断可打断日志字段采样的问题，使控制记录同一快照。
- 1044张灰度、14644次流水线调用，3521必需视觉检查及387控制检查通过。
- ADS 0错13警告，HEX74917d55；原工程未改、未开串口、未烧录。
- 核对用户指定仓库的同源本地归档，不再误用另一国二参考。

## 未完成

- 无记录

## 收益与损耗观察

- Previous implementation solved an unwanted takeover behavior rather than the requested observation error; this round made the controller ownership contract explicit before editing.
- Actual existing OUC target selector was bypassed by a fixed row-window adapter. Whole-frame tests reproduced the blind spot; changing Kp alone cannot supply missing image error.
- Synthetic black occlusion exposed a near-zero valid fallback; a real-exit visibility gate fixed it but reduced gap tolerance, recorded rather than hidden.
- Independent review found a nested-interrupt logging consistency issue; targeted source fix and final compilation closed it.
- Two broad tool reads printed unnecessary full hash manifests; final freeze uses assertions and compact summaries instead.
- The specified public source was already local. Origin, git blob and archive hashes verified provenance; failed webpage access was not called a current-remote verification.

## 修改建议及下一轮验收

- **OBSERVATION-BEFORE-TAKEOVER [adopted]** 先写清控制权归属：纯图像调参必须证明无角点元数据也能产生正确转向，有角点但零偏差不能自动转向。；负责人：codex；下次检查：后续实车同步图像、偏差、角速目标与有效年龄；不得用接管成功替代图像观测修复。
- **PIXEL-UNIT-NOT-OPERATING-POINT [adopted]** 参考实现先核对分辨率、单位、符号、目标位置与输出接口；同为像素不代表相同增益工作点。；负责人：codex；下次检查：试车前恢复已存内环运行参数并单独调整外环；记录新观察模型。
- **ACTIVE-MODE-AND-DIAGNOSTIC-FAILURES [adopted]** 将实际启用模式验收与额外模式诊断分开，保留所有失败和适用范围，禁止将可选失败静默删掉。；负责人：codex；下次检查：若以后打开虚线补线，必须重新通过该模式噪声与遮挡验收。

## 证据

- evidence.json

## 限制

- 仅实线矩形调参候选；虚线、全元素、250高速和整圈未验收。
- 相机几何仍为继承模型，无实车新图像；源码结论与实车根因分开。
- 编译默认PID和风机不是最近临时实跑值，烧录后需恢复并回读。
- 没有同质量配对效率基线，不宣称速度或费用收益。

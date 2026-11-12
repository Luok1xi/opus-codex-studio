# 2026-11-12-ouc-aligned08 工作流复盘

按海大main补齐视觉状态/选点与十字重建缺项，保持原控制公式，在独立候选完成离线回归和TC264编译。

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + isolated candidate + call-chain alignment + real C replay + target build
- 验收状态：passed
- 开始：2026-11-12T02:35:08+00:00
- 测量截止：2026-11-12T04:30:12.342441+00:00
- 墙钟秒数：6904.342441
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Round wall clock to report cutoff | 6904.342 | seconds | UTC task start to report cutoff; includes coordination, environment waits and rework, excludes later remote archive verification. |
| Native contributors | 3 | agents | State/line, image/cross tests, bridge/review; one root coordinator. |
| External model dispatch | 0 | calls | No external Opus or DSH dispatch. |
| Target build attempts | 2 | builds | First failed contiguous DSPR1 RAM placement; second passed after cold backup placement in DSPR0. |
| Hardware operations | 0 | operations | No serial, flashing or launch. |
| Tokens | 未知 | tokens | No scoped provider usage available. |
| Cost | 未知 | currency | No billing evidence. |
| Review archive overhead | 未知 | seconds | Review overlapped implementation; remote verification after cutoff. |

## 验收条件

- 源代码实际调用对齐，区分视觉状态和固定航向接管。
- 保留07与原控制配置，验证边界/真实灰度链及目标编译。
- 明确模型发现与实车验收边界；没有串口/烧录。

## 已完成

- 补视觉ANGLE、fork选边/guide、cross重建和三帧保持；J0/route0保留。
- 桥使用重建前拓扑；修失效旧值显示、保持叠加、抓图超时。
- 状态98、选点858、真实灰度整链54、桥48、外环403、控制不变12检查通过。
- 最终15041次灰度调用和目标0错误13警告；冻结候选并核对旧626输入与HEX不变。
- 发现并修复角态11例遮挡误报；明确保留原式38cm选点突变，不冒称实车稳定。

## 未完成

- 无记录

## 收益与损耗观察

- Three exclusive source scopes enabled review findings to become bounded patches; no matched quality baseline exists, so no speedup claim.
- The first active grayscale test caught a state-dependent validity regression that ordinary-mode parity did not detect; the failed evidence was preserved before correction.
- Target compilation exposed RAM placement missed by host tests; 4800 bytes of cold cross rollback storage moved without changing algorithms.
- Local test adaptation needed explicit UTF-8 reading and robust relative-path resolution; a metadata git read required local permission elevation. These were harness/environment rework, not vehicle failures.
- The bridge reviewer subsequently authored bridge fixes. Reports distinguish author verification from root review, rather than claiming fully independent acceptance.
- Upstream common-min selection caused an early large input step in the inherited camera model. The team retained and disclosed the actual behavior instead of silently smoothing it or calling all tuning solved.

## 修改建议及下一轮验收

- **UPSTREAM-CALLCHAIN-FIRST [adopted]** 以原入口、状态、选点、消费者为一条链验收，并保留刻意适配清单。；负责人：codex；下次检查：后续启用fork或ring必须验证owner生命周期，不用接口存在代替运行时接通。
- **ACTIVE-MODE-VALIDITY-REGRESSION [adopted]** 普通模式对照之外，强制在每个新状态加入遮挡/短线/重复帧/失效恢复样本。；负责人：codex；下次检查：后续视觉修改保留本轮13例和三帧到期整链用例。
- **TARGET-MEMORY-EARLY-CHECK [adopted]** 增加大型静态缓冲前先核对目标RAM余量，host测试通过后仍单独检查link map。；负责人：codex；下次检查：后续图像模块新增缓存时记录所在内存与大小。

## 证据

- evidence.json

## 限制

- Source-aligned visual candidate; not a physical or closed-loop full-course acceptance.
- J0/route0: angle selection active; fork/cross owner interfaces covered offline, not enabled as a new route engine.
- Original common-min switching jumps at modeled 380mm: left -1 to -84, right -1 to +83; retained and reported, not smoothed.
- Normal gap fill remains mode0; ring/inertial replay and all-element routing not enabled.
- Compiled PID defaults are unchanged and do not stand for recent volatile tuning.
- No scoped token/cost or matched workflow baseline; no speedup claim.

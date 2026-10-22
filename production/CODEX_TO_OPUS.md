## 2026-10-18 · WORKFLOW-ROUND-REVIEW-20261018 · Owner要求每轮复盘并归档私人仓库

Owner新要求：每轮任务做技术数据分析，判断实际提效并记录修改建议，上传私人GitHub。规则已在通用studio的 docs/WORKFLOW_REVIEW.md；报告入口 https://github.com/Luok1xi/opus-codex-studio/tree/main/reports/workflow 。同步是否完成以远端回读为准。

请执行任务时记开始/截止、验收、产物、真实usage（未知留空）、失败/返工、等待/交接。向协调者提供聚合数据，一轮只合并一份报告；不追加模型委员会，不上传原始会话/推理/凭据。不要把并行重叠当节省时间，没有同条件同质量基线就明确“净提效未证实”。仅文件移交不等于收到Opus回执。

上一轮已观测：955.986秒；两个Codex子代理重叠193.414秒；84条真实usage。两子代理首输入109218/109258 tokens，建议短任务卡试验；当前没有可比串行基线。完整报告在通用studio reports/workflow/2026-10-18-smartcar-research/。请回执本ID并提供可用的聚合数据，未收到回执前保持待确认。你现有前端/手册工程不覆盖。

---

## 2026-10-15 · 小车现有桌面Opus回执已核实

Opus第49次回信已确认LINECAR-COORD-20261015，读到两份DeepSeek原文并交付修订1；主导为Codex。34个源码文件独立比对v002一致。后续只在Luokixi共同入口协调，不需重复CLI登录。最新草案0.4与新增地图/混合惯导方案在F:/LineCar/疯狂电路方案-20261015/，新增部分尚未经外部模型专项复核。

---

## 2026-10-15 · 小车协作入口纠正（替代下方旧待授权/待CLI状态）

Owner已明确授权技术摘要发往DeepSeek及同范围Opus。咨询e782c56f-e965-4182-a2ad-70bf2aa53ec6已answered，session-d19bbef2-4081-46cb-bae7-83c9e471f8df，SHA f8cff6e351f00bf50b1d0b2b37866f7a8ae255c49e4cb97a3d77bb769484c7b5。原文与人工修正放在F:/LineCar/疯狂电路方案-20261015/；不是实车验证。
Owner要求Codex主导，现有Opus在Luokixi桌面小车会话，已找到第48次回信。共同入口 C:/Users/user/Documents/GitHub/luokixi/docs/LINECAR_COORDINATION_20261015.md；在真实仓库OPUS_TO_CODEX回信，不以独立CLI状态代表桌面可达性。9mm为用户新实测；本轮串口未枚举、无运动命令。修订回执待核实。

---

# Codex → Opus
## CRAZY-CIRCUIT-20261015 · 初步方案与待审材料

- 后续进展：已另建严格仅含公开规则链接与假设团队问题的咨询，key `crazy-circuit-20261015-public-research-1`，job `e937d4bf-bc74-4dac-acc0-4d8f1784bcec`，status=answered，原生session `session-58ea36b6-a7ef-4cd9-b63e-2f6d8a0fbbf5`，答复SHA-256 `8c024a55a5a8f7bfd3920fa1cb8543ab29061363dbcdd30f7b396bd7f0b7d5a2`。本地已阅读并修正其不确定路口默认直行、盲目丢线搜索、正式自主运行依赖通信心跳等建议，合入草案0.2。私人技术摘要仍未发送，不混淆两次请求。
- 用户明确要求与 Opus、DeepSeek 配合形成疯狂电路初步方案；当前车为 STM32 练习车，比赛主控计划 TC264。
- 项目文件：`C:/Users/user/Documents/Codex/2026-10-13/files-pasted-by-the-user-c/outputs/CrazyCircuit-20261015/`，包含方案、测量表、核查状态和继续工作。初稿基于实际源码及公开21届规则，校赛规则未找到；无新实车调参结果、无运动指令、无刷写。
- 当前官方 Claude CLI 探针报告 `Claude CLI login required`，已启动由用户本人操作的官方登录。未收到 Opus 审查。
- DeepSeek 请求：项目 `work/crazy-circuit-20261015/deepseek-request.txt`。自动审批拒绝发送未公开技术摘要，已向用户说明并请求发送到 DeepSeek/Opus 的明确授权。consult 未执行；不得换包装绕过。用户答复后再按同一 key `crazy-circuit-20261015-control-review-1` 检查/执行。
- 操作员复核：Windows未枚举到CH340串口，尽管用户确认已供电；旧黑色画面0000新鲜性未确认，不能认定黑白极性。先解决设备连接，再按测量表读实时数据。
- 后续审查需重点看：规则版本差异、视觉与惯导分支不混用、路口重复计数、摄像头图案干扰、默认停车与重新启动、轮周/计数/死区实测。不要把现有蓝图静态数据当实车反馈。

## BRIDGE-004 · 新会话发现与按任务选人，2026-10-14

- Owner 要求将 DeepSeek 实际入口接进通用工作流，让没看过旧对话的 Codex 可发现，并摆脱单一常驻主脑。本轮继续在同一真实源码分支修改，保留已有实现。
- 已安装 C:/Users/user/.codex/skills/ai-studio/SKILL.md；全局 AGENTS 原为空文件，已备份并加入短指针。仓库 tools/install_codex_skill.py 可重装，保留用户其他说明；不是记忆文件，不改账号或模型全局设置。
- `bridge.py consult --workspace ... --prompt-file ... --key ...` 复用官方 DeepSeek headless，统一保存答复/会话/散列。相同 key 不重复调用，失败或崩溃不进自动工作队列。answered 不等同独立验收通过。
- `routing_rules` 支持规划、验收和能力专长的不同名单，配置规则优先于模型 agent 提示。效率示例及本机配置：Opus 规划优先、Codex high 验收优先、Codex medium 代码执行优先，仍受实际客户端与额度约束。规划与验收不共用原生会话。
- 真实验证：新 Codex 会话 01a137c5-66a9-7f63-a81c-8eca28102669 无旧聊天即找到源码、调用及恢复方法。另在仓库外空目录用官方 skills/list 确认 ai-studio scope=user、enabled=true，零推理；证据 .studio-runtime/fresh-codex-discovery.json、skill-catalog-proof.json。
- DeepSeek 真实审查通过统一入口，账本任务 03c23902-5647-4bfe-affc-68b4ab6a2cae，原生会话 session-fe224af3-a02f-481f-9d39-f7bad690b1cb。采纳其“样本难度偏差”的提醒；不采纳“状态探针耗推理额度”的错误判断，也不做缺少工作目录/输入版本的全局内容缓存。
- 全量 65 测试通过，21 原件散列 PASS。测试含安装保留/重复、咨询去重/崩溃/真实子进程、角色路由与原生会话隔离。未改变 vendor/archive，未推送。
- 方案和边界见 docs/WORKFLOW_INTEGRATION.md：非模型控制器常驻、AI 按需任职、按可比任务质量/返工/时间/用量调优。自动学习选人没有实现；当前规则是起点，不宣传最优。DeepSeek 自动余额/强制只读策略及 Opus 登录仍是后续真实联调事项；没有启动自启后台或接管任意桌面聊天。

## BRIDGE-003 · DeepSeek 主动调用成功，2026-10-14

- Owner 要求实际调用已打开的 DeepSeek 打招呼，并明确要求继续接通。桌面 HTTP 401 只表示会话认证缺失，不能将其等同于所有入口不可用。
- 已独立安装官方 @deepseek-ai/dsh@0.2.0-rc.2，使用 headless 与现有 Harness 共享账户数据。官方 CLI 初始化独立 headless profile；没有读取、复制或导出认证密钥，没有改桌面 profile 或全局 PATH。
- 实际回报：你好！我是 DeepSeek，很高兴和你一起协作。进程退出码 0；最终回合 completed；会话 session-445aed77-c95c-4869-bf84-ea16de36b27c。
- 后续桥接操作员直接调用 tools/deepseek_task.py --prompt-file 请求文件；默认本机连接配置及真实回执在 .studio-runtime，操作方法见 docs/DEEPSEEK.md。不要再次仅因没有 MCP 名称就报告无法调用。
- 入口复用有界进程与回收，支持显式原生会话续接，最终输出按完成事件和退出码核验，不回传内部思考。续接和复杂任务尚未实测；自动额度路由、只读隔离还未启用。
- 本轮只实际调用一次模型用于获授权的问候；正式入口追加离线测试，不重复消耗模型调用。源码未推送。
- 最终全量回归 57 项通过，21 个原件散列通过；正式入口的结果解析器核验了本次保存的真实回执。

## BRIDGE-002 · 以实际效率为目标，2026-10-14

- Owner 最新取舍：优先接入效果可靠的现成工具，减少手动搬运、重复任务和额度消耗；不以补市场空白或造完整编排平台为当前目标。
- 调研确认：LangGraph、Temporal、OpenHands、WAO、ryder、Hydra、ACP 都覆盖部分既有能力。docs/AUTOMATION_RESEARCH.md 记录一手来源、采用决定、未经验证事项；没有同题比较就不排“最强”。
- 已接入的官方 Codex/Claude 接口继续承担执行。本轮新增效率配置 examples/efficient.bridge.json，并在被忽略的 bridge.local.json 应用：Opus 优先，Codex medium 执行、high 候补主脑，同账号共享额度。通过真实官方 config/read 确认配置生效。用户全局设置未改。
- 工作室源码自己的 unittest 与 studio_check 已加入本机 checks 并通过实际命令执行器运行。迁移到其他工作目录时必须替换成其自身检查。
- 故障修复：写入后限额不再盲目重派；未知写结果停止新派工与返工；只读步骤及已核验成功回执可有界恢复，尝试次数和预算不清零；硬失败且无修复预算跳过无效终审；只读返工保留专长、依赖、权限及评审意见。
- 当前证据：53 项全量测试通过，21 个原件散列通过；包含真实子进程写入前后回执丢失的退出测试。详见 docs/VERIFICATION.md。本轮模型推理调用为零。
- 未解决边界：Claude CLI 仍未登录，DeepSeek 未验收；没有任意 GUI 会话接管、任意外部副作用自动对账或真实费用收益结论。needs-reconciliation 需桥接操作员核对实际成果后继续，不能用自动重试伪装恢复。
- 下一步使用真实待办验证，不为演示耗额度。记录完成质量、真实用量、总耗时、返工和人工介入。若某现成执行器在同题上收益明确，用现有 command 合同接入；若需要更复杂持久工作流，先评估 LangGraph/Temporal，而非继续自造。

## BRIDGE-001 · 通用协作内核，2026-10-13

- 基线：真实 GitHub 仓库 Luok1xi/opus-codex-studio，main@707284e。本地工作分支 feat/general-agent-bridge；未推送、未发布、未打包。
- 差异：远端原为 schema 2 的人工交接框架；本机另一个旧输出包的 DeepSeek、北矿娘资料与自动化草稿不在远端。本轮直接扩展真实源码，保留人工入口、历史档案和 21 个锁定第三方原件。
- 已实现：通用目标与工作目录、校验后的任务依赖图、能力与优先级匹配、Opus 优先主脑/Codex 接替、额度窗口与缓存、自定义成员协议、成果交接、SQLite 队列与事件、重复提交去重、并行读/互斥写、检查和有限修复、停止和进程树回收。
- 效率：普通程序负责状态/轮询/检查；按依赖传成果；合并额度查询；避免重复执行；原生成员默认隔离外部 MCP，用户全局设置不变。
- 结构：tools/studio_runtime/ 分为 contracts、store、routing、context、engine、adapters；tools/bridge.py 是薄入口。Python 标准库运行，不依赖网站、游戏、Git、npm 或外部数据库。
- 验证：原框架校验 PASS；代码/资料两个离线流程生成实际文件并通过检查；真实 Codex 调用与限时失败验收均有记录。最终测试数量与真实成功路径见 docs/VERIFICATION.md。
- 独立修复：Windows 换行转换破坏 vendor 散列；模型伪造已完成状态；禁用成员借用额度缓存；预算结束丢失已派发成果；修复回合丢失证据；主脑返回格式错误；进度消息污染最终 JSON；Windows 外部持有管道句柄导致收尾等待。均有相应回归或原件校验。
- 本轮未做：未自动登录、未调用 Opus/DeepSeek 真实推理、未复制个人桌面数据；未接管现有 GUI 聊天、未改网站、未做分布式多写者或自动合并。
- 继续工作：先验收登录后的 Opus 流程及 DeepSeek 正式入口，再基于真实任务收集质量、总用量、成功率与人工介入数据。扩展图形界面/浏览器/媒体能力时使用独立适配器，不能把注册能力标签当成已接通工具。

详细设计：docs/ARCHITECTURE.md；操作方法与真实边界：docs/BRIDGE_GUIDE.md；复现命令、性能口径和失败记录：docs/VERIFICATION.md。

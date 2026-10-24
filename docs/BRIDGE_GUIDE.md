# 使用通用协作桥

## 角色和入口

主脑负责目标、计划、分工与验收；Codex 作为桥接操作员调用本地工具；Python 协调器负责进程与任务记录。协调器不消耗模型额度来轮询、查状态或运行验证命令。

一项目标只需提交一次。`run` 完成当前可执行队列后退出，额度暂不可用的任务保留 waiting；`run --watch` 自动等待新任务或下一次容量检查。闲置间隔为 2 秒，只检查小型 SQLite 索引，不调用 AI；waiting 任务至少间隔 60 秒再观察。优先级 0–100，数字大者先处理；正在进行的目标不中途抢占。

默认状态目录 `.studio-runtime`，可用全局参数 `--state PATH` 改变；所有命令必须使用同一个 state。一个状态目录只能有一个协调器。操作系统锁随崩溃释放；下次 run 会检查原 running 任务：只读步骤可在恢复预算内续接；写步骤已有匹配尝试号且散列正确的成功回执时保留成果，否则进入 needs-reconciliation。检查命令执行中断或恢复预算耗尽时保留 interrupted。已用调用数与修复次数不清零，默认最多自动恢复两次（max_recoveries）。

needs-reconciliation 表示需先核对真实操作结果，再提交带已有证据和明确下一步的新目标；可以由有权限的桥接操作员核对，不能把失联当成未执行。当前没有自动判定任意外部副作用的通用工具。恢复针对进程中断，未验证断电恢复。

## 配置

复制 bridge.example.json 为 bridge.local.json，不提交本机配置。agents 配置官方客户端、模型、能力；lead_order 和 worker_order 是优先顺序。能力可以是 code、research、write、review 等自定义名字，任务所需能力必须有一个成员完整满足。

效率配置可从 `examples/efficient.bridge.json` 开始：Opus 规划优先，Codex high 优先独立验收，Codex 执行成员 medium；后两者共用真实账户额度，不是两份额度。`routing_rules` 按顺序匹配 role 和能力子集，首个匹配规则的 order 是完整候选名单，优先于 agent 提示；未匹配时沿用 lead_order/worker_order 和 agent 提示。复杂步骤可由配置作者添加更具体且靠前的组合能力规则。规划与验收使用不同原生会话。Codex 的 reasoning_effort 仅覆盖当前子进程，所选模型必须支持该档位；未填写则沿用客户端设置。当前本机已验证 medium/high 设置生效，尚未测得真实任务的费用节省比例。

`command` 是 argv 数组而非 shell 字符串；不做 `$()`、反引号或 shell 展开。安装位置可自动从 PATH／官方桌面客户端目录发现，也可显式指定。CLI 更新后应重新运行 doctor。checks 是由配置作者确定的命令数组，例如：

```json
{"checks":{"unit":["python","-m","unittest","discover","-s","tests"]}}
```

配置中的命令有本机执行能力，应由工作室所有者维护。主脑计划不能新增命令、修改预算或注入运行状态。实际工作目录由提交者指定，计划不能改变它。研究／写作任务可以没有命令检查，最终仍需主脑核对资料和成果。

最终成功要求所有步骤完成、配置中的每个机械检查退出码为 0 且正常结束、主脑明确验收通过。任一检查失败都不能被 AI 的“通过”覆盖；在修复上限内重新工作和检查，否则保留 needs-attention。已经存在硬失败且没有修复预算时直接结束，不再浪费一次终审调用。只读返工保留能力与依赖图，不升级为写任务。

## 额度和接替

Codex 从官方 app-server 读取账户是否可用与 Codex 额度窗口；Claude 先确认 CLI 登录，再读取原 CLI 订阅凭据对应的使用量接口，凭据只在进程内使用，不进入回报与状态。Claude 该接口的兼容性可能随客户端变化；不可用时显示未知，不尝试绕过。系统不会复制桌面凭据、自动登录或购买额度。

多个窗口逐一判断，不平均成一个比例。默认保留 5%，快照 60 秒内复用；模型/命令不同的成员分开缓存。`quota_group` 可显式共享缓存，但只应用于相同账户、相同运行入口与相同模型额度范围。自定义金额额度保留金额和币种，可设置 reserve_balance，不换算成订阅百分比。

明确限额错误让该额度组冷却 15 分钟；登录错误冷却一小时，其他成员可以接手。普通 429、权限拒绝、质量问题不自动当作订阅耗尽。主脑在只读计划和验收边界可接替；只读 worker 限额时只重新分配该步骤。写 worker 非成功退出可能已有副作用，进入 needs-reconciliation，停止新派工和自动返工。进程异常或失联不承诺 exactly-once 外部副作用。

## 通用接入协议

内核不要求 Git、不要求编程任务。可配置 provider: command 接入经所有者验证的本地 AI、资料处理器或专用工具。命令从 stdin 收到 JSON：

```json
{"prompt":"当前任务和必要证据","cwd":"工作目录","read_only":true,"session_id":null}
```

stdout 返回一个 JSON 对象，进程退出码必须为 0 才能报告成功：

```json
{"status":"succeeded","text":"实际成果与限制","session_id":null,"usage":{}}
```

status 可为 succeeded、quota、auth、failed、cancelled、timeout。probe_command 是独立、不发起推理的额度/健康查询：

```json
{"available":true,"reason":null,"observed_at":1791900000,"windows":[{"remaining_percent":80,"reset_at":1792000000}]}
```

也可返回 balance: {remaining: 12.5, currency: "CNY"}；必须是真实来源。没有时间、未知、过期、越界的额度不能派工。仅离线演示允许明确标注的夹具额度；不能拿它接真实模型。read_only 必须由包装器实际执行，单靠提示词无法提供隔离。

DeepSeek 通过 `bridge.py consult` 接入统一账本，底层复用已实测的 tools/deepseek_task.py，见 [DEEPSEEK.md](DEEPSEEK.md)。consult 是一次显式调用，不进入自动派工：相同 key 取原记录，回答状态为 answered，失败或中断需要核对。它也使用同一控制器锁；有运行中的协调器时不会插入另一项可能写文件的操作。余额路由、只读约束及复杂任务尚未验收，队列中的原生自动适配器仍未启用。需要电脑图形界面、浏览器、图片或硬件能力时，必须提供经过验收的对应适配器；当前版本不声称已接管所有桌面 AI。

## 交接、成果与停止

每次派发包含固定约束、目标、当前步骤和直接依赖的成果。完整输出按 SHA-256 保存；大回报只传摘要与路径，不循环灌入整个历史。相同提供方的同一步可利用其 session_id 继续；跨提供方交接可见成果，不迁移隐藏推理。

指标中的 prompt_chars 仅统计桥接器新发出的文本字符，不包含客户端自动加载的项目规则、工具内容、恢复会话的历史或计费缓存。它不能直接换算成真实 token 或费用节省。

`stop` 发出停止请求；框架在 Windows 用 Job Object 管理自己启动的后代进程，取消/超时会清理它们。不关闭已有桌面程序、外部 MCP 服务或不属于自己的独立进程。CLI 本身的权限仍保留：Codex 使用 read-only/workspace-write，Claude 使用 plan/acceptEdits 并拒绝无人应答的权限请求。没有危险的全权限跳过开关。

原生自动成员默认不加载外部 MCP。Codex 在子进程中关闭 apps/plugins/hooks，读取有效 MCP 名单、逐个禁用并复验；不会修改用户全局配置。Claude 使用严格空 MCP 配置并禁用 MCP 工具。这样减少无关工具加载，并阻止外部 MCP 绕过 CLI 只读模式产生副作用；不代表完整操作系统隔离。需要这些工具的成员可通过经过验证的 command 包装器单独接入，权限与只读约束由包装器负责。

默认最多 16 次模型调用、每次 15 分钟、一次修复；达到上限留下 needs-attention 和证据。新终端不能绕过状态目录的单实例锁。源码默认不开机自启、不启动后台服务、不自动上传或合并。

工作目录的写入互斥在一个协调器内部生效。管理同一目录的任务应共享同一个 state，不要另外启动独立状态目录来同时修改它；框架无法给外部编辑器或其他独立程序加锁。

## Antigravity Opus 入口

用户已配置通用 Antigravity 规则和官方 CLI，使用方法与实际验证边界见 [ANTIGRAVITY.md](ANTIGRAVITY.md)。它使用独立协作标签 `opus-antigravity`，可进行显式咨询及共享项目交接；不要把它误当 Claude Code 会话。实际读/答/本地写和本人 ack 已核验，正式 handoff 尚待限额恢复后验证。当前没有启用自动队列适配器，也没有已验收的额度路由，不能从程序安装或空 `SUCCESS` 推断可自动派发。

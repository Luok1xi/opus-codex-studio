# Codex × Opus × DeepSeek 工作室

## 2026-10-13 · 自动协作升级方向与真实核查

Owner 最新要求：自动调用成员、检测可获取的剩余额度、设置优先级、主动派发开发与测试；Opus 可用时优先主脑，额度耗尽后由 Codex 接替。本条是新的授权与实施方向，下文人工交接描述仍表示现有实现，不表示自动调度已经完成。现有配置保持原状，尚未启动常驻服务。

本机核查（未调用模型）：
- Codex CLI 0.162.0-alpha.17.2 的官方 `account/rateLimits/read` 实际返回一周窗口已用 11%，其他窗口未返回；这是 2026-10-13 20:53 北京时间附近的快照，不是永久余额。
- Claude Code 2.1.295 可执行，但独立 `auth status --json` 返回 `loggedIn: false`、`authMethod: none`。桌面版 Claude 正在运行，不能据此推断命令行共享其登录。需由用户完成官方 CLI 登录，不能复制桌面凭据代替登录。
- DeepSeek Harness 进程存在；当前 PATH 未发现 dsh，安装路径探测未成功。仅确认客户端正在运行，未验证自动调用入口和额度。

现成项目（只调查，尚未安装或改编）：
- [Agent Orchestrator](https://github.com/OrchestratorInc/agent-orchestrator)：Windows 版、多代理、工作区隔离和任务监督，作为优先验证的完整底座；不把这些能力当作已经实现额度耗尽后的自动主脑替换。
- [backnotprop/orchestrator](https://github.com/backnotprop/orchestrator)：可复用的本地任务调度、状态、恢复及额度查询；文档明确额度快照不负责自动路由，原生 Windows 还需实测。
- [ryderderder/orchestrator](https://github.com/ryderderder/orchestrator)：有按额度路由，但原生 Windows 不支持、需 tmux/WSL；其未知额度按 0% 已用排序的策略不适用于本项目，不能照搬。

实施顺序：先接通 Claude/Codex 官方调用入口，运行一项隔离的测试编写任务并验证真实回报；再加入独立于模型的调度进程、持久任务队列、成员优先级与额度快照。一个主脑租约、一个文件写入者；在任务边界或明确额度错误时交接上下文、改动摘要、测试结果和下一步。额度未知/过期不当作充足；额度耗尽等待恢复或转交其他已授权成员，不绕过限制。主脑切换后不立即抢回，避免重复派工。

跑测试本身由普通进程执行；AI 用于拆任务、写测试、审查和处理失败。每次任务有运行时限、失败重试上限、可见状态和停止入口。先只操作隔离候选目录，保留原人工交接文件，不能让两个 AI 同时覆盖真实网站。尚未配置自动充值、计费升级、提交推送或公网部署。

官方依据：[Codex App Server](https://learn.chatgpt.com/docs/app-server)；[Claude 程序化调用](https://code.claude.com/docs/en/headless)；[Claude 状态行额度字段](https://code.claude.com/docs/en/statusline)。额度字段是否出现取决于账户与接口，不能承诺每个 AI 都能读到精确余额。

本轮证据：`C:/Users/user/Documents/Codex/2026-10-11/gai-s/outputs/studio-readiness.json`；Claude 登录状态随后单独复核为 false。网站轻量化候选暂存同工作区，两个产品文件、23 项单元测试、44 项工具浏览器流程与 4 组加载故障测试通过，尚未交付共享网站；首页启动脚本与样式在隔离 API 条件下由 646476 降至 579085 字节（解码体积，不能代表总页面或公网速度）。

---

| 角色 | 职责 | 任务 / 回报 |
|---|---|---|
| Creative Owner | 用户：目标、授权、最终取舍 | 当前用户指令 |
| Claude Opus | 主导设计、写作、程序，派任务并接入成果 | 两位成员的任务单和回报 |
| Codex | 实现、调研、资产与 QA，交付验证证据 | OPUS_TO_CODEX.md / CODEX_TO_OPUS.md |
| DeepSeek Harness | 按派单实现、调研、文档与验证，交付证据 | OPUS_TO_DEEPSEEK.md / DEEPSEEK_TO_OPUS.md |

任务和回报位于 production/。共享 BOARD.md，动手前登记任务与文件范围，完成或转交后释放占用。
Opus 按任务选择成员；需要复核时，一人改文件，另一人只读检查。同一文件同一时间只由一名成员修改。
协作方式仍为人工文件交接。DeepSeek 派工工具生成可粘贴的任务提示，不自动调用模型。
早期四色路由、检查器和测试保存在 archive/legacy，不能代表当前流程。
DeepSeek 上手见 studio/DEEPSEEK_SETUP.md。

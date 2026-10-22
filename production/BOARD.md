# 任务板

| 任务 | 负责人 | 状态 | 文件范围 | 交付证据 |
|---|---|---|---|---|
| BRIDGE-004 | Codex | 全局发现、统一 DeepSeek 咨询与角色路由已接入 | skills/ai-studio、install_codex_skill、consult、bridge、contracts/routing/engine/store、文档与测试 | 65 项测试和 21 个原件散列；无历史 Codex 实际找到入口；工作室外 skills/list 确认启用；DeepSeek 实际方案审查回执已入账 |
| BRIDGE-003 | Codex | DeepSeek 真实消息调用已通过 | tools/deepseek_task.py、tests/test_deepseek_task.py、docs/DEEPSEEK.md、本机独立官方 CLI | 已收到真实中文问候；退出码 0 / completed；连接配置与回执保存在 .studio-runtime，额度路由和复杂任务未验收 |
| BRIDGE-002 | Codex | 效率配置与故障修复完成，真实多提供方对比待验证 | engine/store/context/contracts/adapters、故障测试、效率配置、调研与入口文档 | 53 项测试；21 原件散列；真实官方接口确认 medium/high 生效；本机测试命令接入；本轮无模型推理 |
| BRIDGE-001 | Codex | 通用内核完成，客户端扩展待联调 | tools/studio_runtime/、tools/bridge.py、tests/、docs/、examples/，入口文档与校验器 | 41 项测试；21 原件散列；2 离线流程；真实 Codex 报告→校验→主脑验收通过；详见 docs/VERIFICATION.md |

2026-10-13 Owner 已授权通用自动协作升级：Opus 优先主脑、Codex 主动桥接及候补主脑。
分工：studio_adapters 独占 adapters.py 与 test_adapters.py；Codex 主进程负责其余实现；架构复核只读。
第三方 vendor 与 archive 原件保留；运行数据、账户、项目私人资料不进入源码。

当前状态：本地 feat/general-agent-bridge，未推送或打包。2026-10-14 Owner 要求优先提高实际工作效率，采用现成工具。DeepSeek 官方 headless 已完成真实消息调用，Opus CLI 仍需登录；DeepSeek 自动余额路由与复杂任务未验收。后续按 production/CODEX_TO_OPUS.md 继续。

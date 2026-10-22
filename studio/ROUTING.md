# 职责与路由
Creative Owner 决定目标与最终取舍。Claude Opus 优先担任主脑，负责计划、分工和验收；能力和额度不足时按配置由 Codex 接替。
Codex 可以作为主动桥接操作员，唤起已接通的成员、传递任务、收取成果和运行检查，也可以承担具体实现。适用编程、研究、资料整理、写作等工作。
人工模式：任务写入 production/OPUS_TO_CODEX.md，回报写入 production/CODEX_TO_OPUS.md，进度写入 production/BOARD.md。
自动模式：显式运行 tools/bridge.py，任务、证据和交接保存在同一个 .studio-runtime 状态目录。配置与协议见 docs/BRIDGE_GUIDE.md。自动派发的成员不再启动其他协调器。
当前用户指令优先。历史四色路由保存在 archive/legacy，仅作早期设计参考。
安装和状态查询不会启动模型；运行桥接器后，已授权队列中的后续派工无需逐次手动唤起。原派工脚本仍可独立使用。

2026-10-14：主脑是按阶段临时调用的角色，不是必须常驻的聊天。规划与验收使用独立原生会话；不同角色可以选择不同成员。当前效率示例中 Opus 优先规划、Codex high 优先验收、Codex medium 优先执行代码工作，实际仍受客户端就绪与真实额度约束。这是可调整的初始策略，不是性能排名。

`routing_rules` 按列表顺序匹配 role 与 capabilities（规则能力须是任务能力的子集），第一条匹配规则的 order 是完整候选名单，优先于模型的 agent 提示；没有匹配规则才用旧 lead_order/worker_order。匹配规则不会绕过能力、禁用、繁忙、额度或冷却检查，不自动追加未列出的成员。更具体的组合能力规则应放前面。

DeepSeek 的实际咨询进入 `bridge.py consult` 和共享账本，可被新 Codex 主动调用；尚未验证自动余额及强制只读隔离，因此没有加入无人值守 worker_order。`answered` 仅表示答复已收到，最终质量由操作员或后续验收判断。未来自适应选人方案与当前实现边界见 docs/WORKFLOW_INTEGRATION.md。

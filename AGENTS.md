> 工作室边界（2026-10-22，v0.2.0）：本仓库是唯一权威工作室，规则见 BOUNDARY.md。旧快照已冻结；其他项目只通过 tools/bridge.py / TeamHub CLI / 工作流 CLI / consult 调用，不复制实现。

# Codex 工作入口
每轮用户任务交付前，执行 docs/WORKFLOW_REVIEW.md：记录真实质量、耗时、用量、协作收益/损耗与改进建议，归档到已授权私人仓库 Luok1xi/opus-codex-studio。无可比基线不报提效百分比；不上传原始会话或凭据。收尾本身不递归生成新轮次。
新会话发现入口：skills/ai-studio/SKILL.md；本机已通过 tools/install_codex_skill.py 安装全局技能和简短 AGENTS 指针。工作流集成、按能力选人和下一步效率方案见 docs/WORKFLOW_INTEGRATION.md。
先读 STUDIO.md、PROJECT_CONTEXT.md、production/BOARD.md 和 production/OPUS_TO_CODEX.md。
按用户或 Opus 分配的具体范围完成工作。领取任务，读取最新文件，避免覆盖并发修改。
完成后将结论、文件、验证证据和待决定事项写入 production/CODEX_TO_OPUS.md。
项目的实时授权与规则优先于历史模板。发布与上传按用户授权执行。

通用自动协作：Codex 可作为桥接操作员和候补主脑，使用 tools/bridge.py 的显式入口；先读 docs/BRIDGE_GUIDE.md。
自动派发的成员只处理当前任务，不启动其他 AI、不另起协调器。不要把 CLI 接入描述为已控制某个现有桌面聊天。

桥接操作员主动调用 DeepSeek：优先 tools/bridge.py consult --workspace 任务目录 --prompt-file 请求文件 --key 唯一任务标识，自动保存共享回执；tools/deepseek_task.py 仍可单独使用。本机连接配置在 .studio-runtime/deepseek-connection.json。入口、会话 ID 与边界见 docs/DEEPSEEK.md；不要再次将未注册 MCP 误判为无法通过官方 CLI 调用。此入口适用于桥接操作员，不授权被派发成员自行启动其他 AI。

<!-- teamhub-shared-data -->
## Shared project data (owner policy, 2026-10-18)
Read docs/TEAMHUB.md. The local catalog is configured in .studio-runtime/teamhub.json; use tools/teamdb.py. Each project MUST have a separate database file. Choose its code with projects, then read context --project CODE --category CATEGORY and inbox --project CODE --agent YOUR_ROLE. Fetch complete cited records with get before deciding.
Use database handoff bodies, tasks, revisions and recipient acknowledgements for current coordination; production handoff files remain historical evidence and artifact links. Do not ask the owner to relay routine file contents. Do not acknowledge for another AI.
Default division: dsh collects/deduplicates/classifies sources and evidence; codex implements/tests/integrates and maintains data; opus designs/independently reviews/accepts. Current owner assignments override these defaults. One writer owns each task's scope; another AI reviews without overwriting it. Role labels are not authentication.
Store only relevant evidence, conclusions and artifact references, never credentials or hidden reasoning. Never edit the archived combined database or upload live databases, exports or backups. All writes use actor, stable key and (for updates) expected revision. Do not silently create an empty database on a missing path.
<!-- /teamhub-shared-data -->

<!-- workflow-database-records -->
Workflow work reports, efficiency analyses, evidence and improvement history belong in the separate WORKFLOW-STUDIO TeamHub project. Read docs/WORKFLOW_DATABASE.md. Store full report JSON using tools/workflow_db.py or tools/workflow_review.py --record-db; retain true author, submitting agent, round, source project and provenance. Corrections append versions; suggestions append status history. Missing peer reports stay missing. Consult prior evidence before workflow updates. Private GitHub remains a sanitized archive; do not upload databases. A successful database_receipt is required; permission-blocked writes remain pending. This is an explicit end-of-round procedure, not a background watcher.
<!-- /workflow-database-records -->

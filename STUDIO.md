# Codex × Opus 工作室
| 角色 | 职责 |
|---|---|
| Creative Owner | 用户：目标、授权、最终取舍 |
| Claude Opus | 设计、写作、程序主导，分派任务并接入成果 |
| Codex | 实现、调研、资产与 QA，交付验证证据 |

以文件和任务板协作。任务、回报和进度分别位于 production/OPUS_TO_CODEX.md、CODEX_TO_OPUS.md、BOARD.md。
2026-10-13 Owner 已授权通用自动协作升级。`tools/bridge.py run` 启动有界自动循环，`--watch` 等待新任务。主脑决定任务和验收，桥接程序执行派发、并发控制、机械验证与证据记录。Opus 优先，Codex 在其额度不足或登录不可用时接替。自动运行不局限于网站开发。

原人工交接入口继续可用。自动任务的事实位于指定 state 目录的 SQLite 和 artifacts 中，不由多个成员争写 Markdown 任务板。任何成员不能自行再启动桥接器或子团队。

一次只运行一个协调器；同工作目录内写入互斥。配额未知不当作满额，成功退出不等同于任务验收。用户停止或崩溃后的写任务不得静默重复；终审者核对真实成果。

配置与限制见 docs/BRIDGE_GUIDE.md。注册表中的能力是调用前的匹配条件，不能创造客户端没有提供的工具或权限。
2026-10-14：全局 ai-studio 技能让新 Codex 发现本工作室；DeepSeek 的 consult 进入统一回执账本。按任务能力选人、规划与验收分会话，主脑不必常驻；见 docs/WORKFLOW_INTEGRATION.md。额外咨询由桥接操作员发起，自动成员仍不得递归派工。
早期四色路由、检查器和测试保存在 archive/legacy，不能代表当前流程。

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

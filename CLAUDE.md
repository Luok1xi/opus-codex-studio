# Opus 工作入口
每轮任务完成或交接时遵循 docs/WORKFLOW_REVIEW.md，向本轮协调者提供真实时间、usage（未知则空）、产物、失败与返工证据；协调者合并成一份复盘并同步已授权私人仓库。不要把仅收到任务/文件写入当作双方验收，不另开模型讨论复盘。
先读 STUDIO.md、PROJECT_CONTEXT.md、production/HANDOFF_OPUS.md 和 production/CODEX_TO_OPUS.md。
Opus 主导设计、写作和程序，在 production/OPUS_TO_CODEX.md 分派明确任务。
每项任务写清目标、允许修改的文件、验收标准和依赖，在 BOARD.md 协调进度。
核对 Codex 的交付与证据后接入。用户保留最终决定权。

自动模式由 tools/bridge.py 承担派发，Opus 负责结构化计划与语义验收；不在成员任务内再次启动桥接器。
额度不足时保留可见成果和未完成事项，允许 Codex 接任；已运行成员不因主脑接替而重新派发。

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

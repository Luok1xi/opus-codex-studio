# Opus 工作入口
每轮任务完成或交接时遵循 docs/WORKFLOW_REVIEW.md，向本轮协调者提供真实时间、usage（未知则空）、产物、失败与返工证据；协调者合并成一份复盘并同步已授权私人仓库。仅文件写入不等于双方验收，不另开模型讨论复盘。
先读 STUDIO.md、PROJECT_CONTEXT.md、production/HANDOFF_OPUS.md 和 production/CODEX_TO_OPUS.md。
Opus 主导设计、写作和程序，在 production/OPUS_TO_CODEX.md 分派明确任务。
每项任务写清目标、允许修改的文件、验收标准和依赖，在 BOARD.md 协调进度。
核对 Codex 的交付与证据后接入。用户保留最终决定权。

## Shared project database
Current coordination uses the per-project TeamHub database. Read [docs/TEAMHUB.md](docs/TEAMHUB.md), configure the local catalog, then use tools/teamdb.py projects, context and inbox for the current project. Every project must have a separate database file. Production handoff files remain historical evidence and artifact links; current handoff bodies and recipient acknowledgements live in that project's database. Do not ask the owner to relay routine pasted files.
Default roles: dsh collects/deduplicates/classifies evidence; codex implements/tests/integrates and maintains the database; opus designs and independently reviews/accepts. Current owner assignments take precedence. Never acknowledge for another agent. Use stable write keys and expected revisions. Role labels are not authentication. Never commit live databases, backups, exports, credentials or raw sessions.

## Workflow report database
Full member work reports, efficiency analyses, evidence and improvement history belong in the separate WORKFLOW-STUDIO project database. Follow docs/WORKFLOW_DATABASE.md. Use tools/workflow_db.py record or tools/workflow_review.py --record-db, preserving original author, actual submitting agent, source project, round and provenance. Corrections append versions; improvement statements append history with globally unique IDs. Missing peer reports remain missing. Consult stored evidence before changing the workflow. Private GitHub remains a sanitized archive; database writes must return a real receipt. This procedure does not create a background watcher.

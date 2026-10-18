# Codex 工作入口
每轮用户任务交付前，执行 docs/WORKFLOW_REVIEW.md：记录真实质量、耗时、用量、协作收益/损耗与改进建议，归档到已授权私人仓库 Luok1xi/opus-codex-studio。无可比基线不报提效百分比；不上传原始会话或凭据。收尾本身不递归生成新轮次。
先读 STUDIO.md、PROJECT_CONTEXT.md、production/BOARD.md 和 production/OPUS_TO_CODEX.md。
按用户或 Opus 分配的具体范围完成工作。领取任务，读取最新文件，避免覆盖并发修改。
完成后将结论、文件、验证证据和待决定事项写入 production/CODEX_TO_OPUS.md。
项目的实时授权与规则优先于历史模板。发布与上传按用户授权执行。

## Shared project database
Current coordination uses the per-project TeamHub database. Read [docs/TEAMHUB.md](docs/TEAMHUB.md), configure the local catalog, then use tools/teamdb.py projects, context and inbox for the current project. Every project must have a separate database file. Production handoff files remain historical evidence and artifact links; current handoff bodies and recipient acknowledgements live in that project's database. Do not ask the owner to relay routine pasted files.
Default roles: dsh collects/deduplicates/classifies evidence; codex implements/tests/integrates and maintains the database; opus designs and independently reviews/accepts. Current owner assignments take precedence. Never acknowledge for another agent. Use stable write keys and expected revisions. Role labels are not authentication. Never commit live databases, backups, exports, credentials or raw sessions.

## Workflow report database
Full member work reports, efficiency analyses, evidence and improvement history belong in the separate WORKFLOW-STUDIO project database. Follow docs/WORKFLOW_DATABASE.md. Use tools/workflow_db.py record or tools/workflow_review.py --record-db, preserving original author, actual submitting agent, source project, round and provenance. Corrections append versions; improvement statements append history with globally unique IDs. Missing peer reports remain missing. Consult stored evidence before changing the workflow. Private GitHub remains a sanitized archive; database writes must return a real receipt. This procedure does not create a background watcher.

# AI 协作工作室 · 边界声明（Project Boundary Declaration）

- 生效日期：2026-10-22
- 权威目录：`C:\Users\user\Documents\Codex\2026-10-11\gai-s\work\opus-codex-studio`
- 版本：见 `VERSION` / `CHANGELOG.md`（当前 **0.2.1**）
- 依据：`.integration-20261022/studio-merge-plan.md`、`studio-management-audit.md`、`management-architecture-v1.md`

## 1. 唯一权威项目

自本声明起，AI 协作工作室（协调器、派单、路由、TeamHub CLI、工作流记录工具、报告、模板、技能、测试、配置）只在本目录维护与更新。

- 旧快照 `C:\Users\user\Documents\Codex\2026-10-06\ni-x20\outputs\codex-opus-studio`：**冻结**（`FROZEN_SNAPSHOT.md`），只读。其主要资产已迁移/归档到本项目（`projects/beikuang*` 迁入；Node autopilot 归档 `archive/node-autopilot-20261013/`；旧独有文档归档 `archive/snapshot-20261013/`）；部分 legacy 脚本（autopilot 包装/旧 dispatch/旧 harness/旧 tests）**仅保留在冻结快照**，权威替代实现见第 3 节，不在本项目复活旧脚本。
- GitHub `origin`（`Luok1xi/opus-codex-studio`）是**发布用脱敏归档线**，不是第二条开发线：开发只在本目录进行；需要发布时由这里生成脱敏版本再推送（推送策略待 Owner 批准）。其 30 个 10-19 提交已合并进本目录（merge commit 见 `CHANGELOG.md`）。
- 网站 `campus/vendor/opus-codex-studio` 只是 3 份模板的只读快照（`PROVENANCE.json`），不得扩写为运行实现。

## 2. 只通过接口调用（Call, don't copy）

| 接口 | 入口 | 形式 | 调用方 | 说明 |
|---|---|---|---|---|
| 协调器 CLI | `tools/bridge.py` | `doctor/consult/submit/run/status/events/stop`，显式运行 | Owner / Opus / Codex / DSH | 默认不自动调用模型（`automatic_model_calls=false`）；每 key 幂等；不代他人回执 |
| TeamHub CLI | `tools/teamdb.py` | `projects/context/inbox/get/tasks/update` + `--project CODE --actor --key [--expected-revision]` | 所有 AI / 各项目 | 每项目独立 SQLite（数据层在 `F:\TeamHub`，不是代码）；缺失不静默建空库 |
| 工作流入库 | `tools/workflow_db.py record`、`tools/workflow_review.py --record-db` | 显式、可回执 | 各 AI | 权威库 `F:\TeamHub\projects\WORKFLOW-STUDIO\teamhub.db`；GitHub 仅脱敏归档 |
| DSH consult | `tools/deepseek_task.py`（经 `bridge.py consult`） | 一次一调用 | 桥接操作员 | DSH 当前为 consult-only；不自动派工、不重发不确定请求 |
| 人工派单（legacy） | `tools/studio/codex_dispatch.ps1` | DryRun 预览，去掉参数才执行 | Owner | 与 bridge 并存的**手动**入口；不参与自动调度 |
| 项目登记 | `projects/<CODE>/project.local.json` | JSON 文件 | 工作室自身 | 北矿娘代码/接口权威在 `BEIKUANG` 项目，不在本仓库复制 |

**调用约束**：只读优先；写操作必须来自用户明确意图；写库用 actor + 稳定 key + expected revision；不复制代码/数据库/凭据；失败即失败，不自动重试不确定结果。

## 3. 相似/重复功能的唯一实现（归并规则）

| 重复功能 | 唯一实现 | 归档/冻结 |
|---|---|---|
| 自动选人/调度（Node autopilot vs Python bridge/routing） | **Python `tools/studio_runtime/{routing,engine,contracts,store}.py` + `tools/bridge.py`** | Node `tools/autopilot/*.mjs` → `archive/node-autopilot-20261013/`，标注 superseded |
| 派单 | `bridge.py`（AI 协作）；`codex_dispatch.ps1` 仅保留为手动 legacy | 不再新增第二套派单器 |
| TeamHub 实现 | `tools/teamdb.py` + `tools/teamhub_partition.py` | 远端重复实现已核对为同内容；保留本地一份 |
| 工作流记录 | `tools/workflow_db.py` / `tools/workflow_review.py`，权威库在 TeamHub | GitHub 归档与 annex 是派生物，不反向覆盖 |
| DSH 调用 | `tools/deepseek_task.py`（consult） | 不复制 DSH/MCP 实现 |
| 北矿娘 MCP 桥 | 权威在 `C:\Users\user\Documents\ChatGPT\New project\companion\tools\beikuang-harness` | 本仓库旧副本已随旧快照冻结，不复制 |
| 合作入口文档 | `AGENTS.md`（Codex）、`CLAUDE.md`（Opus）、`docs/BUILD_GUIDE` 等 | 旧快照 `AGENTS.md`/`CLAUDE.md` 差异已取舍，见 CHANGELOG |

## 4. 数据与凭据

- 运行时状态：`.studio-runtime/`（`studio.sqlite3`、`deepseek-connection.json`、`bridge.local.json`、`controller.lock`）只在本机，**不入库**。
- TeamHub 项目库：`F:\TeamHub\projects\<CODE>\teamhub.db` 归数据层；本仓库不提交任何 `.db/.sqlite/.sqlite3`、导出、备份、凭据、原始会话。
- 报告：`reports/workflow/` 入库的是脱敏/可公开记录；私有 GitHub `workflow-reviews` 是另一层归档，由命令生成，不手工双写。
- 任何项目不得复制本仓库的 `tools/` 实现；需要能力时调用第 2 节 CLI。

## 5. 更新流程（版本 + 验收 + 回滚）

1. 只在本目录修改；先读本文件 → `MODULES.md` → `CHANGELOG.md`/`VERSION`。
2. 变更分级：patch（内部修复）/ minor（新能力、旧 CLI 保留）/ major（CLI/数据契约破坏，需 Owner 批准 + 通知调用方）。
3. 每次发布必须：`python -m unittest discover -s tests -q` 全通过（基线 97）+ `python tools/studio_check.py` PASS + 更新 `VERSION`/`CHANGELOG.md`/`STATUS.json`。
4. 工作流记录变更：先备份 `F:\TeamHub\projects\WORKFLOW-STUDIO\teamhub.db`，再做迁移；迁移前后逐表行数核对。
5. 回滚：`git reset --hard <tag>` 或还原备份分支；数据回滚用备份库；不删除历史 backup。
6. 远端发布：只从本目录生成脱敏副本再推送；**禁止**把本地完整工作区 force push 覆盖脱敏线（待 Owner 定策略）。

## 6. 冻结 / 归档清单

| 位置 | 状态 |
|---|---|
| `...\2026-10-06\ni-x20\outputs\codex-opus-studio` | 冻结只读（`FROZEN_SNAPSHOT.md`） |
| 本仓库 `archive/node-autopilot-20261013/` | 历史归档（Node autopilot，superseded） |
| 本仓库 `archive/merge-20261022/origin-main-side/` | 合并冲突时 origin/main 侧文件留存（证据） |
| `archive/snapshot-20261013/` | 旧快照独有文档归档 |
| 网站 `campus/vendor/opus-codex-studio` | 只读模板快照 |

## 7. 违规处理

发现其他项目复制本仓库实现/数据、或在旧快照上继续修改：
1. 立即冻结该副本并标记；
2. 以本仓库为准回滚/替换，删除复制数据（不合并两边库）；
3. 在 `CHANGELOG.md` 记录；
4. 通知 Owner；涉及凭据时轮换。

## 8. 签署

Owner 签署：____________　日期：____________
监督：任何 AI/子代理在本项目开工前必须先读本文件；违反第 2/4/7 节的操作一律停止并上报。

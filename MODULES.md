# 模块与接口（MODULES）

版本：0.2.0（2026-10-22 合并）｜权威声明见 `BOUNDARY.md`

## 1. 模块分层

| 层 | 路径 | 职责 | 对外接口 |
|---|---|---|---|
| 协调器入口 | `tools/bridge.py` | doctor/consult/submit/run/status/events/stop；显式运行、幂等 key、超时 1-900s | CLI（JSON 输出） |
| 运行时核心 | `tools/studio_runtime/`（`contracts`、`engine`、`routing`、`store`、`adapters`、`context`、`consult`、`teamhub`） | 任务契约、能力/额度路由、SQLite 状态、失败恢复 | 被 bridge 调用 |
| 模型适配 | `tools/studio_runtime/adapters.py`、`tools/deepseek_task.py` | Codex/Claude 适配、DSH consult（一次一调用） | bridge 子命令 |
| 手动派单（legacy） | `tools/studio/codex_dispatch.ps1` | 人工 DryRun 派工；不参与自动调度 | 人工 PowerShell |
| TeamHub | `tools/teamdb.py`、`tools/teamhub_partition.py`；数据层 `F:\TeamHub` | 每项目独立库、actor/key/revision 幂等、分区迁移 | CLI |
| 工作流记录 | `tools/workflow_db.py`、`tools/workflow_review.py`；权威库 `F:\TeamHub\projects\WORKFLOW-STUDIO\teamhub.db` | 报告/复盘/建议/回执入库；GitHub 仅脱敏归档 | CLI |
| 报告与索引 | `reports/workflow/`（入库）、外部 `Luok1xi/workflow-reviews`（归档+索引） | 每轮报告、IMPROVEMENTS、README | 文件/外部命令 |
| 项目登记/工作区 | `projects/beikuang/`（登记/交接/board）、`projects/beikuang-chat/`（Harness 聊天工作区） | 项目接入；北矿娘代码/接口权威在 BEIKUANG 项目 | JSON/Markdown |
| 归档/冻结 | `archive/node-autopilot-20261013/`、`archive/snapshot-20261013/`、`archive/merge-20261022/` | 历史与合并证据；不参与运行 | 只读 |
| 模板/技能/测试 | `templates/`、`skills/ai-studio/`、`schemas/`、`tests/`（97 项）、`tools/studio_check.py` | 契约模板、全局技能、schema、验收 | `python -m unittest discover -s tests -q` |
| 第三方/vendor | `studio/vendor/`、`studio/*.lock.json` | 锁定哈希的第三方原件 | `studio_check.py` 校验 |

## 2. 接口契约（摘要）

| 接口 | 提供方 | 调用方 | 鉴权/限制 | 失败语义 |
|---|---|---|---|---|
| `bridge.py` | 本仓库 | Owner/Opus/Codex/DSH | 本机；显式运行；`automatic_model_calls=false`；key 幂等 | JSON 错误；保留 checkpoint；不自动重试不确定 POST |
| `teamdb.py` | 本仓库 | 各 AI/项目 | 本机文件权限；`--actor/--key/--expected-revision` | 缺库/缺目录明确失败，不建空库 |
| `workflow_db.py record` | 本仓库 | 各 AI | 显式；回执成功才作数 | 失败保留 pending；不代编 |
| `deepseek_task.py` | 本仓库 | 桥接操作员 | consult-only；一次一 key | 无 usage 回传；结果不明不重发 |
| TeamHub 数据 | `F:\TeamHub` | 各项目 | 每项目独立库；只读查询 authorizer | 不跨库拼接 |

## 3. 版本与更新

- 版本载体：`VERSION`、`CHANGELOG.md`、`STATUS.json`、git tag。
- 发布检查：`python -m unittest discover -s tests -q`（基线 97）→ `python tools/studio_check.py` PASS → 更新版本三件套 → tag。
- 破坏性 CLI/数据契约 = major；调用方（DSH、TeamHub 使用者、网站文档）需通知与迁移期。
- 不复制本模块到其他项目；其他项目通过第 2 节调用。

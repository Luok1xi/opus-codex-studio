# 变更记录（CHANGELOG）

## 0.2.1 — 2026-10-22 — 合并后修正 + 工作流索引工具 + 行尾归一

- 冲突口径修正：100 个两边改过文件中 51 个逐字节相同、49 个实际冲突；裁决 = 45 取本地（43 个仅 CRLF 等价 + `.gitignore` + `CLAUDE.md`）+ 1 手工合并（`AGENTS.md`，保留本地完整版并加边界横幅）+ 3 取 origin/main（`reports/workflow/IMPROVEMENTS.md`、`reports/workflow/README.md`、`ningxia-integration/provenance-clarification.md`）；远端侧 49 份已归档。
- 迁移残留修正：`projects/beikuang-chat/AGENTS.md`、`projects/beikuang/INTEGRATION-REPORT.md` 内 3 处旧快照路径改指本仓库新路径；`STATUS.json` 的 `git.head` 修正为实际 HEAD。
- 新增 `tools/review_index.py`（与 `Luok1xi/workflow-reviews` 仓库 `tools/review_index.py` 同 sha256 `B18365F6…` 引入；工作流报告索引的唯一实现，来源为 TeamHub annex `ready-to-commit/tools/` 与 workflow-reviews 仓库同一文件）。
- 行尾归一：按 `.gitattributes`（`* text=auto`、`*.ps1 eol=crlf`、`*.py eol=lf`、vendor/archive `-text`）执行 `git add --renormalize .`，消除未来与 CRLF 历史合并产生的“假冲突”；远端历史归一需 Owner 批准（改写历史）后再做。
- 验证：`python -m unittest discover -s tests -q` 97 OK；`python tools/studio_check.py` PASS。

## 0.2.0 — 2026-10-22 — 合并为唯一权威工作室

### 合并

- **origin/main 脱敏归档线（30 个提交，至 2026-10-19 `0378b91`）并入本地**：merge commit `e50e1d3`；两边共改 100 个文件（51 个逐字节相同、49 个实际冲突），裁决：
  - 45 取本地（43 个仅 CRLF/LF 等价 + `.gitignore` + `CLAUDE.md` 本地实质差异）；
  - 1 手工合并（`AGENTS.md`：保留本地完整版并加边界横幅）；
  - 3 取 origin/main 实质差异（`reports/workflow/IMPROVEMENTS.md`、`reports/workflow/README.md`、`.../ningxia-integration/provenance-clarification.md`）；
  - origin/main 侧 49 份冲突文件全文留档于 `archive/merge-20261022/origin-main-side/`。
- **本地工作快照**（commit `b23cdcb`，合并前 HEAD `707284e`）：Python bridge/`studio_runtime`（contracts/engine/routing/store/adapters/context/consult/teamhub）、`deepseek_task.py`、TeamHub CLI（`teamdb.py`/`teamhub_partition.py`）、工作流入库/复盘（`workflow_db.py`/`workflow_review.py`）、schemas/templates/skills/tests/文档（10-13~10-21 工作）全部入库。

### 从旧快照迁移（`ni-x20\outputs\codex-opus-studio`，已冻结）

- `projects/beikuang/` → 本项目 `projects/beikuang/`（登记、交接、board、runtime 连接元数据）；
- `projects/beikuang-chat/` → 本项目 `projects/beikuang-chat/`（Harness 聊天工作区；旧路径冻结，见 old snapshot `FROZEN_SNAPSHOT.md`）；
- Node autopilot（`tools/autopilot/*.mjs` + 当时 `studio.config.json`）→ `archive/node-autopilot-20261013/`，标注 **superseded**（由 Python bridge/routing 取代）；
- 旧快照独有文档（SOURCE_MANIFEST/VERIFICATION/PROJECTS/PROJECT_CONTEXT 等）→ `archive/snapshot-20261013/`。

### 新增治理文件

- `BOUNDARY.md`：唯一权威、接口清单、相似功能唯一实现（Node autopilot→Python bridge 等）、冻结/归档、数据归属、更新/回滚/违规处理。
- `VERSION`（0.2.0）、`STATUS.json`、`MODULES.md`；`AGENTS.md` 顶部加入边界入口。
- `studio.config.json` 增加 `boundary` 与 `projects` 登记；`projects/beikuang/project.local.json` 路径改指权威北矿娘项目与本仓库新位置。

### 验证

- `python -m unittest discover -s tests -q`：**97 passed**；
- `python tools/studio_check.py`：**PASS**（vendor 21 份哈希一致）；
- 合并后工作区 clean；未启动 bridge/autopilot/模型。

### 未做 / 待 Owner

- 向 GitHub 推送（远端为脱敏线，推送策略待批准；禁止 force push 本地完整工作区）。
- DSH 的 `projects/beikuang-chat` 工作区切换到本项目新路径（旧路径仍只读可用）。
- StudioOps 注册表同步（已更新 `WORKFLOW-STUDIO` 版本与路径说明）。
- 旧快照是否在 P3 删除；网站 `campus/vendor` 模板是否保留。

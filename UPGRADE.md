# UPGRADE — 给其他 AI 的升级入口

本仓库是 **AI 协作工作室的唯一权威项目**。升级/接手前按顺序读：

1. `BOUNDARY.md` — 边界、接口、重复功能唯一实现、冻结清单（最高优先级）
2. `MODULES.md` — 模块与接口契约
3. `CHANGELOG.md` + `VERSION` — 当前版本与最近变更
4. `STATUS.json` — 机器可读状态（git、接口、数据、待办）

## 升级步骤（标准）

```powershell
# 1. 先备份/提交自己的未提交工作，再拉取（只允许 fast-forward）
git pull --ff-only origin main

# 2. 必跑检查（不得跳过）
python -m unittest discover -s tests -q      # 基线 97 项
python tools/studio_check.py                 # 必须 PASS

# 3. 只在本目录开发；读 BOUNDARY 第 2/4/7 节后动手
```

## 规则（违反即回滚）

- 只在本仓库开发；不得复制 `tools/` 实现到网站、北矿娘、TeamHub、小车或其他项目，也不得在旧快照（`ni-x20\...`）上继续修改。
- 需要工作室能力 → 调用 `tools/bridge.py`（CLI）、`tools/teamdb.py`（TeamHub CLI）、`tools/workflow_db.py`/`workflow_review.py`（工作流记录）、`deepseek_task.py`（consult）；不复制实现。
- 不提交 `.studio-runtime/`、`bridge.local.json`、任何 `.db/.sqlite`、密钥、原始会话。
- 版本：patch=修复；minor=新能力（旧接口保留）；major=破坏 CLI/数据契约，需 Owner 批准并通知调用方。
- 发布 = 本仓库 `main` + tag `vX.Y.Z` 推送到 `origin`；不得把旧快照或本地副本当第二条发布线。

## 当前发布

- 远端：`https://github.com/Luok1xi/opus-codex-studio`，分支 `main`
- 版本：见 `VERSION`；发布 tag 见 `git tag -l`
- 历史/回滚点：`pre-consolidation-20261022`、`local-work-20261022`、`v0.2.0`、`v0.2.1`、`v0.2.2`

# SUPERSEDED — Node autopilot（旧快照，2026-10-13）

本目录是从旧工作室快照 `C:\Users\user\Documents\Codex\2026-10-06\ni-x20\outputs\codex-opus-studio` 迁移来的 **Node autopilot 原型**，自 2026-10-22 起 **已被取代，不再维护、不再运行**。

- 取代者：本仓库 `tools/bridge.py` + `tools/studio_runtime/{routing,engine,contracts,store,adapters}.py`（Python 协调器；显式运行、额度闸门、失败升级、幂等 key）。
- 旧配置快照：`studio.config.snapshot-20261013.json`（含当时的 autopilot 段，仅作历史参考，不要加载）。
- 原因：同一“自动选人/调度”能力存在两套实现会互相打架；按 `BOUNDARY.md` 第 3 节，只保留 Python bridge/routing 一套。
- 保留价值：历史行为参考、旧快照回滚证据。**禁止**把它们接回运行链路或在其他项目复制。

如需恢复类似能力：在本仓库 `tools/studio_runtime/` 内实现，补测试与文档，按 minor 版本发布，不要直接复活本目录脚本。

# 职责与路由
Creative Owner 决定目标与最终取舍。Claude Opus 主导设计、写作和程序，并分派具体任务。
Codex 按任务范围完成实现、调研、美术和验证，提交证据。
任务写入 production/OPUS_TO_CODEX.md，回报写入 production/CODEX_TO_OPUS.md，进度写入 production/BOARD.md。
当前用户指令优先。历史四色路由保存在 archive/legacy，仅作早期设计参考。
工具不会在后台自动启动模型。需要执行 Codex 时，由操作者明确调用派工脚本。

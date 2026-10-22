# 北矿娘项目登记

- 项目：北矿娘「小煤渣」，原 Miku / 墨玉的连续身份。
- 原始源码：C:\Users\user\Documents\ChatGPT\New project\companion
- 技术：Node.js 24，本地网页与 SQLite；原项目 ARCHITECTURE.md 是现有模块接口的依据。
- 本地服务：http://127.0.0.1:17839
- 原始角色卡：vendor/airi/moyu-card.json（在原始源码目录中）。
- 开发分工：用户最终决定，Opus 主导，Codex 和 DeepSeek 按明确派单实现与验证。
- 专属派单：本目录 production/OPUS_TO_CODEX.md、OPUS_TO_DEEPSEEK.md。
- 专属回报：本目录 production/CODEX_TO_OPUS.md、DEEPSEEK_TO_OPUS.md。
- 专属任务板：本目录 production/BOARD.md。
- 日常模型、记忆、排程、预算、去重和主动提醒：继续由原北矿娘程序管理。
- Harness 连接工具：工作室 tools/beikuang-harness/server.mjs，通过 MCP stdio 与原本地 HTTP 服务交互。
- 聊天会话：在 Harness 选择工作室 projects/beikuang-chat，先检查工具可用，再读取当前角色卡。

## 开发约定
先读原源码 ARCHITECTURE.md 和当前模块的接口/测试。禁止复制或重建原数据库来替代现有记忆；不把 data、.env、账号缓存、真实聊天或整个 node_modules 纳入工作室包。
不改原账号、平台收发或主动提醒默认状态。框架接入不要求改写已有业务模块。
测试使用内存库或专用临时目录，不向真实私聊或群聊发送测试消息。涉及模型的真实聊天验证要与离线测试分别报告。

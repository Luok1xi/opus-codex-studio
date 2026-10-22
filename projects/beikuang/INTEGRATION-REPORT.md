北矿娘 × 工作室 × Harness 接入报告 · 2026-10-10

一、实际完成
- 北矿娘已登记为通用工作室正式项目。原源码 C:\Users\user\Documents\ChatGPT\New project\companion 已新增 AGENTS.md、CLAUDE.md、STUDIO-INTEGRATION.md，并逐文件校验复制散列。
- 专属派单、回报和任务板位于工作室 projects/beikuang/production。用户最终决定，Opus 主导，Codex / DeepSeek 执行。
- 聊天工作区 C:\Users\user\Documents\Codex\2026-10-11\gai-s\work\opus-codex-studio\projects\beikuang-chat 已提供专属入口，按需读原角色卡，使用原程序的记忆、任务、关系与聊天。
- 独立 MCP 连接工具已注册到 Harness desktop profile，原模型、账号和其他插件设置保留。
- Harness 已热加载并真实初始化 MCP：2026-10-10 11:57:17.936（北京时间），client=dsh-mcp-client，桥接 PID=34612，父进程 PID=59996，已核对父进程为 DeepSeek Harness.exe。
- 四个真实 MCP 工具：beikuang_status、beikuang_identity、beikuang_context、beikuang_chat。

二、验证
- 原北矿娘 /health 实际返回 app=miku-local、ready=true。
- 官方 MCP 客户端完成真实 stdio 握手，发现四工具；原服务状态与有限实时关系上下文读取成功；当前角色为小煤渣、identityVersion=2、原模型已配置。
- 连接工具 7 项测试通过：回环地址限定、SSE 完成/错误、有限上下文、原 Service/Store 聊天及去重、403 认证刷新、不确定 POST 不自动重发、MCP 握手及工具调用。
- 聊天与状态修改的测试运行原北矿娘程序，使用内存数据库、注入离线模型、background=false；没有修改真实任务或记忆。
- 工作室 12 项测试通过，21 份第三方原件散列一致。两部分合计 19 项。

三、本轮边界
- 未向真实北矿娘发送测试聊天、未调用真实付费模型；自然对话效果和用户主动发消息后的真实回报尚未验收。
- 原 SQLite、关系和历史继续由原服务持有，连接器没有复制或重建数据库；原业务源码没有改写，仅新增开发入口文档。
- 未新增主动消息发送器，未向 QQ / 微信 / 飞书发测试消息，未验证本轮手机送达。
- Harness 自己的模型用量与原北矿娘聊天模型账本分别计算；本轮验证没有产生模型调用。
- 未上传、发布或修改系统代理。临时下载辅助仅为连接器依赖安装服务，结束后停止。
- 初次选择聊天工作区仍需用户在 Harness 中完成；原工作室接入自检 DS-ONBOARD-001 已收到 DeepSeek 11:38 的真实回报。

四、现在怎么用
在 Harness 新建会话并选择 C:\Users\user\Documents\Codex\2026-10-11\gai-s\work\opus-codex-studio\projects\beikuang-chat。
首次发送：先检查北矿娘连接，只调用状态、身份和关系读取工具，不发送聊天、不修改数据；告诉我实际连通结果。
检查通过后正常与她聊天。开发程序时，选择原源码 C:\Users\user\Documents\ChatGPT\New project\companion 并按专属任务单工作。

# Antigravity Opus 工作室入口

本机已安装官方 Antigravity CLI 1.4.7；桌面版独立复核为2.26.0。它们属于 Antigravity 入口，与 Claude Code 分开。

## 通用共享入口

Antigravity 的全局规则 `~/.gemini/config/rules/opus-codex-studio.md` 已指向现有 ai-studio 和 TeamHub。用户在任意项目明确要求工作室协作时，代理按项目目录选库，读取上下文与自己的收件箱；普通无关任务不启动协作。

Antigravity 的 Opus 使用标签 `opus-antigravity`；Claude Code 的现有标签仍为 `opus`。标签不是模型认证。只有实际客户端选择和真实答复才能证明调用了哪一个模型。每个接收者只确认自己的消息。

## 官方命令入口

已安装路径：`%LOCALAPPDATA%/agy/bin/agy.exe`。官方安装器已加入用户 PATH，新开的终端可使用 `agy`；已有终端可直接使用完整路径。

在需要工作的目录打开 PowerShell：

```powershell
& "$env:LOCALAPPDATA/agy/bin/agy.exe" models
& "$env:LOCALAPPDATA/agy/bin/agy.exe" --model claude-opus-5-5-medium
```

模型标识来自本机2026-10-24实际返回的列表。以后客户端或模型升级时先重新查询，不静默改用其他模型。登录、首次权限和模型可用性由官方客户端处理，不能从列表成功推断推理一定可用。

初次启动后可说：进入工作室，按当前项目读取TeamHub收件箱。具体任务正文直接读取项目数据库，无须人工搬运。

## 当前验证边界

2026-10-24已核验帮助、版本、模型列表，以及真实 Opus 读取两份获批文档并写回本地复核。初次默认模式拒绝写文件，续接同一会话使用官方 `--mode accept-edits` 后写回成功；没有启用跳过权限。最初 `SUCCESS` 为空正文，因此单看退出码不够。

记录位于接入任务的 `outputs/antigravity-studio/opus-{check,followup,write,teamhub}-receipt.json`。接入交接 `AG-STUDIO-ONBOARD-20261024` 已在 CRAZY-CIRCUIT 收到 `opus-antigravity` 的真实记录回执；其界面模型 High 是成员陈述，CLI 明确选择的是 Medium。两条入口的证据不能混写。

后续CLI调用遇到服务端 `RESOURCE_EXHAUSTED`，当时提示约4小时9分恢复，已停止追加调用。额度恢复时间是当时观察值，不保证未来仍适用；不得轮换入口绕过限制，也不能把这次限额说成登录失效。

接收者ack与本地文件已核对，正式 `AG-STUDIO-RECEIPT` handoff尚未生成；完整数据库交接状态仍为待验证。不要把已安装、可调用或一次读写成功称作稳定无人值守协作。

共享数据入口、一次真实咨询、自动队列派发是不同验收阶段。现有自动调度器尚未增加 Antigravity 适配器：真实额度、只读隔离、取消与失败恢复未完成验证。不要将其配置为已可用的自动后备成员，也不要复制桌面凭据或启用跳过所有权限的开关。

官方说明：[规则](https://antigravity.google/docs/rules)、[CLI非交互模式](https://antigravity.google/docs/cli/headless)。

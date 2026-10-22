# 主动调用 DeepSeek

2026-10-14 已用官方 `@deepseek-ai/dsh@0.2.0-rc.2` 的 headless 入口完成真实请求，退出码 0、turn_end 为 completed，最终回复：

> 你好！我是 DeepSeek，很高兴和你一起协作。

本机已经安装独立 CLI，连接文件为被 Git 忽略的 `.studio-runtime/deepseek-connection.json`。官方运行时自行读取 Harness 共享账户状态；连接文件只有命令路径与工作目录，不保存账户密钥。CLI 初始化了 `$DSH_HOME/profiles/headless`，桌面 profile 未改。

## 给桥接操作员

统一工作流入口（推荐，自动保存答复与会话）：

```text
python tools/bridge.py consult --workspace /absolute/task/workspace --prompt-file /absolute/request.txt --key task-unique-id
python tools/bridge.py status 返回的任务ID
```

在工作室目录执行，或在其他目录用 `--state` 指定同一个工作室状态目录。连接默认按脚本位置定位；不是按调用者的当前目录猜测。文本咨询可用空工作目录，并要求不使用工具；这不是额外的权限隔离。要继续原生会话，加 `--session`，保持工作目录相同，使用新的任务 key。

结果 `answered` 表示收到完整答复，`results.consult.artifact.path` 是答复文件，`session_id` 用于续接。相同 key 和相同请求返回原记录，不再次付费调用；同 key 不同请求报错。失败、异常或中途崩溃保留账本并要求核对，不转交普通任务队列自动重做。不将咨询答复标成已独立验收。

把当前获授权的请求写进 UTF-8 文本，然后在工作室根目录执行：

```text
python tools/deepseek_task.py --prompt-file request.txt
```

输出包含 status、session_id、text；只有进程成功退出、最终回合完成且有非空答复才报告 succeeded。命令有默认 120 秒上限，并复用现有进程树回收；不自动重试。只回传最终答复，不回传内部思考事件。

```text
python tools/deepseek_task.py --prompt-file followup.txt --session 上次返回的会话ID
python tools/deepseek_task.py --prompt-file task.txt --workspace C:\path\to\project
```

续接必须保留相同工作目录并满足 Harness 自身的会话规则。当前验证会话为 `session-445aed77-c95c-4869-bf84-ea16de36b27c`，工作目录在 `.studio-runtime/deepseek-greeting`；回执在 `.studio-runtime/deepseek-greeting-result.json`。正式入口的解析器和命令转发有离线测试；本次真实调用验证了新会话，尚未再次调用模型验证续接。

## 其他机器的安装

需要官方支持的 Node 版本。用独立目录安装固定版本，不需要覆盖桌面版或改全局 PATH：

```text
npm install --prefix /path/to/deepseek-runtime --save-exact @deepseek-ai/dsh@0.2.0-rc.2
```

本机 npm 的旧缓存有复制文件错误，实际安装使用工作区独立缓存成功。安装程序报告部分可选/原生依赖脚本待批准；本次问候没有依赖它们，没有批量放行。以后使用终端等工具需要按实际需求单独验证。

本地连接文件结构（替换为真实绝对路径）：

```json
{
  "command": ["/path/to/node", "/path/to/deepseek-runtime/node_modules/@deepseek-ai/dsh/lib/bin.js"],
  "workspace": "/path/to/authorized-workspace"
}
```

## 已证实的边界

- 这是通过官方命令行创建的持久会话，不是接管用户已打开的桌面聊天。当前对话无需新增 MCP 才能由 Codex 调用该入口。
- 真实问候已通过；复杂开发、工具权限、自动余额查询及续接尚未完成真实验收。`bridge.py` 的 DeepSeek 自动调度仍未启用，避免把一个问候测试当成全部能力已通过。
- 普通 headless 继承 Harness 自身工具与权限配置，这个薄入口不额外提供只读隔离。派发写任务须有对应授权；失败后先核对结果，不盲目重复。
- 桌面 HTTP 服务返回 401 是浏览器会话认证要求，不能据此断言 DeepSeek 整体不可调用。不要复制 cookie、导出认证密钥或改认证机制来接管桌面。

官方依据：[命令行入口](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md)、[headless 合同](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/bundle/headless/README.md)、[桌面与 CLI 的共享数据边界](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/desktop/README.md#bundled-command-runtime)。文档 master 可变化，本机验收版本以固定安装版本为准。

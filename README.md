# 通用 AI 协作工作室

让主脑制定计划、成员完成任务、桥接程序处理唤起、交接和证据。用于编程、资料整理、研究、文档写作等本地工作；内核没有网站、游戏、Git 或 npm 的运行依赖。

默认 Opus 优先主脑，Codex 承担桥接操作和候补主脑。额度不足时在同一任务中交接，已完成步骤保留。原人工任务板、便携 Codex 派工脚本与第三方原件仍可使用。

当前是经过本地验证的实验性协作层。目标是提高实际工作效率；已有官方客户端和测试工具直接使用，框架只补交接缺口。选型与已知局限见 [自动化调研与采用决定](docs/AUTOMATION_RESEARCH.md)。

## 从这里开始

Python 3.11+，运行内核只用标准库。先跑不调用 AI 的两个完整示例：

```text
python tools/demo_bridge.py
```

示例实际生成并验证代码与资料报告，但成员是明确标注的离线夹具，不代表模型能力或真实账号联调。

真实协作：复制 `bridge.example.json` 为 `bridge.local.json`，在对应官方客户端完成登录。在任务文本文件里写清目标，然后执行：

也可采用 `examples/efficient.bridge.json` 的角色配置：Opus 优先主脑，Codex 执行与候补主脑分别使用 medium/high。为目标项目填入现有测试命令；两种 Codex 角色共用账户额度。

```text
python tools/bridge.py doctor
python tools/bridge.py submit --workspace C:\path\to\project --goal-file goal.txt --key my-task-001
python tools/bridge.py run
```

`run --watch` 保持等待新任务；空闲时不调用模型、不查询额度。`status` 看状态，`events 任务ID --after 游标` 增量取证，`stop` 停止当前桥接器拥有的任务进程。具体配置、自动化边界和接入协议见 [使用指南](docs/BRIDGE_GUIDE.md)。

## 已实现

- 任意本地工作目录；能力匹配与任务依赖，独立只读任务并行，同目录写入互斥。
- Opus → Codex 主脑顺序；真实可获取的额度窗口、额度缓存、过期与未知状态、失败冷却。
- 原生 Codex／Claude 调用；自定义 `command` 接入协议；[DeepSeek 主动消息入口](docs/DEEPSEEK.md) 已收到真实回复，自动额度路由与只读执行仍待验收。
- SQLite 任务与事件；重复提交去重、已完成步骤保留、异常退出不盲目重播写任务。
- 有界自动恢复只读步骤与已核验回执；未知写入结果暂停核对，失败且无修复预算时跳过无效终审。
- 有界交接内容与内容散列成果；机械检查由普通进程执行，主脑负责语义验收和有限修复。
- Windows 隐藏进程、完整自有后代进程清理、调用数／时限／修复次数上限。

## 差异、设计与证据

[源码差异与定位](docs/ARCHITECTURE.md) · [性能与验收](docs/VERIFICATION.md)

新 Codex 自动发现工作室：`python tools/install_codex_skill.py` 安装用户技能和全局短指针，保留既有说明。DeepSeek 的 `bridge.py consult` 已接入统一账本；规划、验收、执行可按能力分别选人。详见 [工作流接入与选人方案](docs/WORKFLOW_INTEGRATION.md)。

```text
python tools/studio_check.py
python -m unittest discover -s tests -v
python tools/benchmark_bridge.py
```

性能基准使用同一模拟任务图对比调度行为，不代表真实模型速度、质量或费用。`downloads/` 中旧 ZIP、`SOURCE_MANIFEST.json` 与根目录旧 `VERIFICATION.json` 属于历史发布快照；当前功能以源码与 `docs/VERIFICATION.md` 为准。

## 原人工入口
1. 以 STUDIO.md 了解分工；在 PROJECT_CONTEXT.md 填写新项目资料。
2. Opus 在 production/OPUS_TO_CODEX.md 写任务；Codex 在 CODEX_TO_OPUS.md 回报；BOARD.md 协调进度。
3. `python tools/studio_check.py` 检查框架和第三方原件散列。
4. `python -m unittest discover -s tests -v` 验证检查器对缺文件、篡改与路径越界的处理。
5. Windows 显式派工：`powershell -File tools/studio/codex_dispatch.ps1 -Task TASK-001 -ProjectRoot C:\path\to\project -DryRun`。预览正确后去掉 `-DryRun`；需本机已安装并登录 Codex CLI。登录由操作者完成。

## 目录
- 根目录：整理后的协作入口和配置。
- production/、templates/：空白交接模板。
- tools/、tests/：便携派工脚本、框架完整性检查和测试。
- studio/vendor/：上游参考模板、许可证与锁定清单。
- archive/legacy/：原始早期工具与模板，按原字节保存。旧工具含游戏路径与过期流程，使用前应读 archive/legacy/README.md。
- SOURCE_MANIFEST.json：原件来源、散列和整理后文件的对应记录。

## 许可与运行边界
只包含工作室框架与工具。实际剧情、美术音频、已填写的个人交接与聊天档案未打包。
自动队列仅在明确执行 `bridge.py run` 后开始；`bridge.py consult` 明确调用一次 DeepSeek。导入、安装、状态查询均不触发推理。不自动充值、上传、发布或合并。账号登录仍在对应客户端完成，运行数据默认保存在被 Git 忽略的 `.studio-runtime/`。
第三方许可见 THIRD_PARTY_NOTICES.md。本仓库未授予其余代码额外开源许可。

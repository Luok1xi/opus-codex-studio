# Codex × Opus 工作室框架与工具
从现有工作室工程整理的独立源码包，包含协作约定、任务与回报模板、原始工具、便携派工脚本和第三方工作流。

## 使用
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

## 范围与验证
只包含工作室框架与工具。实际剧情、美术音频、已填写的个人交接与聊天档案未打包。
框架是文件协作约定；派工脚本只有被明确运行时才启动 Codex。
本次验证覆盖包完整性、Python 检查与测试、PowerShell 语法与派工预览；未启动实际模型任务。
第三方许可见 THIRD_PARTY_NOTICES.md。本仓库未授予其余代码额外开源许可。

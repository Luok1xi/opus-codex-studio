# 手动文件交接

本流程裁剪 CCGS 的模板、证据与交接做法。没有后台模型编排器。

1. 读取一个任务记录。用 `python3 tools/task_route.py GREEN` 等命令查看职责，不执行模型调用。
2. 只打开任务引用的设定、Scene Card 和差异。
3. GREEN 工程：Codex 实现和验证，写短报告。无需 Opus。
4. YELLOW 创作：Lead Writer 起草和自查，无需自动 Codex review；已批准场景的程序录入属于工程工作。
5. ORANGE：Showrunner Scene Card → Lead Writer 一稿 → 一次 review → 一次修订。
6. RED：主题、栞死亡、旁白真相、结尾不得单方面改；最多两轮，之后用户裁决。
7. 把稿件、diff、Scene Report 放进同一仓库分支；不自动请求审稿人、不发消息、不合并主分支。
8. 更新 production/session-state/active.md：完成、剩余、下一步。不要复制整个聊天历史。

上游模板仅参考；上游“每一步都询问”“多层 Agent 委派”不适用于此项目。
本项目的当前用户指令优先于模板。

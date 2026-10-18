# 工作流报告与改进依据

用户于 2026-10-18 确认：三方工作报告、效率分析、工作流更新依据存入共享数据库，以便核对更新。统一目录仍是 `F:/TeamHub/catalog.json`；工作流自身使用独立项目 **WORKFLOW-STUDIO**，数据库为 `F:/TeamHub/projects/WORKFLOW-STUDIO/teamhub.db`。业务项目的源码、采购、赛道等资料继续留在各自项目库。这里只存工作流相关报告、聚合证据及原项目代码。

数据库是日常报告、核对和改进依据入口；私人 GitHub 保存经过脱敏的报告和维护源码。数据库本体、备份、原始会话、推理和凭据不上传。

| 分类 | 内容 |
|---|---|
| 01 成员工作报告 | Codex、Opus、DeepSeek 各自的目标、产出、问题与证据 |
| 02 效率分析与轮次复盘 | 质量、实际耗时/用量、协作和返工成本、基线比较 |
| 03 改进建议与状态历史 | 建议 ID、来源报告、报告者、负责人、状态、下次验收 |
| 04 验证证据 | 随报告存入的脱敏聚合证据 JSON；大产物以路径和校验和引用 |
| 05 归档与协作回执 | 私人仓库回读凭据、真实交接确认、待同步事项 |

## 每轮怎样执行

1. 各成员完成自己负责的部分，按 `templates/workflow-work-report.json` 提交成员报告；未知指标保留 `null`。一个协调者收集实际收到的报告，未收到的注明缺失。
2. 协调者按 `templates/workflow-review.json` 完成效率复盘，通过既有校验器生成 Markdown 并入库。没有匹配质量门槛的同条件基线，不宣称提效。
3. 对照上一版建议和证据，决定提出或采用哪些更新。建议的状态只是报告者的声明，不等于独立验收；需要其他成员确认时，保留待确认状态。
4. 按既有授权上传脱敏报告和必要源码，实际回读后登记归档回执。报告/归档自身不另开工作轮次。

成员报告入库（解释器使用本机已配置的 Python；命令从工作室源码根目录执行）：

```text
python tools/workflow_db.py record member-report.json --kind work --author opus --submitted-by opus --source-project CRAZY-CIRCUIT --provenance "本次成员报告的文件或实际会话回执"
```

协调者代导入时，`--author` 写真实原作者，`--submitted-by` 写实际导入者，`--provenance` 必须给出可核对的原报告来源。不要把自己写的总结冒充对方报告，也不能代他人确认交接。

每轮效率报告生成并入库：

```text
python tools/workflow_review.py reports/workflow/YYYY-MM-DD-task/review.json --record-db --actor codex --source-project WORKFLOW-STUDIO --evidence reports/workflow/YYYY-MM-DD-task/evidence.json
```

这里 `--source-project` 表示被分析的业务项目；本轮在维护工作流本身才用 WORKFLOW-STUDIO。`--evidence` 可省略，不能用空证据声称验证过。命令成功输出 `database_receipt` 才是成功入库；生成 Markdown 本身不是入库成功。

## 核对更新

```text
python F:/TeamHub/teamdb.py context --project WORKFLOW-STUDIO --category 02
python F:/TeamHub/teamdb.py search --project WORKFLOW-STUDIO --table reviews --text ROUND_ID
python F:/TeamHub/teamdb.py get --project WORKFLOW-STUDIO reviews RECORD_ID
python F:/TeamHub/teamdb.py search --project WORKFLOW-STUDIO --table decisions --text WF-07
```

`get` 读取完整 JSON 正文和证据，不依赖原报告文件仍然存在。`context` 是有限长度摘要，不可当作完整报告。JSON 中记录作者、入库者、源项目、轮次、类型、版本、前一版本 ID 和 SHA-256。同内容重试复用原记录；更正正文新增版本，保留旧版。建议每次状态声明新增记录，引用来源报告和前一状态 ID，不覆盖历史；不同作者的声明并存，以实际证据和复核结果确定采用情况，不能按入库时间直接覆盖决策。

建议 ID 在工作流库内全局唯一：先查已有条目；更新同一建议沿用 ID，新建议申请新 ID，业务项目专属建议可加项目代码前缀。不同成员不要各自从 `IMP-001` 开始编号，否则会被视为同一建议的状态历史。

普通工作报告使用简洁模板；效率报告经过 `workflow_review.analyse` 校验。一个报告及其改进建议在同一事务中保存，失败全部回滚。角色名称是协作标签，不是鉴权。

## 初始化与运行边界

```text
python tools/workflow_db.py init --catalog F:/TeamHub/catalog.json
```

初始化会保留其他项目的目录项和数据库；重复执行只核对既有工作流库，不重建。若目录出现不完整项目、锁文件残留或注册冲突，先核查并恢复，不能删除旧库强行初始化。

目前这是依靠明确命令和入口规则执行的工作流，没有后台监听所有聊天。上轮已实测 DeepSeek 能读取，但嵌套 Windows 沙箱阻止自动写回；Opus 未给本人回执。失败时保留报告并标注待入库/待确认，不能把接口测试等同于三方都已采用，也不要反复派模型或扩大沙箱权限。

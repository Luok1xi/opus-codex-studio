# 2026-11-10-astra-preview 工作流复盘

Separate historical failure stages and test an isolated steering preview boundary change.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：None
- 测量截止：2026-11-10T02:24:31.8919228+08:00
- 墙钟秒数：None
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Actual provider usage | 未知 | tokens | Not available |
| Round time | 未知 | seconds | No reliable round start timestamp |
| Simulation run wall | 51.7904 | seconds | Existing qualification runner |
| Native audit agents | 2 | agents | Read-only reports inspected |
| Vehicle operations | 0 | operations | Host and target builds only |
| Test setup rework | 1 | attempts | Late route fixture initially failed to skip already traversed replay segments |
| Review overhead | 未知 | seconds | Not measured separately |

## 验收条件

- Isolated patch, shared source build and two-engine regression

## 已完成

- Host unit cases passed
- 16 complete simulated laps; eight matched case trace and event hashes
- TC264 built; six matching shared source hashes

## 未完成

- 无记录

## 收益与损耗观察

- Parallel readers independently distinguished admission from exit failures. A fixture had to carry prior replay progress to represent a later route occurrence. Initial target build needed the existing compiler environment and patch check had to account for CRLF.

## 修改建议及下一轮验收

- **WF-20261110-LATE-ROUTE-REPLAY-FIXTURE [proposed]** For isolated late route fixtures, carry both node index and completed replay state.；负责人：codex；下次检查：Verify wrong branch and correct branch in both directed visits.

## 证据

- 16/16 simulated laps; per-case route event and trace hashes matched baseline
- Host and TC264 compiled same six source hashes
- Boundary and directed-junction tests

## 限制

- No matched workflow timing baseline
- Candidate not deployed; no new hardware evidence

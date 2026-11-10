# 2026-11-10-school250-data-fit 工作流复盘

Fit a forward wheel response, compare corner speed policies on the frozen course, and check requested deployment readiness.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-11-10T22:20:56+08:00
- 测量截止：2026-11-10T22:33:24.1441782+08:00
- 墙钟秒数：748.144178
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Actual model usage | 未知 | tokens | Provider usage unavailable |
| Holdout records | 4 | runs | Leave-one-run-out checks on complete saved records |
| Offline trials | 28 | runs | Seven variants, two plants and two conditions |
| Physical writes | 0 | writes | No matching programmer or deployment receipt |
| Review overhead | 未知 | seconds | Not separately metered |

## 验收条件

- Verify physical target readiness for the selected prebuilt image
- Fit and hold out existing wheel records
- Compare bounded speed policies on the same frozen route

## 已完成

- Verified the selected image hash and checked the physical programmer repeatedly
- Completed four held-out wheel model checks
- Completed and plotted the two-engine controlled matrix

## 未完成

- Selected board image remains unflashed because the programmer was not detected

## 收益与损耗观察

- The requested speed was interpreted both as a ceiling and as a constant base. Keeping the map fixed distinguished the effect of corner planning.
- A first compile exposed a reference unused under constant speed. Keeping the original ceiling in the test arm repaired the build without weakening compiler checks.
- A better local forward-wheel fit did not establish lateral or camera fidelity. Separating reference and fitted variants exposed this limit.

## 修改建议及下一轮验收


## 证据

- Local snapshot and build receipts
- Local held-out fit, simulation commands, traces, summary and plot
- Local device enumeration and deployment preflight

## 限制

- No new physical driving evidence
- No matched workflow baseline

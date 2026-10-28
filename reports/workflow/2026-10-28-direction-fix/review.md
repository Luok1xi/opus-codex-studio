# 2026-10-28-direction-fix 工作流复盘

Implement the paired direction correction and assess reuse of the complete firmware speed-tuning mode.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：partial
- 开始：2026-10-28T07:08:56Z
- 测量截止：2026-10-28T07:18:21.011292+00:00
- 墙钟秒数：565.011292
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native independent worker | 1 | agents | Review and source-derived host tests. |
| External Opus calls | 0 | calls | Project database handoffs only; no reply claimed. |
| Host assertions | 224 | checks | Candidate zero failures; original 11 failures. |
| ADS compile duration | 6.031 | seconds | Build log; not total task duration. |
| Provider usage | 未知 | tokens | Unavailable. |
| Model cost | 未知 | currency | Unavailable. |
| Coordination/review overhead | 未知 | seconds | Interleaved; archive interval separately recorded. |

## 验收条件

- Paired output/feedback fix, source-derived negative-control tests, isolated ADS build, checked installation and explicit hardware limits.

## 已完成

- Installed five-change patch in current test source and GBK mirror; preserved original control gains and motor/probe functions.
- 224 source-derived host assertions passed; original source failed 11 assertions under the same physical-forward model.
- ADS full build completed with zero errors/warnings and all 649 input hashes unchanged.
- Published local HEX and project handoff 363.
- Verified complete firmware already has single-wheel speed mode and explicitly bypasses camera readiness in that mode.

## 未完成

- No flashing or physical direction acceptance.
- Actual Opus acknowledgement and complete-firmware integration remain pending.

## 收益与损耗观察

- Independent review prevented an extra output negation that would break the automatic wiring branch.
- Existing ADS automation was reused in a separate workspace without touching the owner workspace.
- Owner questioned maintaining a parallel test firmware; source inspection confirmed an existing production speed mode.
- Coordinator initially inferred a camera gate from its name; reading the function body showed an explicit bypass, and the statement was immediately corrected before edits.
- The worker corrected one test extraction boundary and retried one blocked WSL call; no firmware change was required by those test corrections.
- A production git status read was denied; bounded source reads sufficed for the advisory finding. Two nonexistent source filenames were corrected by reading the actual call path.
- No matched workflow baseline; efficiency remains unproven.

## 修改建议及下一轮验收

- **WF-DIRECTION-SHARED-PATH-20261028 [proposed]** Use the existing complete-firmware speed mode for subsequent gain tuning; validate called readiness functions before claiming blockers.；负责人：codex+opus；下次检查：Production tuning must execute existing PID/output/encoder functions with matched telemetry and mode reset validation.

## 证据

- evidence.json; local build log, source manifest, host test report and installation receipt.

## 限制

- No hardware actions; the host direction model follows owner observations.
- Complete production firmware was read but not modified.
- Raw captures, firmware, credentials and live project databases excluded from archive.

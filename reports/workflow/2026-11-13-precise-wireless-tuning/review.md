# 2026-11-13-precise-wireless-tuning 工作流复盘

Deliver a stopped-only precise wireless tuning candidate with immutable configuration/run/owner-evaluation records; correct the review map display.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：Single coordinator; scoped firmware, host integration and independent native review
- 验收状态：passed
- 开始：2026-11-13T05:39:10.006Z
- 测量截止：2026-11-13T06:26:50.899Z
- 墙钟秒数：2860.893
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| native_contributors | 3 | agents | Two scoped implementers and one independent reviewer returned evidence. |
| external_studio_calls | 0 | calls | No external DSH/Opus worker invoked. |
| python_tests | 92 | tests | Final two-suite receipt: 34 tuning/ledger plus 58 existing monitor. |
| default_trace_matches | 2 | plants | Final candidate C and physics-plant CSV hashes equal frozen baseline. |
| hardware_operations | 0 | operations | No real serial, flash, command or launch. |
| approval_timeout | 1 | events | Final local test approval timed out; one allowed retry succeeded. |
| initial_target_build_failures | 1 | builds | Snapshot RAM placement failed target linker, retained evidence then assigned CPU0 RAM. |
| tokens | 未知 | tokens | No reliable complete measurement. |
| cost | 未知 | currency | No reliable complete measurement. |
| coordination_wait | 未知 | seconds | No reliable complete measurement. |
| review_overhead | 未知 | seconds | No reliable complete measurement. |
| archive_overhead | 未知 | seconds | No reliable complete measurement. |
| total_rework | 未知 | events | No reliable complete measurement. |

## 验收条件

- Single stopped parameter write, complete checked readback and exact historical restore.
- Bind actual configuration revision to runs and preserve owner observations without altering old trials.
- Compile target and preserve default simulation behavior; verify local report UI.

## 已完成

- 92 Python tests pass; actual C-generated configuration and M2 bytes parse correctly.
- Target build has 0 errors and 13 inherited warnings; two default plant traces exactly match the frozen baseline.
- Immutable configuration archives, partial-write handling, reboot invalidation and per-run binding implemented.
- Desktop/mobile waveform, owner-note export and comparison UI checked in installed browser.
- Complete optical map displayed; missing upper-left link was presentation-only, map hashes remain unchanged.

## 未完成

- 无记录

## 收益与损耗观察

- Fine user-facing steps follow actual control and electrical resolution, and float restoration preserves raw bits.
- Independent review found an old write path bypassing revision and an M2 arrival ordering bug that altered the previous completed run; both fixed with bounded tests.
- Owner noticed a missing map link: the report had drawn only route traversal; full optical geometry now displays separately from planned route.
- Artifact registration waited for current source/build hashes instead of reusing an earlier successful HEX.
- Initial temporary test directory access failed; tests moved inside the workspace. Packaging assumed a generic zip filename, then used the actual frozen manifest name.
- No matched quality/time baseline exists, so no general speedup claimed.

## 修改建议及下一轮验收

- **TUNE-CONFIG-RUN-REVISION [adopted]** Keep full configuration snapshots plus runtime revision and freeze completed-run bindings against later M2 arrivals.；负责人：codex；下次检查：First supervised hardware trial must verify reboot, readback and next-run separation.
- **FULL-MAP-SEPARATE-ROUTE [adopted]** Render the full optical course separately from the planned route; test an untraversed branch.；负责人：codex；下次检查：Any subsequent course update must retain the known full-map link and geometry hash.

## 证据

- Sanitized evidence.json contains aggregates; source/logs/photos remain local.
- Local project task147 and handoff hold complete implementation evidence. Earlier capability audit is in reports/workflow/2026-11-13-wireless-capability/.

## 限制

- Candidate 9773c598 is frozen but unflashed; no real wireless throughput, control-period or changed-parameter race validation.
- Only two default nominal plants rerun; not a new full disturbance matrix.
- Optical symbols remain inherited references and are not guaranteed identical to newly placed field components.
- Legacy writing clients are disabled in this candidate; only the checked tuning client writes parameters.
- Measurement starts at implementation read checkpoint and ends before archival.

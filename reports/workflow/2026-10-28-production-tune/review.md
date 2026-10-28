# 2026-10-28-production-tune 工作流复盘

Integrate speed-loop tuning into production firmware and the existing local web console while preserving concurrent Opus direction fixes.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md
- 验收状态：passed
- 开始：2026-10-28T07:21:18Z
- 测量截止：2026-10-28T08:17:15.931892+00:00
- 墙钟秒数：3357.931892
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Native workers | 3 | agents | Control, backend, protocol/web; same workers also reviewed relevant boundaries. |
| External Opus model calls | 0 | calls | Read actual production changes and sent database handoffs; no response or acceptance claimed. |
| Control source checks | 41 | checks | Source-derived native harness passed. |
| Backend host assertions | 9691 | assertions | Strict compiler, ASan and UBSan; separate seven call-wiring checks passed. |
| Canonical web tests | 46 | tests | Targeted parser/model/data/chart/production tests passed. |
| Mock browser checks | 12 | checks | Desktop and narrow viewport; no page errors. |
| C-to-JS chunk modes | 5 | modes | 1, 7, 64, 512 and whole payload; counts, time, gain metadata and gyro agree. |
| ADS compile duration | 3.95 | seconds | Compiler build log only; not total task duration. |
| Provider usage | 未知 | tokens | No reliable provider usage available. |
| Model cost | 未知 | currency | Unavailable. |
| Coordination and rework duration | 未知 | seconds | Interleaved work; not separately measured. |
| Review overhead | 未知 | seconds | Interleaved; archive interval starts at measurement cutoff. |

## 验收条件

- Production entry reuses existing control functions; bounded commands/capture and physical start; source tests, full ADS build, canonical web checks and checked integration.

## 已完成

- Installed eight firmware changes and a guide, with a local commit limited to this round; preserved concurrent direction, encoder, gyro and S5 changes.
- Built a distinctly named HEX with all 681 source hashes unchanged through compilation; zero errors and eleven warnings in unchanged legacy files.
- Installed the existing-site UI/model changes; canonical tests and build passed, original local service returned HTTP 200.
- Validated real C export functions against the JS parser with simulated hardware and five packet chunk sizes.
- Created project handoffs 366 and 31; software tasks 69 and 11 completed. Physical acceptance remains separate.

## 未完成

- 无记录

## 收益与损耗观察

- File ownership and protocol were agreed before parallel edits; isolated candidates were compared with current production hashes before installation.
- Review fixed capture-time gain metadata and prevention of partial-line interleaving before integration.
- An existing speed-mode camera bypass was verified in its implementation; no new camera bypass was needed.
- The final native control review follow-up returned useful feedback but then hit model capacity before a final artifact; it is not represented as completed external Opus acceptance.
- Corrected one invalid project category and one query option; an oldest-first inbox produced irrelevant historical output. Targeted queries are preferable.
- Localhost HTTP and production git reads needed scoped elevated retries. Broad compiler-warning search initially matched flags; final counts came from the build summary and diagnostics.
- Worker fixture dependency and extraction issues were resolved with existing tools; no dependencies or extra site service were added.
- No matched quality baseline exists; parallel activity and passing checks do not establish net speedup.

## 修改建议及下一轮验收

- **WF-PRODUCTION-CONTRACT-20261028 [adopted]** Freeze command units, file ownership and source hashes before firmware/UI parallel work.；负责人：codex；下次检查：Next integration must reject changed source baselines and validate a source-generated capture in the UI.
- **WF-PRODUCTION-OPUS-ACCEPT-20261028 [proposed]** Recipient independently reviews the identified production artifact and records physical direction acceptance before high-speed tuning.；负责人：opus；下次检查：Require the recipient own acknowledgement and hardware evidence; a handoff alone is not acceptance.

## 证据

- evidence.json; local source manifests, host reports, ADS build log, browser report, canonical test/build logs and installation receipts.

## 限制

- No flashing, physical serial connection or motor operation; physical direction and straightness remain unverified.
- Local website updated; no public site deployment this round.
- The binary includes preserved pre-existing working-tree changes; the new local commit alone is not a full reconstruction identity.
- No raw captures, project source, live databases, credentials or conversations are uploaded.

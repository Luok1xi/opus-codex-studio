# 2026-10-30-vision-ipm-implementation 工作流复盘

Implement sparse inverse perspective geometry in an isolated vehicle firmware candidate, evaluate actual C correctness and cost, and hand off a reviewed shadow integration.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md + TEAMHUB.md, read 2026-10-30
- 验收状态：partial
- 开始：2026-10-30T00:50:39Z
- 测量截止：2026-10-30T01:18:30.659678+00:00
- 墙钟秒数：1671.659678
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Observed wall time to delivery/review cutoff | 1671.66 | seconds | UTC start and cutoff; includes development, three native worker scopes, rebase, build recovery and handoff. Remote archive follows. |
| Native workers with received artifacts | 3 | agents | Distinct module, matched replay/performance, independent review scopes; coordinator consolidates. |
| Passed final target builds | 2 | builds | OFF and MODEL complete target compile/link, independent source-to-receipt hash checks. |
| Earlier compiled builds rejected | 2 | builds | A successful compile did not detect camera buffer macro aliasing; both outputs explicitly rejected and replaced. |
| Behavioral defects fixed | 4 | defects | Named cases in evidence; one was inherited from the upstream version. Source declaration compile repair was part of header isolation. |
| Actual module test invocations | 4 | runs | Module worker reported four passing invocations, with regressions added for two product fixes. |
| Actual matched replay evaluations | 3 | runs | Initial implementation, pole validation repair, then public-header isolation; final result supersedes earlier timing. |
| Project-settings import recovery | 1 | incidents | Initial isolated copy excluded required device settings; restored settings and retained them in copy helper. |
| Documented failed target source build | 1 | observed logs | Captured final failed build had undeclared border arrays after header isolation; explicit declarations repaired. Not an exhaustive total build-attempt count. |
| Patch byte-equivalence harness corrections | 1 | incidents | Global newline conversion changed applied bytes; isolated apply with autocrlf disabled reproduced all six final files exactly. |
| Module public-header edit precondition failures | 1 | incidents | Worker reported a CRLF/LF precondition failure before any write; fixed matching without replacing other file bytes. |
| New physical hardware operations | 0 | operations | No serial, flashing or motor control in coordinator or worker scopes. |
| Total failed tool invocations | 未知 | operations | Permissions, temporary-directory setup and CLI option correction also occurred; no reliable exhaustive instrumentation. |
| Exclusive review overhead | 未知 | seconds | Review and rework overlapped coordinator work; no complete exclusive attribution. |
| Exclusive coordination wait | 未知 | seconds | No separate wait accounting. |
| Provider token usage | 未知 | tokens | No provider-complete parent/child usage evidence. |
| Actual monetary cost | 未知 | currency | No billing evidence. |
| Archive overhead | 未知 | seconds | Archive is subsequent to this cutoff; receipt records its completion separately. |

## 验收条件

- Implement sparse ground geometry and CPU1 shadow integration
- Run actual C correctness, unchanged-output replay and matched host timing checks
- Build isolated ADS candidate and report RAM/limits
- Deliver code and evidence to Opus without touching hardware

## 已完成

- Implemented sparse geometry, physical-point fitting with held-out validation, and CPU1 shadow integration on the newest frozen upstream version.
- Ran actual C edge cases, same-frame output equivalence, malformed-geometry rejection, real camera-copy and reader regressions with failing old-version controls.
- Built final OFF and MODEL target artifacts; verified exact source identity and a minimal byte-reproducible patch; live firmware source remained unchanged.
- Delivered final implementation and measured limitations through the project handoff database.

## 未完成

- Current vehicle calibration, board timing, and same-conditions physical driving comparison remain unperformed; no real-car performance benefit is claimed.
- The final Opus handoff has not yet received acceptance.

## 收益与损耗观察

- Independent review found a projection singularity and inherited reader failure-path defect. Coordinator integration then found a macro leak missed by the first review.
- Existing replay tests injected processing buffers directly, bypassing the camera producer/consumer boundary. Adding the real ISR copy regression reproduced the defect and its correction.
- Target compile success alone was insufficient: two compiled artifacts were withdrawn before delivery. The final header has a compile guard against camera aliases.
- Upstream advanced during development. A fresh frozen handoff was read, 684 files verified, and only the integration was rebased; no concurrent source was overwritten.
- Final host timing shows added work with substantial scheduling noise; different percentages across runs are not an optimization claim.
- Native parallel roles provided specific findings, but no matched workflow quality baseline exists to quantify net speedup.

## 修改建议及下一轮验收

- **IPM-IMPLEMENTATION-BOUNDARY-20261030 [adopted]** For new public headers, verify macro exports and test the real producer-to-consumer buffer copy, including an old-fault negative control.；负责人：codex；下次检查：Future camera candidates pass the same actual-copy test and compile guard.
- **IPM-IMPLEMENTATION-FREEZE-20261030 [adopted]** Keep exact source manifests and target build receipts per configuration; retain required IDE device settings and verify minimal patch bytes.；负责人：codex；下次检查：Next integration starts from the current accepted freeze and a settings-complete isolated tree.
- **IPM-IMPLEMENTATION-PHYSICAL-20261030 [proposed]** Accept physical geometry only after same-domain held-out calibration, board timing and matched driving evidence; keep shadow quantities out of pixel-unit control gains meanwhile.；负责人：opus；下次检查：Receive an actual acceptance and physical evidence through the project database.

## 证据

- Local implementation, final actual-C evaluation, final independent review and build manifests, identified only by aggregate hashes here.
- Project handoffs 468, 469, 470 and 471.

## 限制

- This is a complete offline/shadow delivery with partial physical acceptance, not a flashed or road-tested change.
- Host performance measurements are not target frame rate or lap time.
- Archive completion requires verified private remote readback.

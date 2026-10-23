# 2026-10-23-antigravity-open-source-options 工作流复盘

Search current primary sources for remedies and source-available alternatives for Antigravity's regional rejection, distinguishing subscription access from API billing.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; primary-source research only
- 验收状态：passed
- 开始：2026-10-23T06:49:41.364Z
- 测量截止：2026-10-23T06:51:54.838Z
- 墙钟秒数：133.474
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Provider usage | 未知 | tokens | No usage receipt. |
| Cost | 未知 | currency | No billing receipt. |
| Delegated agents | 0 | agents | Coordinator research only. |
| Software installed | 0 | packages | Read-only research. |
| Account/network mutations | 0 | actions | None. |
| Model calls tested | 0 | calls | No authorization or generation initiated. |
| Research rework | 未知 | calls | Older search snapshots conflicted with current repository metadata; exact repeated-lookup overhead not isolated. |
| Review and archive overhead | 未知 | seconds | Final database archive receipt measures to remote verification. |

## 验收条件

- Verify actual repositories and their relevant capabilities.
- Check whether a published workaround applies to the observed official-client endpoint.
- State licensing, account and billing limits without claiming a tested fix.

## 已完成

- Verified upstream documentation for Antigravity Manager, CLIProxyAPI, OpenCode auth plugin and Cline.
- Found an endpoint-order workaround in a first-hand issue; it applies to sandbox-to-daily fallback. The previously observed official client already used daily, so it is not a confirmed remedy here.
- Verified Google's current third-party-login restrictions and Gemini CLI consumer migration notice.
- Separated API-key coding-client options from Google AI Pro subscription usage.
- No installation, account authorization, credential export, endpoint modification or model calls.

## 未完成

- 无记录

## 收益与损耗观察

- Primary repository metadata contradicted an older search snapshot about archived status; no stale archived claim was propagated.
- An old Gemini CLI subscription tutorial is unsuitable for current consumer accounts because the official migration announcement supersedes it.
- Public source code does not imply removal of Google's server checks; Antigravity Manager also uses a non-commercial source license.
- Account suspension risk is explicitly documented by Google for third-party use of Antigravity login; this is an observed provider rule, not a hypothetical warning.
- A Cline/API path needs a minimal API generation check first and has its own project quota/billing and regional availability.
- No matched baseline; research cannot establish a working repair or workflow speedup.

## 修改建议及下一轮验收

- **WF-AG20261023-REPO-CURRENT [adopted]** When recommending a workaround, match its failing endpoint and account channel to the observed client; verify current upstream README and migration notices rather than relying on old search snippets.；负责人：codex；下次检查：Next software recommendation must identify compatibility and billing/authentication boundaries before install guidance.

## 证据

- https://github.com/lbjlaq/Antigravity-Manager/issues/3525
- https://github.com/router-for-me/CLIProxyAPI
- https://github.com/NoeFabris/opencode-antigravity-auth
- https://github.com/cline/cline/blob/main/docs/provider-config/google-gemini.mdx
- https://antigravity.google/docs/faq
- https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/
- https://ai.google.dev/gemini-api/docs/billing

## 限制

- No candidate project was installed or tested with the owner's account.
- No reliable removal of the remote region check was established.
- Only sanitized research/workflow aggregates are archived; no account data, raw logs, public IPs, credentials or sessions.

# 2026-10-23-antigravity-vpn-region-investigation 工作流复盘

Investigate a location rejection despite a US VPN and user-confirmed supported Google account region; provide a concrete supported troubleshooting path.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：WORKFLOW_REVIEW.md; read-only owner-context routing and egress verification
- 验收状态：partial
- 开始：2026-10-23T06:16:04.670Z
- 测量截止：2026-10-23T06:19:57.723Z
- 墙钟秒数：233.053
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Model usage | 未知 | tokens | Provider usage unavailable. |
| Cost | 未知 | currency | Billing unavailable. |
| Delegated agents | 0 | agents | No delegation. |
| Egress diagnostic services | 3 | services | IPinfo, Cloudflare trace and IP.sb. |
| Observed model-server HTTPS connections routed through VPN | 4 | connections | Socket destination route lookup snapshot. |
| Additional model requests initiated | 0 | requests | Used existing error evidence. |
| Account/network/firewall mutations | 0 | actions | Inspection only. |
| Coordination waiting time | 未知 | seconds | Owner clarifications arrived during ongoing independent work; active versus waiting not separated. |
| Review and archive overhead | 未知 | seconds | Final category-05 archive receipt measures through verified remote content. |
| Total tool failure count | 未知 | calls | Some documentation fetches required login or timed out; no complete comparable count. |

## 验收条件

- Classify actual network path and independent egress location.
- Check current official guidance and primary first-hand issue reports.
- Give a bounded next test without claiming a server-side fix.

## 已完成

- Three independent public diagnostic services agreed on US IPv4 egress; existing model-server HTTPS connections selected VPN split routes.
- Current API DNS results were IPv4 only; no configured endpoint/proxy environment overrides in the diagnostic context.
- Owner corrected their earlier country-page reading and confirmed a supported account country. Synchronization failure was retained as unproven.
- Created a local support summary without credentials, raw chats or public IPs.
- No region bypass, firewall, DNS, endpoint, billing or account changes were applied.

## 未完成

- Successful Gemini invocation not restored or tested on a second egress.
- Google's exact server-side geolocation/eligibility decision and region-change approval timing not independently verified.

## 收益与损耗观察

- A VPN /1 split route is more specific than the physical adapter /0 default route. Inspecting only the default route would misrepresent the actual path.
- Network geolocation services do not establish Google's own eligibility verdict. A data-center ASN is a hypothesis signal, not proof of an IP block.
- Account-country interpretation changed after owner clarification. The proposed correction path was withdrawn once a supported country was confirmed.
- No authoritative synchronization SLA was found. Unverified forum claims of 48-72 hours were not presented as Google guarantees.
- Earlier consideration of a firewall guard was not implemented because actual model-server route checks already selected the VPN and the owner prioritized root-cause investigation.
- A same-account, same-model comparison using one different egress is the smallest next test; if still rejected, official support must inspect service-side eligibility.
- No matched quality baseline exists; no speedup claim.

## 修改建议及下一轮验收

- **WF-AG20261023-ROUTE-COUNTRY [adopted]** Before attributing location errors to a proxy leak or country-sync failure, verify longest-prefix routes for actual model-server sockets and explicitly distinguish owner-confirmed account state from an independently inspected approval.；负责人：codex；下次检查：Next regional rejection: retain exact server error, current route snapshot, verified-versus-reported country status, and a bounded comparison plan before suggesting mutations.

## 证据

- evidence.json
- https://antigravity.google/docs/faq
- https://policies.google.com/faq?hl=zh-CN
- https://discuss.ai.google.dev/t/antigravity-2-24-0-http-400-location-error-persists-with-verified-jp-us-egress-while-gemini-web-works/190459

## 限制

- No server-side region check was disabled.
- No unsupported-country or synchronization conclusion can be made from the corrected account report.
- Local support artifact remains local; no credentials, public IPs, raw logs, messages or databases are archived.

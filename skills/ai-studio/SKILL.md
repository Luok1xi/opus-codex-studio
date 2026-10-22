---
name: ai-studio
description: Use the user's local Opus, Codex and DeepSeek studio for authorized multi-AI collaboration, delegated research or development, independent review, quota-aware routing and durable handoff. Applies across projects; ordinary tasks that need no collaboration stay local to the current agent.
---

# Local AI studio

The maintained studio is `@STUDIO_ROOT@`. Use it for coordination; the user's current project remains the task workspace. Python is `@PYTHON@`. This skill is a discovery entry, not permission to publish, sign in, access unrelated data or buy credits.

## Choose the smallest useful path

- Direct deterministic work (searching files, running configured checks) needs no extra AI. Do not create a committee for a trivial task.
- When the user requests DeepSeek or a second opinion, call the already verified official Harness CLI through the shared `consult` entry below. No MCP registration or desktop clicking is necessary. An open Desktop chat is not the CLI's session.
- For a bounded multi-step task, use `tools/bridge.py`: `doctor`, `submit`, `run`, `status`, `events`. Read [BRIDGE_GUIDE.md](@STUDIO_ROOT@/docs/BRIDGE_GUIDE.md) before submitting. The Python controller owns the queue; AI leads are called only to plan and review. Owner-written plans can skip AI planning.
- Agents dispatched as workers must only do their assigned work. They must not call other AIs or start another controller. Only the current operator/controller dispatches. Existing task authorization applies; do not ask the user to copy prompts between apps.

## Call DeepSeek and retain the handoff

Write a concise UTF-8 request containing the useful inputs, the desired result and acceptance criteria. Use a fresh empty directory for text-only consultation and explicitly request no tools; this instruction is NOT an enforced sandbox. For file work, supply only the authorized project workspace. Read [DEEPSEEK.md](@STUDIO_ROOT@/docs/DEEPSEEK.md) if permissions, continuation or setup matters.

From the studio root:

```text
python tools/bridge.py consult --workspace /absolute/authorized/workspace --prompt-file /absolute/request.txt --key unique-task-id
```

Use the Python path above if `python` is not on PATH. The local connection is `.studio-runtime/deepseek-connection.json`. The CLI reads its own existing login; never read or copy credential files or cookies. Do not promise that account balances are known: automatic DeepSeek quota routing is still disabled until verified.

The job result contains a native session ID and a hashed answer artifact. Read that artifact for the actual answer. `answered` means a reply arrived, not that its content passed independent acceptance. If the call is interrupted, use the SAME key or `status JOB_ID` to inspect the saved outcome before deciding anything else; never blindly use a new key to replay a possible write. Continue a verified session with `--session SESSION_ID`, same workspace, and a new task key.

## Choose people by the task, keep progress outside chat

Read [ROUTING.md](@STUDIO_ROOT@/studio/ROUTING.md) for the current policy. `routing_rules` in the owner configuration can choose different candidates for planning, review and specialist work. Availability, real quota and capability checks still apply. Opus is preferred for planning when its actual CLI is ready; Codex is the fallback. Do not equate desktop login with CLI readiness.

When changing a rule, use observed acceptance, rework, elapsed time and actual usage for comparable tasks. Model self-confidence and one successful greeting are not performance evidence. Unknown quotas remain unknown. Save outputs in the shared ledger or the production handoff so a new chat can continue without this conversation.

## Per-round workflow review

Owner requires each completed user task round to include an evidence-based efficiency review and improvement suggestions in the private repository `Luok1xi/opus-codex-studio`. Follow [WORKFLOW_REVIEW.md](@STUDIO_ROOT@/docs/WORKFLOW_REVIEW.md); use the existing metrics and `tools/workflow_review.py`. A coordinator produces one report, including workers' evidence; reporting does not recursively create another round. The 2026-10-18 user instruction authorizes sanitized workflow reports and related workflow changes to this private repository, not raw sessions, credentials or unrelated project files. Verify private visibility and remote contents before claiming uploaded. Without a matched quality-controlled baseline, report that net efficiency is unproven.

## Shared categorized project data

Read [TEAMHUB.md](@STUDIO_ROOT@/docs/TEAMHUB.md). Use `@STUDIO_ROOT@/tools/teamdb.py` with `.studio-runtime/teamhub.json`, or the shared local entry `F:/TeamHub/teamdb.py`. The catalog holds only project locations; every project has a different physical database. First list projects, then select the current project/category and your inbox; use `get` for full evidence. Store current handoff bodies and acknowledgements in that project database. Historical handoff files are evidence, not the current queue. Do not write the frozen old combined database or request manual paste relays.

Default responsibilities: DeepSeek/dsh collects, deduplicates and classifies sources; Codex implements, tests and integrates; Opus designs and independently reviews. User assignments override defaults. Only recipients acknowledge their actual receipts. These labels are cooperative conventions, not authentication. No live project databases, backups or exports go into GitHub.

## Workflow evidence database

Store each member work report and coordinator efficiency analysis in WORKFLOW-STUDIO, a separate project database in the shared catalog. Read [WORKFLOW_DATABASE.md](@STUDIO_ROOT@/docs/WORKFLOW_DATABASE.md). Save full JSON, original author, actual submitting agent, source project, round and evidence. Corrections append history. Missing peer reports remain missing; receipt failures remain pending. Private GitHub keeps sanitized archives, not live databases.

# Connected ESC parked-signal review

Round: `2026-11-03-fan-first-trial`; coordinator: codex. Status: partial hardware diagnosis; parked digital timing verified.

KingstVIS 3.6.6 and a real LA1010 acquired CH0 at 1 MHz for 1 second, threshold 1.50 V. The operator reported the ESC connected, wheel driver disabled and no S5. After a deliberate S1-off capture became flat low, the next powered capture contained different transition positions and 50 complete positive pulses of 1000 us. Its 49 rising periods were 20000 us (47) and 20001 us (2). First rising edge was sample 5627, versus 12134 in the earlier isolated capture.

The final raw file SHA256 is `2ef260c7ad12f41c72376b1fda93d2b55446329c522d38bacbfb4b6c98f85b67`. Five saved files total 7760 bytes; an earlier newly named powered file was byte-identical to the old buffer and remains excluded as independent evidence. Raw files, screenshots, complete transitions and firmware remain local.

The coordinator and a native independent reviewer re-read the files and agreed. Parsing uses a narrow reader based on a third-party reverse-engineered kvdat format, with complete byte consumption and monotonically ordered edge checks. GUI settings match the binary header. Same-capture CSV comparison is incomplete; no manufacturer binary-format certification or independent timebase calibration is claimed.

This verifies parked digital timing only at the identified mainboard probe point under operator-reported connected conditions. It does not establish analog amplitude, ESC internal reception or arming, throttle response, supply health, motor phases or mechanical condition. The historical humming/nonrotation cause is unresolved. No vehicle serial commands, S5, nonzero throttle or firmware flash were issued. An existing analyzer PWM1 output was disabled earlier; no analyzer output was enabled.

The round began at 13:43:23 UTC on 2026-11-03; final measurement cutoff was 2945.129 seconds later. This is wall time including user actions, reviews, GUI rework and approval delays, not computation time. Two native review workers supported the coordinator; no real Opus consultation occurred. Tokens, cost, itemized waiting, review overhead and archive overhead are unknown (null). There is no matched quality baseline and no efficiency-gain claim.

Rework included stale window geometry, unconfirmed channel settings, partial filename input, misreading a restricted process listing as application exit, and a default filename differing from the requested name. The exit claim was corrected and the extra unconnected demo instance closed. Four GUI approvals timed out; one earlier report upload timed out and succeeded on its permitted retry. A background F5 message was queued but did not establish acquisition. User-assisted capture and local parsing provided the fallback.

Adopted improvements: bind GUI actions to the intended process/window; verify actual saved files; distinguish filename creation from acquisition; use an observable input-state change when freshness is uncertain; switch to clearly bounded user-assisted saving after repeated approval delays. These are evidence-based process changes, not proven speedups.

The detailed earlier [workflow report](https://github.com/Luok1xi/opus-codex-studio/blob/3c6ca33120969b730b687aac4b9679a041b69798/reports/workflow/2026-11-03-fan-first-trial/kingstvis-operation/review.md) preserves the isolated baseline. Format reference: [open-source kvdat reader](https://github.com/andy-qingcai/KintstvisMcp/blob/main/kingstvis_mcp/kformats.py#L71-L128).

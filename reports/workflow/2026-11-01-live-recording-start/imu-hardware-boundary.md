# Same-round clarification: zero output does not clear hardware

The owner asked whether the earlier stationary-rate anomaly could be hardware-related. A read-only refresh found 1,380 post-calibration stopped-state samples over approximately 345 seconds, with the latest processed rate at zero. There are no synchronized human-motion labels for that entire interval, so it is not a controlled stationary or dynamic test.

One reused independent source reviewer confirmed that the displayed readiness flag is latched from initialization and that the rate is bias-corrected, filtered and deadbanded. Neither flag nor a displayed zero proves ongoing communication health or excludes a stuck sensor. No new device command, parameter change or flash occurred. A drive-disabled manual left/right response check is proposed and has not been performed in this clarification.

Quality improvement: distinguish recovery of processed telemetry from hardware acceptance. Both calibration error and a hardware/communication fault remain possible; no unsupported fault probability or component-replacement recommendation is given. Vendor calibration guidance supports the general bias-subtraction principle, while the vehicle-specific limits come from inspected local source. Model usage, cost and exclusive review labor remain unknown; there is no matched efficiency baseline. This is a supplement to the ongoing review, not a new review round. Raw captures remain local.

Public principle reference: https://www.bosch-sensortec.com/media/boschsensortec/downloads/development_desktop_software/usermanuals/dd_2-1_user_manual-2.pdf

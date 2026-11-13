# 2026-11-13-quiet-launch-build-flash ����������

Reorder launch to quiet IMU calibration, fan pre-spin, then wheel release; freeze, compile and deploy the minimal repair. Physical launch and driving acceptance remain pending under project task149.

**���ۣ�֤�ݲ��㣺û�кϸ��ͬ�������ߣ������жϾ���Ч��**

δ���������ֹ۲�򵥴���Բ���֤���ձ�������档

- ��������Single root hardware owner; bounded native worker implementation/registration; separate sanitized archive worker. Existing WORKFLOW_REVIEW and TeamHub rules.
- ����״̬��partial
- ��ʼ��None
- ������ֹ��2026-11-13T07:40:39.343257+00:00
- ǽ��������None
- �ϸ���Ժ�ʱ�仯��%����None

## ʵ������

| ָ�� | ֵ | ��λ | �ھ� |
|---|---:|---|---|
| target_build_duration | 9.844000000011874 | seconds | Final official ADS receipt; not whole-stage elapsed time. |
| launch_mock_duration | 6.772225951000053 | seconds | Recorded actual-C ASan/UBSan invocation; not a vehicle test. |
| flash_difference | 0 | bytes | Saved official flash verification log. |
| saved_flash_receipts | 1 | receipts | One successful receipt supplied for this stage; not a claim about unrecorded attempts. |
| flash_tool_duration | δ֪ | seconds | No exact duration available in the bounded saved receipt/log used. |
| metadata_repairs_observed | 1 | repairs | QUIET-LAUNCH.md and FREEZE.json record restoring ADS .settings omitted from old source ZIP, and including it in new source package. |
| whole_stage_elapsed | δ֪ | seconds | No trustworthy stage start timestamp; do not infer from file modification times. |
| whole_stage_rework_count | δ֪ | reworks | Only one packaging repair documented; full coding/retry ledger unavailable. |
| review_preparation_checkpoint | 130.343257 | seconds | Archive worker clock checkpoint to evidence extraction cutoff; excludes earlier review work and subsequent database/upload. |
| archive_overhead | δ֪ | seconds | In progress at this report cutoff; final archive receipt records its measured checkpoint interval. |
| coordination_wait | δ֪ | seconds | Not separately timed. |
| tokens | δ֪ | tokens | No provider usage for matching parent/child scope. |
| cost | δ֪ | currency | No billing record. |

## ��������

- Preserve original quiet-calibration thresholds/retries and local S5 cancellation.
- Compile and freeze exact target artifact; confirm flash byte comparison and stopped outputs.
- Verify the changed launch sequence on the physical car before claiming the symptom fixed.

## �����

- Actual C launch mock passed ASan/UBSan, including phase cancellation, noisy retries, fan timing and STOP reason.
- ADS build accepted with 0 errors and 13 existing warnings; inputs unchanged.
- Frozen 5dafe559 HEX programmed with PASS and 0 different bytes.
- Saved postflash M2 CRCs valid; wheel/fan outputs zero.
- Tuning registry adds only the new exact HEX and same schema; original 9773 retained.

## δ���

- Root/Owner wireless physical launch and driving acceptance. No successful new launch or course completion claimed.

## ��������Ĺ۲�

- Finding CC-F#218 distinguishes a calibration wait with zero wheel commands from a turn-controller failure; its vibration cause remains a hypothesis.
- Physical launch stays with the root hardware owner; archive worker opens no serial port, flashes nothing and does not dispatch another agent.
- The stage restores missing ADS project metadata instead of changing behavior to work around a build issue.
- Owner narrowed work to the immediate repair; no new track matrix or expanded tuning test suite was run, and old passing results are not relabeled as new acceptance.
- Successful programming, stopped reboot and mocked phase coverage are distinct from physical launch success.
- No matched same-quality baseline exists; net speedup cannot be established.

## �޸Ľ��鼰��һ������

- **QUIET-LAUNCH-PACKAGE-METADATA [adopted]** Keep ADS .settings and project descriptors in future frozen source packages; the new quiet package includes them.�������ˣ�codex���´μ�飺Next isolated extraction should compile without restoring missing project preferences.
- **QUIET-LAUNCH-PHYSICAL-GATE [proposed]** Append a new physical launch result to the existing finding instead of rewriting the earlier diagnosis as confirmed.�������ˣ�codex���´μ�飺Use the next actual S5 launch to confirm quiet calibration completes before fan pre-spin and wheel release; retain failure evidence.

## ֤��

- evidence.json: sanitized hashes and aggregate checks only.
- CRAZY-CIRCUIT task149 remains in_progress; finding218 is unchanged.
- Prior stage fc5d3df remains unchanged; this is a separate build/flash acceptance stage.

## ����

- Physical new launch and driving were not accepted at this cutoff.
- Fan vibration is plausible but was not directly measured in raw calibration samples.
- Gyro filtered output can remain stale during calibration and cannot prove raw stability.
- No measured fan RPM or suction; software output/timing checks only.
- Original noisy-calibration retry policy remains; no threshold was bypassed.
- Volatile live parameters are not persisted by flashing and need fresh readback.
- Stage start, total cost, total model usage and overall rework count are unknown.
- No raw logs/source/HEX/credentials or databases are uploaded.

# 2026-10-21-vision-integration 工作流复盘

Integrate and independently validate full-circuit visual routing on an existing vehicle project and simulation site.

**结论：证据不足：没有合格的同条件基线，不能判断净提效。**

未建立；单轮观察或单次配对不能证明普遍因果收益。

- 工作流：TeamHub evidence reuse, bounded native reviews, existing C replay pipeline and target IDE validation
- 验收状态：partial
- 开始：2026-10-21T04:16:39.635000+00:00
- 测量截止：2026-10-21T04:37:50.881032+00:00
- 墙钟秒数：1271.246032
- 合格配对耗时变化（%）：None

## 实测数据

| 指标 | 值 | 单位 | 口径 |
|---|---:|---|---|
| Wall time through functional delivery | 1271.246 | seconds | Recorded round start and current cutoff; includes one interruption, recovery, independent checks and rework. |
| Native task dispatches | 5 | tasks | Hardware/source/target reviewers, one interrupted target continuation and calibration sensitivity task; not Opus calls. |
| New Opus or DeepSeek model calls | 0 | calls | Reused real Opus handoff and candidate; database messages pending, no fabricated response. |
| Target build errors | 0 | errors | ADS GUI target build log. |
| Target build warnings | 11 | warnings | Inherited OUC/driver diagnostic locations. |
| Model usage and cost | 未知 | unknown | Provider usage/billing not available. |
| Coordination and review overhead | 未知 | seconds | Overlapping activities and interruption not individually instrumented. |
| Review archive overhead | 未知 | seconds | Archive not finished at measurement cutoff; receipt will record verification. |

## 验收条件

- Full-map route comparison and inspectable visual evidence on the original website.
- Compatible target-source integration with honest hardware/calibration boundaries.
- Fault protection and source/CLI/browser consistency validated.

## 已完成

- Reused current collaborator route candidate and audited hardware pins, signs and units.
- Fixed and fault-tested indefinite gyro hold after camera freeze.
- Added full-map real-C replay and 29 landmark inspection links to the existing website; browser and all replay checks passed.
- Added default-disabled target route preset; actual ADS compiler/linker succeeded; calibration gate tests passed.

## 未完成

- Real camera and odometry calibration, physical direction checks and autonomous finish stopping remain required.
- Full-map symbol-name classification is not implemented; current objective tested is planned traversal.
- Independent Opus acceptance of this round corrections remains pending.

## 收益与损耗观察

- Reusing the collaborator candidate avoided another controller implementation; no matched workflow baseline supports a speedup percentage.
- Independent review found stale-camera bypass, host-only route provisioning, evaluation-only lap ending and calibration sensitivity.
- Browser validation caught null-HEX rendering failure that source-data tests missed; corrected and rechecked both screen widths.
- Initial server absent after interruption; original start entry restored after database backup and migration plan check.
- Repeated oversized reads and one accidental invalid WSL invocation added overhead; no data loss. Standalone compiler/headless IDE failures required the supported GUI build path.

## 修改建议及下一轮验收

- **VISION-TARGET-BOUNDARY-20261021 [adopted]** Require a target route initialization check and a sensor-dropout test whenever simulated full-lap success is proposed for hardware.；负责人：codex；下次检查：Next route revision reproduces frozen-frame stop and target preset gates before promotion.
- **VISION-CALIBRATION-PERTURBATION-20261021 [proposed]** Separate plant truth from controller calibration in validation; include odometry and camera errors before any real-car reliability claim.；负责人：opus；下次检查：After measured calibration, rerun at least +/-5 percent odometry and measured camera-height/pitch uncertainty.

## 证据

- evidence.json

## 限制

- Real camera and odometry calibration, physical direction checks and autonomous finish stopping remain required.
- Full-map symbol-name classification is not implemented; current objective tested is planned traversal.
- Independent Opus acceptance of this round corrections remains pending.

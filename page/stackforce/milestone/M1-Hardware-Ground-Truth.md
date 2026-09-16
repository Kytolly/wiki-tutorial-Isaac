# M1 — Hardware Ground Truth

> **Links / 链接:** [[Home]] · [[Roadmap与里程碑]] · [[evidence-registry]] · [[T-ACT-001-Canonical-Real-Sim-Component-Identity]]

## Objective

冻结真实四足轮腿机器人的 physical mechanism、actuator identity、controller routing 与 command semantics；未知的 dynamics、Deployment action adapter 和 Optional External Ground Truth 保持分离。

## Status

**PASS WITH DECLARED NON-BLOCKING GAPS**

## Progress

**10 / 10 PASS**

## Gates

| Gate | Title | Status | Current result |
|---|---|---|---|
| [[M1-G01-硬件清点]] | 硬件清点 | **PASS** | controller/board/actuator inventory frozen |
| [[M1-G02-传感器映射]] | 传感器映射 | **PASS** | onboard observation availability frozen |
| [[M1-G03-执行器映射]] | 执行器映射 | **PASS** | PCA1-PCA8 and four Wheel identities frozen; powered all-channel regression normal |
| [[M1-G04-关节标定]] | 关节标定边界 | **PASS** | reference command and servo_off frozen; mechanical u0/q remain optional external ground truth |
| [[M1-G05-指令定性]] | 指令定性 | **PASS** | Servo degree command and Wheel raw command semantics frozen |
| [[M1-G06-控制测频]] | 控制测频 | **PASS** | controller timing contract retained |
| [[M1-G07-延迟测量]] | 延迟测量 | **PASS** | measured timing retained under M3 dynamics ownership |
| [[M1-G08-尺寸测量]] | 尺寸测量 | **PASS** | nominal physical geometry sufficient for M1 |
| [[M1-G09-质量测量]] | 质量测量 | **PASS** | higher-fidelity mass/inertia moved to M3 dynamics fidelity |
| [[M1-G10-停机验证]] | 停机验证 | **PASS** | post-flash timeout/STOP and powered return/zero evidence PASS |

## Frozen Result

- REAL_SINGLE_LEG_MECHANISM_CONTRACT = FROZEN
- REAL_ACTUATOR_IDENTITY_CONTRACT = FROZEN
- REAL_PCA_SERVO_MAPPING = FROZEN
- REAL_WHEEL_IDENTITY_CONTRACT = FROZEN
- REAL_COMMAND_PHYSICAL_CONTRACT = PARTIAL
- OFFLINE_M1_COMPLETE = YES
- ADDITIONAL_REAL_M1_EXPERIMENT_REQUIRED = NO

The historical ch7 non-return event remains in E-CAL-001; E-M1-002#P04 records the later powered all-channel regression that removes it as a current blocker. Absolute Servo joint-positive direction and Wheel chassis-forward sign remain Deployment work. Servo q_real/qd_real and precision mechanical u0 remain Optional External Ground Truth.

## Remaining Boundaries

| Ownership | Open work |
|---|---|
| M1_PHYSICAL_CONTRACT | None requiring another powered experiment |
| M2_SIM_ASSET | PhysX closure/runtime |
| M3_DYNAMICS | response, delay, stiffness, damping, Wheel SI, contact/friction |
| DEPLOYMENT | policy-to-hardware sign/scale/saturation/routing |
| OPTIONAL_GROUND_TRUTH | external Servo angle/velocity and precision mechanical zero |

## Changelog / 更新日志

- 2026-09-17：依据 E-M1-002 与 powered Dataset 004 reproduction，将 M1 冻结为 10/10 PASS WITH DECLARED NON-BLOCKING GAPS；保留历史 ch7 failure，不再将其列为当前 blocker。
- 2026-09-15：重构为标准 Milestone 规范并保留当时 7/10 状态。

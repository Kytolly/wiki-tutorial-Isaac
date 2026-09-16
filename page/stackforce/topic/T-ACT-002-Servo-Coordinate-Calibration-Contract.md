# T-ACT-002 — Servo Coordinate & Calibration Contract

> **Links / 链接:** [[M1-Hardware-Ground-Truth]] · [[M1-G04-关节标定]] · [[T-ACT-001-Canonical-Real-Sim-Component-Identity]] · [[evidence-registry]]

## Status

**CONTROLLER CONTRACT FROZEN / DEPLOYMENT TRANSFORM PARTIAL**

## Scope

本 Topic 严格区分三类量：

| Quantity | Meaning | Current status |
|---|---|---|
| reference command | normal IK 启动/返回姿态下的 post-offset absolute Servo command | FROZEN |
| servo_off | firmware 对各通道 IK 输出施加的 assembly trim | FROZEN |
| mechanical u0 | canonical physical joint frame 的机械零位 | OPTIONAL_EXTERNAL_GROUND_TRUTH |

reference command 与 servo_off 均不得当作 measured q_real、qd_real 或 mechanical u0。

## Frozen PCA Contract

| PCA | Canonical Servo | Reference command (deg) | servo_off (deg) | Powered execution/return |
|---:|---|---:|---:|---|
| 1 | FR_Outer_Servo | 112 | -4 | PASS |
| 2 | FR_Inner_Servo | 214 | -5 | PASS |
| 3 | FL_Inner_Servo | 146 | +5 | PASS |
| 4 | FL_Outer_Servo | 237 | -7 | PASS |
| 5 | RL_Outer_Servo | 113 | -3 | PASS |
| 6 | RL_Inner_Servo | 214 | -5 | PASS |
| 7 | RR_Inner_Servo | 133 | -8 | PASS |
| 8 | RR_Outer_Servo | 252 | +8 | PASS |

Evidence: E-M1-002#P02-P04. The historical ch7 failure remains in E-CAL-001#P04 but is no longer the current status after the powered all-channel regression.

## Controller Mapping

Firmware maps target degrees to PCA9685 output at 50 Hz:

    pulse_us = 500 + 2000 * target / 300
    off = floor(pulse_us * 4096 / 20000)

The software interval 0..300 deg is an API representation range, not a mechanical safe range. Powered +/-10 deg commands established visible bounded motion and return, not measured physical angle.

## Physical Direction Boundary

- Historical 2026-09-10 observation recorded PCA4 +command as CW, PCA5 as CCW, and PCA6 as CW under that session's observer convention.
- Powered Dataset 004 confirmed all PCA channels move and return safely, but Human did not provide reliable per-channel physical direction labels.
- A portable joint-positive sign requires a canonical body/joint-axis convention. That transform belongs to Deployment, not the frozen M1 identity contract.
- Sim mirror symmetry must not be used to invent Real physical polarity.

## External Ground Truth Boundary

Servo q_real/qd_real, precision mechanical u0, physical deadband, compliance, stiffness, damping, and exact command-to-angle scale are not available from the onboard controller. They remain Optional External Ground Truth or M3 Dynamics, and are not a blocker for M1 closure.

## Engineering Conclusion

M1 freezes command identity, reference, trim, PWM/count mapping, powered execution, and return. REAL_COMMAND_PHYSICAL_CONTRACT remains PARTIAL only because absolute physical coordinate signs and external joint measurements are unresolved. No additional powered M1 experiment is required.

## 更新日志

- 2026-09-17：移除过时的 ch7 current blocker，导入 E-M1-002 powered all-channel regression；严格分离 reference command、servo_off 与 mechanical u0。

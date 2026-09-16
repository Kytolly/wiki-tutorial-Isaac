# T-ACT-001 — Canonical Real↔Sim Component Identity

> 专题编号：`T-ACT-001`  
> 状态：`ANALYZED`  
> 范围：Physical PCA registration、Firmware legacy actuator aliases、official retained URDF branch 与 project canonical closed-chain simulation asset 的 identity cross-validation。

## 1. Engineering Question

PCA channel、real servo alias、canonical Servo、canonical Sim Hip Joint 与 Outer/Inner branch 是否形成唯一且可追溯的 identity chain，同时保持 12-dimensional action ordering 与 M2 frozen physics semantics？

## 2. Evidence Set

### Physical / Documentation

- `[[E-HW-002#p01]]` — PCA9685 eight-channel hardware topology.
- `[[E-FW-003#p03-five-bar-inverse-kinematics]]` — firmware function parameters and channel writes.

### Simulation / Validation

- `[[E-SIM-001#P03]]` — 20 tree revolute joints, 12 active and 8 passive partition.
- `[[E-SIM-003#P03]]` — PhysX closure revolute construction and body relation.
- `[[E-VAL-001#P01]]` — canonical actuator group and action-space static validation.

## 3. Cross-Validation Matrix

| 对照维度 | 涉及证据 Part | 比对状态 | 分析与工程说明 |
|---|---|---|---|
| PCA ↔ Firmware channel write | `E-HW-002#p01` vs `E-FW-003#p03` | VERIFIED | PCA1–PCA8 and the eight firmware parameter names match the frozen channel table. |
| Firmware alias ↔ canonical Servo | `E-FW-003#p03` vs registry | VERIFIED | `servoRightRear→FR_Outer_Servo`, `servoRightFront→FR_Inner_Servo`, `servoLeftRear→FL_Outer_Servo`, `servoLeftFront→FL_Inner_Servo`, and the four rear aliases are recorded as SOURCE_ALIAS. |
| Canonical Servo ↔ canonical Hip Joint | registry vs `E-SIM-001#P03` | VERIFIED | Outer Servo actuates Outer Hip; Inner Servo actuates Inner Hip. Actuation state is metadata and is not encoded in joint identity. |
| Canonical branch ↔ legacy M1/M2 | raw source vs registry | CONSISTENT | M1/M2 are retained only as historical/source aliases; current code uses Outer/Inner. |
| Canonical Wheel Motor ↔ Wheel Joint | `E-M1-002#P02/P04` vs `E-SIM-001#P05` | VERIFIED | Four physical Wheel command identities and the canonical Wheel Joints are uniquely linked; powered +/- raw behavior and zero were observed. |
| Canonical Closure Joint ↔ loop-cut/PhysX | `E-SIM-001#P02` vs `E-SIM-003#P03-P04` | VERIFIED | URDF omits the loop edge; closed USD restores a revolute joint with `excludeFromArticulation=true`. |

## 4. Canonical identity table

| PCA | Canonical Servo | Canonical Sim Joint | Legacy Real | Legacy Sim |
|---|---|---|---|---|
| PCA1 | `FR_Outer_Servo` | `FR_Outer_Hip_Joint` | `servoRightRear` | `FR_thigh_joint` |
| PCA2 | `FR_Inner_Servo` | `FR_Inner_Hip_Joint` | `servoRightFront` | `FR_M2_joint` |
| PCA3 | `FL_Inner_Servo` | `FL_Inner_Hip_Joint` | `servoLeftFront` | `FL_M2_joint` |
| PCA4 | `FL_Outer_Servo` | `FL_Outer_Hip_Joint` | `servoLeftRear` | `FL_thigh_joint` |
| PCA5 | `RL_Outer_Servo` | `RL_Outer_Hip_Joint` | `servoBackRightRear` | `RL_thigh_joint` |
| PCA6 | `RL_Inner_Servo` | `RL_Inner_Hip_Joint` | `servoBackRightFront` | `RL_M2_joint` |
| PCA7 | `RR_Inner_Servo` | `RR_Inner_Hip_Joint` | `servoBackLeftFront` | `RR_M2_joint` |
| PCA8 | `RR_Outer_Servo` | `RR_Outer_Hip_Joint` | `servoBackLeftRear` | `RR_thigh_joint` |

Wheel identity is branch-independent: `{LEG}_Wheel_Motor → {LEG}_Wheel_Joint`. Closure identity is `{LEG}_Closure_Joint`; `W2` is a source/frame alias.

## 5. Engineering Conclusion

- **SUPPORTED**：PCA1–PCA8 map uniquely to the eight canonical Servo identities above; the corresponding Sim Hip Joint is deterministic from URDF parent/child and actuator partition.
- **SUPPORTED**：the active action set remains 12 entries: Outer Hip group, Inner Hip group, then Wheel group; passive knees and Closure Joints remain outside policy action space.
- **INFERRED**：firmware parameter names describe physical servo registration aliases, while command sign, zero, scale, and feedback remain calibration properties.
- **SUPPORTED**：four Wheel_Motor identities and controller routes are frozen by `E-M1-002#P02/P04`.
- **UNRESOLVED**：absolute forward-positive and feedback sign remain Deployment/M3 properties; this Topic does not infer them.

## 6. Conflicts and open questions

- **Q-01**: wheel identity is complete; only forward-positive/feedback sign remains outside M1.
- **Q-02**: keep registration-code claims under `T-HW-REG-001`; this migration does not infer a physical registration code.

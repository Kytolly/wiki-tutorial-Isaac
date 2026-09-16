---
id: E-M1-002
title: M1实机物理契约复审与Powered全通道回归
track: REAL_HARDWARE_CONTRACT
status: VALID
created: 2026-09-17
last_verified: 2026-09-17
sources:
- source_id: SRC-M1-REAUDIT-20260917
  type: GENERATED_REPORT
  path_or_url: doc/research/StackForceDog/M1_outcome/M1-hardware-ground-truth.md
  revision: 2026-09-17
- source_id: SRC-M3-POWERED-004-20260917
  type: PHYSICAL_MEASUREMENT
  path_or_url: doc/StackforceDog/M3-Outcome/artifacts/real-logs/M3_ELEVATED_DYNAMICS_DATASET_004_POWERED_REPRO_001/
  revision: 2026-09-17
epistemic_role: PHYSICAL_AND_AUDIT
---

# E-M1-002 — M1实机物理契约复审与Powered全通道回归

> **Links / 链接:** [Contents / 目录](#contents) · [中文](#chinese) · [English](#english) · [[evidence-registry]] · [[M1-Hardware-Ground-Truth]]

<a id="contents"></a>
## Contents / 目录

- [中文](#chinese)
- [English](#english)

<a id="chinese"></a>
## 中文

### E-M1-002#P01：Real physical mechanism contract

官方机械装配 Evidence `E-DOC-003#P02-P04`、电气/firmware Evidence `E-HW-002#P01/P04` 与 `E-FW-003#P03` 共同支持：真实机器人具有 `FR/FL/RL/RR` 四腿；每腿由 Outer 与 Inner 两条支链组成，每条支链包含 body-mounted active Servo Hip、被动 Knee 和末端 Calf，并在共享 Foot/Wheel assembly 处形成物理五杆闭环。每腿 Wheel_Motor 驱动车轮，内侧电机/联轴器驱动、外侧由轴件/轴承支撑。

### E-M1-002#P02：Canonical actuator and controller identity

PCA1-PCA8 依次为 `FR_Outer`, `FR_Inner`, `FL_Inner`, `FL_Outer`, `RL_Outer`, `RL_Inner`, `RR_Inner`, `RR_Outer` Servo。Wheel identity 为 rear local `M0=RL`, `M1=RR`，front CAN target1=`FR`, target2=`FL`。rear S3 (`Device 0x01`) 执行 normal IK 并写 PCA；前轮命令经 CAN `0x02` 到 front S3；两侧 S3 均经 `Serial2/SF_BLDC` 到 motor-side S1。

### E-M1-002#P03：Reference command boundary

冻结 reference command `[112,214,146,237,113,214,133,252] deg` 与 `servo_off=[-4,-5,+5,-7,-3,-5,-8,+8] deg`。前者是启动/返回姿态的 post-offset controller command，后者是每通道 firmware trim；两者均不是 mechanical `u0`、measured `q_real` 或 `qd_real`。

### E-M1-002#P04：Powered all-channel regression supersedes current blocker

`M3_ELEVATED_DYNAMICS_DATASET_004_POWERED_REPRO_001` 保留独立 immutable raw 与 Human observation。冻结 protocol 为 Servo `+/-10 deg`、Wheel `+/-2 raw`、700 ms command window，覆盖 PCA1-PCA8 与四个 canonical Wheel identity。Human Evidence 记录：Servo clearly visible bounded motion、Wheel clearly visible continuous rotation、正负 Wheel behavior clearly opposite、`SAFETY=NORMAL`、return normal、Wheel zero/stop normal，且无 large motion、jitter、binding 或 abnormal sound。

因此 2026-09-10 `E-CAL-001#P04` 的 ch7 non-return 仍是有效历史事件，但不再是当前 powered-actuation blocker。两个来源不合并、不删除：旧 source 描述当时失败，新 source 描述后续当前回归状态。

### E-M1-002#P05：Unresolved ownership boundary

- Servo absolute joint-positive polarity 与 Wheel chassis-forward sign 未由 Human 可靠标定，归 `DEPLOYMENT` action adapter。
- mechanical `u0`、Servo `q_real/qd_real` 归 `OPTIONAL_EXTERNAL_GROUND_TRUTH`。
- Wheel SI conversion、feedback response、delay/stiffness/damping/contact/friction 归 `M3_DYNAMICS`。
- PhysX closure/runtime 归 `M2_SIM_ASSET`。

这些项均不阻塞 `M1_PHYSICAL_CONTRACT` 的机构、身份与控制路径冻结。

<a id="english"></a>
## English

The re-audit freezes the real four-leg dual-branch five-bar mechanism, all twelve actuator identities, PCA mapping, Wheel routing, S3 ownership, and the reference/trim command boundary. The powered Dataset 004 reproduction provides later all-channel physical evidence with normal safety, return, and zero behavior. It supersedes the historical channel-7 event only as a current blocker; the older failure remains immutable provenance.

Absolute coordinate signs, mechanical zero, external joint state, wheel SI conversion, dynamics, and simulation closure retain separate ownership and are not inferred.

## 更新日志

- 2026-09-17：建立 M1 offline re-audit 与 powered all-channel regression 的原子 Evidence，保留历史 ch7 failure provenance 并清除其当前 blocker 状态。

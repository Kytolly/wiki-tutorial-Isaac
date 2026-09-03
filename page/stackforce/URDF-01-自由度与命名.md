# URDF-01-自由度与命名

> 本页属于：stackforce 机器狗实战（M2 URDF 实操）
> 前置知识：[[M2-URDF建模]]
> 预计阅读时间：15 分钟

## 🎯 为什么需要这个？

先建立"机器人骨架"，**不要急着处理 STL**。第一件事是确定真实机器狗到底有多少个运动刚体和自由度，并定死命名与坐标系——这是 URDF 最容易做错、后期最难修的部分。

## 阶段 1：确定刚体与自由度

按 Mini 模型，先假设每条腿：

```text
body
 │
 ├── hip joint
 ▼
upper_leg
 │
 ├── knee joint
 ▼
lower_leg
 │
 ├── wheel joint
 ▼
wheel
```

四条腿：

```text
                     base_link
          ┌────────┬────────┬────────┐
          │        │        │        │
         FL       FR       RL       RR
          │        │        │        │
        hip      hip      hip      hip
          ↓        ↓        ↓        ↓
       upper    upper    upper    upper
          │        │        │        │
       knee     knee     knee     knee
          ↓        ↓        ↓        ↓
       lower    lower    lower    lower
          │        │        │        │
       wheel    wheel    wheel    wheel
          ↓        ↓        ↓        ↓
        wheel    wheel    wheel    wheel
```

若实机确实如此：

```text
4 × (2 + 1) = 12 DOF
```

> 但这**必须以实机为准**。手动确认每条腿：有几个舵机/电机？哪些轴真的能转？转轴方向？wheel 是否独立驱动？有没有机械耦合？

## 第一份成果：Joint 表

**这张表确认之前，不写 URDF。**

| Joint | Parent | Child | Type | Axis |
|-------|--------|-------|------|------|
| FL_hip | base | FL_upper | revolute | 待确认 |
| FL_knee | FL_upper | FL_lower | revolute | 待确认 |
| FL_wheel | FL_lower | FL_wheel | continuous | 待确认 |
| FR_hip | base | FR_upper | revolute | 待确认 |
| ... | ... | ... | ... | ... |

## 阶段 2：统一坐标系（ROS 约定）

```text
              +Z
               ↑
               │
               │
               └────→ +X  Forward
              /
             /
           +Y  Left
```

即：

```text
+X = 机器人前方     +Y = 机器人左方     +Z = 机器人上方
```

四条腿固定命名：

```text
             FRONT
               +X
                ↑
       FL ○──────────○ FR
         │            │
 +Y ←    │  base_link │
         │            │
       RL ○──────────○ RR
```

- **FL = Front Left，FR = Front Right，RL = Rear Left，RR = Rear Right**

以后所有 joint / mesh / motor ID / Isaac Lab regex / observation / action 都统一这套命名，例如 `FL_hip_joint`、`FL_knee_joint`、`FL_wheel_joint`。

> 千万不要一部分叫 `LT`、另一部分叫 `front_left`、实机又叫 `motor_3`——后面 Sim-to-Real 会非常痛苦。

## ✏️ 小练习

**1.** 为什么"统一命名"要在最前面做？

<details>
<summary>查看答案</summary>

命名贯穿 joint/mesh/motor/regex/obs/action，后期改一处就牵一发动全身；Sim-to-Real 时命名不一致会直接对不上。
</details>

**2.** `continuous` 和 `revolute` 关节的区别？

<details>
<summary>查看答案</summary>

revolute 有角度上下限；continuous 可无限旋转（如轮子绕轴连续转）。
</details>

## 本章小结

- 先假设 12 DOF（4 腿 ×（髋+膝+轮）），但以实机为准。
- 做 Joint 表，确认前不写 URDF。
- 统一 ROS 坐标系（+X 前 / +Y 左 / +Z 上）与 FL/FR/RL/RR 命名。

## 下一步

- 上一页：[[M2-URDF建模]]
- 下一页：[[URDF-02-零件与腿部运动学]]
- 返回：[[Home]]

## 更新日志

- 2026-09-02：新增本页。来源：用户 URDF 建模路线（阶段 1–2）、ROS REP 103 坐标约定。

# M1-02-Joint-Map与单执行器

> 本页属于：stackforce 机器狗实战（M1 实操）
> 前置知识：[[M1-01-硬件清单与传感器]]
> 预计阅读时间：20 分钟

## 🎯 为什么需要这个？

Joint Map 是整个 M1 最重要的成果。做完它，再架起机器逐个 enable 执行器验证方向。

## M1.3 建立 Joint Map

最终做成（12 DOF = 2 腿关节 + 1 轮关节 × 4 腿）：

| Joint | Hardware ID | Zero | Positive Direction | Min | Max |
|-------|-------------|------|--------------------|-----|-----|
| FL_hip | ? | ? | ? | ? | ? |
| FL_knee | ? | ? | ? | ? | ? |
| FL_wheel | ? | — | forward | — | — |
| FR_hip | ? | ? | ? | ? | ? |
| FR_knee | ? | ? | ? | ? | ? |
| FR_wheel | ? | — | forward | — | — |
| RL_hip | ? | ? | ? | ? | ? |
| RL_knee | ? | ? | ? | ? | ? |
| RL_wheel | ? | — | forward | — | — |
| RR_hip | ? | ? | ? | ? | ? |
| RR_knee | ? | ? | ? | ? | ? |
| RR_wheel | ? | — | forward | — | — |

命名从现在就固定（FL=Front Left 等），URDF / Isaac Lab / 实机程序全部同一顺序：

```python
JOINT_NAMES = [
    "FL_hip", "FL_knee", "FL_wheel",
    "FR_hip", "FR_knee", "FR_wheel",
    "RL_hip", "RL_knee", "RL_wheel",
    "RR_hip", "RR_knee", "RR_wheel",
]
```

## M1.4 单执行器控制实验

机器**架起来，四轮离地**，一次只 enable 一个 actuator，其他保持安全状态。发非常小的位置变化：

```text
q_d = q_0 + 0.05 rad   →   观察方向
q_d = q_0 - 0.05 rad   →   观察方向
```

记录每个关节：

```text
FL_hip   +command → 实机向 ______ 转
         -command → 实机向 ______ 转
FL_knee  ...
FL_wheel ...
FR / RL / RR 依次做完
```

这一步与 URDF 对应：若确定 `FL_hip positive = 从机器人左侧观察逆时针`，那么 URDF 的 `<axis xyz="..."/>` 必须产生同样正方向。即：

```text
q_sim > 0  和  q_real > 0  必须表示同一个物理运动
```

## ✏️ 小练习

**1.** Joint Map 为什么是 M1 最重要成果？

<details>
<summary>查看答案</summary>

它把 Hardware ID / 零位 / 正方向 / 限位统一，是 URDF、Isaac Lab、实机程序三处一致性的唯一依据。
</details>

**2.** 单执行器实验为什么要架起来、四轮离地？

<details>
<summary>查看答案</summary>

避免机器人因动作落地/移动造成意外，只验证单个关节运动方向，安全。
</details>

## M1-1 源码基线结论（Actuator Map）

**8 路舵机**（PCA9685 channel；源码保留"前/后舵机"称呼，暂不命名为 hip/knee）：

| 逻辑位置 | channel | 源码变量 | servo_off | 物理关节语义 |
|----------|---------|----------|-----------|--------------|
| 左前-前舵机 | 3 | servoLeftFront | -5° | UNKNOWN |
| 左前-后舵机 | 4 | servoLeftRear | -7° | UNKNOWN |
| 右前-前舵机 | 2 | servoRightFront | +5° | UNKNOWN |
| 右前-后舵机 | 1 | servoRightRear | +3° | UNKNOWN |
| 右后-后舵机 | 7 | servoBackLeftFront | -8° | UNKNOWN |
| 右后-前舵机 | 8 | servoBackLeftRear | +8° | UNKNOWN |
| 左后-后舵机 | 6 | servoBackRightFront | -5° | UNKNOWN |
| 左后-前舵机 | 5 | servoBackRightRear | +3° | UNKNOWN |

驱动参数：PCA9685@0x40，PWM 50Hz，angle API 0–300°，pulse 500–2500μs，enable GPIO42，无反馈。`0–300°` 是 API 映射范围，**不等于** URDF joint limit。实际舵机型号、机械角度范围、关节零位、正方向仍 UNKNOWN（对应 U01–U04）。

**4 轮电机**：

| 物理轮 | BLDC | 所属控制器 | command sign | feedback sign |
|--------|------|-----------|--------------|---------------|
| 左后 | M0 | Device 0x01 | +1 | +1 |
| 右后 | M1 | Device 0x01 | -1 | -1 |
| 左前 | target2 发送 | Device 0x02 | +1(M3Dir) | UNKNOWN |
| 右前 | target1 发送 | Device 0x02 | -1(M4Dir) | UNKNOWN |

> **重要**：整机程序调用 `motors.setModes(4,4)`，底层 `SF_Motor.h` 定义 mode 4 = **TORQUE_MODE**（1=VELOCITY，2=FORCE_ANGLE，3=VEL_ANGLE）。即当前四轮 BLDC 底层是 torque mode，不能仅凭变量名"目标速度"误判。

## 本章小结

- Joint Map：12 行，Hardware ID/Zero/方向/限位。
- 固定 JOINT_NAMES 顺序。
- 架空后逐个执行器 ±0.05 rad 验证方向，保证 q_sim>0 与 q_real>0 同义。

## 下一步

- 上一页：[[M1-01-硬件清单与传感器]]
- 下一页：[[M1-03-控制接口与频率延迟]]
- 返回：[[Home]]

## 更新日志

- 2026-09-03：同步 `doc/research` M1-1 最新源码结论：舵机驱动参数补"实际型号/机械角度范围/关节零位/正方向 UNKNOWN（对应 U01–U04）"。来源：本地 `doc/research/02_actuator_map.md`。
- 2026-09-02：新增本页。来源：用户 M1 实操路线（M1.3–M1.4）。

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

## 本章小结

- Joint Map：12 行，Hardware ID/Zero/方向/限位。
- 固定 JOINT_NAMES 顺序。
- 架空后逐个执行器 ±0.05 rad 验证方向，保证 q_sim>0 与 q_real>0 同义。

## 下一步

- 上一页：[[M1-01-硬件清单与传感器]]
- 下一页：[[M1-03-控制接口与频率延迟]]
- 返回：[[Home]]

## 更新日志

- 2026-09-02：新增本页。来源：用户 M1 实操路线（M1.3–M1.4）。

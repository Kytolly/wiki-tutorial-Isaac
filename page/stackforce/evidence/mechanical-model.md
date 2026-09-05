# 机械模型证据（mechanical-model）

> 本页属于：stackforce 机器狗实战（evidence）
> 状态：CURRENT EVIDENCE（M2 拓扑审核的独立基线）

## 核心结论

- **[CONFIRMED]** 每条轮足是含 1 个机械闭环的**双支链机构**，不是 Mini 式单串联链。
- **[SUPPORTED]** 每条轮足：**5 个运动刚体、6 个转动连接、3 个独立控制量**；整机：**20 个运动刚体、24 个转动连接、4 个闭环、12 个独立控制量**。
- **[CONFIRMED_BY_ASSEMBLY]** `M = motor-side = inner branch`，`S = support-side = outer branch`。

```text
base
├─ hip_M(active) ─ thigh_M ─ elbow_M(passive) ─ lower_M ─ wheel_motor(active) ─┐
│                                                                               ├─ wheel
└─ hip_S(active) ─ thigh_S ─ elbow_S(passive) ─ lower_S ─ wheel_support(passive)┘
```

## 刚体分组

| 刚体 | 包含零件 | 状态 |
|------|----------|------|
| base_link | 主体、连接件、盖板、8 舵机壳体、外固定、舵机盖板、控制板 | CONFIRMED |
| thigh_M / thigh_S | 大腿 STL + 金属舵盘 + 紧固件 | CONFIRMED |
| lower_M | 电机侧小臂 + 轮电机定子 + 编码器 + 线束 | CONFIRMED |
| lower_S | 支承侧小臂 + 轮轴盖 + 轴承外圈 | SUPPORTED |
| wheel | 轮胎/轮体 + 联轴器 + 轮毂 + 电机转子 + 磁环 | SUPPORTED |

## Joint 清单（每条轮足）

| Joint | Parent→Child | 主动/被动 | 闭环边 | 状态 |
|-------|--------------|-----------|--------|------|
| hip_M | base→thigh_M | 主动（舵机） | 否 | CONFIRMED |
| elbow_M | thigh_M→lower_M | 被动 | 否 | CONFIRMED |
| wheel_motor | lower_M→wheel | 主动（轮电机） | 否 | CONFIRMED |
| hip_S | base→thigh_S | 主动（舵机） | 否 | CONFIRMED |
| elbow_S | thigh_S→lower_S | 被动 | 否 | CONFIRMED |
| wheel_support | lower_S→wheel | 被动同轴支承 | 是 | CONFIRMED |

## 名义几何

| 几何 | 值 | 状态 |
|------|----|------|
| thigh_M / thigh_S | 60 mm | SUPPORTED |
| lower_M / lower_S | 100 mm | SUPPORTED |
| L5（两 hip 投影间距） | 40 mm | SUPPORTED（仅二维投影） |
| 整机 | ≈375×215×105–205 mm，≈1.3 kg | SUPPORTED |

## 未解决项（关键）

- `Front/Rear` hip 与 `M/S` 支链的二选一对应：UNKNOWN
- 两个半车体到 base_link 的装配变换：UNKNOWN
- 两支链横向偏置、轮体几何：UNKNOWN
- 舵机零位/符号/限位、轮电机方向：M1_REQUIRED

## 更新日志

- 2026-09-03：由 `mechanical_model.md` 迁移为 evidence。

# 几何基线证据（geometry-baseline）

> 本页属于：stackforce 机器狗实战（evidence）
> 状态：CURRENT EVIDENCE（M2-03 几何审核基线）

## 冻结名义几何

| 项目 | 基线 | 状态 |
|------|------|------|
| thigh_M / thigh_S | 60 mm | SUPPORTED |
| lower_M / lower_S | 100 mm | SUPPORTED |
| 两 hip 二维投影间距 L5 | 40 mm | SUPPORTED（仅投影） |
| Mini tire 直径 / 轴向宽 | ≈66.0 / 29.9 mm | SUPPORTED（仅 wheel visual 候选） |

## 三维结构解释

M/S 两个大腿根**不是同一三维点**；真实机构不是"压成一张纸"的五连杆。正确三维闭环条件：

1. 两支链 wheel endpoint 在腿平面投影一致；
2. `wheel_motor` 与 `wheel_support` 轴方向平行；
3. 两轴线最短距离为 0（同一物理 wheel axis）。

不再使用错误条件 `p_M == p_S`（三维端点重合）。

## 闭环验证结果

- 对称 nominal pose 理论 closure residual = 0：PASS
- 10000 组随机姿态 sweep 最大残差 4.3e-14 mm：PASS
- 三维 wheel-axis 共线条件：PASS（几何约束层）

## 坐标与 Mesh→Link 基线

- `+X forward / +Y left / +Z up`（ROBOT_BASE）
- Link Frame：thigh origin=hip axis、lower origin=elbow axis、纵向 +X、revolute 无符号方向 +Y
- thigh/lower STL 主关节轴沿 raw +Z、杆长 raw +X → 统一 `R_link_mesh = Rx(-90°)`（几何约定，非 actuator 正方向）

## 已否决的候选

- `±76.5 mm` half-body longitudinal translation：**REJECTED**（见 archive）

## 更新日志

- 2026-09-03：由 `M2-4_final_report.md` 与 geometry CSV 迁移为 evidence。

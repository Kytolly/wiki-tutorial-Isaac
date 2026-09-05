# 来源清单证据（source-inventory）

> 本页属于：stackforce 机器狗实战（evidence）
> 状态：CURRENT EVIDENCE

## 证据基线

| ID | 资料 | 用途 | 状态 |
|----|------|------|------|
| Q-INSTALL | `1安装文档.pdf`（48 页） | 装配顺序、刚性固定、被动转轴、轮部支承 | CONFIRMED |
| Q-WIRING | `2接线文档.pdf` | FL/FR/RL/RR 布局、前/后舵机标签 | CONFIRMED |
| Q-DEBUG | `3调试文档.pdf` | 8 舵机布局/校零、轮电机方向调试 | CONFIRMED |
| Q-STL | `quadrupedal-wheeled-robot/Structure/` | 官方零件名称/数量/几何 | CONFIRMED |
| Q-CODE | `课程代码/lesson4_Gait/src/`（commit 8d7f79c） | 双支链 IK、名义杆长、8 舵机输出 | SUPPORTED |
| MINI-URDF | `bipedal_wheeled_robot/.../20250820_1.urdf` | 仅 URDF 格式/局部尺寸交叉检查 | SUPERSEDED（不可作四轮足 tree） |

## 状态定义

`CONFIRMED`（官方直接展示）/ `SUPPORTED`（≥2 项官方资料互证）/ `UNKNOWN`（资料不足）/ `M1_REQUIRED`（需实机确认）/ `SUPERSEDED`（被更高质量资产替代）/ `REJECTED`（已实测否决）。

## 更新日志

- 2026-09-03：由 `mini_vs_quadruped.md` 证据基线迁移为 evidence。

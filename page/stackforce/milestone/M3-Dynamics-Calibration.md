# M3 — Dynamics Calibration

## Objective

在真实四足轮腿机器人与仿真环境之间完成执行器动力学（刚度/阻尼/滞后）、电机特性曲线与地面接触物理参数的系统辨识与响应对齐，正式解除 `rl_ready = false` 边界锁定。

## Status

IN PROGRESS

## Progress

0 / 6 PASS (1 IN PROGRESS, 5 TODO)

## Gates

| Gate | Title | Status | Required Criteria | Passed | Next Action |
|---|---|---|---:|---:|---|
| [[M3-G01-激励冻结]] | 激励冻结 | **IN PROGRESS** | 4 / 4 | 2 | 冻结架空台架阶跃/正弦激励实验协议 |
| [[M3-G02-实机采样]] | 实机采样 | **TODO** | 3 / 3 | 0 | 架空连接真机采集高频遥测数据集 |
| [[M3-G03-舵机标定]] | 舵机标定 | **TODO** | 3 / 3 | 0 | 辨识舵机等效一阶传递函数与死区 |
| [[M3-G04-轮机标定]] | 轮机标定 | **TODO** | 3 / 3 | 0 | 辨识轮机相电阻与扭矩系数 Kt |
| [[M3-G05-接触标定]] | 接触标定 | **TODO** | 3 / 3 | 0 | 实测轮面摩擦角并配置 PhysX 材质 |
| [[M3-G06-响应对齐]] | 响应对齐 | **TODO** | 3 / 3 | 0 | Hold-out 独立测试集验证并解除 rl_ready=false |

## Current Foundation

M3 已经具备以下已完成的工程基础：

1. **Canonical Actuator Identity**: 已在 `T-ACT-001` 全面冻结。
2. **PCA ↔ Servo Identity**: PCA1~8 与四腿内外舵机映射明确。
3. **Servo ↔ Sim Hip Joint Identity**: 仿真关节与物理通道一一对应。
4. **Canonical Component Naming**: 全面落实在 `canonical-component-topology.md`。
5. **M2 Simulation Asset**: 已 8/8 PASS 冻结，具备 2400 步重力稳定基线。

## Current Focus

1. 细化并冻结阶跃与正弦激励实验协议（`M3-G01`）。
2. 对接实机，利用 `T02-实验日志` 标准 CSV 格式录制高频动态遥测序列。

## Dependencies

- `M1-Hardware-Ground-Truth`：实机基础控制链路。
- `M2-Simulation-Asset`：8/8 PASS 仿真闭环数字资产（已具备）。
- 待连接真实机器人以获取动态采样数据。

## Remaining Blockers / Evidence Debt

以下关键物理量尚未完成真实验证，严禁主观推导或硬编码伪数据：
- Servo mechanical zero / u0
- Servo physical command sign
- Servo command-to-angle scale
- Servo feedback capability
- Wheel physical registration
- Wheel SI scaling
- Real dynamics dataset
- Contact calibration

## Changelog / 更新日志

- 2026-09-15：重构为标准 Milestone 规范；修正状态为 IN PROGRESS；移除非法过期的 M2 阻断断言；列明已完成基础与待采集实机数据项。

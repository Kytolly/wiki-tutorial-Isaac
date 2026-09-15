# M4 — Locomotion

## Objective

在 Isaac Lab 环境下基于 Manager-Based 工作流完成四轮足机器人站立自平衡、抗扰与全向运动强化学习策略训练，导出推理权重。

## Status

TODO

## Progress

0 / 6 PASS (6 TODO)

## Gates

| Gate | Title | Status | Required Criteria | Passed | Next Action |
|---|---|---|---:|---:|---|
| [[M4-G01-环境验收]] | 环境验收 | **TODO** | 3 / 3 | 0 | 待 M3 动力学参数就绪后加载环境 |
| [[M4-G02-站立达标]] | 站立达标 | **TODO** | 2 / 2 | 0 | 训练原地自恢复站立策略 |
| [[M4-G03-平衡达标]] | 平衡达标 | **TODO** | 2 / 2 | 0 | 训练轮腿自平衡抗扰策略 |
| [[M4-G04-速度达标]] | 速度达标 | **TODO** | 2 / 2 | 0 | 训练前进/后退/差速转向线速度跟踪 |
| [[M4-G05-策略复现]] | 策略复现 | **TODO** | 2 / 2 | 0 | 多随机种子训练收敛一致性检验 |
| [[M4-G06-策略导出]] | 策略导出 | **TODO** | 2 / 2 | 0 | 导出 ONNX / JIT 并在机载平台评估延迟 |

## Current Focus

等待 M3 动力学标定完成并解除 `rl_ready = false` 门禁。

## Dependencies

- `M2-Simulation-Asset`（已就绪）。
- `M3-Dynamics-Calibration`（进行中，前置依赖）。

## Remaining Blockers / Evidence Debt

- 当前数字资产受 `rl_ready = false` 边界约束，动力学参数未标定前不得越级开展训练。

## Changelog / 更新日志

- 2026-09-15：重构为标准 Milestone 规范；修正时序状态为 TODO；严格直接引用 G01~G06。

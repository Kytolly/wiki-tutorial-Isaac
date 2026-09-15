# M6 — Sim-to-Real

## Objective

实施 Sim-to-Real 真机部署，完成在线观测/动作对齐、软件安全联锁、影子推理、悬空驱动及真机着地平稳运动全流程闭环验证。

## Status

TODO

## Progress

0 / 8 PASS (8 TODO)

## Gates

| Gate | Title | Status | Required Criteria | Passed | Next Action |
|---|---|---|---:|---:|---|
| [[M6-G01-观测对齐]] | 观测对齐 | **TODO** | 2 / 2 | 0 | 统一真机传感预处理与仿真张量 |
| [[M6-G02-动作对齐]] | 动作对齐 | **TODO** | 2 / 2 | 0 | 验证策略 12 维动作分发映射 |
| [[M6-G03-安全联锁]] | 安全联锁 | **TODO** | 3 / 3 | 0 | 部署倾覆切断、通信看门狗与急停守护 |
| [[M6-G04-影子推理]] | 影子推理 | **TODO** | 2 / 2 | 0 | 机载计算机实测 100Hz 影子推理 |
| [[M6-G05-悬空执行]] | 悬空执行 | **TODO** | 2 / 2 | 0 | 架空驱动验证电机实际旋转方向 |
| [[M6-G06-实机站立]] | 实机站立 | **TODO** | 2 / 2 | 0 | 四轮着地自平衡站立验证 |
| [[M6-G07-实机平衡]] | 实机平衡 | **TODO** | 2 / 2 | 0 | 地面人工轻度推扰自平衡测试 |
| [[M6-G08-实机运动]] | 实机运动 | **TODO** | 3 / 3 | 0 | 速度指令平稳全向移动与转向终验 |

## Current Focus

待 M1 硬件安全解封与 M5 鲁棒性策略导出后启动真机联调。

## Dependencies

- `M1-Hardware-Ground-Truth`（硬件健康与安全回路）。
- `M4-Locomotion` / `M5-Robustness`（部署就绪的策略模型）。

## Remaining Blockers / Evidence Debt

- 实机部署需前置完成动力学标定与鲁棒策略训练。

## Changelog / 更新日志

- 2026-09-15：重构为标准 Milestone 规范；严格直接引用 G01~G08。

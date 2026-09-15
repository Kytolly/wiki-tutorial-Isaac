# M5 — Robustness

## Objective

开展质量分布、摩擦系数、传感器噪声与动作时延的域随机化（Domain Randomization）训练，提高步态策略在非结构化复杂地形上的抗扰鲁棒性与泛化能力。

## Status

TODO

## Progress

0 / 6 PASS (6 TODO)

## Gates

| Gate | Title | Status | Required Criteria | Passed | Next Action |
|---|---|---|---:|---:|---|
| [[M5-G01-范围冻结]] | 范围冻结 | **TODO** | 2 / 2 | 0 | 冻结物理参数随机化采样区间 |
| [[M5-G02-参数随机]] | 参数随机 | **TODO** | 2 / 2 | 0 | 注入刚体质量与转动惯量扰动 |
| [[M5-G03-观测扰动]] | 观测扰动 | **TODO** | 2 / 2 | 0 | 注入真实传感器噪声与零漂 |
| [[M5-G04-延迟注入]] | 延迟注入 | **TODO** | 2 / 2 | 0 | 模拟总线传输延迟与抖动 |
| [[M5-G05-推扰恢复]] | 推扰恢复 | **TODO** | 2 / 2 | 0 | 突加冲量推扰下平衡恢复验证 |
| [[M5-G06-泛化达标]] | 泛化达标 | **TODO** | 2 / 2 | 0 | 斜坡、台阶与异质摩擦地面通行验证 |

## Current Focus

待 M4 基础步态与自稳策略训练收敛后启动。

## Dependencies

- `M4-Locomotion`（基础策略模型就绪）。

## Remaining Blockers / Evidence Debt

- 前置 Milestone 尚未完成。

## Changelog / 更新日志

- 2026-09-15：重构为标准 Milestone 规范；严格直接引用 G01~G06。

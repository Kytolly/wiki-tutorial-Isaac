# M4 — Locomotion

## Goal

让机器人在仿真中完成定义好的站立、平衡和运动任务。

## Progress

- [ ] [[M4-G01-环境验收]] — IN PROGRESS
- [ ] [[M4-G02-站立达标]] — TODO
- [ ] [[M4-G03-平衡达标]] — TODO
- [ ] [[M4-G04-速度达标]] — TODO
- [ ] [[M4-G05-策略复现]] — TODO
- [ ] [[M4-G06-策略导出]] — TODO

Progress: 0 / 6 Gates PASS

## Current TODO

- [ ] 用冻结的 M2/M3 baseline 完成环境 smoke test。
- [ ] 先验收 stand，再扩展 balance、velocity tracking 和轮足协调。
- [ ] 固定评测场景、指标、checkpoint 和导出格式。

## Blockers

- M2/M3 尚未完成，当前训练结果不能作为最终 locomotion 证据。
- `sf_quad` 的 Manager-Based 配置仍引用 Cartpole 模板；当前 StackForce 任务以 Direct 实现为主。

## Exit Criteria

- 六个 Gate 全部 PASS。
- 规定的仿真运动任务达到明确性能阈值。
- 固定 checkpoint 能在干净环境中复现评测结果。

## Status

IN PROGRESS

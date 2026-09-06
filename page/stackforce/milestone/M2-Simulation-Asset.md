# M2 — Simulation Asset

## Goal

建立与真实机器人结构一致、物理属性完备、可被 Isaac Sim 与 `sf_quad` 使用的数字机器人资产。

## Progress

- [ ] [[M2-G01-来源冻结]] — IN PROGRESS
- [ ] [[M2-G02-拓扑对齐]] — IN PROGRESS
- [ ] [[M2-G03-几何对齐]] — IN PROGRESS
- [ ] [[M2-G04-坐标对齐]] — BLOCKED
- [ ] [[M2-G05-惯性完备]] — BLOCKED
- [ ] [[M2-G06-碰撞可用]] — TODO
- [ ] [[M2-G07-关节可动]] — TODO
- [ ] [[M2-G08-Lab载入]] — IN PROGRESS

Progress: 0 / 8 Gates PASS

## Current TODO

- [ ] 完成 `sf_robot` provenance、拓扑、几何和闭环表达审核。
- [ ] 用 M1 的实测质量、限位和坐标结果替换候选资产中的待定值。
- [ ] 对 `sf_quad` 资产载入、碰撞和关节运动做无头验证。

## Blockers

- M1 的关节标定、尺寸和质量数据尚未完成。
- `sf_robot.usda` 当前只有 visual load 证据，不能替代物理验证。

## Exit Criteria

- 八个 Gate 全部 PASS。
- 一个明确版本的资产成为 M3/M4 的 simulation baseline。
- baseline 的拓扑、坐标、质量、碰撞、关节和接口证据可追溯。

## Status

IN PROGRESS

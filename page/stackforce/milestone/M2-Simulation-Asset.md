# M2 — Simulation Asset

## Goal

建立与真实机器人结构一致、物理属性完备、可被 Isaac Sim 与 `sf_quad` 使用的数字机器人资产。

## Progress

- [x] [[M2-G01-来源冻结]] — PASS
- [x] [[M2-G02-拓扑对齐]] — PASS
- [x] [[M2-G03-几何对齐]] — PASS
- [x] [[M2-G04-坐标对齐]] — PASS
- [x] [[M2-G05-惯性完备]] — PASS
- [x] [[M2-G06-碰撞可用]] — PASS
- [x] [[M2-G07-关节可动]] — PASS
- [x] [[M2-G08-Lab载入]] — PASS

Progress: 8 / 8 Gates PASS

## Completed

- [x] 完成 `sf_robot` provenance、reduced topology、geometry、coordinate 和 inertial audit。
- [x] 完成 collision、gravity settle、四轮接地、滚动和 joint mobility runtime 验证。
- [x] 完成 Direct 与 Manager-Based 的 N=1/N=16 Gym/Isaac Lab lifecycle 验证。

## Boundary

- M2 PASS 冻结的是官方 reduced serial training model，不表示与真实 five-bar topology 动力学等价。
- M1 实测质量、关节零位/限位和执行器响应仍是 M3/M6 的输入，不回退 M2 的资产内部验收。
- inertia/friction/actuator 的真实标定与 Sim2Real 尚未完成。

## Exit Criteria

- 八个 Gate 全部 PASS。
- 一个明确版本的资产成为 M3/M4 的 simulation baseline。
- baseline 的拓扑、坐标、质量、碰撞、关节和接口证据可追溯。

## Status

PASS

## 更新日志

- 2026-09-08：同步 M2-G01–G08 outcome；M2 以 8/8 Gates PASS 收口。

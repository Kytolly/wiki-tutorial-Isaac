# M2-G08 Lab载入

## Goal

证明候选资产能被 `sf_quad` 的 Isaac Lab 任务正确载入、索引和执行最小动作。

## Why

Isaac Sim 可加载不代表训练环境的 asset path、joint mapping、reset 和 observation 合同正确。

## Topics

- [[M2-T06-实验室接入]]

## Known Facts

- Direct 与 Manager-Based 任务均已通过 Gym registration、config resolution、`gym.make()`、正确 `sf_robot` asset、reset/step/close 生命周期和 N=1/N=16 验证。
- Direct 的 12-action / 48-observation contract 与 vectorized action isolation 已通过。
- Manager-Based 的 Cartpole scene residue 与 reward API 迁移问题已经修复并验证，当前为 12-action / 48-observation StackForce 环境。

## Completed

- [x] 验证正式 Gym / Isaac Lab 入口与配置解析。
- [x] 验证 Direct 和 Manager-Based 的 N=1/N=16 lifecycle。
- [x] 验证 Direct vectorized action isolation 和 Manager 初始化。

## Acceptance Criteria

- [x] Direct 与 Manager-Based 均能无错误创建、reset、step 和 close。
- [x] 两条工作流的 12 actions / 48 observations 合同一致。
- [x] N=1/N=16 lifecycle 与 Direct vectorized action isolation 通过。

## Evidence

- `sf_quad/source/sf_quad/sf_quad/tasks/direct/sf_quad/`
- `doc/StackForceDog/M2_outcome/M2-G08.md`

## Status

PASS

## 更新日志

- 2026-09-08：同步 M2-G08 outcome，Direct 与 Manager-Based Lab 接入验收通过。

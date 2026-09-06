# M2-G08 Lab载入

## Goal

证明候选资产能被 `sf_quad` 的 Isaac Lab 任务正确载入、索引和执行最小动作。

## Why

Isaac Sim 可加载不代表训练环境的 asset path、joint mapping、reset 和 observation 合同正确。

## Topics

- [[M2-T06-实验室接入]]

## Known Facts

- `sf_quad` Direct 任务注册为 `Template-Sf-Quad-Direct-v0`。
- Direct 配置声明 12 actions 和 48 observations。
- Manager-Based 配置仍使用 Cartpole 资产，不能作为 StackForce 接入证据。

## TODO

- [ ] 运行 `list_envs`、reset 和无头 smoke test。
- [ ] 核对 joint name resolution、动作顺序和传感器路径。

## Acceptance Criteria

- [ ] 任务能在目标环境中无错误创建和 reset。
- [ ] 12 个动作和 observation shape 与接口文档一致。
- [ ] 零动作或最小动作运行达到规定步数并保存日志。

## Evidence

- `sf_quad/source/sf_quad/sf_quad/tasks/direct/sf_quad/`
- 待补 `sf_quad` 运行日志。

## Status

IN PROGRESS

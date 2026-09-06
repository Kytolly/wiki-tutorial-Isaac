# M3 — Dynamics Calibration

## Goal

让仿真机器人在相同输入下呈现与实机足够接近的动态响应。

## Progress

- [ ] [[M3-G01-激励冻结]] — TODO
- [ ] [[M3-G02-实机采样]] — TODO
- [ ] [[M3-G03-舵机标定]] — BLOCKED
- [ ] [[M3-G04-轮机标定]] — BLOCKED
- [ ] [[M3-G05-接触标定]] — TODO
- [ ] [[M3-G06-响应对齐]] — TODO

Progress: 0 / 6 Gates PASS

## Current TODO

- [ ] 固定关节与轮子的同输入实验协议。
- [ ] 建立同步的实机和仿真数据记录。
- [ ] 定义响应误差指标与 PASS 阈值。

## Blockers

- M1 尚未提供完整的指令量程、频率、延迟和质量基线。
- M2 尚未冻结可运行的 simulation asset。

## Exit Criteria

- 六个 Gate 全部 PASS。
- 关键关节和轮子的响应误差达到预先定义的阈值。
- 标定参数、数据和比较脚本可复现。

## Status

TODO

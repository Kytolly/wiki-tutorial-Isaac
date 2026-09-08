# M1 — Hardware Ground Truth

## Goal

建立能够准确、可复现描述真实 StackForce 机器人的硬件基线。

## Progress

- [ ] [[M1-G01-硬件清点]] — IN PROGRESS
- [ ] [[M1-G02-传感器映射]] — IN PROGRESS
- [ ] [[M1-G03-执行器映射]] — BLOCKED（静态合同完成，待真机 identity）
- [ ] [[M1-G04-关节标定]] — BLOCKED（静态合同完成，待 firmware baseline 与真机标定）
- [ ] [[M1-G05-指令定性]] — IN PROGRESS
- [ ] [[M1-G06-控制测频]] — IN PROGRESS（静态时序完成）
- [ ] [[M1-G07-延迟测量]] — IN PROGRESS（静态路径完成）
- [ ] [[M1-G08-尺寸测量]] — IN PROGRESS（名义尺寸完成）
- [ ] [[M1-G09-质量测量]] — IN PROGRESS（质量先验完成）
- [ ] [[M1-G10-停机验证]] — BLOCKED（P0 安全缺口）

Progress: 0 / 10 Gates PASS

## Current TODO

- [x] 完成 G01–G10 的源码级静态合同与验收边界审计。
- [ ] 冻结目标 firmware 的构建、烧录和只读启动基线。
- [ ] 完成传感器/执行器注册、关节标定、尺寸、质量、频率与延迟实测。
- [ ] 关闭 G10 的 command timeout、last-command persistence 和 runtime stop-test P0 缺口。

## Blockers

- Firmware Baseline 尚未冻结，首次主动关节测试不得开始。
- 当前没有实机测量记录，无法把静态合同升级为完整 Ground Truth。
- `flat=1` 固定 wheel target，CAN/PPM/Serial2 缺少已证明的统一 timeout/last-command 清零机制；G10 PASS 前不得进行正常 locomotion。

## Exit Criteria

- 十个 Gate 全部 PASS。
- 所有硬件、传感器、执行器和通信字段都有来源或测量证据。
- U01–U17 不再有未归属的 UNKNOWN。

## Status

IN PROGRESS

## 更新日志

- 2026-09-08：同步 M1-G01–G10 静态审计；总 PASS 保持 0/10，并记录 G10 P0 安全缺口。

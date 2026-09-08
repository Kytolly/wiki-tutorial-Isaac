# Wiki 状态

## Scope

- NVIDIA Isaac Sim / Isaac Lab 学习教程。
- StackForce 四轮足项目的 Milestone、Gate、Topic、Evidence 和 Archive。
- 内容源：`doc/wiki/page/`。
- 实现真源：`sf_quad/`。
- 参考工程：`Stackforce-simready-111-isaac-lab/`，read-only reference。

## StackForce Status

| Milestone | PASS | Total | Status |
|---|---:|---:|---|
| M1 Hardware Ground Truth | 0 | 10 | IN PROGRESS |
| M2 Simulation Asset | 8 | 8 | PASS |
| M3 Dynamics Calibration | 0 | 6 | TODO |
| M4 Locomotion | 0 | 6 | IN PROGRESS |
| M5 Robustness | 0 | 6 | TODO |
| M6 Sim-to-Real | 0 | 8 | TODO |

总进度：8 / 44 Gates PASS。

## Current Findings

- M1 的 10 个 Gate 均已有静态审计进展，但 firmware baseline、关节/传感器注册、时序、尺寸、质量和 stop test 仍缺实机验证。
- M1-G10 发现 P0 安全缺口：`flat=1` 固定 wheel target，CAN/PPM/Serial2 路径缺少已证明的统一 timeout/last-command 清零机制。
- M2 已完成 8/8 Gates：reduced asset 的来源、拓扑边界、几何、坐标、惯性、碰撞、关节可动与 Lab integration 均 PASS。
- Direct 与 Manager-Based 均已通过 N=1/N=16 lifecycle；Manager-Based 的 Cartpole residue 与 reward API 迁移问题已修复验证。
- 参考工程的日志和 checkpoint 不计入 `sf_quad` Gate PASS。

## Status Vocabulary

事实等级：`KNOWN` / `MEASURED` / `VERIFIED` / `INFERRED` / `ASSUMED` / `UNKNOWN`。

Gate 状态：`TODO` / `IN PROGRESS` / `BLOCKED` / `PASS`。

只有 Acceptance Criteria 全部满足且 Evidence 可访问时才允许 PASS。

## Last Update

- 2026-09-08：同步 M1-T01–T05 与 M2-T01–T07，清理旧 evidence 路径并消除与 M2 PASS 冲突的专题描述。
- 2026-09-08：为 M1/M2 Milestone Dashboard 增加逐 Gate Evidence Snapshot、PASS 边界和剩余验收项。
- 2026-09-08：同步 `doc/StackForceDog/M1_outcome` 与 `M2_outcome`；M2 以 8/8 PASS 收口，总进度更新为 8/44，并记录 M1-G10 P0 安全缺口。
- 2026-09-06：按 Milestone → Gate → Topic → Acceptance → Evidence 重构 StackForce 信息架构，建立六个 Dashboard、44 个原子 Gate、21 个 Topic 和迁移归档。

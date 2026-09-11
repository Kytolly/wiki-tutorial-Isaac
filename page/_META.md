# Wiki 状态

## Scope

- wiki_mode: `project-docs`
- audience: StackForce 开发、实验与验收人员
- evidence_policy: 重要状态与接口 claim 必须追踪到源码、outcome 或实验产物
- completeness_policy: architecture/interface/safety contract 完整；未知项保留为 evidence debt
- last_source_audit: 2026-09-11
- last_coverage_audit: 2026-09-11
- NVIDIA Isaac Sim / Isaac Lab 学习教程。
- StackForce 四轮足项目的 Milestone、Gate、Topic、Evidence 和 Archive。
- 内容源：`doc/wiki/page/`。
- 实现真源：`sf_quad/`。
- 参考工程：`Stackforce-simready-111-isaac-lab/`，read-only reference。

## StackForce Status

| Milestone | Closed Gates | Total | Status |
|---|---:|---:|---|
| M1 Hardware Ground Truth | 7 | 10 | BLOCKED |
| M2 Simulation Asset | 8 | 8 | PASS |
| M3 Dynamics Calibration | 0 | 6 | TODO |
| M4 Locomotion | 0 | 6 | IN PROGRESS |
| M5 Robustness | 0 | 6 | TODO |
| M6 Sim-to-Real | 0 | 8 | TODO |

总进度：15 / 44 Gates closed。

## Current Findings

- M1 已完成两次可审计架空 session：G01/G02 PASS，G05–G09 在明确 evidence debt 下关闭，G03/G04/G10 BLOCKED。
- current source 已关闭旧 `flat=1` 与 PPM/CAN freshness 风险；当前最高优先级 blocker 是 ch7 在 firmware return/STOP 后物理回中失败。
- 修复 ch7/ch8 前 actuator rail 必须断电；离线 interface 与首版 kinematic Reference-B 可继续。
- M2 已完成 8/8 Gates：reduced asset 的来源、拓扑边界、几何、坐标、惯性、碰撞、关节可动与 Lab integration 均 PASS。
- Direct 与 Manager-Based 均已通过 N=1/N=16 lifecycle；Manager-Based 的 Cartpole residue 与 reward API 迁移问题已修复验证。
- 参考工程的日志和 checkpoint 不计入 `sf_quad` Gate PASS。

## Status Vocabulary

事实等级：`KNOWN` / `MEASURED` / `VERIFIED` / `INFERRED` / `ASSUMED` / `UNKNOWN`。

Gate 状态：`TODO` / `IN PROGRESS` / `BLOCKED` / `PASS`；`PASS WITH EVIDENCE DEBT` 表示最低 acceptance 已满足，但保留明确、不影响当前 Gate 关闭的精度或保真度债务。

只有 Acceptance Criteria 全部满足且 Evidence 可访问时才允许 PASS。

## Last Update

- 2026-09-11：同步 M1 outcome 与现场产物；M1 更新为 7/10 closed、总进度 15/44，并冻结 ch7 安全 blocker。
- 2026-09-08：同步 M1-T01–T05 与 M2-T01–T07，清理旧 evidence 路径并消除与 M2 PASS 冲突的专题描述。
- 2026-09-08：为 M1/M2 Milestone Dashboard 增加逐 Gate Evidence Snapshot、PASS 边界和剩余验收项。
- 2026-09-08：同步 `doc/StackForceDog/M1_outcome` 与 `M2_outcome`；M2 以 8/8 PASS 收口，总进度更新为 8/44，并记录 M1-G10 P0 安全缺口。
- 2026-09-06：按 Milestone → Gate → Topic → Acceptance → Evidence 重构 StackForce 信息架构，建立六个 Dashboard、44 个原子 Gate、21 个 Topic 和迁移归档。

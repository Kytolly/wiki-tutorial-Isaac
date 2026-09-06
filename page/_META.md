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
| M2 Simulation Asset | 0 | 8 | IN PROGRESS |
| M3 Dynamics Calibration | 0 | 6 | TODO |
| M4 Locomotion | 0 | 6 | IN PROGRESS |
| M5 Robustness | 0 | 6 | TODO |
| M6 Sim-to-Real | 0 | 8 | TODO |

总进度：0 / 44 Gates PASS。

## Current Findings

- M1 已有较完整源码级 hardware audit，但关节、传感器、时序、尺寸和质量仍缺实机验证。
- M2 已有机械拓扑和几何证据；`sf_robot.usda` 仅 visual load PASS，物理行为未完成验收。
- M4 的 `sf_quad` Direct 环境已有代码实现，但没有当前项目自己的运行与评测日志。
- `sf_quad` Manager-Based 配置仍引用 Cartpole 模板，不能作为 StackForce 环境证据。
- 参考工程的日志和 checkpoint 不计入 `sf_quad` Gate PASS。

## Status Vocabulary

事实等级：`KNOWN` / `MEASURED` / `VERIFIED` / `INFERRED` / `ASSUMED` / `UNKNOWN`。

Gate 状态：`TODO` / `IN PROGRESS` / `BLOCKED` / `PASS`。

只有 Acceptance Criteria 全部满足且 Evidence 可访问时才允许 PASS。

## Last Update

2026-09-06：按 Milestone → Gate → Topic → Acceptance → Evidence 重构 StackForce 信息架构，建立六个 Dashboard、44 个原子 Gate、21 个 Topic 和迁移归档。

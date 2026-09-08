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

## Evidence Snapshot

M2 的 PASS 表示数字资产已经像一辆完成台架检查的样车：内部结构与运行接口可复现，但它还不是实机动力学的等比例替身。

| Gate | 关键证据 | PASS 边界 |
|---|---|---|
| [[M2-G01-来源冻结]] | 官方机器人资料、四轮足仓库、SimReady / Isaac Lab 候选包和当前实现边界 | 冻结 provenance，不证明资产物理正确性 |
| [[M2-G02-拓扑对齐]] | 真实双支链闭环与每腿 2R + wheel 的 reduced serial model 已逐项对照 | 控制维数同为 12，不代表机械拓扑等价 |
| [[M2-G03-几何对齐]] | URDF、wheel mesh、60/100 mm firmware five-bar 参数与 gait 工作区交叉核对 | 冻结名义 reduced geometry，不替代本机实测 |
| [[M2-G04-坐标对齐]] | base/leg frame、joint axis、wheel direction、镜像与 velocity command 合同 | 不要求 serial coordinate 等同真实 servo coordinate |
| [[M2-G05-惯性完备]] | 质量为正、惯量对称正定、主惯量合法、四腿镜像和尺度检查通过 | 1.352539 kg 是 reduced asset 总质量，不是实机称重 |
| [[M2-G06-碰撞可用]] | spawn、gravity settle、4 轮接地、penetration 与 low-speed rolling 通过 | simplified collision/convex hull 当前可用，不证明真实接触参数 |
| [[M2-G07-关节可动]] | 12/12 inventory 与 actuator coverage；8/8 腿关节正负响应；4/4 轮可动 | ±1.20 rad 只证明 finite behavior，不证明 loaded tracking |
| [[M2-G08-Lab载入]] | Direct/Manager：Gym、config、make、reset/step/close、N=1/N=16 通过 | Direct vector isolation 已验；训练质量由 M4 验收 |

### 已修复并保留的迁移教训

- Manager-Based task 名称和 Gym 注册正确，不代表 scene asset 已从 Cartpole 完成迁移；必须检查实际 scene object。
- Direct reward 不能假设存在同名 Manager MDP API；RewardManager 初始化和 lifecycle 必须单独验证。

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

- 2026-09-08：新增逐 Gate Evidence Snapshot 与 Manager-Based 迁移教训。
- 2026-09-08：同步 M2-G01–G08 outcome；M2 以 8/8 Gates PASS 收口。

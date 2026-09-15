# M2 — Simulation Asset

## Objective

构建与实机完全对齐的闭链四足轮腿机器人单父树 URDF/USD 仿真数字资产，完成 PhysX 闭环副自动重构与 2400 步 CPU 悬空重力烟囱测试，确立驱动拓扑与仿真工程边界。

## Status

PASS

## Progress

8 / 8 PASS

## Gates

| Gate | Title | Status | Required Criteria | Passed | Next Action |
|---|---|---|---:|---:|---|
| [[M2-G01-来源冻结]] | 来源冻结 | **PASS** | 2 / 2 | 2 | 官方 CAD/STL 与图纸版本唯一锁定 |
| [[M2-G02-拓扑对齐]] | 拓扑对齐 | **PASS** | 3 / 3 | 3 | 29 Links, 28 Joints 严格单父树拓扑确立 |
| [[M2-G03-几何对齐]] | 几何对齐 | **PASS** | 3 / 3 | 3 | W1/W2 轴向偏置 -44.95mm、残差 < 1.83e-17m 机器校验通过 |
| [[M2-G04-坐标对齐]] | 坐标对齐 | **PASS** | 2 / 2 | 2 | 四腿底盘对称反射矩阵与单平面镜像绕向反转确立 |
| [[M2-G05-惯性完备]] | 惯性完备 | **PASS** | 2 / 2 | 2 | 29 构件质量大于零且惯性张量满足正定性 |
| [[M2-G06-碰撞可用]] | 碰撞可用 | **PASS** | 2 / 2 | 2 | 五杆闭环自碰撞过滤矩阵生效，初始位姿无穿模 |
| [[M2-G07-关节可动]] | 关节可动 | **PASS** | 3 / 3 | 3 | PhysX RevoluteJoint 注入，配置 excludeFromArticulation |
| [[M2-G08-Lab载入]] | Lab 载入 | **PASS** | 4 / 4 | 4 | 2400 步 CPU 悬空下沉测试 PASS (漂移 <= 0.0595mm) |

## Canonical Actuation Architecture

基于 Frozen Canonical Component Naming 合同，全机自由度与构件划分规范如下：

- **12 Actuated Tree Joints（主动驱动树关节）**：
  - 4 Outer Hip Joints (`{LEG}_Outer_Hip_Joint`)
  - 4 Inner Hip Joints (`{LEG}_Inner_Hip_Joint`)
  - 4 Wheel Joints (`{LEG}_Wheel_Joint`)
- **8 Passive Tree Joints（从动被动铰接）**：
  - 4 Outer Knee Joints (`{LEG}_Outer_Knee_Joint`)
  - 4 Inner Knee Joints (`{LEG}_Inner_Knee_Joint`)
- **4 Closure Joints（闭环运动学约束副）**：
  - 4 腿 `{LEG}_Closure_Joint`，在 Inner Calf 末端切断并在 USD 中作为 `PhysicsRevoluteJoint` 闭环重构，配置 `excludeFromArticulation = true`。

## Current Focus

保持 M2 仿真资产完全冻结状态，输出给 M3 进行执行器动力学与地面接触标定。

## Dependencies

- 全部门禁已通过自包含测试工具与 Isaac Sim 无头环境验证闭环。

## Remaining Blockers / Evidence Debt

- **Boundary Invariant**: 当前资产明确处于 `rl_ready = false` 状态（`E-VAL-002#P05`）。未完成执行器动力学标定（刚度/阻尼/力矩曲线）与真实地面接触摩擦标定前，严禁越级开展强化学习步态策略训练。

## Changelog / 更新日志

- 2026-09-15：重构为标准 Milestone 规范；规范化引用 G01~G08；全面采用 Canonical Component Naming 消除旧代号混用；明确 `rl_ready = false` 动力学边界。

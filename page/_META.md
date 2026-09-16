# Wiki 状态

## Scope

- wiki_mode: `project-docs`
- audience: StackForce 开发、实验与验收人员
- evidence_policy: 重要状态与接口 claim 必须追踪到源码、outcome 或实验产物，统一通过 [[evidence-registry]] 注册
- completeness_policy: architecture/interface/safety contract 完整；未知项保留为 evidence debt
- last_source_audit: 2026-09-14
- last_coverage_audit: 2026-09-14
- NVIDIA Isaac Sim / Isaac Lab 学习教程。
- StackForce 四轮足项目的 Milestone、Gate、Topic、Evidence 和 Archive。
- 内容源：`page/`。
- 实现真源：`$PROJECT_ROOT/sf_quad/`（便携路径，本地便利定位：`/home/kytolly/Project/IsaacProject/sf_quad/`）。
- 参考工程：`Stackforce-simready-111-isaac-lab/`，read-only reference。

## StackForce Macro Status（宏观研发路线）

| Milestone | Closed Gates | Total | Status |
|---|---:|---:|---|
| M1 Hardware Ground Truth | 10 | 10 | PASS_WITH_DECLARED_GAPS |
| M2 Simulation Asset | 8 | 8 | PASS |
| M3 Dynamics Calibration | 0 | 6 | TODO |
| M4 Locomotion | 0 | 6 | IN PROGRESS |
| M5 Robustness | 0 | 6 | TODO |
| M6 Sim-to-Real | 0 | 8 | TODO |

总进度：18 / 44 Gates closed；M1 physical contract is 10/10 PASS_WITH_DECLARED_GAPS。

## StackForce Closed-Link Asset Sub-Progression（闭链数字资产研发子阶段）

| 子阶段 | 名称与目标 | 核心证据 | 状态 |
|---|---|---|---|
| Sub-1 | Mechanical geometry identification（双支链五杆识别） | `E-MECH-001` | **PASS** |
| Sub-2 | FR canonical inner-chain registration（右前内链注册） | `E-ASSET-002` | **PASS** |
| Sub-3 | Four-leg inner-chain construction（四腿镜像与绕向） | `E-MECH-001` | **PASS** |
| Sub-4 | Eight-chain loop-cut URDF（29 links / 28 joints 单根树） | `E-ASSET-001` | **PASS** |
| Sub-5 | Closure-frame metadata / invariants（闭环元数据） | `E-ASSET-002` | **PASS** |
| Sub-6 | Isaac USD import + closure recovery（PhysX 闭环恢复） | `E-ASSET-003` | **PASS** |
| Sub-7 | Static asset validation（自动化静态全检） | `E-ASSET-004` | **PASS** |
| Sub-8 | Suspended-base physics smoke validation（悬空重力烟囱测试） | `E-PHYS-001`, `E-PHYS-002` | **PASS** |

## Current Findings & Validation Boundary

- **实机与硬件基线（M1）**：机构、12 个执行器身份、PCA/Wheel mapping 与 S3 控制关系已冻结；powered Dataset 004 reproduction 记录全通道 visible bounded response、正常 return/zero 与 NORMAL safety。历史 ch7 failure 保留在原 Evidence，但不再是当前 blocker；绝对 physical sign、mechanical u0 与 q_real 仍分属 Deployment/Optional Ground Truth。
- **闭链数字资产（M2/Simulation Asset）**：
  - 8/8 门禁全检 PASS；
  - 几何与拓扑：四腿内外八链几何对齐，URDF 保持严格单父树（29 links / 28 joints，唯一根 `base_link`，W2 显式 loop-cut 切断）；
  - 闭环约束：W1/W2 轴向偏置 $-44.950\text{ mm}$，径向共线残差 $< 1.83 \times 10^{-17}\text{ m}$，PhysX 闭环重构脚本已生成闭链 USD 并配置 `excludeFromArticulation=true`；
  - 静态校验：`validate_asset.py` 全检全绿通过；
  - 物理烟囱测试：CPU 悬空重力 2400 步（10 s @ 240 Hz）实测运动位移 0.0906 m，最大锚点漂移 0.0595 mm（$\le 0.060\text{ mm}$，远低于 1 mm 门禁），最大轴向角误差 $5.23 \times 10^{-6}\text{ rad}$；负对照禁用闭环副导致漂移 129 mm 崩溃（`E-PHYS-001`, `E-PHYS-002`）。
- **执行器与 RL 边界（BOUNDARY / NEXT）**：
  - **`rl_ready = false`**：当前资产尚未完成驱动器真实刚度/阻尼动力学标定，地面接触与步态控制尚未验收，严禁越级宣称已就绪。
- **自由度划分规范**：整机为 20 个树状转动关节（4 腿 $\times$ 5），12 个主动驱动（4 M1 + 4 M2 + 4 W1），8 个被动铰接（4 P1 + 4 P2），4 个 PhysX 闭环约束副（W2）；严禁表述为“20 自由度”。

## Status Vocabulary

事实等级：`KNOWN` / `MEASURED` / `VERIFIED` / `INFERRED` / `ASSUMED` / `UNKNOWN`。

里程碑状态：`TODO` / `IN PROGRESS` / `BLOCKED` / `PASS` / `NEXT`。

只有 Acceptance Criteria 全部满足且 Evidence 可访问时才允许 PASS。

## Last Update

- 2026-09-17：依据 E-M1-002 更新 M1 为 10/10 PASS_WITH_DECLARED_GAPS；历史 ch7 failure 保留为 provenance，解除其当前 blocker 状态。
- 2026-09-13：根据真实交付物（URDF、USD、`closure_frames.json`、`validate_asset.py`、`recover_closed_loops.py`）确立静态门禁 PASS 与动态验证边界。
- 2026-09-11：同步 M1 两次架空实机 session；当时记录 ch7 powered-actuation blocker，现由后续 E-M1-002 保留为历史 provenance。
- 2026-09-08：同步 M1-T01–T05 与 M2-T01–T07，清理旧 evidence 路径并消除与 M2 PASS 冲突的专题描述。
- 2026-09-08：为 M1/M2 Milestone Dashboard 增加逐 Gate Evidence Snapshot、PASS 边界和剩余验收项。
- 2026-09-08：同步 `doc/StackForceDog/M1_outcome` 与 `M2_outcome`；M2 以 8/8 PASS 收口，总进度更新为 8/44，并记录 M1-G10 P0 安全缺口。

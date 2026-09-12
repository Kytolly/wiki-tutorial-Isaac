# Wiki 状态

## Scope

- wiki_mode: `project-docs`
- audience: StackForce 开发、实验与验收人员
- evidence_policy: 重要状态与接口 claim 必须追踪到源码、outcome 或实验产物
- completeness_policy: architecture/interface/safety contract 完整；未知项保留为 evidence debt
- last_source_audit: 2026-09-13
- last_coverage_audit: 2026-09-13
- NVIDIA Isaac Sim / Isaac Lab 学习教程。
- StackForce 四轮足项目的 Milestone、Gate、Topic、Evidence 和 Archive。
- 内容源：`page/`。
- 实现真源：`/home/kytolly/Project/IsaacProject/sf_quad/`。
- 参考工程：`Stackforce-simready-111-isaac-lab/`，read-only reference。

## StackForce Macro Status（宏观研发路线）

| Milestone | Closed Gates | Total | Status |
|---|---:|---:|---|
| M1 Hardware Ground Truth | 7 | 10 | BLOCKED |
| M2 Simulation Asset | 8 | 8 | PASS |
| M3 Dynamics Calibration | 0 | 6 | TODO |
| M4 Locomotion | 0 | 6 | IN PROGRESS |
| M5 Robustness | 0 | 6 | TODO |
| M6 Sim-to-Real | 0 | 8 | TODO |

总进度：15 / 44 Gates closed。

## StackForce Closed-Link Robot Milestones（闭链数字资产高层里程碑）

| 里程碑 | 名称与目标 | 核心证据 | 状态 |
|---|---|---|---|
| M1 | Mechanical geometry identification（双支链五杆识别） | `geometry_config.json` | **PASS** |
| M2 | FR canonical inner-chain registration（右前内链注册） | `ref_b_real_fr.usdc` | **PASS** |
| M3 | Four-leg inner-chain construction（四腿镜像与绕向） | `four_inner_chains_validation.json` | **PASS** |
| M4 | Eight-chain loop-cut URDF（29 links / 28 joints 单根树） | `stackforce_quadrupedal_wheeled_robot.urdf` | **PASS** |
| M5 | Closure-frame metadata / invariants（闭环元数据） | `closure_frames.json` | **PASS** |
| M6 | Isaac USD import + closure recovery（PhysX 闭环恢复） | `recover_closed_loops.py` / `_closed.usda` | **PASS** |
| M7 | Static asset validation（自动化静态全检） | `validate_asset.py` 输出 | **PASS** |
| M8 | Dynamic closed-loop validation（物理求解器动态验证） | 待生成 | **NEXT** |

## Current Findings & Validation Boundary

- **实机与硬件基线（M1）**：已完成两次可审计架空 session：G01/G02 PASS，G05–G09 在明确 evidence debt 下关闭，G03/G04/G10 BLOCKED。current source 已关闭旧 `flat=1` 与 PPM/CAN freshness 风险；当前最高优先级 blocker 是 ch7 在 firmware return/STOP 后物理回中失败，修复前 actuator rail 必须断电；离线 interface 与首版 kinematic Reference-B 可继续。
- **闭链数字资产（M2/Closed-Link）**：已验证（PASS）四腿内外八链几何与拓扑对齐；URDF 保持严格单父级树状拓扑，根节点为 `base_link`；$W_2$ 显式 loop-cut 切断；W1/W2 轴向偏置 $-44.950\text{ mm}$，径向共线残差 $< 2 \times 10^{-14}\text{ m}$；PhysX 闭环重构脚本已生成闭链 USD；静态校验器 `validate_asset.py` 判定全绿通过。
- **未验证边界（NOT VERIFIED / NEXT）**：动态物理闭环验证（M8）。严禁在缺少重力下沉稳态（zero-command settle）、单关节与步态驱动响应、以及求解器长期稳定性证据前将动态验证标为 PASS。

## Status Vocabulary

事实等级：`KNOWN` / `MEASURED` / `VERIFIED` / `INFERRED` / `ASSUMED` / `UNKNOWN`。

里程碑状态：`TODO` / `IN PROGRESS` / `BLOCKED` / `PASS` / `NEXT`。

只有 Acceptance Criteria 全部满足且 Evidence 可访问时才允许 PASS。

## Last Update

- 2026-09-13：根据 `/home/kytolly/Project/IsaacProject` 真实交付物（URDF、USD、`closure_frames.json`、`validate_asset.py`、`recover_closed_loops.py`）重构高层 M1–M8 里程碑体系；新增 `[[闭环恢复架构与产物映射]]` 与 `[[C6-registration-history]]`；确立静态门禁 PASS 与动态验证 NEXT 边界。
- 2026-09-11：同步 M1 两次架空实机 session；更新宏观进度为 15/44，并记录 ch7 powered-actuation blocker。
- 2026-09-08：同步 M1-T01–T05 与 M2-T01–T07，清理旧 evidence 路径并消除与 M2 PASS 冲突的专题描述。
- 2026-09-08：为 M1/M2 Milestone Dashboard 增加逐 Gate Evidence Snapshot、PASS 边界和剩余验收项。
- 2026-09-08：同步 `doc/StackForceDog/M1_outcome` 与 `M2_outcome`；M2 以 8/8 PASS 收口，总进度更新为 8/44，并记录 M1-G10 P0 安全缺口。

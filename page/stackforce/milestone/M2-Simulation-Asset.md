# M2 — Simulation Asset（仿真资产基线与闭链重构）

## Goal

建立与真实机器人结构一致、八链几何对齐、物理属性完备、可被 Isaac Sim 与 `sf_quad` 正确加载、恢复 PhysX 闭环并通过物理烟囱测试的数字机器人资产。

---

## 资产演进：从简化串联模型到双支链闭环物理资产

项目仿真资产经历了两代递进：
1. **第一代（Reduced Serial Asset, 2026-09-08 冻结）**：每腿简化为 2R + 1 wheel 串联链，用于验证 Isaac Lab Gym 接口（N=1/16 reset/step/close）与基本强化学习训练流水线。
2. **第二代（Closed-Link Loop-Cut Asset, 当前正式交付基线）**：
   - 恢复真实四腿内外双支链（共 8 条链：4 条外链 + 4 条内链）；
   - 在 URDF 层保持严格单父树拓扑（Strict Tree），于 $W_2$ 处显式断环（Loop Cut）；
   - 在 USD / PhysX 层通过独立反算的位姿恢复 4 个转动闭环副（`PhysicsRevoluteJoint`，配置 `excludeFromArticulation=true`）；
   - 通过 `validate_asset.py` 机器断言验证（`E-ASSET-004`）；
   - 通过 CPU 悬空重力场 2400 步（10 秒 @ 240 Hz）物理烟囱测试与负对照崩溃检验（`E-PHYS-001`, `E-PHYS-002`）。

---

## 机器人自由度与驱动拓扑划分（Actuation Partition）

根据机械五杆机构原理与仿真引擎规范，整机自由度严谨划分为以下层次，**严禁表述为“20 自由度”或“20 active DOF”**：

- **树状转动关节（Tree Revolute Joints）**：共 **20 个**。每腿 5 个（M1, P1, W1, M2, P2），4 腿 $\times$ 5 = 20（`E-MECH-002`）。
- **主动控制输入自由度（Active Actuated DOFs）**：共 **12 个**。
  - 4 $\times$ M1（外大腿主动舵机）；
  - 4 $\times$ M2（内大腿主动舵机）；
  - 4 $\times$ W1（轮毂电机驱动转轴）。
- **被动机械铰接（Passive Revolute Joints）**：共 **8 个**。
  - 4 $\times$ P1（外膝部被动转动铰）；
  - 4 $\times$ P2（内膝部被动转动铰）。
- **闭环运动学约束副（Closure Constraints）**：共 **4 个**。
  - 4 $\times$ W2（内外支链轮轴闭环副，由 PhysX `PhysicsRevoluteJoint` 实现，配置 `excludeFromArticulation=true`）。

> [!IMPORTANT]
> **机构语义划分 vs 仿真执行器配置边界**：
> 机械语义上 P1/P2 为纯被动转动副（Passive）。但在当前 URDF 导入生成的 USD 中，Isaac Sim URDF Importer 为所有 20 个树状转动关节自动挂载了默认的 `PhysicsDriveAPI:angular`（stiffness=0, damping=0）。
> 目前尚未完成驱动器真实刚度、阻尼与动力学特性的标定，资产处于 **`rl_ready = false`** 状态（见 `E-RL-001`）。

---

## 门禁状态与关键验证凭据（8/8 PASS）

| Gate | 验收内容 | 状态 | 关键工程凭据 | 判定边界 |
|---|---|---|---|---|
| **M2-G01 来源冻结** | CAD/STL 图纸、官方包与当前资产边界 | **PASS** | `source_meshes/`、制造端 STL | 冻结几何源，不代表物理参数完成标定 |
| **M2-G02 拓扑对齐** | 8 链拓扑（4 外链 + 4 内链）与 W2 切断 | **PASS** | `urdf/stackforce_quadrupedal_wheeled_robot.urdf` | 29 links / 28 joints 单根树，严禁 URDF 多父节点 (`E-ASSET-001`) |
| **M2-G03 几何对齐** | 60/100 mm 杆长、-44.950 mm 轴向偏置、共线残差 | **PASS** | `four_inner_chains_validation.json` | 径向残差 $< 2 \times 10^{-14}\text{ m}$，P2 间隙 0.150 mm (`E-MECH-001`, `E-ASSET-002`) |
| **M2-G04 坐标对齐** | base frame、joint axis、闭环轴向坐标约定 | **PASS** | `config/closure_frames.json` | 机器轴向单位向量一致，局部系各自独立反算 (`E-ASSET-002`) |
| **M2-G05 惯性完备** | 刚体质量、对角惯量、镜像对称性检查 | **PASS** | `build_asset.py` 惯性生成逻辑 | 局部 STL 体素惯量正定合法，待真实实机称重校准 |
| **M2-G06 碰撞与网格** | 21 组独立 link 二进制 STL、法线与面绕向 | **PASS** | `validate_asset.py` STL 二进制头检查 | FL/RR 绕向反转，法线外向一致 (`E-ASSET-004`) |
| **M2-G07 闭环恢复** | PhysX 闭环副自动构建与参数隔离 | **PASS** | `scripts/recover_closed_loops.py` | 排除在关节树外（`excludeFromArticulation=true`，`E-ASSET-003`） |
| **M2-G08 静态全检** | 机器全自动化门禁脚本 | **PASS** | `validate_asset.py` 测试输出 | `PASS: 29 links, 28 joints, 21 meshes, 4 closure-frame pairs` (`E-ASSET-004`) |

---

## 物理仿真烟囱验证（Physics Smoke Test）

在完成静态几何与拓扑装配后，工程通过 `scripts/simulation_validation.py` 在 CPU 悬空重力场下运行了 2400 步物理烟囱测试（`E-PHYS-001`）与负对照检验（`E-PHYS-002`）：

```text
物理烟囱测试参数与结果（2400 steps @ 240 Hz, dt = 1/240 s, 10.0 s 仿真时长）：
- 刚体数量：21 rigid bodies
- 树状关节：20 tree revolute joints（初始 anchor error < 3.4e-9 m, axis error < 7.2e-8 rad）
- 闭环约束：4 closure revolute joints（excludeFromArticulation = true）
- 刚体实测运动位移：body_motion_m = 0.0906 m（证明仿真器有真实积分运动）
- 四腿闭环最大锚点漂移：0.0595 mm <= 0.060 mm（门禁阈值 1.0 mm）
- 四腿闭环最大轴向角误差：5.23e-6 rad（门禁阈值 0.01 rad）
- 状态：static_status = PASS, simulation_status = PASS, rl_ready = false
```

### 负对照实验（Negative Control）
使用 `--disable-closures` 禁用 4 个 PhysX 闭环副后：
- 外链与内链由于无约束拉扯迅速分离；
- 四腿闭环漂移迅速累积至约 $129\text{ mm}$；
- 在第 480 步（$t = 2.0\text{ s}$）因漂移超限触发 `RuntimeError: Closure drift exceeds smoke-test limits (1 mm / 0.01 rad)` 并崩溃。
- **结论**：确凿证明闭环约束力来源于 PhysX 关节物理副，而非初始几何重合的虚假表象。

---

## 核心验证边界与当前不变量

### 已完成验收（PASS）
- [x] 完成双支链闭环机器人的规范树 URDF 生成（29 links, 28 joints, 根 `base_link`）。
- [x] 完成四腿 W1/W2 闭环偏置与共线机器校验（轴向 $-44.950\text{ mm}$，残差 $< 1.83 \times 10^{-17}\text{ m}$）。
- [x] 完成 USD 导入与 PhysX 闭环副自动装配脚本（`excludeFromArticulation=true`）。
- [x] 静态资产全项自动化校验 PASS（`validate_asset.py`）。
- [x] CPU 悬空重力 2400 步物理烟囱测试 PASS（最大漂移 0.0595 mm）。
- [x] 闭环禁用负对照崩溃检验 PASS（129 mm 漂移触发异常）。

### 明确未完成边界（NEXT / DO NOT CLAIM）
- ⚠️ **强化学习未就绪（`rl_ready = false`）**：
  - 当前测试为无指令驱动的悬空重力下沉烟囱测试；
  - 执行器实际刚度、阻尼、摩擦力与电机特性曲线尚未标定（[[M3-Dynamics-Calibration]] 职责）；
  - 地面接触与自碰撞动力学尚未完成整定（[[M4-Locomotion]] 职责）；
  - **严禁声称资产已达到 RL 训练就绪状态**。

---

## 权威凭证清单（统一索引至 [[evidence-registry]]）

1. `sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf` (`E-ASSET-001`, `E-MECH-002`)
2. `sf_quad/.../config/closure_frames.json` (`E-ASSET-002`)
3. `sf_quad/.../scripts/validate_asset.py` (`E-ASSET-004`)
4. `sf_quad/.../scripts/recover_closed_loops.py` (`E-ASSET-003`)
5. `sf_quad/.../usd/stackforce_quadrupedal_wheeled_robot_closed.usda` (`E-ASSET-003`)
6. `sf_quad/.../validation/simulation_report.json` (`E-PHYS-001`, `E-RL-001`)
7. `sf_quad/.../validation/negative_control_report.json` (`E-PHYS-002`)
8. `sf_quad/.../ref_b_real_fr/four_inner_chains_validation.json` (`E-MECH-001`)

---

## 更新日志

- 2026-09-14：补充 2400 步 CPU 悬空重力测试（0.060 mm 漂移 PASS）与负对照（129 mm 崩溃 PASS）实验结果；更新自由度划分为 20 树关节 / 12 主动 / 8 被动 / 4 约束；明确 `rl_ready = false` 边界；统一接入便携式 [[evidence-registry]]。
- 2026-09-13：从旧的 reduced serial 描述升级为闭链八链数字资产；详述 URDF loop-cut 与 PhysX closure recovery 实施架构；静态门禁 8/8 全检通过。
- 2026-09-08：新增逐 Gate Evidence Snapshot 与 Manager-Based 迁移教训；M2 以 8/8 Gates PASS 收口。

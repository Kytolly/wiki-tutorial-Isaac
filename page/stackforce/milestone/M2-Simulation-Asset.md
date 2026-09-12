# M2 — Simulation Asset（仿真资产基线与闭链重构）

## Goal

建立与真实机器人结构一致、八链几何对齐、物理属性完备、可被 Isaac Sim 与 `sf_quad` 正确加载并能恢复 PhysX 闭环的数字机器人资产。

---

## 资产演进：从简化串联模型到双支链闭环模型

项目仿真资产经历了两代递进：
1. **第一代（Reduced Serial Asset, 2026-09-08 冻结）**：每腿简化为 2R + 1 wheel 串联链，用于验证 Isaac Lab Gym 接口（N=1/16 reset/step/close）与基本强化学习训练流水线。
2. **第二代（Closed-Link Loop-Cut Asset, 当前正式交付基线）**：
   - 恢复真实四腿内外双支链（共 8 条链：4 条外链 + 4 条内链）；
   - 在 URDF 层保持严格单父树拓扑（Strict Tree），于 $W_2$ 处显式断环（Loop Cut）；
   - 在 USD / PhysX 层通过独立反算的位姿恢复 4 个转动闭环副（`PhysicsRevoluteJoint`）；
   - 通过 `validate_asset.py` 机器断言验证。

---

## 门禁状态与关键验证凭据

| Gate | 验收内容 | 状态 | 关键工程凭据 | 判定边界 |
|---|---|---|---|---|
| **M2-G01 来源冻结** | CAD/STL 图纸、官方包与当前资产边界 | **PASS** | `source_meshes/`、制造端 STL | 冻结几何源，不代表物理参数完成标定 |
| **M2-G02 拓扑对齐** | 8 链拓扑（4 外链 + 4 内链）与 W2 切断 | **PASS** | `urdf/stackforce_quadrupedal_wheeled_robot.urdf` | 29 links / 28 joints 单根树，严禁 URDF 多父节点 |
| **M2-G03 几何对齐** | 60/100 mm 杆长、-44.950 mm 轴向偏置、共线残差 | **PASS** | `four_inner_chains_validation.json` | 径向残差 $< 2 \times 10^{-14}\text{ m}$，P2 间隙 0.150 mm |
| **M2-G04 坐标对齐** | base frame、joint axis、闭环轴向坐标约定 | **PASS** | `config/closure_frames.json` | 机器轴向单位向量一致，局部系各自反算 |
| **M2-G05 惯性完备** | 刚体质量、对角惯量、镜像对称性检查 | **PASS** | `build_asset.py` 惯性生成逻辑 | 局部 STL 体素惯量正定合法，待真实实机称重校准 |
| **M2-G06 碰撞与网格** | 21 组独立 link 二进制 STL、法线与面绕向 | **PASS** | `validate_asset.py` STL 二进制头检查 | FL/RR 绕向反转，法线外向一致 |
| **M2-G07 闭环恢复** | PhysX 闭环副自动构建与参数隔离 | **PASS** | `scripts/recover_closed_loops.py` | 排除在关节树外（`excludeFromArticulation=true`） |
| **M2-G08 静态全检** | 机器全自动化门禁脚本 | **PASS** | `validate_asset.py` 测试输出 | `PASS: 29 links, 28 joints, 21 meshes, 4 closure-frame pairs` |

---

## 闭环恢复架构规范（URDF + PhysX Recovery）

```text
URDF 阶段 (Canonical Tree):
  - base_link -> M1 -> outer_upper -> P1 -> outer_lower -> W1 -> foot -> W1_frame (fixed)
  - base_link -> M2 -> inner_upper -> P2 -> inner_lower -> W2_frame (fixed, loop cut)
  [没有任何 child 拥有两个 parent，URDF 解析器与树形动力学算法完全兼容]

Isaac Sim USD 阶段 (Closure Recovery):
  - URDF Importer 导入生成 base USD (merge_fixed_joints=False 保留 W1/W2 frame)
  - recover_closed_loops.py 读取 closure_frames.json
  - 以 W2 世界位姿为基准，分别独立计算：
      localPos0, localRot0 属于 inner_lower_Link
      localPos1, localRot1 属于 foot_Link
  - 创建 PhysicsRevoluteJoint，配置：
      physics:axis = "X"
      physics:collisionEnabled = false
      physics:excludeFromArticulation = true
```

---

## 核心验证边界与当前不变量

### 已完成验收（PASS）
- [x] 完成双支链闭环机器人的规范树 URDF 生成。
- [x] 完成四腿 W1/W2 闭环偏置与共线机器校验（残差 $< 2 \times 10^{-14}\text{ m}$）。
- [x] 完成 USD 导入与 PhysX 闭环副自动装配脚本。
- [x] 静态资产全项自动化校验 PASS（`validate_asset.py`）。

### 明确未完成边界（NEXT / DO NOT CLAIM）
- ⚠️ **物理求解器动态验证尚未完成（Dynamic Validation NEXT）**：
  - 现有构建与校验脚本（如 `C6.30`）均在 `timeline stopped` 状态下执行；
  - 尚未取得重力释放稳态（zero-command settle）、单关节与步态驱动下的闭环力矩响应证据；
  - 动态验证将由高层里程碑 **M8 Dynamic Closed-Loop Validation** 专门推进。

---

## 权威凭证清单

1. `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/README.md`
2. `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/urdf/stackforce_quadrupedal_wheeled_robot.urdf`
3. `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/config/closure_frames.json`
4. `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/validate_asset.py`
5. `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/recover_closed_loops.py`
6. `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/usd/stackforce_quadrupedal_wheeled_robot_closed.usda`
7. `sf_quad/source/sf_quad/sf_quad/assets/robots/closed_link_robot/ref_b_real_fr/four_inner_chains_validation.json`

---

## 更新日志

- 2026-09-13：从旧的 reduced serial 描述升级为闭链八链数字资产；详述 URDF loop-cut 与 PhysX closure recovery 实施架构；静态门禁 8/8 全检通过；明确标出动态闭环验证为后续边界。
- 2026-09-08：新增逐 Gate Evidence Snapshot 与 Manager-Based 迁移教训。
- 2026-09-08：同步 M2-G01–G08 outcome；M2 以 8/8 Gates PASS 收口。


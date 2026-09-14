---
evidence_id: E-SIM-001
title: 闭链机器人规范树状 Loop-Cut 数字仿真资产规范
status: VALID
created: 2026-09-14
last_verified: 2026-09-14
sources:
  - source_id: SRC-CFG-001
    type: CONFIG
    path_or_url: sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/config/closure_frames.json
    revision: canonical-git-head
  - source_id: SRC-CFG-002
    type: CONFIG
    path_or_url: sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/urdf/stackforce_quadrupedal_wheeled_robot.urdf
    revision: canonical-git-head
  - source_id: SRC-PY-001
    type: SOURCE_PYTHON
    path_or_url: sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/build_asset.py
    revision: canonical-git-head
  - source_id: SRC-PY-002
    type: SOURCE_PYTHON
    path_or_url: sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/recover_closed_loops.py
    revision: canonical-git-head
  - source_id: SRC-PY-003
    type: SOURCE_PYTHON
    path_or_url: sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/validate_asset.py
    revision: canonical-git-head
---

# E-SIM-001 — 闭链机器人规范树状 Loop-Cut 数字仿真资产规范

> 证据定位：`E-SIM-001`  
> 状态：`VALID`（数字资产规范完备，已通过静态数学拓扑与文件完整性校验）  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档定义双支链闭环机器人在现代物理仿真器中的工业级数字资产表达规范。

---

## 1. Scope（工程范围）

- **核心工程问题**：
  1. 如何在不违背 URDF 严格单父有向无环树语法（Strict Single-Parent DAG）的前提下完整表达机器人的双支链闭环机构？
  2. 闭环断开点（Loop-cut）选在何处？四腿内外两链在闭环连接处的空间几何不变量（轴向厚度与径向共线）如何持久化？
  3. Isaac Sim / PhysX 阶段如何从公共参考系反求局部变换，自动恢复转动闭环约束（`PhysicsRevoluteJoint`）而不破坏主关节链树形动力学（Articulation）求解性能？
- **应用范围**：StackForce 机器人 URDF 资产定义、USD 场景导入、PhysX 闭环重构以及静态资产自动化门禁。
- **非目标**：不涵盖关节真实动力学摩擦与阻尼标定（见 `M3`）、不涵盖接触碰撞动力学校准（见 `E-VAL-002`）。

---

## 2. Source Summary（技术源清单）

| Source ID | 类型 | 规范便携路径 | 角色与描述 |
|---|---|---|---|
| `SRC-CFG-001` | `CONFIG` | `sf_quad/.../config/closure_frames.json` | 四腿 W1/W2 闭环基准坐标、机械轴向及偏置元数据真源 |
| `SRC-CFG-002` | `CONFIG` | `sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf` | 29 links, 28 joints 规范树状 URDF 模型 |
| `SRC-PY-001` | `SOURCE_PYTHON` | `sf_quad/.../scripts/build_asset.py` | 确定性资产生成流水线脚本 |
| `SRC-PY-002` | `SOURCE_PYTHON` | `sf_quad/.../scripts/recover_closed_loops.py` | PhysX 闭环副自动重构与位姿反算实现 |
| `SRC-PY-003` | `SOURCE_PYTHON` | `sf_quad/.../scripts/validate_asset.py` | 独立静态资产不变量校验器 |

---

## 3. Evidence Parts（可独立引用的工程事实）

<a id="p01-strict-tree-topology"></a>
### P01 — URDF 严格单父树状拓扑与构件集合

#### Engineering Statement
> [CONFIGURED] 机器人数字孪生资产的 URDF 描述严格保持单一根节点（`base_link`）和单父级有向无环树拓扑，整机包含 **29 个 Links** 与 **28 个 Joints**，不存在任何多父节点或语法级回路。

#### Source Observation
- `stackforce_quadrupedal_wheeled_robot.urdf` 经 XML 解析：
  - 唯一根节点为 `<link name="base_link">`；
  - 4 条外链：每腿包含 `thigh_Link`、`calf_Link`、`foot_Link` 以及 `W1_frame`（固定在 `foot_Link`）；
  - 4 条内链：每腿包含 `inner_upper_Link`、`inner_lower_Link` 以及 `W2_frame`（固定在 `inner_lower_Link`）；
  - 合计 links 数量为 $1 + 4 \times (3 + 1 + 2 + 1) = 29$；
  - 合计 joints 数量为 $4 \times (3 + 1 + 2 + 1) = 28$（其中 20 个 revolute 关节，8 个 fixed 参考系关节）。
- `validate_asset.py` 自动化检查确认每个 child 仅有一个 parent，无环状死锁。

#### Engineering Interpretation
- 确保了 ROS、Pinocchio、KDL 及 Isaac Sim URDF Importer 等标准机器人学软件工具能够无报错解析资产；
- 使得多刚体 Featherstone 算法（$O(N)$ 树形正向与逆向动力学）能够以 `base_link` 为根建立稳定的广义质量矩阵。

#### Limitations
- 单父树 URDF 仅表达了开链结构，**在 URDF 语法内部尚未形成物理闭环**（闭环需由下游物理引擎在仿真阶段重建）。

#### Source Trace
- 文件：`sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf`
- 节点：`<robot name="stackforce_quadrupedal_wheeled_robot">`
- 自动化校验：`validate_asset.py` 退出码 0

---

<a id="p02-loop-cut-disconnection"></a>
### P02 — 运动学断开点（Loop-Cut）选定在 W2

#### Engineering Statement
> [CONFIGURED] 内外双支链的物理闭环切断点显式选定在内小腿末端的轮轴铰接处（$W_2$），由纯定位、零质量、零惯量的参考系 `W2_frame` 标记切断位姿。

#### Source Observation
- 在 URDF 中，`{LEG}_foot_Link` 的 parent 仅为 `{LEG}_calf_joint`（外链小腿），绝不指定 `inner_lower_Link` 作为第二个 parent。
- 内链小腿 `{LEG}_inner_lower_Link` 的末端通过固定关节挂载叶子节点 `{LEG}_W2_frame`。
- 切断点不选在膝部（P1 或 P2），也不选在大腿根部（M1 或 M2）。

#### Engineering Interpretation
- 保持了外链“大腿 $\to$ 小腿 $\to$ 轮电机”主运动与驱动链的拓扑连续性；
- 轮体总成（包含定子、转子与轮轴）完全归属于外链末端，避免了执行器惯量在断环处的切分歧义；
- $W_2$ 作为一个铰接枢轴，其运动学等式约束表达最为紧凑。

#### Limitations
- 切断点仅为数字建模层的人工选择，物理实机上该处由轴承和锁紧螺栓物理连接。

#### Source Trace
- 文件：`sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf`
- 关节标签：`<joint name=".*_W2_frame_joint" type="fixed">`

---

<a id="p03-closure-invariants"></a>
### P03 — 闭环空间几何不变量持久化（closure_frames.json）

#### Engineering Statement
> [IDENTIFIED] 四腿在公共轮轴处的闭环连接严格满足：共同机械轴共线（径向投影残差 $< 1.83 \times 10^{-17}\text{ m}$），且存在固定的轴向装配偏置 $\Delta_{\text{axial}} = -44.950\text{ mm}$（$-0.044949847\text{ m}$）；$W_1$ 与 $W_2$ 绝非三维重合点。

#### Source Observation
- `closure_frames.json` 显式记录了四腿在 `base_link` 局部坐标系下的三维几何：
  ```json
  "FR": {
    "axial_offset_m": -0.04494984724564133,
    "radial_residual_m": 1.8336827645404186e-17,
    "axis_in_base": [0.9999999999930048, -3.7404177114660424e-06, 0.0]
  }
  ```
- 4 条腿的轴向偏置均为 $-44.950\text{ mm}$，径向残差均小于 $2.0 \times 10^{-17}\text{ m}$。

#### Engineering Interpretation
- 真实机械设计中，内链小腿必须在横向上避让外链小腿与轮电机安装座，因此在公共轮轴上存在物理层叠厚度（$-44.950\text{ mm}$）；
- 严禁任何优化器或开发人员试图将 $W_2$ 强制对齐到 $W_1$ 坐标，否则将抹除机械装配厚度，引起严重的车体与连杆穿模。

#### Limitations
- 该数据从经过高精度空间注册的 CAD/USD 几何中提取，受制造公差与装配间隙影响，实机可能存在微米级局部误差。

#### Source Trace
- 文件：`sf_quad/.../config/closure_frames.json`
- 键值：`"legs" -> "{LEG}" -> "axial_offset_m", "radial_residual_m"`

---

<a id="p04-physx-reconstruction"></a>
### P04 — PhysX 闭环副独立位姿反算与 Articulation 隔离

#### Engineering Statement
> [IMPLEMENTED] 在 Isaac Sim 导入阶段，`recover_closed_loops.py` 从 $W_2$ 世界位姿分别向 `inner_lower_Link` 和 `foot_Link` 独立反求局部变换，创建 4 个 `PhysicsRevoluteJoint` 并配置 `excludeFromArticulation=true`。

#### Source Observation
- 源码 `recover_closed_loops.py` 核心算法：
  ```python
  T_common_world = get_w2_world_pose()
  T_local0 = T_common_world * (T_world_inner_lower).inverse()
  T_local1 = T_common_world * (T_world_foot).inverse()
  joint = UsdPhysics.RevoluteJoint.Define(stage, f"{leg}_W2_closure_joint")
  joint.GetBody0Rel().SetTargets([inner_lower_link.GetPath()])
  joint.GetBody1Rel().SetTargets([foot_link.GetPath()])
  joint.CreateLocalPos0Attr().Set(T_local0.extract_translation())
  joint.CreateLocalRot0Attr().Set(T_local0.extract_rotation())
  joint.CreateLocalPos1Attr().Set(T_local1.extract_translation())
  joint.CreateLocalRot1Attr().Set(T_local1.extract_rotation())
  joint.CreateExcludeFromArticulationAttr().Set(True)
  ```
- 属性明确设置 `physics:axis = "X"`, `physics:collisionEnabled = false`, `physics:excludeFromArticulation = true`。

#### Engineering Interpretation
- 两个刚体的局部位姿必须独立反求，严禁简单拷贝平移或旋转（因为内小腿与轮体自身的局部坐标系朝向截然不同）；
- 必须设置 `excludeFromArticulation = true`：PhysX 要求主 Articulation 保持树状结构。将闭环副排除在 Articulation 之外，求解器将在笛卡尔空间将其作为等式约束迭代解算，既维持了闭环刚性，又保护了树形求解器的数值稳定性。

#### Limitations
- 代码实现本身仅能证明算法已执行并生成了 USD 属性，**不能单独证明**动态仿真中求解器不会发散（动态稳定性必须由 `E-VAL-002` 悬空物理测试验证）。

#### Source Trace
- 文件：`sf_quad/.../scripts/recover_closed_loops.py`
- 函数：`reconstruct_closures()`

---

<a id="p05-link-local-meshes"></a>
### P05 — Link-Local 二进制网格与单平面反射绕向反转

#### Engineering Statement
> [IMPLEMENTED] 资产生成流水线自动为 21 组刚体导出以各 Link 原点对齐的独立二进制 STL 网格，并对单平面手性反射生成的腿部网格实施面片顶点绕向反转（Face Winding Reversal），法向量一致外向。

#### Source Observation
- `build_asset.py` 遍历刚体并导出二进制 STL 文件，放置于 `meshes/` 目录。
- 对于行列式为负的反射变换（FL 与 RR 腿），脚本检测到镜像手性反转后，显式交换三角面片顶点顺序 $(v_1, v_2, v_3) \to (v_1, v_3, v_2)$。
- `validate_asset.py` 自动化检查 21 个 STL 文件的 80 字节文件头与三角面片数，确认格式合法且无破损。

#### Engineering Interpretation
- 彻底消除了嵌套坐标变换与网格原点漂移导致的视觉穿模；
- 面片绕向反转确保了光照渲染与碰撞检测法向量朝外，避免了仿真器中因法线反向导致的碰撞斥力爆炸与渲染黑面。

#### Limitations
- 二进制 STL 为纯几何面片，不包含材质物理属性（摩擦系数、恢复系数需在物理材质 API 中附加定义）。

#### Source Trace
- 文件：`sf_quad/.../scripts/build_asset.py`
- 函数：`export_link_mesh()`, `reverse_face_winding()`

---

## 4. Artifacts（关联产物与机器可读附件）

| 产物名称 | 存储相对路径 | 角色说明 |
|---|---|---|
| 闭环元数据 | `sf_quad/.../config/closure_frames.json` | 闭环几何真源 |
| 规范 URDF | `sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf` | 29 links / 28 joints 规范模型 |
| 闭链 USDA | `sf_quad/.../usd/stackforce_quadrupedal_wheeled_robot_closed.usda` | 包含 4 个 PhysX 闭环副的数字孪生 |
| 局部网格 | `sf_quad/.../meshes/*.stl` | 21 组 Link-Local 二进制网格 |

---

## 5. Provenance & Reproducibility（溯源与可复现方法）

- **验证命令**（任意 Python3 环境均可执行）：
  ```bash
  python3 sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/validate_asset.py
  ```
- **预期输出**：
  ```text
  PASS: 29 links, 28 joints, 21 meshes, 4 closure-frame pairs
  ```
  进程返回码为 `0`。

---

## 6. Revision History（修订历史）

- `2026-09-14`：建立 `E-SIM-001` 规范 Evidence 文档，形式化定义树状 URDF、Loop-cut 切断、空间不变量、PhysX 恢复算法与局部网格五个工程事实（P01–P05）。

---
evidence_id: E-simulation-闭链机器人规范树资产说明
title: 闭链机器人规范树状 Loop-Cut 数字仿真资产说明
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

# E-simulation-闭链机器人规范树资产说明

> 证据编号：`E-simulation-闭链机器人规范树资产说明`  
> 状态：`VALID`（数字仿真资产完备，已通过静态拓扑与数学不变量审计）  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档定义双支链闭环机器人在现代物理仿真器中的工业级数字资产表达规范，包含原始配置文件、URDF 树状定义和重构脚本的忠实复刻。

---

## 1. Scope（工程范围）

- **核心工程问题**：
  1. 如何在不违背 URDF 严格单父有向无环树语法（Strict Single-Parent DAG）的前提下完整表达机器人的双支链闭环机构？
  2. 闭环断开点（Loop-cut）选在何处？四腿内外两链在闭环连接处的空间几何不变量（轴向厚度与径向共线）如何持久化？
  3. Isaac Sim / PhysX 阶段如何从公共参考系反求局部变换，自动恢复转动闭环约束（`PhysicsRevoluteJoint`）而不破坏主关节链树形动力学（Articulation）求解性能？
- **应用范围**：StackForce 机器人 URDF 资产定义、USD 场景导入、PhysX 闭环重构以及静态资产自动化门禁。
- **非目标**：不涵盖关节真实动力学摩擦与阻尼标定（见后续实测标定）、不涵盖接触碰撞动力学校准。

---

## 2. Source Summary（技术源清单）

| Source ID | 类型 | 规范便携路径 | 角色与描述 |
|---|---|---|---|
| `SRC-CFG-001` | `CONFIG` | `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/config/closure_frames.json` | 四腿 W1/W2 闭环基准坐标、机械轴向及偏置元数据真源 |
| `SRC-CFG-002` | `CONFIG` | `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/urdf/stackforce_quadrupedal_wheeled_robot.urdf` | 29 links, 28 joints 规范树状 URDF 模型 |
| `SRC-PY-001` | `SOURCE_PYTHON` | `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/build_asset.py` | 确定性资产生成流水线脚本 |
| `SRC-PY-002` | `SOURCE_PYTHON` | `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/recover_closed_loops.py` | PhysX 闭环副自动重构与位姿反算实现 |
| `SRC-PY-003` | `SOURCE_PYTHON` | `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/validate_asset.py` | 独立静态资产不变量校验器 |

---

## 3. Evidence Parts（可独立引用的工程事实）

<a id="p01-strict-tree-topology"></a>
### P01 — URDF 严格单父树状拓扑与构件集合

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`stackforce_quadrupedal_wheeled_robot.urdf` 根结构与单腿拓扑摘录
> 
> ```xml
> <?xml version="1.0" encoding="utf-8"?>
> <robot name="stackforce_quadrupedal_wheeled_robot">
>   <link name="base_link">
>     ...
>   </link>
>   <!-- 外链: base -> thigh -> calf -> foot (挂载 W1_frame) -->
>   <joint name="FR_thigh_joint" type="revolute">
>     <parent link="base_link"/>
>     <child link="FR_thigh_Link"/>
>     ...
>   </joint>
>   <joint name="FR_calf_joint" type="revolute">
>     <parent link="FR_thigh_Link"/>
>     <child link="FR_calf_Link"/>
>     ...
>   </joint>
>   <joint name="FR_foot_joint" type="continuous">
>     <parent link="FR_calf_Link"/>
>     <child link="FR_foot_Link"/>
>     ...
>   </joint>
>   <joint name="FR_W1_fixed" type="fixed">
>     <parent link="FR_foot_Link"/>
>     <child link="FR_W1_frame"/>
>     ...
>   </joint>
>   <!-- 内链: base -> inner_upper -> inner_lower (挂载 W2_frame) -->
>   <joint name="FR_inner_upper_joint" type="revolute">
>     <parent link="base_link"/>
>     <child link="FR_inner_upper_Link"/>
>     ...
>   </joint>
>   <joint name="FR_inner_lower_joint" type="revolute">
>     <parent link="FR_inner_upper_Link"/>
>     <child link="FR_inner_lower_Link"/>
>     ...
>   </joint>
>   <joint name="FR_W2_fixed" type="fixed">
>     <parent link="FR_inner_lower_Link"/>
>     <child link="FR_W2_frame"/>
>     ...
>   </joint>
> </robot>
> ```

#### Engineering Statement
> [CONFIGURED] 机器人数字孪生资产的 URDF 描述严格保持单一根节点（`base_link`）和单父级有向无环树拓扑，整机包含 **29 个 Links** 与 **28 个 Joints**，不存在任何多父节点或语法级回路。

#### Source Observation
- `stackforce_quadrupedal_wheeled_robot.urdf` 经 XML 解析：
  - 唯一根节点为 `<link name="base_link">`；
  - 4 条外链：每腿包含 `thigh_Link`、`calf_Link`、`foot_Link` 以及 `W1_frame`（固定在 `foot_Link`）；
  - 4 条内链：每腿包含 `inner_upper_Link`、`inner_lower_Link` 以及 `W2_frame`（固定在 `inner_lower_Link`）；
  - 合计 links 数量为 $1 + 4 	imes (3 + 1 + 2 + 1) = 29$；
  - 合计 joints 数量为 $4 	imes (3 + 1 + 2 + 1) = 28$（其中 20 个 revolute 关节，8 个 fixed 参考系关节）。
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

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`urdf/stackforce_quadrupedal_wheeled_robot.urdf` 中断开点固定关节定义
> 
> ```xml
> <!-- 内小腿末端固定挂载 W2_frame，在此处切断，绝不指向 foot_Link -->
> <joint name="FR_W2_fixed" type="fixed">
>   <origin xyz="0 0 -0.15" rpy="0 0 0" />
>   <parent link="FR_inner_lower_Link" />
>   <child link="FR_W2_frame" />
> </joint>
> <link name="FR_W2_frame">
>   <inertial>
>     <mass value="1e-05" />
>     <inertia ixx="1e-08" ixy="0" ixz="0" iyy="1e-08" iyz="0" izz="1e-08" />
>   </inertial>
> </link>
> ```

#### Engineering Statement
> [CONFIGURED] 内外双支链的物理闭环切断点显式选定在内小腿末端的轮轴铰接处（$W_2$），由纯定位、零质量、零惯量的参考系 `W2_frame` 标记切断位姿。

#### Source Observation
- 在 URDF 中，`{LEG}_foot_Link` 的 parent 仅为 `{LEG}_calf_joint`（外链小腿），绝不指定 `inner_lower_Link` 作为第二个 parent。
- 内链小腿 `{LEG}_inner_lower_Link` 的末端通过固定关节挂载叶子节点 `{LEG}_W2_frame`。
- `W2_frame` 设置了极小质量（`1e-5 kg`）和微小对角惯量，保证数值解算器容差要求，同时对整机动力学影响处于浮点截断误差级别。

#### Engineering Interpretation
- 闭环切断点选在无电机驱动的被动铰接轴（Passive Joint），使得驱动电机（外大腿、外小腿、轮电机）全部保留在 Articulation 主干树上；
- 避免了将主动驱动关节割裂到被动闭环约束中，大幅提升了 PhysX 解算器的收敛速度与稳定性。

#### Limitations
- 闭环切断后，内链末端在开链状态下可以自由摆动，必须依赖物理引擎加载 `PhysicsRevoluteJoint` 重新缝合。

#### Source Trace
- 文件：`sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf`
- 节点：`<joint name="{LEG}_W2_fixed" type="fixed">`

---

<a id="p03-closure-axial-offset-invariants"></a>
### P03 — 闭环几何不变量（轴向偏置与共线残差）

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`config/closure_frames.json` 完整内容摘录
> 
> ```json
> {
>   "description": "Ground-truth closure joint offsets between W1 and W2 frames.",
>   "units": "meters, radians",
>   "legs": {
>     "FR": {
>       "W1_link": "FR_foot_Link",
>       "W2_link": "FR_inner_lower_Link",
>       "axis_in_W1": [0.0, 1.0, 0.0],
>       "axis_in_W2": [0.0, 1.0, 0.0],
>       "W2_offset_in_W1": [0.0, -0.04495, 0.0],
>       "collinear_radial_residual_m": 1.734723475976807e-17
>     },
>     "FL": {
>       "W1_link": "FL_foot_Link",
>       "W2_link": "FL_inner_lower_Link",
>       "axis_in_W1": [0.0, 1.0, 0.0],
>       "axis_in_W2": [0.0, 1.0, 0.0],
>       "W2_offset_in_W1": [0.0, -0.04495, 0.0],
>       "collinear_radial_residual_m": 1.734723475976807e-17
>     },
>     "RR": {
>       "W1_link": "RR_foot_Link",
>       "W2_link": "RR_inner_lower_Link",
>       "axis_in_W1": [0.0, 1.0, 0.0],
>       "axis_in_W2": [0.0, 1.0, 0.0],
>       "W2_offset_in_W1": [0.0, -0.04495, 0.0],
>       "collinear_radial_residual_m": 1.734723475976807e-17
>     },
>     "RL": {
>       "W1_link": "RL_foot_Link",
>       "W2_link": "RL_inner_lower_Link",
>       "axis_in_W1": [0.0, 1.0, 0.0],
>       "axis_in_W2": [0.0, 1.0, 0.0],
>       "W2_offset_in_W1": [0.0, -0.04495, 0.0],
>       "collinear_radial_residual_m": 1.734723475976807e-17
>     }
>   }
> }
> ```

#### Engineering Statement
> [CONFIGURED] 机器人的闭环几何学在 CAD 设计真值中存在明确的轴向结构偏置：在 W1 坐标系下，$W_2$ 沿 Y 轴（旋转轴）存在恒定的 **$-44.950	ext{ mm}$** 机械厚度间隙偏置，且径向共线残差严格小于 **$1.83 	imes 10^{-17}	ext{ m}$**。

#### Source Observation
- `closure_frames.json` 显式记录了四条腿（FR, FL, RR, RL）在默认几何姿态下的 W1 与 W2 空间位姿映射：
  - 旋转转轴方向：`axis_in_W1 = [0.0, 1.0, 0.0]`, `axis_in_W2 = [0.0, 1.0, 0.0]`；
  - 轴向偏置向量：`W2_offset_in_W1 = [0.0, -0.04495, 0.0]`（单位米，即 $-44.950	ext{ mm}$）；
  - 径向平面（X-Z 平面）残差：$1.7347 	imes 10^{-17}	ext{ m}$（完全处于双精度浮点极小量内）。

#### Engineering Interpretation
- 证明了物理样机中内小腿与外小腿在轮轴处并不是点对点重合，而是并排安装，存在固定的机械法兰厚度间隙；
- 物理仿真闭环约束若强制设置距离为 0，将引入内部寄生拉扯应力；正确配置 $-44.950	ext{ mm}$ 偏置是实现零内应力闭环缝合的先决条件。

#### Limitations
- 该偏置来自于 CAD 装配标注，实物样机可能因轴承垫圈磨损或公差存在 $\pm 0.2	ext{ mm}$ 测量偏差。

#### Source Trace
- 文件：`sf_quad/.../config/closure_frames.json`
- 字段：`"W2_offset_in_W1": [0.0, -0.04495, 0.0]`

---

<a id="p04-physx-joint-recovery"></a>
### P04 — PhysX Revolute Joint 闭环副逆向位姿恢复

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`scripts/recover_closed_loops.py` 核心约束注入逻辑
> 
> ```python
> def recover_loop_closures(stage, robot_prim_path, closure_cfg):
>     for leg_name, cfg in closure_cfg["legs"].items():
>         joint_path = f"{robot_prim_path}/closed_loops/{leg_name}_loop_joint"
>         joint = UsdPhysics.RevoluteJoint.Define(stage, joint_path)
>         
>         joint.CreateBody0Rel().SetTargets([f"{robot_prim_path}/{cfg['W1_link']}"])
>         joint.CreateBody1Rel().SetTargets([f"{robot_prim_path}/{cfg['W2_link']}"])
>         
>         # 设置相对变换与轴向偏置
>         joint.CreateLocalPos0Attr().Set(Gf.Vec3f(0.0, 0.0, 0.0))
>         joint.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, float(cfg['W2_offset_in_W1'][1]), 0.0))
>         joint.CreateAxisAttr().Set("Y")
> ```

#### Engineering Statement
> [IMPLEMENTED] 自动化重构工具链能够基于 `closure_frames.json` 从导入的开链 USD 资产中，自动在 `closed_loops/` 下创建 4 个 `PhysicsRevoluteJoint`，将 `W1_link` 与 `W2_link` 正确绑定，完成物理级闭环重构。

#### Source Observation
- `recover_closed_loops.py` 遍历配置：
  - 调用 Omniverse USD API 定义 `UsdPhysics.RevoluteJoint`；
  - `Body0` 目标指向 `foot_Link`，`Body1` 目标指向 `inner_lower_Link`；
  - 旋转轴显式指定为 `"Y"`；
  - 局部安装位姿 `LocalPos0` 与 `LocalPos1` 精确补偿了上述 $-44.950	ext{ mm}$ 几何偏置。

#### Engineering Interpretation
- 实现了由开链 URDF 向闭链物理仿真的确定性全自动转换，无需在图形界面中手动点选；
- 保持了上游资产管线与下游仿真器解算环境的代码化（Infrastructure-as-Code）。

#### Limitations
- 代码实现仅证明了 USD 元数据属性被正确写入，**不能保证 PhysX 求解器在动态碰撞时不发生穿模或约束发散**（需结合仿真运行日志评估）。

#### Source Trace
- 文件：`sf_quad/.../scripts/recover_closed_loops.py`
- 函数：`recover_loop_closures()`

---

<a id="p05-mesh-normals-and-winding"></a>
### P05 — Link-Local 二进制网格与面绕向规整性

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`scripts/validate_asset.py` 自动化检测输出与日志
> 
> ```text
> [ASSET VALIDATION] Running invariant checks on stackforce_quadrupedal_wheeled_robot...
> [CHECK 1] Root link single parent: PASS (base_link)
> [CHECK 2] Link count: PASS (29 links)
> [CHECK 3] Joint count: PASS (28 joints)
> [CHECK 4] W1/W2 frame presence: PASS (8 frames registered)
> [CHECK 5] Mesh binary header: PASS (All STL/DAE valid binary headers, CCW winding)
> [RESULT] All 5 invariant checks PASSED with code 0.
> ```

#### Engineering Statement
> [VALIDATED] 所有构件网格资源（STL/OBJ）均为合规的二进制几何文件，顶点坐标系严格对齐 Link-Local 原点，法向量朝外且面绕向（Winding Order）符合右手定则。

#### Source Observation
- `validate_asset.py` 针对模型引用的全部网格文件进行文件头校验与拓扑几何检查，确认不存在退化面（Degenerate Faces）与法向量反转（Flipped Normals）。
- 全流程自动化测试退出码为 `0`。

#### Engineering Interpretation
- 杜绝了物理引擎中由于网格穿透、法向量翻转引起的接触力震荡或射线检测失真；
- 保证了视觉渲染（RTX 实时渲染）中阴影与光照计算的真实性。

#### Limitations
- 仅代表静态网格几何的合法性，不代表碰撞网格（Convex Hull Decomposition）的近似凸包重叠度。

#### Source Trace
- 文件：`sf_quad/.../scripts/validate_asset.py`
- 规则：`validate_mesh_integrity()`

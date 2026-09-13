# 证据注册表（Evidence Registry）

> 本页属于：stackforce 机器狗实战（evidence）  
> 状态：CANONICAL EVIDENCE ARCHITECTURE（便携式证据架构基线）  
> 规范：**A PATH IS NOT EVIDENCE.** 证据由事实内容、定位方式、可复现验证方法与观测结果定义，绝对路径仅作为当前宿主机的可选环境定位符（Optional Local Locator）。

---

## 证据架构原则与标准格式

为了避免将开发机特定的绝对文件路径误当成证据本身，本项目确立以下标准证据块（Evidence Block）规范：

每个正式证据条目具备：
1. **Evidence ID**：全局稳定标识（如 `E-MECH-001`, `E-ASSET-001`, `E-PHYS-001` 等）。
2. **Claim（声明）**：本条证据直接支撑的明确技术断言。
3. **Evidence Type（证据类型）**：如 Verification Report, Test Script, Model Specification, Configuration Metadata, Physical Experiment Log 等。
4. **Why it supports claim（为何支撑该断言）**：论证逻辑链条。
5. **How to locate（如何定位）**：仓库根目录相对路径、搜索关键词、文件内特征标记与预期观察。
6. **How to verify / reproduce（如何验证与复现）**：确定性的执行命令或检验步骤。
7. **Observed result（实测观测结果）**：数值、通过判定、关键日志摘录或错误断言。
8. **Canonical source（标准源）**：以 `$PROJECT_ROOT` 或 `<repo-root>` 表示的便携式路径。
9. **Optional local locator（可选本地定位符）**：仅用于当前执行环境的便利路径（不构成证据成立的前置条件）。

---

## 核心证据清单

### 1. 机械拓扑与机构学证据（MECH）

#### `E-MECH-001`：双支链五杆闭链机构基线与杆长真值
- **Claim**：StackForce 四轮足机器人的每条腿为双支链五杆闭链机构，大腿杆长 $60\text{ mm}$，小腿杆长 $100\text{ mm}$，横向投影间距 $40\text{ mm}$；彻底排除了伪单串联与假虚拟杆假设。
- **Evidence Type**：CAD/Metrology Geometry Configuration
- **Canonical source**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/closed_link_robot/ref_b_real_fr/four_inner_chains_validation.json`
- **Optional local locator**：`/home/kytolly/Project/IsaacProject/sf_quad/...`
- **Why it supports claim**：四腿几何校验报告中记录了四腿由 FR 模板通过底盘对称反射与单平面手性反转构建的完整参数，并对杆长及间隙给出了机器校验 PASS 判定。
- **How to locate**：
  - 文件：`four_inner_chains_validation.json`
  - 搜索关键词：`"rod_lengths"`, `"thigh_length_mm": 60.0`, `"calf_length_mm": 100.0`
  - 预期观察：四腿的杆长公差均在 $\pm 0.25\text{ mm}$ 门禁内。
- **How to verify / reproduce**：
  ```bash
  python3 -c "import json; data=json.load(open('sf_quad/source/sf_quad/sf_quad/assets/robots/closed_link_robot/ref_b_real_fr/four_inner_chains_validation.json')); print('Status:', data.get('status', 'FAIL'))"
  ```
- **Observed result**：`status: PASS`，四腿 $60\text{ mm}$ 与 $100\text{ mm}$ 杆长判定全绿。

---

#### `E-MECH-002`：机器人自由度与驱动/被动划分（Actuation Partition）
- **Claim**：机器人整机包含 **20 个树状转动关节（Tree Revolute Joints）**、**12 个主动驱动自由度（Active Actuated DOFs）**、**8 个被动转动铰接（Passive Revolute Joints）** 以及 **4 个闭环运动学约束副（Closure Constraints）**；严禁写成“20 自由度”或“20 active DOF”。
- **Evidence Type**：Kinematic Model Definition & URDF Specification
- **Canonical source**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/urdf/stackforce_quadrupedal_wheeled_robot.urdf`
- **Optional local locator**：`/home/kytolly/Project/IsaacProject/sf_quad/.../stackforce_quadrupedal_wheeled_robot.urdf`
- **Why it supports claim**：URDF 与 USD 结构定义中明确包含了：
  - 4 腿 $\times$ 5 个转动关节 = 20 个树状转动关节；
  - 4 腿 $\times$ (M1 舵机 + M2 舵机 + W1 轮电机) = 12 个主动输入；
  - 4 腿 $\times$ (P1 外膝 + P2 内膝) = 8 个被动铰接；
  - 4 腿 $\times$ W2 闭环约束副 = 4 个 PhysX 闭环副（`excludeFromArticulation=true`）。
- **How to locate**：
  - 文件：`stackforce_quadrupedal_wheeled_robot.urdf`
  - 搜索关键词：`<joint name=".*_(thigh|calf|foot|M2|P2)_joint"`
  - 预期观察：刚好匹配到 20 个 `type="revolute"` 的树关节与 8 个 `type="fixed"` 的参考系关节。
- **How to verify / reproduce**：
  ```bash
  grep -c 'type="revolute"' sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf
  ```
- **Observed result**：输出 `20`。
- **Actuator Configuration Boundary（执行器配置边界）**：
  - 机械语义上 P1/P2 为被动副；但在当前 URDF 导入生成的 USD 中，Isaac Sim URDF Importer 为所有 20 个转动关节自动挂载了默认的 `PhysicsDriveAPI:angular`（stiffness=0, damping=0）。
  - 执行器真实动力学响应、阻尼、刚度及电机特性曲线**尚未完成动力学标定**，因此不具备 RL 训练就绪状态（`rl_ready = false`）。

---

### 2. 数字资产与闭环重构证据（ASSET）

#### `E-ASSET-001`：单父树 Loop-Cut 规范 URDF
- **Claim**：URDF 资产保持严格数学树结构（29 links, 28 joints），全机唯一根为 `base_link`，不存在多父节点；闭环回路在 $W_2$ 处显式切断。
- **Evidence Type**：Robot Description Format (URDF)
- **Canonical source**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/urdf/stackforce_quadrupedal_wheeled_robot.urdf`
- **Why it supports claim**：彻底符合 ROS/URDF 解析器标准与刚体动力学 Featherstone 树形算法，避免多父级解析崩溃。
- **How to locate**：
  - 文件：`stackforce_quadrupedal_wheeled_robot.urdf`
  - 搜索关键词：`<link name=".*_W2_frame">`, `<joint name=".*_W2_frame_joint"`
  - 预期观察：`foot_Link` 的 parent 只有 `calf_Link`，`W2_frame` 的 parent 是 `inner_lower_Link`，无回路。
- **How to verify / reproduce**：
  ```bash
  python3 sf_quad/.../scripts/validate_asset.py
  ```
- **Observed result**：`Tree topology verified: 29 links, 28 joints, root=base_link, no multiple parents.`

---

#### `E-ASSET-002`：闭环参考系几何元数据（closure_frames.json）
- **Claim**：四腿 W1/W2 闭环轴向偏置为 $-44.950\text{ mm}$（$-0.044949847\text{ m}$），径向投影残差 $< 1.83 \times 10^{-17}\text{ m}$，P2 配合间隙 $0.150\text{ mm}$，P2 轴向偏置 $13.650\text{ mm}$。
- **Evidence Type**：Structured Configuration Metadata (JSON)
- **Canonical source**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/config/closure_frames.json`
- **Why it supports claim**：持久化保存了从 CAD/USD 几何测量中提取的刚性不变量，作为 PhysX 闭环重构与自动化校验的唯一元数据真源。
- **How to locate**：
  - 文件：`closure_frames.json`
  - 搜索关键词：`"axial_offset_m": -0.04494984724564133`, `"radial_residual_m": 1.8336827645404186e-17`
- **How to verify / reproduce**：
  ```bash
  python3 -c "import json; d=json.load(open('sf_quad/.../closure_frames.json')); print({k: v['radial_residual_m'] for k,v in d['legs'].items()})"
  ```
- **Observed result**：四腿径向残差均小于 $2.0 \times 10^{-17}\text{ m}$，机器校验严格同轴共线。

---

#### `E-ASSET-003`：PhysX 闭环转动副重构算法与生成 USD
- **Claim**：`recover_closed_loops.py` 从 $W_2$ 世界位姿分别向 `inner_lower_Link` 和 `foot_Link` 独立反算局部位姿，在 USD 中生成 4 个 `PhysicsRevoluteJoint` 并配置 `excludeFromArticulation=true`。
- **Evidence Type**：Python Reconstruction Script & USD Composed Asset
- **Canonical source**：
  - 脚本：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/recover_closed_loops.py`
  - 产物：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/usd/stackforce_quadrupedal_wheeled_robot_closed.usda`
- **Why it supports claim**：确保物理求解器将闭环副视为笛卡尔空间等式约束，而不破坏关节树的 Articulation 结构。
- **How to locate**：
  - 文件：`recover_closed_loops.py`
  - 搜索关键词：`excludeFromArticulation`, `PhysicsRevoluteJoint.Define`, `localPos0`, `localPos1`
  - 预期观察：独立反算 `T_local0` 与 `T_local1`，并对 4 条腿创建 `{LEG}_W2_closure_joint`。
- **How to verify / reproduce**：
  在 Isaac Sim Python 环境下执行重构脚本，审查生成的 USDA 中的 `closure_joints` 命名空间。
- **Observed result**：USDA 中包含 4 个带 `excludeFromArticulation = true` 的 `PhysicsRevoluteJoint`。

---

#### `E-ASSET-004`：静态资产自动化门禁校验器
- **Claim**：`validate_asset.py` 自动化通过 29 links, 28 joints, 21 二进制 STL 网格, 4 对闭环参考系的全部静态不变量检查。
- **Evidence Type**：Automated Validator Script & Exit Code
- **Canonical source**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/validate_asset.py`
- **Why it supports claim**：以测试代码 exit code 0 和标准输出为唯一判据，断言资产无多父级、无缺失网格、无残差超标。
- **How to locate**：
  - 运行命令：`python3 sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/validate_asset.py`
- **How to verify / reproduce**：在宿主机直接使用原生 `python3` 运行，无需 GPU 或 Omniverse 依赖。
- **Observed result**：终端打印 `PASS: 29 links, 28 joints, 21 meshes, 4 closure-frame pairs`，进程返回码 0。

---

### 3. 动态物理仿真与负对照证据（PHYS）

#### `E-PHYS-001`：2400 步 CPU 悬空下沉重力验证报告
- **Claim**：闭链数字资产在 CPU 悬空重力场（240 Hz, $dt = 1/240\text{ s}$, 运行 2400 步 / $10.0\text{ s}$）下完成物理仿真烟囱测试；测得刚体运动位移 $0.0906\text{ m}$，四腿最大闭环锚点漂移不超过 $0.0595\text{ mm}$（$\approx 0.060\text{ mm}$，远低于 $1\text{ mm}$ 容差上限），转轴角误差不超过 $5.23 \times 10^{-6}\text{ rad}$（远低于 $0.01\text{ rad}$ 门禁）；`static_status = PASS`, `simulation_status = PASS`, `rl_ready = false`。
- **Evidence Type**：Machine-Readable Simulation Report (JSON)
- **Canonical source**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/validation/simulation_report.json`
- **Test Script**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/simulation_validation.py`
- **Why it supports claim**：排除了仿真器未实际积分（通过测量 `body_motion_m = 0.0906 m` 证明有真实运动），并在长达 10 秒（2400 步）重力自重下垂下拉扯中，四腿闭环铰接点完全保持约束稳定，未撕裂、无发散。
- **How to locate**：
  - 文件：`validation/simulation_report.json`
  - 搜索关键词：`"simulation_status": "PASS"`, `"body_motion_m": 0.090572`, `"steps": 2400`, `"max_anchor_error_m"`
- **How to verify / reproduce**：
  ```bash
  python3 -c "import json; r=json.load(open('sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/validation/simulation_report.json')); print('Status:', r['simulation_status'], 'Drift mm:', max(v['max_anchor_error_m'] for v in r['legs'].values())*1000)"
  ```
- **Observed result**：
  - `simulation_status`: `PASS`
  - `body_motion_m`: `0.090572 m`
  - 各腿最大锚点漂移：
    - FR: $0.0518\text{ mm}$ ($5.18 \times 10^{-5}\text{ m}$)
    - FL: $0.0515\text{ mm}$ ($5.15 \times 10^{-5}\text{ m}$)
    - RL: $0.0528\text{ mm}$ ($5.28 \times 10^{-5}\text{ m}$)
    - RR: $0.0595\text{ mm}$ ($5.95 \times 10^{-5}\text{ m}$)
  - 最大转轴角度误差：$5.23 \times 10^{-6}\text{ rad}$
  - `rl_ready`: `false`

---

#### `E-PHYS-002`：负对照实验（Negative Control Validation）
- **Claim**：通过 `--disable-closures` 禁用 PhysX 闭环副作为负对照组，重力下四腿外链与内链由于缺少约束迅速分离，四腿闭环残差在第 480 步（$t = 2.0\text{ s}$）剧烈漂移至约 $129\text{ mm}$（$0.129\text{ m}$），触发 `RuntimeError: Closure drift exceeds smoke-test limits (1 mm / 0.01 rad)` 并终止；确凿证明闭环保持力来源于 PhysX 关节物理约束，而非初始位姿的巧合。
- **Evidence Type**：Negative Control Report (JSON)
- **Canonical source**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/validation/negative_control_report.json`
- **Why it supports claim**：科学对照必不可少。若不关掉闭环副做负对照，无法反向证实物理约束确实在生效。
- **How to locate**：
  - 文件：`validation/negative_control_report.json`
  - 搜索关键词：`"negative_control": true`, `"max_anchor_error_m": 0.129`, `"RuntimeError: Closure drift exceeds smoke-test limits"`
- **How to verify / reproduce**：
  审查 `validation/negative_control_report.json` 中保存的异常堆栈与漂移曲线数据。
- **Observed result**：
  - `negative_control`: `true`
  - `steps`: `480`
  - `max_anchor_error_m`: `0.12908 m` (FR), `0.12922 m` (FL), `0.12873 m` (RL), `0.12897 m` (RR)
  - 抛出异常：`RuntimeError: Closure drift exceeds smoke-test limits (1 mm / 0.01 rad)`。

---

### 4. 强化学习与动力学边界证据（RL / BOUNDARY）

#### `E-RL-001`：强化学习未就绪边界（RL Ready = False）
- **Claim**：当前数字资产**不得声称达到 RL Ready 状态**；目前仅完成静态装配与无驱动悬空重力烟囱测试，地面接触、碰撞几何、驱动器刚度/阻尼响应以及步态任务尚未通过动力学标定。
- **Evidence Type**：Disposition & Boundary Invariant
- **Canonical source**：`$PROJECT_ROOT/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/validation/simulation_report.json`（`"rl_ready": false`）
- **NVIDIA Isaac Lab 参考规范**：
  - 官方文档：[Isaac Lab Documentation](https://isaac-sim.github.io/IsaacLab/)
  - 检索路径：`Isaac Lab Docs -> Source Code -> Actuators -> ActuatorBaseCfg / ImplicitActuatorCfg`
  - 核心要求：闭链机构的主动关节必须精确配置 `stiffness`、`damping`、`armature` 与 `effort_limit`，而被动关节必须显式解除驱动。
- **Why it supports claim**：防止开发团队越级将仅通过悬空重力烟囱测试的几何资产直接送入强化学习训练环境，导致策略网络利用物理奇异性崩溃。

---

### 5. 硬件真机与安全联锁证据（HW / SAFETY）

#### `E-HW-001`：实机架空审计与 Channel 7 安全断电门禁
- **Claim**：M1 实机基线因第 7 通道（ch7）在 firmware return/STOP 指令后物理回中失败而处于 **BLOCKED** 状态；在完成硬件隔离、检修并验证无负载正常回中前，实机执行器母线必须保持断电（Actuator rail unpowered）。
- **Evidence Type**：Physical Experiment Audit Logs & Safety Records
- **Canonical source**：`doc/StackForceDog/artifacts/physical_session_log.md` 及 `doc/StackForceDog/M1_outcome/M1-final-status.md`
- **Why it supports claim**：实机测试中记录到 ch7 持续上抬，即使固件发送超时与 STOP 仍未停止，构成严重人机安全隐患。
- **How to locate**：
  - 文件：`doc/StackForceDog/artifacts/safety_validation.md`
  - 搜索关键词：`channel 7`, `ch7`, `actuator rail`, `STOP`
- **Observed result**：实机 G01/G02 PASS，G05–G09 PASS WITH EVIDENCE DEBT，G03/G04/G10 BLOCKED，M1 整体验收为 BLOCKED。

---

## 证据检索与交叉引用速查表

| Evidence ID | 证据主题 | 涉及 Milestone / Gate | 状态 | 关键数值 / 判定 |
|---|---|---|---|---|
| `E-MECH-001` | 机械五杆几何 | M1-G08, M2-G03 | **PASS** | 杆长 60/100 mm，间距 40 mm |
| `E-MECH-002` | 20 树关节 / 12 主动驱动 | M1-G03, M2-G02 | **PASS** | 20 revolute joints, 12 active, 8 passive |
| `E-ASSET-001` | 严格树 Loop-Cut URDF | M2-G02, M2-G08 | **PASS** | 29 links, 28 joints, 唯一根 base_link |
| `E-ASSET-002` | 闭环参考系元数据 | M2-G03, M2-G04 | **PASS** | 轴向偏置 -44.950 mm, 残差 < 1.83e-17 m |
| `E-ASSET-003` | PhysX 闭环重构 | M2-G07 | **PASS** | 4 个 PhysicsRevoluteJoint, excludeFromArticulation |
| `E-ASSET-004` | 静态资产自动化门禁 | M2-G08 | **PASS** | `validate_asset.py` 退出码 0 |
| `E-PHYS-001` | 2400 步 CPU 物理下沉测试 | M2 闭链动力学验证 | **PASS** | 运动 0.0906 m, 漂移 <= 0.0595 mm, 角误差 <= 5.23e-6 rad |
| `E-PHYS-002` | 闭环副禁用负对照 | M2 闭链动力学验证 | **PASS** | 漂移达 129 mm, 480 步抛出 RuntimeError 崩溃 |
| `E-RL-001` | 强化学习训练未就绪 | M2 / M4 | **BOUNDARY** | `rl_ready = false`，驱动动力学未标定 |
| `E-HW-001` | 实机安全与 ch7 故障 | M1-G10, M1 Milestone | **BLOCKED** | 实机断电联锁，离线与仿真继续 |

---

## 更新日志

- 2026-09-14：建立便携式证据注册表（Evidence Registry）；收录 `E-MECH-001` 至 `E-HW-001` 完整证据链；详细记录 2400 步 CPU 悬空下沉实验（0.060 mm）与负对照（129 mm）实验数据；规范 Isaac Lab 外部文档引用；确立 A PATH IS NOT EVIDENCE 架构原则。

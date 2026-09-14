---
id: E-SIM-002
title: 双支链闭环几何装配不变量与参考系配置
type: sim
role: config
source_files:
  - /home/kytolly/Project/IsaacProject/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/config/closure_frames.json
status: specified
tags:
  - closure-frames
  - geometric-invariants
  - kinematic-closure
  - simulation-config
---

# E-SIM-002 双支链闭环几何装配不变量与参考系配置

> **认识论角色说明**：本文件属于 `CONFIG`（几何不变量与参考系配置），忠实归档自 `/home/kytolly/Project/IsaacProject/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/config/closure_frames.json`。本文件严格限定于机器人腿部五连杆机构切断点几何装配不变量、各腿参考系空间映射与轴向尺寸公差 Fact 的审计；闭环副的动力学重建脚本与 URDF 资产定义见 [`E-SIM-003`](./E-SIM-003-PhysX闭环副自动重构与USD后处理实现.md) 与 [`E-SIM-001`](./E-SIM-001-闭链四足轮腿机器人单父树URDF资产.md)。

---

## 1. 资产清单与哈希校验

| 资产相对路径 | 资产类型 | 包含配置 | SHA-256 校验和 |
|---|---|---|---|
| `closure_frames.json` | JSON 几何配置契约 | 4条腿几何闭环映射 | `68ad48b32a078c50935bc8021072a146deab447555ebfdebd4759a46aa30ef70` |

---

## 2. 闭环几何参数真值矩阵

| 腿部代号 | 旋转轴在 base_link 投影 | W1 坐标 (m) | W2 坐标 (m) | 轴向距离 $\Delta_{\text{axial}}$ (mm) | 径向残差 (m) |
|---|---|---|---|---|---|
| **FR** | `[ 1.0,  3.74e-6, 0.0]` | `[ 0.0973,  0.1109, -0.0730]` | `[ 0.0524,  0.1109, -0.0730]` | **-44.950** | $1.83 \times 10^{-17}$ |
| **FL** | `[-1.0,  3.74e-6, 0.0]` | `[-0.0973,  0.1109, -0.0730]` | `[-0.0524,  0.1109, -0.0730]` | **-44.950** | $1.83 \times 10^{-17}$ |
| **RL** | `[-1.0, -3.74e-6, 0.0]` | `[-0.0973, -0.1109, -0.0730]` | `[-0.0524, -0.1109, -0.0730]` | **-44.950** | $1.83 \times 10^{-17}$ |
| **RR** | `[ 1.0, -3.74e-6, 0.0]` | `[ 0.0973, -0.1109, -0.0730]` | `[ 0.0524, -0.1109, -0.0730]` | **-44.950** | $1.83 \times 10^{-17}$ |

---

## 3. 原子工程事实与几何不变量（Parts）

### Part 01: 轴向恒定偏置不变量 `axial_offset_m` (`P01`)

1. **几何恒定性**：
   - 四条腿在初始装配状态下，从动连杆参考系 $W_2$ 与轮端连杆参考系 $W_1$ 沿回转主轴的轴向偏移量严格恒等于：
     $$\Delta_{\text{axial}} = -44.949847\,\text{mm} \approx -44.950\,\text{mm}$$
   - 该间距是由腿部平行双连杆的物理厚度、轴承法兰沉头以及装配衬套厚度共同决定的机械常数，不随腿部抬起或伸缩发生形变。

---

### Part 02: 径向共线投影极限精度 `radial_residual_m` (`P02`)

1. **同轴度测定**：
   - 设 $W_1$ 与 $W_2$ 空间向量差为 $\mathbf{\Delta} = \mathbf{P}_{W2} - \mathbf{P}_{W1}$，轴线单位向量为 $\mathbf{u}_{\text{axis}}$；
   - 径向法向投影残差定义为：
     $$\delta_{\text{radial}} = \|\mathbf{\Delta} - (\mathbf{\Delta} \cdot \mathbf{u}_{\text{axis}}) \mathbf{u}_{\text{axis}}\|$$
   - 测定结果四腿皆严格收敛于 $1.83368 \times 10^{-17}\,\text{m}$，达到 IEEE 754 双精度浮点数的机器精度极限，证明装配几何在数学拓扑上做到了绝对严格共轴。

---

### Part 03: P2 关节轴向间距与结构装配间隙 (`P03`)

1. **物理轴向偏置**：
   - `p2_axis_offset_m = 0.013650002766096564` ($\approx 13.650\,\text{mm}$)，精确表征了从动内连杆副与主动驱动支链之间的横向跨距；
2. **防干涉表面间隙**：
   - `p2_surface_gap_m = 0.00014999979090898725` ($\approx 0.150\,\text{mm}$)，为 3D 打印件与金属舵盘运转时预留的最小安全物理防摩擦间隙。

---

### Part 04: 四足空间对称旋转轴向量变换真值 (`P04`)

1. **左右镜像对称**：
   - 右侧前后腿（FR, RR）主轴向量在 X 方向为正向单位向量（$+1.0$）；
   - 左侧前后腿（FL, RL）主轴向量在 X 方向为反向单位向量（$-1.0$）；
2. **前后俯仰微偏量**：
   - Y 轴分量存在微米级安装倾角补偿 $\pm 3.7431 \times 10^{-6}$，忠实反映了机械 CAD 导出时的真实坐标系细微偏置。

---

### Part 05: 闭环副重构校验契约与阈值边界 (`P05`)

1. **配置引用源状态**：
   - 配置显式声明关联前置静态校验产物 `four_inner_chains_validation.json`，且状态标记为 `"PASS"`；
2. **重构残差容差限**：
   - 锚点位置残差上限：$\le 0.001\,\text{m}$ (1.0 mm)；
   - 回转轴向角度残差上限：$\le 0.01\,\text{rad}$ ($0.57^\circ$)；
   - 实测径向残差比容差限小 14 个数量级，完全满足高保真多体动力学仿真的零应力闭环重构条件。

---

## 4. 技术关联与交叉索引

- **URDF 拓扑定义**：[`E-SIM-001 闭链四足轮腿机器人单父树URDF资产`](./E-SIM-001-闭链四足轮腿机器人单父树URDF资产.md)
- **PhysX USD 闭环副自动注入**：[`E-SIM-003 PhysX闭环副自动重构与USD后处理实现`](./E-SIM-003-PhysX闭环副自动重构与USD后处理实现.md)
- **强化学习闭环收敛校验报告**：[`E-VAL-002 强化学习闭环约束收敛与悬空重力烟囱测试报告`](./E-VAL-002-强化学习闭环约束收敛与悬空重力烟囱测试报告.md)

# 机械模型证据（mechanical-model）

> **STATUS**: `ARCHIVED`  
> **NOTICE**: `NOT A CURRENT SOURCE OF TRUTH`  
> 本页面属于重构前几何/机械模型归档记录。最新工程分析见 [[M2-T02-机械拓扑]] 与 E-SIM-001；原子事实真源见 `docs/evidence/`。

---


> 本页属于：stackforce 机器狗实战（evidence）  
> 状态：CANONICAL DELIVERABLE EVIDENCE（八链闭环机器人真实架构）

---

## 核心拓扑抽象

StackForce 四轮足机器人的每条腿不是单串联链，而是包含 1 个闭环的**双支链五杆机构**。整机自由度与驱动拓扑严谨划分为：**20 个树状转动关节（Tree Revolute Joints）、12 个主动驱动自由度（Active Actuated DOFs: 4 Outer Hip + 4 Inner Hip + 4 Wheel）、8 个被动机械铰接（Passive Revolute Joints: 4 Outer Knee + 4 Inner Knee）以及 4 个闭环约束副（Closure Constraints: 4 Closure PhysX Revolute Joints，excludeFromArticulation=true）**。严禁表述为“20 自由度”或“20 active DOF”（见 `E-MECH-002`）。

在工程实现中，机器人被规范形式化为 **4 条 Outer chains（外链/主运动链） + 4 条 Inner chains（内链/闭环支承链）**：

```text
Outer chain (外链 / 主串联支链):
base_link
  -> Outer Hip ({LEG}_Outer_Hip_Joint, 主动舵机转轴)
  -> Outer Thigh ({LEG}_Outer_Thigh_Link, 金属舵盘大腿, 长度 60 mm)
  -> Outer Knee ({LEG}_Outer_Knee_Joint, 膝部转动副)
  -> Outer Calf ({LEG}_Outer_Calf_Link, 外部小腿, 长度 100 mm)
  -> Wheel ({LEG}_Wheel_Joint, 轮电机直驱转轴)
  -> Foot ({LEG}_Foot_Link, 轮毂/轮体/驱动总成)
       └─ Wheel_Frame (fixed frame, 闭环基准参考系)

Inner chain (内链 / 闭环支承副支链):
base_link
  -> Inner Hip ({LEG}_Inner_Hip_Joint, 主动舵机转轴)
  -> Inner Thigh ({LEG}_Inner_Thigh_Link, 内侧金属大腿, 长度 60 mm)
  -> Inner Knee ({LEG}_Inner_Knee_Joint, 被动膝部转动副)
  -> Inner Calf ({LEG}_Inner_Calf_Link, 内部小腿, 长度 100 mm)
  -> Closure [loop cut] ({LEG}_Closure_Frame, 闭环切断点参考系)
```

---

## 刚体与关节对应表（每腿）

| 构件代号 | URDF Link 名称 | 包含零件与物理实体 | 运动学角色 |
|---|---|---|---|
| `base_link` | `base_link` | 铝制半车体连接、8 舵机固定座、主控板、电池 | 树根节点（Root） |
| `Outer Thigh` | `{LEG}_Outer_Thigh_Link` | 金属舵片大腿、螺栓组、驱动盘 | 主动输入（Outer Hip, 60 mm） |
| `Outer Calf` | `{LEG}_Outer_Calf_Link` | 外部小臂、轴承座 | 被动连杆（Outer Knee, 100 mm） |
| `Foot` | `{LEG}_Foot_Link` | 轮电机定子、转子、磁环、轮毂、轮胎 | 轮驱转动（Wheel） |
| `Inner Thigh` | `{LEG}_Inner_Thigh_Link` | 内侧金属舵片大腿、紧固件 | 主动输入（Inner Hip, 60 mm） |
| `Inner Calf` | `{LEG}_Inner_Calf_Link` | 内部小臂、轴承支承 | 被动连杆（Inner Knee, 100 mm） |
| `Wheel frame` | `{LEG}_Wheel_Frame` | 无质量定位坐标系（Fixed child of Foot_Link） | 外侧闭环参考点 |
| `Closure frame` | `{LEG}_Closure_Frame` | 无质量定位坐标系（Fixed child of Inner_Calf_Link） | 内侧闭环切断点（Loop Cut） |

---

## 真实闭环几何关系（Wheel 与 Closure 的物理约定）

$W_1$ 与 $W_2$ 绝非三维同一点！二者在三维机械装配中满足：

$$\text{axis}(W_1) \parallel \text{axis}(W_2)$$

$$W_2 - W_1 = \Delta_{\text{axial}} \cdot \mathbf{a} + \mathbf{r}_{\text{radial}}$$

根据 `closure_frames.json` 与 `four_inner_chains_validation.json` 的机器校验实测真值：

| 参数项 | 实测物理值 | 机器公差 / 状态 | 物理意义 |
|---|---:|---|---|
| **Inner Hip–Inner Knee 杆长** | `60.000 mm` | 严格等于设计值 | 内链大腿孔距 |
| **Inner Knee–Closure 杆长** | `100.000 mm` | 严格等于设计值 | 内链小腿孔距 |
| **Wheel–Closure 轴向偏置** | `-44.949847 mm` ($\approx -44.950\text{ mm}$) | 允许物理层叠错位 | 内外支链在公共轮轴上的物理装配厚度 |
| **Wheel–Closure 径向残差** | $1.83368 \times 10^{-17}\text{ m}$ ($1.83 \times 10^{-14}\text{ mm}$) | $< 2.0 \times 10^{-6}\text{ m}$ (PASS) | 两转轴严格共线，无异面错位 |
| **Inner Knee 轴向偏置** | `13.650003 mm` ($\approx 13.650\text{ mm}$) | 结构装配真值 | 内侧大腿与小腿配合处厚度错开 |
| **Inner Knee 表面配合间隙** | `0.1499998 mm` ($\approx 0.150\text{ mm}$) | $0.15 \pm 0.10\text{ mm}$ (PASS) | 保证小腿内侧不与大腿发生干涉摩擦 |
| **四腿对称性误差** | $\le 6.14 \times 10^{-6}\text{ mm}$ | $< 2.0 \times 10^{-3}\text{ mm}$ (PASS) | FL, RL, RR 由 FR 精确底盘反射推导 |

---

## 历史未决项解决状态

此前留在 Wiki 中的未决疑点已全部由工程资产闭环解决：

- **Front/Rear hip 与 Outer/Inner 支链对应**：**已解决**。外链统一对应 Outer Servo 站位，内链对应 Inner Servo 站位。
- **半车体到 base_link 装配变换**：**已解决**。由 `build_asset.py` 统一定义在 `base_link` 单一世界基准下，无浮动半车体。
- **两支链横向偏置与轮体几何**：**已解决**。横向偏置实测精确为 $-44.950\text{ mm}$；轮体 `Foot_Link` 网格统一对齐。
- **URDF 树拓扑与闭环冲突**：**已解决**。URDF 采用 $W_2$ 单向 loop-cut 保持 29 links / 28 joints 严格单父树；Isaac Sim 阶段通过 `recover_closed_loops.py` 建立 PhysX revolute joint 重建闭环。

---

## 验证凭证文件（统一索引至 [[evidence-registry]]）

- 闭环参考系元数据：`sf_quad/.../config/closure_frames.json` (`E-ASSET-002`)
- 四腿几何验证报告：`sf_quad/.../ref_b_real_fr/four_inner_chains_validation.json` (`E-MECH-001`)
- 规范树状 URDF：`sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf` (`E-ASSET-001`, `E-MECH-002`)
- 静态资产校验器：`sf_quad/.../scripts/validate_asset.py` (`E-ASSET-004`)

---

## 更新日志

- 2026-09-14：补充严格驱动与关节划分（20 树关节 / 12 主动 / 8 被动 / 4 约束）；统一接入 [[evidence-registry]] 并消除绝对路径。
- 2026-09-13：根据四腿闭环交付物与校验 JSON 全面更新；将原 UNKNOWN 项升级为精确机器测量值；规范内外八链拓扑与闭环轴向/径向数学关系。
- 2026-09-03：由 `mechanical_model.md` 迁移为 evidence。


> 兼容说明：旧 CAD/URDF 记录中的 M1/M2/P1/P2/Wheel/Closure、`thigh_Link` 等仅作为 Source Alias；当前工程身份以 canonical registry 和 T-ACT-001 为准。

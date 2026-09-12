# 机械模型证据（mechanical-model）

> 本页属于：stackforce 机器狗实战（evidence）  
> 状态：CANONICAL DELIVERABLE EVIDENCE（八链闭环机器人真实架构）

---

## 核心拓扑抽象

StackForce 四轮足机器人的每条腿不是单串联链，而是包含 1 个闭环的**双支链五杆机构**。整机具备：**20 个运动构件、24 个转动铰接、4 个闭环、12 个独立控制输入**。

在工程实现中，机器人被规范形式化为 **4 条 Outer chains（外链/主运动链） + 4 条 Inner chains（内链/闭环支承链）**：

```text
Outer chain (外链 / 主串联支链):
base_link
  -> M1 (thigh_joint, 主动舵机转轴)
  -> outer_upper (thigh_Link, 金属舵盘大腿, 长度 60 mm)
  -> P1 (calf_joint, 膝部转动副)
  -> outer_lower (calf_Link, 外部小腿, 长度 100 mm)
  -> W1 (foot_joint, 轮电机直驱转轴)
  -> foot (foot_Link, 轮毂/轮体/驱动总成)
       └─ W1_frame (fixed frame, 闭环基准参考系)

Inner chain (内链 / 闭环支承副支链):
base_link
  -> M2 (M2_joint, 主动舵机转轴)
  -> inner_upper (inner_upper_Link, 内侧金属大腿, 长度 60 mm)
  -> P2 (P2_joint, 被动膝部转动副)
  -> inner_lower (inner_lower_Link, 内部小腿, 长度 100 mm)
  -> W2 [loop cut] (W2_frame, 闭环切断点参考系)
```

---

## 刚体与关节对应表（每腿）

| 构件代号 | URDF Link 名称 | 包含零件与物理实体 | 运动学角色 |
|---|---|---|---|
| `base_link` | `base_link` | 铝制半车体连接、8 舵机固定座、主控板、电池 | 树根节点（Root） |
| `outer_upper` | `{LEG}_thigh_Link` | 金属舵片大腿、螺栓组、驱动盘 | 主动输入（M1, 60 mm） |
| `outer_lower` | `{LEG}_calf_Link` | 外部小臂、轴承座 | 被动连杆（P1, 100 mm） |
| `foot` | `{LEG}_foot_Link` | 轮电机定子、转子、磁环、轮毂、轮胎 | 轮驱转动（W1） |
| `inner_upper` | `{LEG}_inner_upper_Link` | 内侧金属舵片大腿、紧固件 | 主动输入（M2, 60 mm） |
| `inner_lower` | `{LEG}_inner_lower_Link` | 内部小臂、轴承支承 | 被动连杆（P2, 100 mm） |
| `W1_frame` | `{LEG}_W1_frame` | 无质量定位坐标系（Fixed child of foot_Link） | 外侧闭环参考点 |
| `W2_frame` | `{LEG}_W2_frame` | 无质量定位坐标系（Fixed child of inner_lower_Link） | 内侧闭环切断点（Loop Cut） |

---

## 真实闭环几何关系（W1 与 W2 的物理约定）

$W_1$ 与 $W_2$ 绝非三维同一点！二者在三维机械装配中满足：

$$\text{axis}(W_1) \parallel \text{axis}(W_2)$$

$$W_2 - W_1 = \Delta_{\text{axial}} \cdot \mathbf{a} + \mathbf{r}_{\text{radial}}$$

根据 `closure_frames.json` 与 `four_inner_chains_validation.json` 的机器校验实测真值：

| 参数项 | 实测物理值 | 机器公差 / 状态 | 物理意义 |
|---|---:|---|---|
| **M2–P2 杆长** | `60.000 mm` | 严格等于设计值 | 内链大腿孔距 |
| **P2–W2 杆长** | `100.000 mm` | 严格等于设计值 | 内链小腿孔距 |
| **W1–W2 轴向偏置** | `-44.949847 mm` ($\approx -44.950\text{ mm}$) | 允许物理层叠错位 | 内外支链在公共轮轴上的物理装配厚度 |
| **W1–W2 径向残差** | $1.83368 \times 10^{-17}\text{ m}$ ($1.83 \times 10^{-14}\text{ mm}$) | $< 2.0 \times 10^{-6}\text{ m}$ (PASS) | 两转轴严格共线，无异面错位 |
| **P2 轴向偏置** | `13.650003 mm` ($\approx 13.650\text{ mm}$) | 结构装配真值 | 内侧大腿与小腿配合处厚度错开 |
| **P2 表面配合间隙** | `0.1499998 mm` ($\approx 0.150\text{ mm}$) | $0.15 \pm 0.10\text{ mm}$ (PASS) | 保证小腿内侧不与大腿发生干涉摩擦 |
| **四腿对称性误差** | $\le 6.14 \times 10^{-6}\text{ mm}$ | $< 2.0 \times 10^{-3}\text{ mm}$ (PASS) | FL, RL, RR 由 FR 精确底盘反射推导 |

---

## 历史未决项解决状态

此前留在 Wiki 中的未决疑点已全部由工程资产闭环解决：

- **Front/Rear hip 与 M/S 支链对应**：**已解决**。外链统一对应 M1 舵机站位，内链对应 M2 舵机站位。
- **半车体到 base_link 装配变换**：**已解决**。由 `build_asset.py` 统一定义在 `base_link` 单一世界基准下，无浮动半车体。
- **两支链横向偏置与轮体几何**：**已解决**。横向偏置实测精确为 $-44.950\text{ mm}$；轮体 `foot_Link` 网格统一对齐。
- **URDF 树拓扑与闭环冲突**：**已解决**。URDF 采用 $W_2$ 单向 loop-cut 保持 29 links / 28 joints 严格单父树；Isaac Sim 阶段通过 `recover_closed_loops.py` 建立 PhysX revolute joint 重建闭环。

---

## 验证凭证文件

- `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/config/closure_frames.json`
- `sf_quad/source/sf_quad/sf_quad/assets/robots/closed_link_robot/ref_b_real_fr/four_inner_chains_validation.json`
- `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/urdf/stackforce_quadrupedal_wheeled_robot.urdf`
- `sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/scripts/validate_asset.py`

---

## 更新日志

- 2026-09-13：根据四腿闭环交付物与校验 JSON 全面更新；将原 UNKNOWN 项升级为精确机器测量值；规范内外八链拓扑与闭环轴向/径向数学关系。
- 2026-09-03：由 `mechanical_model.md` 迁移为 evidence。


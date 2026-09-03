# URDF-02-零件与腿部运动学

> 本页属于：stackforce 机器狗实战（M2 URDF 实操）
> 前置知识：[[URDF-01-自由度与命名]]
> 预计阅读时间：20 分钟

## 🎯 为什么需要这个？

拿到 STL 后不能"一个 STL = 一个 link"，也不能从零猜腿部运动学。本页讲：**物理 link 合并**、**复用 Mini URDF 的腿部变换**、**确定腿根位置**。

## 阶段 3：STL 分成"物理 link"和"装饰零件"

URDF 的 link 表示"物理上整体刚性运动的刚体"。官方 STL 有：

```text
1x主体中间连接件.stl   1x电池盖板.stl
2x主体.stl            2x前后主体盖板.stl
4x前小臂.stl          4x后小臂.stl
4x轮固定.stl          4x轮毂.stl        4x轮轴盖子.stl
8x舵机盖板.stl        8x金属舵片大腿部.stl  8x外固定.stl
```

固定在一起的零件要**合并到同一 link**：

```text
主体 + 盖板 + 电池盖板 + 连接件 + 螺丝 + PCB + 电池  →  base_link
```

轮子相关若一起刚性旋转：

```text
wheel_link
├── 轮毂 visual
├── 轮轴盖 visual
└── 轮固定 visual
```

**不要因为有三个 STL 就做三个运动 link。**

## 阶段 4：复用 Mini URDF 恢复腿部运动学

本地已找到 Mini/双轮足 URDF：`~/Library/bipedal_wheeled_robot/模型/SF_bipedalWheel/urdf/20250820_1.urdf`，提供 `base → LT → LC → LW` 的 joint origin / axis / limit / inertia / COM / mesh。对照：

```text
Mini:      base → LT → LC → LW
Quadruped: base → FL_upper → FL_lower → FL_wheel
```

**已从该 URDF 提取的腿部数据（左腿，米/弧度）：**

| 关节 | origin xyz (m) | axis | lower/upper (rad) | effort |
|------|----------------|------|-------------------|--------|
| LT_joint（髋） | 0.0372, 0.0401, 0.0056 | (0, -1, 0) | -1.3479 / 0.3363 | 30 |
| LC_joint（膝） | 0.0040, 0.0083, -0.0600 | (0, -1, 0) | -0.2915 / 1.25 | 30 |
| LW_joint（轮） | 0.0020, 0.0240, -0.1000 | (0, 1, 0) | -1e6 / 1e6（连续） | 5 |

link 质量（初始估计）：base 0.266 kg，大腿 0.008 kg，小腿 0.0166 kg，轮 0.056 kg。

> **最值得复用的是相对变换**：`upper→lower`、`lower→wheel`；若机械尺寸相同可直接作为四轮足初版的 `<origin>`。而 `base→FL/FR/RL/RR` 四个腿根必须按四轮足重新确定。

## 阶段 5：确定四个腿根位置（最关键尺寸）

需要得到：

```text
p_FL=(x_FL, y_FL, z_FL)   p_FR=...   p_RL=...   p_RR=...
```

若高度对称可能类似：

```text
FL=(+L/2, +W/2, z)   FR=(+L/2, -W/2, z)
RL=(-L/2, +W/2, z)   RR=(-L/2, -W/2, z)
```

但**不要直接假定**。没有 STEP assembly 时，用游标卡尺实测：

```text
前后 hip axis 中心距离 L = ? mm
左右 hip axis 中心距离 W = ? mm
hip axis 相对 body 中心高度 = ? mm
```

> 测的是 **joint axis center → joint axis center**，不是外壳尺寸。这个尺寸比外壳尺寸重要得多。

## ✏️ 小练习

**1.** 为什么固定零件要合并成一个 link？

<details>
<summary>查看答案</summary>

URDF 的 link 是"整体刚性运动"的刚体；固定在一起的零件不产生相对运动，拆成多个 link 只会徒增刚体和计算量。
</details>

**2.** Mini URDF 里最该复用的是什么？

<details>
<summary>查看答案</summary>

腿内的相对变换（upper→lower、lower→wheel 的 origin/axis/limit），而不是 base→各腿根的绝对位置。
</details>

## 本章小结

- STL 分组：固定件合并，轮子相关件归 wheel_link。
- 复用 Mini URDF 的腿部 origin/axis/limit/inertia（见上表）。
- 腿根位置 L/W/z 用游标卡尺实测 joint axis 中心距。

## 下一步

- 上一页：[[URDF-01-自由度与命名]]
- 下一页：[[URDF-03-最小骨架与验证]]
- 返回：[[Home]]

## 更新日志

- 2026-09-02：新增本页。来源：用户 URDF 路线（阶段 3–5）+ 本地 `bipedal_wheeled_robot/.../20250820_1.urdf`。

# 几何基线证据（geometry-baseline）

> 本页属于：stackforce 机器狗实战（evidence）  
> 状态：CANONICAL DELIVERABLE EVIDENCE（四腿机器校验真值）

---

## 冻结机械几何参数

根据右前腿（FR）经典几何注册及全车底盘对称镜像扩展，所有四腿均已达到机器可验证的高精度收敛状态：

| 几何参数项 | 标称与实测值 | 机器校验公差 | 状态与判定来源 |
|---|---:|---|---|
| **大腿杆长（M1–P1 / M2–P2）** | `60.000 mm` | $\pm 0.25\text{ mm}$ | **PASS** (`four_inner_chains_validation.json`) |
| **小腿杆长（P1–W1 / P2–W2）** | `100.000 mm` | $\pm 0.25\text{ mm}$ | **PASS** (`four_inner_chains_validation.json`) |
| **两 hip 间距（L5 投影）** | `40.000 mm` | $\pm 0.25\text{ mm}$ | **PASS** (`geometry_config.json`) |
| **P2 轴承轴向错位** | `13.650003 mm` | $\pm 0.05\text{ mm}$ | **PASS** (`closure_frames.json`) |
| **P2 表面配合间隙** | `0.1499998 mm` ($\approx 0.150\text{ mm}$) | $0.15 \pm 0.10\text{ mm}$ | **PASS** (`four_inner_chains_validation.json`) |
| **W1/W2 轴向偏置（Axial Offset）** | `-44.949847 mm` ($\approx -44.950\text{ mm}$) | 允许物理层叠错位 | **PASS** (`closure_frames.json`) |
| **W1/W2 径向残差（Radial Residual）** | $1.83368 \times 10^{-14}\text{ mm}$ ($1.83 \times 10^{-17}\text{ m}$) | $\le 2.0 \times 10^{-6}\text{ m}$ | **PASS** (`validate_asset.py`) |
| **四腿镜像对称性误差** | $\le 6.14 \times 10^{-6}\text{ mm}$ | $\le 2.0 \times 10^{-3}\text{ mm}$ | **PASS** (`four_inner_chains_validation.json`) |

---

## 四腿底盘对称扩展关系

FR 是唯一人工精细注册并经装配验证的主内链模板。以 `base_link` 中心 $C$ 为原点，对于 FR 任意点 $p$，其余三腿位置严格由底盘反射变换生成：

$$\begin{aligned}
\text{FR: } p' &= C + \text{diag}( 1,  1, 1) (p - C) \\
\text{FL: } p' &= C + \text{diag}(-1,  1, 1) (p - C) \\
\text{RL: } p' &= C + \text{diag}(-1, -1, 1) (p - C) \\
\text{RR: } p' &= C + \text{diag}( 1, -1, 1) (p - C)
\end{aligned}$$

> **注意绕向反转**：FL 与 RR 属于单平面镜像（行列式为 $-1$），其 STL mesh 三角面顶点绕向（face winding）必须反转，以保证法向量一致向外。严禁对 FL/RL/RR 进行独立点位搜索。

---

## 三维闭环物理条件

真实双支链五杆机构不是“压成一张纸”的二维连杆：

1. **同轴平行**：$\text{axis}(W_1) \parallel \text{axis}(W_2)$，四腿转轴方向单位向量已写入 `closure_frames.json`。
2. **共线无异面**：径向投影残差 $\|\mathbf{d} - (\mathbf{d} \cdot \mathbf{a})\mathbf{a}\| = 1.83 \times 10^{-17}\text{ m}$，机器验证严格共线。
3. **允许轴向错位**：轴向投影 $\mathbf{d} \cdot \mathbf{a} = -44.950\text{ mm}$，代表内外支链在轮轴上的实际装配厚度。

---

## 已否决的历史候选与反模式（Anti-Patterns）

- ❌ **$W_1 == W_2$ 重合论**：**REJECTED**。三维端点若强制重合，会导致内外腿丧失轴向装配厚度，使小腿穿透车体。
- ❌ **$\pm 76.5\text{ mm}$ 半车体纵向平移**：**REJECTED**。实机与 FreeCAD 装配检验已彻底否决。
- ❌ **降维至二维平面 IK**：**REJECTED**。真实五连杆机构在横向有物理厚度分布，二维 IK 会产生错误的虚假干涉。
- ❌ **为修补视觉穿模擅自修改铰接位置**：**REJECTED**。铰链位置为运动学绝对真值，穿模属于 mesh 局部偏置/翻转问题，两者严禁耦合。

---

## 更新日志

- 2026-09-13：根据四腿闭环交付报告与校验 JSON 全面升级；更新为四腿 60/100/40 mm 机器校验真值、-44.950 mm 轴向偏置与 1.83e-14 mm 径向残差；固化底盘对称反射与防踩坑不变量。
- 2026-09-03：由 `M2-4_final_report.md` 与 geometry CSV 迁移为 evidence。


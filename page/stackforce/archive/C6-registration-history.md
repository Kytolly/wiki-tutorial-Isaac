# 几何注册历史与实验归档（C6 Registration History）

> 本页属于：stackforce 机器狗实战（archive）  
> 状态：HISTORICAL PROVENANCE & AUDIT TRAIL（非当前主基线，作为溯源留存）

---

## 概述

在达成当前正式的闭链八链数字资产前，工程团队在右前腿（FR）主链注册和四腿装配中经历了密集的调试与审计探索（代号 C6.xx 系列）。为保持 Wiki 首页与主里程碑页面简洁清晰，历史探索被完整归档于本页，并严格分类为 **已采纳凭据（Accepted）**、**已被替代实验（Superseded）** 和 **已否决/失败分支（Rejected/Failed）**。

---

## 实验与分支分类矩阵

| 实验代号 | 主题内容 | 分类评级 | 历史地位与结论 |
|---|---|---|---|
| **C6.17 / RefB** | FR 初始姿态反求 | **SUPERSEDED** | 验证了从实机照片和 CAD 初步提取大腿/小腿空间坐标的可行性，后被高精度注册替代 |
| **C6.18** | FR 局部参考系注册 | **SUPERSEDED** | 确定了 `base_link` 与大腿根部局部坐标系的基准关系 |
| **C6.19** | FR P2 闭环初次恢复 | **SUPERSEDED** | 首次验证在 Isaac Sim 中通过局部反算重建闭环转动副，但未包含表面装配间隙 |
| **C6.20–C6.23** | 轴向层叠与手性堆叠探索 | **ACCEPTED EVIDENCE** | **关键突破**：确立了内外两链不是二维重合五连杆，而是在轴向有 $-44.950\text{ mm}$ 物理厚度层叠 |
| **C6.24** | 翻转硬币面（Double Coin Flip） | **ACCEPTED EVIDENCE** | 解决了小臂 STL 在特定视角下视觉厚度朝向的装配匹配 |
| **C6.25** | 下外侧小腿轴向堆叠 | **ACCEPTED EVIDENCE** | 验证了轮体固定端与外小臂连接面的厚度匹配 |
| **C6.26** | W2 轴承转轴对齐审计 | **ACCEPTED EVIDENCE** | 证实 $W_1$ 与 $W_2$ 轴线严格平行共线，径向残差趋近于零 |
| **C6.27** | 考虑厚度的几何优化 | **ACCEPTED EVIDENCE** | 引入 $0.150\text{ mm}$ P2 表面防摩擦间隙 |
| **C6.28** | FR P2 表面精准贴合固化 | **FINAL ACCEPTED GEOMETRY** | 固化 FR 经典内链几何：M2-P2 60 mm、P2-W2 100 mm、P2 间隙 0.150 mm、W1/W2 偏置 -44.950 mm |
| **C6.29** | 四腿内链对称扩展与绕向反转 | **FINAL ACCEPTED GEOMETRY** | 将 FR 经典几何通过底盘镜像推导至 FL/RL/RR，反转 FL/RR 三角面绕向，生成全车闭链 |
| **C6.30** | 四腿内链机器验证门禁 | **CANONICAL VALIDATION** | 输出 `four_inner_chains_validation.json`，验证全四腿对称误差 $\le 6.14\times 10^{-6}\text{ mm}$，全票 PASS |

---

## 明确否决的历史错误路线（Negative Knowledge）

为防止后续开发者或自动化 Agent 重复过去的死胡同，以下历史假设已被权威否决：

1. **二维连杆 IK 假设（Planar Five-Bar Assumption）**：
   - *错误做法*：假设内外支链在大腿根部和轮端三维重合，使用纯二维几何求解逆运动学。
   - *否决原因*：实机内外支链沿转轴方向错开近 $45\text{ mm}$，强行二维化会导致机械装配严重干涉。
2. **重搜铰链中心修补穿模（Pivot Relocalization for Meshes）**：
   - *错误做法*：看到网格面有穿模就重新优化 M2/P2 铰链三维坐标。
   - *否决原因*：铰链轴心是绝对运动学真值，网格穿模属于 STL 导出时局部原点或翻转问题，二者必须解耦。
3. **URDF 双父级多环路语法（Multi-Parent URDF）**：
   - *错误做法*：在 URDF 语法内将 `foot_Link` 同时设为 `calf_Link` 与 `inner_lower_Link` 的 child。
   - *否决原因*：破坏标准 URDF 树状定义，导致 ROS 与 Isaac Sim 均无法完成刚体树初始化。

---

## 历史日志归档索引

相关原始运行日志均归档于 `sf_quad/logs/debug/`：
- `RefB_C618_FR_LocalFrameRegistration_20260912_205821.log`
- `RefB_C619_FR_P2ClosureRecovery_20260912_210843.log`
- `RefB_C620_FR_AxialStacking_20260912_211434.log`
- `RefB_C626_FR_W2BearingAxisAudit_20260912_224626.log`
- `RefB_C627_FR_ThicknessAware_20260912_230948.log`
- `C6_28_FR_P2_surface_snap_20260912_231706.log`
- `C6_29_four_inner_chains_20260912_234853.log`
- `C6_30_four_inner_chains_validation_20260912_234915.log`

---

## 更新日志

- 2026-09-13：创建 C6 注册历史归档；将 C6.18–C6.30 历史调试探索降级并归类为历史溯源，消除主页面对具体 debug 编号的依赖。

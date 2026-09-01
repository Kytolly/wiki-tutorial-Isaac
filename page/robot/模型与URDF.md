# 模型与URDF

> 本页属于：robot StackForce 实战
> 前置知识：[[硬件与接口]]
> 预计阅读时间：15 分钟

## 🎯 为什么需要这个？

Isaac Lab 需要机器人的 **URDF/xacro** 来描述连杆、关节、质量和惯量。但 StackForce 仓库里**只有 STL 打印件，没有 URDF**，所以我们要自己建——这是把真实机器人搬进仿真的第一步。

## 💡 一个类比

URDF = 机器人的"骨骼 + 关节说明书"：每块骨头多长、多重、绕哪个轴转、转多大范围。STL 只是"外形皮肤"，URDF 才是"能动的骨架"。

## 🐍 最小必要知识

| 术语 | 是什么 |
|------|--------|
| **link（连杆）** | 刚体段（大腿、小腿、机身），有质量/惯量/碰撞体 |
| **joint（关节）** | 两连杆间的运动约束（revolute 旋转） |
| **origin/axis** | 关节坐标系原点与旋转轴 |
| **visual vs collision** | 显示用网格 vs 物理碰撞网格 |

## 🤖 从固件参数重建 URDF

固件里已有关键尺寸（单位 mm）：

```text
L1=60（大腿上段）  L2=100  L3=100  L4=60（小腿）  L5=40（足/轮）
BASE_HEIGHT=110（站立高度）  HEIGHT_MAX=130
```

据此建立 xacro（示意，真实值需按 STL 精修）：

```xml
<link name="base_link"/>
<!-- 右前腿 α 肩关节 -->
<joint name="RF_alpha" type="revolute">
  <parent link="base_link"/>
  <child link="RF_thigh"/>
  <origin xyz="0.06 0.05 0" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="2.0" velocity="10.0"/>
</joint>
```

> 实际项目建议：用 `xacro` 写一个腿模板，四腿复用；质量/惯量先用估算值，之后按真实重量修正。

## ✏️ 小练习

**1.** 仓库里为什么没有现成 URDF？

<details>
<summary>查看答案</summary>

仓库只开源了 3D 打印 STL 和固件代码，没有提供机器人描述文件，所以需要从 STL + 固件尺寸参数自行建立 URDF/xacro。
</details>

**2.** visual 和 collision 网格有什么区别？

<details>
<summary>查看答案</summary>

visual 是渲染显示用的精细网格；collision 是物理碰撞用的简化网格，简化可提升仿真速度。
</details>

## 本章小结

- 仓库无 URDF，需自建：STL 提供外形，固件 L1–L5 提供尺寸，8 舵机提供关节。
- URDF 核心：link（质量/惯量）+ joint（revolute + origin/axis/limit）。
- 建议 xacro 参数化，四腿复用同一模板。

## 下一步

- 上一页：[[硬件与接口]]
- 下一页：[[导入Isaac-Lab]]
- 返回：[[Home]]

## 更新日志

- 2026-08-31：新增本页。来源：本地仓库 `Structure/*.stl` 与 `kinematics.h`（L1–L5 尺寸）。

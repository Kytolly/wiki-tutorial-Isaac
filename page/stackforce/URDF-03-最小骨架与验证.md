# URDF-03-最小骨架与验证

> 本页属于：stackforce 机器狗实战（M2 URDF 实操）
> 前置知识：[[URDF-02-零件与腿部运动学]]
> 预计阅读时间：20 分钟

## 🎯 为什么需要这个？

先写**完全没有 mesh 的 URDF**，用简单几何体把 12 DOF 骨架跑通，再谈 STL。这样你只调 Kinematics，不会同时面对 mesh 原点/单位/rpy/axis 五个问题混在一起。

## 阶段 6：无 mesh URDF 骨架

```xml
<robot name="stackforce_quadruped">
  <link name="base_link"/>
  <link name="FL_upper_link"/>
  <link name="FL_lower_link"/>
  <link name="FL_wheel_link"/>
  ...（FR/RL/RR 同理）
</robot>
```

joint 示例：

```xml
<joint name="FL_hip_joint" type="revolute">
  <parent link="base_link"/>
  <child link="FL_upper_link"/>
  <origin xyz="0.037 0.040 0.006" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.35" upper="0.34" effort="30" velocity="10"/>
</joint>
```

先把 12 个 DOF 全部建起来（4 腿 ×（髋+膝+轮））。

## 阶段 7：用简单几何体验证骨架

body 用 box，腿用 cylinder，轮用 cylinder：

```xml
<visual>
  <geometry>
    <box size="0.2 0.1 0.04"/>
  </geometry>
</visual>
```

得到一个"丑但运动学正确"的骨架：

```text
        ┌──────────┐
    ○───┤          ├───○
        │   BODY   │
    ○───┤          ├───○
        └──────────┘
```

然后导入 Isaac Sim，逐个操作 `FL_hip / FL_knee / FL_wheel / FR_...`，检查：

- 转轴是否在真实轴心
- 正方向是否正确
- 左右是否镜像、前后是否正确
- wheel 是否绕轮轴旋转
- link 是否断开/漂移

做到 **骨架完全正确** 再继续。

## ✏️ 小练习

**1.** 为什么第一步不放 STL？

<details>
<summary>查看答案</summary>

先把 mesh 原点/单位/rpy 等问题隔离出去，只验证 Kinematics；否则多个错误混在一起难定位。
</details>

**2.** 骨架阶段要验证哪些项？

<details>
<summary>查看答案</summary>

转轴轴心、正方向、左右镜像、前后、wheel 转轴、link 是否断开/漂移。
</details>

## 本章小结

- 无 mesh URDF 先把 12 DOF 建齐。
- 用 box/cylinder 验证骨架。
- 导入 Isaac Sim 逐个关节检查，骨架完全正确再进 STL。

## 下一步

- 上一页：[[URDF-02-零件与腿部运动学]]
- 下一页：[[URDF-04-视觉碰撞与动力学]]
- 返回：[[Home]]

## 更新日志

- 2026-09-02：新增本页。来源：用户 URDF 路线（阶段 6–7）。

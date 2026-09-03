# URDF-04-视觉碰撞与动力学

> 本页属于：stackforce 机器狗实战（M2 URDF 实操）
> 前置知识：[[URDF-03-最小骨架与验证]]
> 预计阅读时间：20 分钟

## 🎯 为什么需要这个？

骨架对了之后，才加 STL 外观、简化碰撞、补质量/惯量、写关节限位。顺序不能乱：**先几何，再动力学，再执行器**。

## 阶段 8：加入 STL visual mesh

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <mesh filename="package://stackforce_description/meshes/xxx.stl"
          scale="0.001 0.001 0.001"/>
  </geometry>
</visual>
```

> **STL 单位**：STL 通常不携带可靠单位。若官方 STL 是 mm、URDF 用 m，则 `scale="0.001 0.001 0.001"` 可能必要。但先实际检查 STL 尺寸，不能盲目加。

## 阶段 9：Visual 和 Collision 分开

复杂 STL 只做 visual；collision 用简化几何：

```xml
<visual>
  <geometry><mesh filename="...复杂_body.stl"/></geometry>
</visual>

<collision>
  <geometry><box size="0.2 0.1 0.04"/></geometry>
</collision>
```

- 腿：visual 用复杂 STL，collision 用 capsule / box
- 轮子：visual 用轮毂 STL，collision 用简单 cylinder

> 后面要 4096 / 8192 / 16384 并行环境，复杂三角网格 collision 对大规模 RL 非常不划算。

## 阶段 10：质量、COM、惯量

```xml
<inertial>
  <origin xyz="COM_x COM_y COM_z"/>
  <mass value="..."/>
  <inertia ixx="..." ixy="..." ixz="..." iyy="..." iyz="..." izz="..."/>
</inertial>
```

- 腿部若与 Mini 相同，可先用 Mini URDF 数据作 **v1.0 initial estimate**（大腿 0.008 / 小腿 0.0166 / 轮 0.056 kg）。
- body 必须重算。建议实际称重：整机 / body assembly / 单腿 assembly / wheel assembly / battery。
- CAD 给惯量 `I_CAD`，实测给质量 `m_real`；若 CAD 密度只是统一假设，按质量比例修正：

```text
I_corrected ≈ I_CAD × (m_real / m_CAD)
```

## 阶段 11：joint limit 和 actuator 信息

从实机确认 `q_min, q_max`、`qdot_max`、`τ_max`：

```xml
<limit lower="..." upper="..." effort="..." velocity="..."/>
```

> **不要直接相信 Mini URDF 里 velocity=1000 就是实机规格**。真正限制从 motor datasheet / firmware / 实机测试获得。

## ✏️ 小练习

**1.** 为什么 collision 要简化？

<details>
<summary>查看答案</summary>

复杂三角网格碰撞在大规模并行环境里非常耗算力；用 box/capsule/cylinder 轻得多。
</details>

**2.** `velocity=1000` 能直接用吗？

<details>
<summary>查看答案</summary>

不能。Mini URDF 的 velocity 常是导出器占位值，需从 datasheet/firmware/实机测试确认真实速度上限。
</details>

## 本章小结

- 加 STL visual，注意 mm→m 的 scale。
- visual 与 collision 分离，collision 用简化几何。
- 质量实测、惯量用 CAD 并按质量比例修正。
- limit/actuator 以 datasheet/firmware/实机为准。

## 下一步

- 上一页：[[URDF-03-最小骨架与验证]]
- 下一页：[[URDF-05-到Isaac-Lab与系统辨识]]
- 返回：[[Home]]

## 更新日志

- 2026-09-02：新增本页。来源：用户 URDF 路线（阶段 8–11）。

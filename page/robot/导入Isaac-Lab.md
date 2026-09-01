# 导入Isaac-Lab

> 本页属于：robot StackForce 实战
> 前置知识：[[模型与URDF]]、[[Isaac-Lab项目结构与训练流程]]
> 预计阅读时间：20 分钟

## 🎯 为什么需要这个？

有了 URDF，还要把它转成 Isaac Sim 能用的 **USD**，再写 Isaac Lab 的机器人配置（关节、执行器、初始状态），机器人才能在仿真里"站起来"。

## 💡 一个类比

URDF 是"设计图纸"，USD 是"施工完成后的实体"，Isaac Lab 配置是"给每个关节装上马达、定好初始姿势"。

## 核心概念

| 概念 | 是什么 |
|------|--------|
| **URDF importer** | Isaac Sim 把 URDF → USD 的导入器 |
| **ArticulationCfg** | 描述机器人关节/连杆的配置类 |
| **ImplicitActuatorCfg** | 隐式执行器：给定刚度/阻尼/限幅 |
| **init_state** | 机器人生成时的初始关节角/位置 |

## 快速上手

```python
import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg

STACKFORCE_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path="<你的urdf路径>/stackforce.urdf",
        usd_dir="<导出usd目录>",
        fix_base=False,                # 不固定机身，让它能自由运动
        rigid_props=sim_utils.RigidBodyPropertiesCfg(disable_gravity=False),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0, 0, 0.11),              # 站立高度约 110mm
        joint_pos={"RF_alpha": 0.0, "RF_beta": 0.0, "...": 0.0},  # 8 关节初始角
    ),
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=["RF_alpha", "RF_beta", "LF_alpha", "LF_beta",
                              "RB_alpha", "RB_beta", "LB_alpha", "LB_beta"],
            effort_limit_sim=20.0,       # 舵机力矩限幅（估算）
            velocity_limit_sim=10.0,
            stiffness=40.0,              # 舵机近似刚度
            damping=2.0,
        ),
    },
)
```

> 舵机不是力矩源而是位置源，ImplicitActuatorCfg 只是近似；更准可用 `IdealPDActuatorCfg` 或自定义执行器模型（见 train 级）。

## 验证

写 standalone 脚本 spawn 机器人、`sim.step()` 若干步，确认：不穿模、不炸飞、关节能动。

## 本章小结

- 流程：URDF → USD（UrdfFileCfg）→ ArticulationCfg + Actuators。
- fix_base=False 让机器人自由落地；init_state 给站立姿态。
- 舵机用位置式执行器近似，限幅和刚度需要实测修正。

## 下一步

- 上一页：[[模型与URDF]]
- 下一页：[[运动任务设计]]
- 返回：[[Home]]

## 更新日志

- 2026-08-31：新增本页。来源：Isaac Lab 文档 ArticulationCfg / Actuators 章节。

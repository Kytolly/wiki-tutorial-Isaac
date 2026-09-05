# M2-06-Isaac-Lab接入

> 本页属于：stackforce 机器狗实战（M2 资产检查）
> 前置知识：[[M2-05-Isaac-Sim验证]]
> 预计阅读时间：15 分钟

## 🎯 为什么需要这个？

资产最终要能被 Isaac Lab 当作环境里的机器人使用，接口要审核通过。

## 审核清单

- `ArticulationCfg` 与 asset path
- joint name resolution（关节名能否被 regex 解析）
- actuator mapping（legs / wheels 分组）
- default state（默认姿态）
- action dimension（应为 12 主动控制量）
- observations（可用观测）
- reset
- headless smoke test（无头冒烟测试）

```python
STACKFORCE_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(usd_path="sf_robot.usda"),
    actuators={
        "legs": ImplicitActuatorCfg(joint_names_expr=[".*_hip_.*"], ...),   # 待按 sf_robot 实际命名
        "wheels": ImplicitActuatorCfg(joint_names_expr=[".*_wheel_.*"], ...),
    },
)
```

> 具体 regex 必须以 sf_robot 的实际 joint 命名为准，未审核前不写死。

## M2 Final Gate

- **Validated Digital Robot Asset**：通过 provenance / topology / geometry / physics / Isaac Lab 接口审核，才能进入 M3/M4。

## 下一步

- 上一页：[[M2-05-Isaac-Sim验证]]
- 下一页：[[M3-动力学对齐]]
- 返回：[[Home]]

## 更新日志

- 2026-09-03：新增本页。来源：用户 IA 要求。

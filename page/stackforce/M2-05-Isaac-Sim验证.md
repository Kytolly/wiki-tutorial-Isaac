# M2-05-Isaac-Sim验证

> 本页属于：stackforce 机器狗实战（M2 资产检查）
> 前置知识：[[M2-04-物理资产审核]]
> 预计阅读时间：15 分钟

## 🎯 为什么需要这个？

在 Isaac Sim 里实际加载并验证资产的行为，而不是只看文件。

## 验证清单

- visual load（视觉加载）
- articulation root（articulation 根）
- rigid bodies（刚体数量）
- joint motion（关节能动）
- DOF（自由度）
- gravity（重力响应）
- collision / contact（碰撞接触）
- wheel rotation（轮旋转）
- closed-loop stability（闭环稳定性）
- default pose（默认姿态）

## 当前已知

| 项 | 结果 |
|----|------|
| `sf_robot.usda` 在 Isaac Sim 6.0.1 视觉加载 | **visual load PASS** |
| physics validation | **未做，不能标 PASS** |

> 只能标记 visual load PASS；不要自动把 physics validation 标为 PASS。

## 下一步

- 上一页：[[M2-04-物理资产审核]]
- 下一页：[[M2-06-Isaac-Lab接入]]
- 返回：[[Home]]

## 更新日志

- 2026-09-03：新增本页。来源：用户 IA 要求（sf_robot visual load PASS）。

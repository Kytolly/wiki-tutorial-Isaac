# Home

> 这是一份**新手友好、中文、分级**的学习讲义：同时带你学会 NVIDIA 的两个机器人仿真学习工具——**Isaac Sim**（物理仿真器）和 **Isaac Lab**（强化学习框架）。
> 本知识库包含 `intro → setup → train → build → deploy → advance` 学习路径，以及按 **Milestone → Gate → Topic → Acceptance → Evidence** 管理的 StackForce 工程知识库。

## 一句话理解这套知识库

- **Isaac Sim**：一个"可以物理级仿真、还能渲染得像照片一样真实"的 3D 世界，用来让机器人在电脑里"试错"。
- **Isaac Lab**：架在 Isaac Sim 之上的**机器人强化学习训练框架**，帮你把"让机器人学会一项技能"这件事流水线化。
- 两者关系：**Isaac Sim 是舞台和物理引擎，Isaac Lab 是训练教练和流水线**。

## 目标读者

- 零基础 / 机器人、强化学习新手（有 Python 基础更好，但 intro 不强求）。
- 想快速上手 Isaac Lab + Isaac Sim，跑通第一个 demo、完成第一次训练的工程师/学生。
- 想系统理解"物理仿真 + 强化学习"如何配合的人。

## 分级学习地图

| 分级 | 目标 | 主要页面 | 完成标准 |
|------|------|----------|----------|
| **intro 概念启蒙** | 建立心智模型 | Isaac-Sim是什么、Isaac-Lab是什么、Isaac Sim架构与核心概念、Isaac-Sim与Isaac-Lab如何协作 | 说清两框架是什么、彼此关系与协作分工 |
| **setup 环境与 Demo** | 装好并跑通 | 安装与环境配置、运行第一个Demo、USD场景入门、物理仿真设置、学习路线与下一步、版本与API速查 | 装好环境、跑通官方示例、读懂场景/USD 与物理设置、会查版本与 API |
| **train 训练入门** | 完成最小训练 | 强化学习核心概念、传感器与合成数据、渲染与LiDAR感知、Isaac-Lab项目结构与训练流程、第一个训练任务 | 理解 RL、加装传感器/测距、独立跑一次训练并回放 |
| **build 自建环境进阶** | 自建环境与调试 | Direct环境类深入、奖励设计与观测修改、训练调参与调试、Manager-Based工作流入门、Direct与Manager-Based对比迁移、自定义机器人资产导入、Isaac Sim扩展开发入门、Domain随机化与Sim2Real、端到端实战案例 | 两种工作流自由切换、自建环境、导入自研资产、写扩展、Sim2Real，并串起完整项目 |
| **deploy 部署与性能** | 加速与落地 | 多卡与分布式训练、仿真加速与性能优化、真机部署 | 多卡/分布式训练、仿真加速调优、策略导出与真机部署 |
| **advance 进阶方向** | 五级之后继续深入 | 进阶方向概览、模仿学习与数据采集、RL后端对比与选型、容器化与Docker复现 | 知道五级之后有哪些高价值方向，能跑通至少一个进阶小项目 |
| **stackforce 机器狗实战** | 用可验收 Gate 推进四轮足项目 | Roadmap与里程碑、M1–M6 里程碑、闭链架构、证据注册表 | 宏观 15/44 closed（M1 7/10 BLOCKED，M2 8/8 PASS）；闭链数字资产通过 2400 步悬空重力烟囱测试（PASS），明确保持 rl_ready=false |

## 学习顺序（推荐）

1. [[Isaac-Sim是什么]] → 2. [[Isaac-Lab是什么]] → 3. [[Isaac Sim架构与核心概念]] → 4. [[Isaac-Sim与Isaac-Lab如何协作]] → 5. [[安装与环境配置]] → 6. [[运行第一个Demo]] → 7. [[USD场景入门]] → 8. [[物理仿真设置]] → 9. [[学习路线与下一步]] → 10. [[强化学习核心概念]] → 11. [[Isaac-Lab项目结构与训练流程]] → 12. [[第一个训练任务]] → 13. [[传感器与合成数据]] → 14. [[渲染与LiDAR感知]] → 15. [[Direct环境类深入]] → 16. [[奖励设计与观测修改]] → 17. [[训练调参与调试]] → 18. [[Manager-Based工作流入门]] → 19. [[Direct与Manager-Based对比迁移]] → 20. [[自定义机器人资产导入]] → 21. [[Isaac Sim扩展开发入门]] → 22. [[Domain随机化与Sim2Real]] → 23. [[端到端实战案例]] → 24. [[多卡与分布式训练]] → 25. [[仿真加速与性能优化]] → 26. [[真机部署]]

> 两工具按"逐环节协作"学习（见 [[Isaac-Sim与Isaac-Lab如何协作]]）：每个环节都有 Isaac Sim 页 ↔ Isaac Lab 页成对。
> 五级之后可进入 **进阶方向**：[[进阶方向概览]] → [[模仿学习与数据采集]] / [[RL后端对比与选型]] / [[容器化与Docker复现]]。
> **StackForce 工程路线**：[[Roadmap与里程碑]] → [[M1-Hardware-Ground-Truth]] / [[M2-Simulation-Asset]] → [[M3-Dynamics-Calibration]] → [[M4-Locomotion]] → [[M5-Robustness]] → [[M6-Sim-to-Real]]。
> 证据真源统一见：[[evidence-registry]]。
> 待办：Isaac Lab v3.0 正式版发布后的版本核对与 API 更新。

## StackForce 当前工程状态（2026-09-14）

- **顶级六阶段路线（M1–M6）**：当前总进度 15 / 44 门禁关闭。
  - **M1 Hardware Ground Truth（7/10 BLOCKED）**：两次架空 session 冻结硬件/固件、IMU、控制窗口与几何基线；由于 ch7 执行器在 return/STOP 指令后未能物理回中，实机执行器母线强制断电，保持 BLOCKED。
  - **M2 Simulation Asset（8/8 PASS）**：完成双支链五杆闭链机器人的规范树 URDF（29 links, 28 joints，唯一根 `base_link`，W2 显式切断）、PhysX 闭环转动副恢复（`excludeFromArticulation=true`）以及全自动化静态门禁；在 CPU 悬空重力场下完成 2400 步（10 秒 @ 240 Hz）物理烟囱测试（实测运动位移 0.0906 m，最大漂移 0.0595 mm，负对照 129 mm 崩溃，见 `E-PHYS-001`/`E-PHYS-002`）。
  - **M3 Dynamics Calibration（0/6 TODO）**：执行器刚度、阻尼与真实电机响应待标定。
  - **M4 Locomotion（0/6 IN PROGRESS）**：强化学习环境接入进行中；当前资产保持 **`rl_ready = false`**，严禁越级宣称已就绪。
  - **M5 Robustness（0/6 TODO）**：域随机化待启动。
  - **M6 Sim-to-Real（0/8 TODO）**：待 M1 安全解封与 M3 动力学对齐。
- **自由度划分规范**：整机为 20 个树状转动关节（4 腿 $\times$ 5），12 个主动驱动（4 M1 + 4 M2 + 4 W1），8 个被动铰接（4 P1 + 4 P2），4 个 PhysX 闭环约束副（W2）；严禁表述为“20 自由度”。
- 详情见 [[Roadmap与里程碑]]、[[M2-Simulation-Asset]]、[[闭环恢复架构与产物映射]] 与 [[evidence-registry]]。

## 更新日志

- 2026-09-14：重构宏观工程状态为标准 M1–M6 架构；引入便携式 [[evidence-registry]]；更新 M2 闭链资产 2400 步 CPU 重力下沉实验 PASS（0.060 mm）与负对照（129 mm）实验；明确驱动器动力学与 RL 未就绪边界（`rl_ready = false`）。
- 2026-09-13：更新 StackForce 状态至闭链资产静态验证 PASS，确立静态门禁 PASS 与动态验证边界。
- 2026-09-11：同步 M1 两次架空实机 session；更新宏观进度为 15/44，并记录 ch7 powered-actuation blocker。
- 2026-09-08：同步 StackForce M1/M2 Topic 层的证据路径、runtime 状态和验收边界。
- 2026-09-08：补充 M1/M2 Dashboard 的逐 Gate Evidence Snapshot。
- 2026-09-08：同步 StackForce M1/M2 outcome，更新为 8/44 Gates PASS。

## 版本说明（截至 2026-08-31）

- **Isaac Sim**：最新 pip 包为 `6.0.1.0`（Python 3.12）；传统"独立桌面版"最后一代为 **4.5.0**（Omniverse Launcher 已于 2025-10-01 起逐步弃用，推荐改用 pip 安装）。
- **Isaac Lab**：最新稳定版为 **v2.3.2**（2026-02），`3.0` 系列处于 beta（v3.0.0-beta2）。
- 本讲义安装路线采用官方 Quickstart（Isaac Sim 5.1.0 pip + Isaac Lab 源码 + PyTorch 2.7.0 / Python 3.11），这是当前文档推荐的、可复现的组合。

## 外部资源

- Isaac Lab 官方文档：<https://isaac-sim.github.io/IsaacLab/>（访问于 2026-08-31）
- Isaac Sim 官方文档：<https://docs.isaacsim.omniverse.nvidia.com/>（访问于 2026-08-31）
- Isaac Lab 源码：<https://github.com/isaac-sim/IsaacLab>（访问于 2026-08-31）

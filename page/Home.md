# Home

> 这是一份**新手友好、中文、分级**的学习讲义：同时带你学会 NVIDIA 的两个机器人仿真学习工具——**Isaac Sim**（物理仿真器）和 **Isaac Lab**（强化学习框架）。
> 本知识库采用"按任务自定"分级（`intro → setup → train → build → deploy`），导航按"**阶段 tab → 技术主题 → 文章**"组织（顶部/侧边共 6 个 tab，每 tab 下分主题），并同步维护 `_Sidebar` 导航、`_META` 状态和每页互链。

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
| **stackforce 机器狗实战** | 用 StackForce 四轮足机器狗按里程碑走通全流程 | Roadmap与里程碑、M1硬件吃透、M2 资产检查、M3动力学对齐、M4 Isaac Lab训练、M5鲁棒性、M6 Sim2Real部署 | 按 Hardware→URDF→Dynamics→RL→Robustness→Sim2Real 六里程碑走通 |

## 学习顺序（推荐）

1. [[Isaac-Sim是什么]] → 2. [[Isaac-Lab是什么]] → 3. [[Isaac Sim架构与核心概念]] → 4. [[Isaac-Sim与Isaac-Lab如何协作]] → 5. [[安装与环境配置]] → 6. [[运行第一个Demo]] → 7. [[USD场景入门]] → 8. [[物理仿真设置]] → 9. [[学习路线与下一步]] → 10. [[强化学习核心概念]] → 11. [[Isaac-Lab项目结构与训练流程]] → 12. [[第一个训练任务]] → 13. [[传感器与合成数据]] → 14. [[渲染与LiDAR感知]] → 15. [[Direct环境类深入]] → 16. [[奖励设计与观测修改]] → 17. [[训练调参与调试]] → 18. [[Manager-Based工作流入门]] → 19. [[Direct与Manager-Based对比迁移]] → 20. [[自定义机器人资产导入]] → 21. [[Isaac Sim扩展开发入门]] → 22. [[Domain随机化与Sim2Real]] → 23. [[端到端实战案例]] → 24. [[多卡与分布式训练]] → 25. [[仿真加速与性能优化]] → 26. [[真机部署]]

> 两工具按"逐环节协作"学习（见 [[Isaac-Sim与Isaac-Lab如何协作]]）：每个环节都有 Isaac Sim 页 ↔ Isaac Lab 页成对。
> 五级之后可进入 **进阶方向**：[[进阶方向概览]] → [[模仿学习与数据采集]] / [[RL后端对比与选型]] / [[容器化与Docker复现]]。
> **StackForce 机器狗实战路线**：[[Roadmap与里程碑]] → [[M1-硬件吃透]] → [[M2-资产检查]] → [[M3-动力学对齐]] → [[M4-Isaac-Lab训练]] → [[M5-鲁棒性]] → [[M6-Sim2Real部署]]。
> 待办：Isaac Lab v3.0 正式版发布后的版本核对与 API 更新。

## 版本说明（截至 2026-08-31）

- **Isaac Sim**：最新 pip 包为 `6.0.1.0`（Python 3.12）；传统"独立桌面版"最后一代为 **4.5.0**（Omniverse Launcher 已于 2025-10-01 起逐步弃用，推荐改用 pip 安装）。
- **Isaac Lab**：最新稳定版为 **v2.3.2**（2026-02），`3.0` 系列处于 beta（v3.0.0-beta2）。
- 本讲义安装路线采用官方 Quickstart（Isaac Sim 5.1.0 pip + Isaac Lab 源码 + PyTorch 2.7.0 / Python 3.11），这是当前文档推荐的、可复现的组合。

## 外部资源

- Isaac Lab 官方文档：<https://isaac-sim.github.io/IsaacLab/>（访问于 2026-08-31）
- Isaac Sim 官方文档：<https://docs.isaacsim.omniverse.nvidia.com/>（访问于 2026-08-31）
- Isaac Lab 源码：<https://github.com/isaac-sim/IsaacLab>（访问于 2026-08-31）

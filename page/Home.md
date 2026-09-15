# Home

> 这是一份**新手友好、中文、分级**的学习讲义：同时带你学会 NVIDIA 的两个机器人仿真学习工具——**Isaac Sim**（物理仿真器）和 **Isaac Lab**（强化学习框架）。  
> 本知识库包含 `intro → setup → train → build → deploy → advance` 分级教程，以及按 **Milestone → Gate → Acceptance Criterion → Evidence#Part → Source / Artifact** 严格追溯管理的 StackForce 四轮足机器狗工程知识体系。  
> **Topic 层**定位为横向 Cross-Validation 与工程分析层，不阻断主验收链。

---

## 1. 一句话理解这套知识库

- **Isaac Sim**：一个"可以物理级仿真、还能渲染得像照片一样真实"的 3D 世界，用来让机器人在电脑里"试错"。
- **Isaac Lab**：架在 Isaac Sim 之上的**机器人强化学习训练框架**，帮你把"让机器人学会一项技能"这件事流水线化。
- 两者关系：**Isaac Sim 是舞台和物理引擎，Isaac Lab 是训练教练和流水线**。

---

## 2. 目标读者与分级地图

- 零基础 / 机器人、强化学习新手，希望从零跑通 Isaac Sim / Lab 仿真到真机落地。
- 机器人工程师与高校学生，希望系统掌握闭链机构、PhysX 约束重构与 Sim2Real 关键流程。

| 分级模块 | 学习目标 | 核心页面导航 | 达成指标 |
|---|---|---|---|
| **intro 概念启蒙** | 建立物理仿真与强化学习心智模型 | [[Isaac-Sim是什么]]、[[Isaac-Lab是什么]]、[[Isaac Sim架构与核心概念]]、[[Isaac-Sim与Isaac-Lab如何协作]] | 讲清两框架核心定位与协作边界 |
| **setup 环境与 Demo** | 独立搭建开发环境并跑通官方用例 | [[安装与环境配置]]、[[运行第一个Demo]]、[[USD场景入门]]、[[物理仿真设置]]、[[学习路线与下一步]]、[[版本与API速查]] | 跑通示例，理解 USD 场景图与物理场景设置 |
| **train 训练入门** | 完成强化学习最小闭环训练 | [[强化学习核心概念]]、[[传感器与合成数据]]、[[渲染与LiDAR感知]]、[[Isaac-Lab项目结构与训练流程]]、[[第一个训练任务]] | 理解 RL 循环，独立训练策略并回放观测 |
| **build 自建进阶** | 自建机器人资产、环境与扩展开发 | [[Direct环境类深入]]、[[奖励设计与观测修改]]、[[训练调参与调试]]、[[Manager-Based工作流入门]]、[[Direct与Manager-Based对比迁移]]、[[自定义机器人资产导入]]、[[Isaac Sim扩展开发入门]]、[[Domain随机化与Sim2Real]]、[[端到端实战案例]] | 双工作流切换自如，导入自研数字资产 |
| **deploy 部署与性能** | 加速计算与策略真机落地 | [[多卡与分布式训练]]、[[仿真加速与性能优化]]、[[真机部署]] | 多卡分布式训练、实时推理与安全防护 |
| **advance 进阶方向** | 前沿方向探索与容器化复现 | [[进阶方向概览]]、[[模仿学习与数据采集]]、[[RL后端对比与选型]]、[[容器化与Docker复现]] | 掌握模仿学习与容器化环境复现 |
| **stackforce 机器狗实战** | 六阶段严谨门禁推进闭链四轮足真机 | [[Roadmap与里程碑]]、[[M1-Hardware-Ground-Truth]] ~ [[M6-Sim-to-Real]]、[[T-ACT-001-Canonical-Real-Sim-Component-Identity]]、[[evidence-registry]] | 严格由 Acceptance Criteria 驱动验收 |

---

## 3. StackForce 当前工程状态速览（Current Engineering Status）

- **顶级六阶段路线推进（M1–M6）**：全机 44 个 Gate 中当前 **15 / 44 PASS**。
  - **[[M1-Hardware-Ground-Truth]]（7/10 PASS，IN PROGRESS）**：硬件清单、传感器、时序测频、延迟基线已冻结；Channel 7 舵机硬件已修复，当前聚焦修复后回归测试与 8 舵机物理零位量化标定。
  - **[[M2-Simulation-Asset]]（8/8 PASS）**：严格单父树闭链 URDF（29 links, 28 joints）与 PhysX 闭环副重构全部通过；2400 步 CPU 悬空下沉重力烟囱测试通过（漂移 $\le 0.0595\text{ mm}$）；明确保持 **`rl_ready = false`** 动力学未标定边界。
  - **[[M3-Dynamics-Calibration]]（0/6 PASS，IN PROGRESS）**：当前核心推进阶段。基础构件映射与数字资产已具备，待实机连接采集高频动态遥测。
  - **[[M4-Locomotion]]（0/6 TODO）**：等待 M3 动力学参数对齐后解除门禁锁定。
  - **[[M5-Robustness]]（0/6 TODO）**：等待 M4 基础步态收敛后开展域随机化。
  - **[[M6-Sim-to-Real]]（0/8 TODO）**：等待 M1 安全解封与 M5 策略导出后开展真机落地。
- **当前核心焦点（Current Focus）**：M3-G01 激励协议冻结与真机架空动态响应数据采样。
- **下一步行动（Next Action）**：连接真机运行架空激励实验，录制标准 CSV 遥测数据集。

---

## 4. 全局工程导航指引

- **宏观进度与路线总览**：见 [[Roadmap与里程碑]]。
- **门禁与阶段验收明细**：见各 Milestone（[[M1-Hardware-Ground-Truth]] ~ [[M6-Sim-to-Real]]）及下辖 Gate 页面。
- **横向分析与交叉核验**：见 [[T-ACT-001-Canonical-Real-Sim-Component-Identity]]、[[T01-机器人接口]]、[[T03-安全联锁]] 等 Topic 页面。
- **证据真源与来源索引**：见 [[evidence-registry]]（证据索引）与 [[source-inventory]]（来源索引）。

---

## 5. 更新日志

- 2026-09-15：重构为纯 Summary / View 门户；修正主验收架构链条描述；同步各 Milestone 最新状态（M1 7/10 IN PROGRESS, M2 8/8 PASS, M3 IN PROGRESS）；全面应用 Canonical 构件命名。

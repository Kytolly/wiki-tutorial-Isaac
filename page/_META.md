# Wiki 状态

- 领域：NVIDIA Isaac Lab（机器人强化学习框架）+ Isaac Sim（Omniverse 物理仿真器）
- 分级：按任务自定（`intro 概念启蒙 → setup 环境与 Demo → train 训练入门 → build 自建环境进阶 → deploy 部署与性能`）
- 导航：阶段式 tab（概念启蒙 / 环境与Demo / 训练入门 / 自建进阶 / 部署与性能 / 关于，+首页共 7 个），每 tab 下按"技术主题 → 文章"分组；tab 数量控制在 4-8 个，新内容并入已有 tab 或新增主题
- 关联仓库：<https://github.com/Kytolly/wiki-tutorial-Isaac>
- 当前进度：**全部五级完成（共 26 页）；联动改造与双侧深化已落地；待办：v3.0 版本核对**
- 信息截止：2026-08-31

## 页面清单

- [x] Home（2026-08-31）
- [x] intro/Isaac-Sim是什么（2026-08-31）
- [x] intro/Isaac-Lab是什么（2026-08-31）
- [x] intro/Isaac Sim架构与核心概念（2026-08-31）
- [x] intro/Isaac-Sim与Isaac-Lab如何协作（2026-08-31）
- [x] setup/安装与环境配置（2026-08-31）
- [x] setup/运行第一个Demo（2026-08-31）
- [x] setup/USD场景入门（2026-08-31）
- [x] setup/物理仿真设置（2026-08-31）
- [x] setup/学习路线与下一步（2026-08-31）
- [x] train/强化学习核心概念（2026-08-31）
- [x] train/传感器与合成数据（2026-08-31）
- [x] train/渲染与LiDAR感知（2026-08-31）
- [x] train/Isaac-Lab项目结构与训练流程（2026-08-31）
- [x] train/第一个训练任务（2026-08-31）
- [x] build/Direct环境类深入（2026-08-31）
- [x] build/奖励设计与观测修改（2026-08-31）
- [x] build/训练调参与调试（2026-08-31）
- [x] build/Manager-Based工作流入门（2026-08-31）
- [x] build/Direct与Manager-Based对比迁移（2026-08-31）
- [x] build/自定义机器人资产导入（2026-08-31）
- [x] build/Isaac Sim扩展开发入门（2026-08-31）
- [x] build/Domain随机化与Sim2Real（2026-08-31）
- [x] build/端到端实战案例（2026-08-31）
- [x] deploy/多卡与分布式训练（2026-08-31）
- [x] deploy/仿真加速与性能优化（2026-08-31）
- [x] deploy/真机部署（2026-08-31）
- [ ] Isaac Lab v3.0 正式版发布后的版本核对与 API 更新（规划中）

## changelog

- 2026-08-31：新建 Home、_Sidebar、_META、_Footer，完成 intro/setup/train 三级（原 L0/L1）。
- 2026-08-31：按更新后的 skill 规范，分级从 L0/L1 迁移为 intro/setup/train，页面去掉分级前缀。
- 2026-08-31：完成 build 首批 3 页（Direct环境类深入、奖励设计与观测修改、训练调参与调试），导航/学习地图/学习路线同步更新。来源：Isaac Lab 官方文档与源码、GitHub 讨论区（详见各页更新日志）。
- 2026-08-31：导航重构为"阶段 tab → 技术主题 → 文章"三层（mkdocs.yml nav 与 _Sidebar 同步），tab 数控制为 6 个。
- 2026-08-31：完成 build 第二批 3 页（Manager-Based工作流入门、自定义机器人资产导入、Domain随机化与Sim2Real），build 级全部完成（共 6 页），导航/学习地图/学习路线同步更新。来源：Isaac Lab 官方教程、资产与随机化文档、源码（详见各页更新日志）。
- 2026-08-31：新增 deploy 分级与"部署与性能"tab（第 7 个），完成 3 页（多卡与分布式训练、仿真加速与性能优化、真机部署），四级全部完成（共 17 页）。来源：Isaac Lab Multi-GPU 文档、isaac_ros_deploy、策略部署文档（详见各页更新日志）。
- 2026-08-31：Isaac Sim 专项扩充批（共 4 页）：新增 Isaac Sim架构与核心概念（intro）、USD场景入门与物理仿真设置（setup）、传感器与合成数据（train），并深化 Isaac-Sim是什么（能力地图+对比）；上一页/下一页链同步重排，总页数 17→21。来源：Isaac Sim 官方文档（架构/USD/物理/Replicator），详见各页更新日志。
- 2026-08-31：联动改造 + 双侧深化批（共 5 页 + 全局互链）：新增全景联动页（Isaac-Sim与Isaac-Lab如何协作）、Isaac Sim 深化（Isaac Sim扩展开发入门、渲染与LiDAR感知）、Isaac Lab 深化（Direct与Manager-Based对比迁移、端到端实战案例）；为 build 级 6 页与架构页补"与另一工具的联系"小节并打通双向链接；总页数 21→26。来源：Isaac Sim 扩展/渲染/LiDAR 文档、Isaac Lab 环境设计文档（详见各页更新日志）。

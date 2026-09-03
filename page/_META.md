# Wiki 状态

- 领域：NVIDIA Isaac Lab（机器人强化学习框架）+ Isaac Sim（Omniverse 物理仿真器）
- 分级：按任务自定（`intro → setup → train → build → deploy → advance → stackforce 机器狗实战`）
- 导航：阶段式 tab（概念启蒙 / 环境与Demo / 训练入门 / 自建进阶 / 部署与性能 / 进阶方向 / StackForce实战 / 关于，+首页），每 tab 下按"技术主题 → 文章"分组；tab 数量控制在 4-8 个，新内容并入已有 tab 或新增主题
- 关联仓库：<https://github.com/Kytolly/wiki-tutorial-Isaac>
- 当前进度：**六级 + 进阶方向 + StackForce 机器狗实战（含 M1 实操 5 页 + URDF 实操 5 页），共 48 个内容页；待办：v3.0 正式版核对**
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
- [x] setup/版本与API速查（2026-09-01）
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
- [x] advance/进阶方向概览（2026-09-01）
- [x] advance/模仿学习与数据采集（2026-09-01）
- [x] advance/RL后端对比与选型（2026-09-01）
- [x] advance/容器化与Docker复现（2026-09-01）
- [x] stackforce/Roadmap与里程碑（2026-09-02）
- [x] stackforce/M1-硬件吃透（2026-09-02）
- [x] stackforce/M1-01-硬件清单与传感器（2026-09-02）
- [x] stackforce/M1-02-Joint-Map与单执行器（2026-09-02）
- [x] stackforce/M1-03-控制接口与频率延迟（2026-09-02）
- [x] stackforce/M1-04-机械参数与重量（2026-09-02）
- [x] stackforce/M1-05-硬件API与安全（2026-09-02）
- [x] stackforce/M2-URDF建模（2026-09-02）
- [x] stackforce/M3-动力学对齐（2026-09-02）
- [x] stackforce/M4-Isaac-Lab训练（2026-09-02）
- [x] stackforce/M5-鲁棒性（2026-09-02）
- [x] stackforce/M6-Sim2Real部署（2026-09-02）
- [x] stackforce/URDF-01-自由度与命名（2026-09-02）
- [x] stackforce/URDF-02-零件与腿部运动学（2026-09-02）
- [x] stackforce/URDF-03-最小骨架与验证（2026-09-02）
- [x] stackforce/URDF-04-视觉碰撞与动力学（2026-09-02）
- [x] stackforce/URDF-05-到Isaac-Lab与系统辨识（2026-09-02）
- [ ] Isaac Lab v3.0 正式版发布后的版本核对与 API 更新（规划中）

## changelog

- 2026-09-02：新增 **stackforce/M1 实操 5 页**（硬件清单与传感器、Joint-Map与单执行器、控制接口与频率延迟、机械参数与重量、硬件API与安全），展开 M1 硬件吃透路线（M1.1–M1.6 + 机械/重量/API/Logger/安全 + 验收标准）。来源：用户 M1 实操路线。
- 2026-09-02：新增 **stackforce/URDF 实操 5 页**（自由度与命名、零件与腿部运动学、最小骨架与验证、视觉碰撞与动力学、到Isaac-Lab与系统辨识），展开 M2 的 14 阶段 URDF 建模路线；补充本地 Mini URDF（bipedal_wheeled_robot/20250820_1.urdf）的腿部 origin/axis/limit/inertia 数据。来源：用户 URDF 路线 + 本地仓库。
- 2026-09-02：按用户 Roadmap 重构机器狗实战为 **stackforce 分级**（7 页：Roadmap与里程碑 + M1–M6 六里程碑），取代原 robot 初稿；六里程碑结构：Hardware→URDF→Dynamics→RL→Robustness→Sim2Real。来源：用户 Roadmap + 本地仓库 `quadrupedal-wheeled-robot`。
- 2026-08-31：新增 robot 机器狗实战初稿（8 页），后被 stackforce 分级取代。来源：本地仓库 `/home/kytolly/Library/quadrupedal-wheeled-robot`（SF_IMU/SF_Servo/kinematics/gait/PID）。
- 2026-08-31：新建 Home、_Sidebar、_META、_Footer，完成 intro/setup/train 三级（原 L0/L1）。
- 2026-08-31：按更新后的 skill 规范，分级从 L0/L1 迁移为 intro/setup/train，页面去掉分级前缀。
- 2026-08-31：完成 build 首批 3 页（Direct环境类深入、奖励设计与观测修改、训练调参与调试），导航/学习地图/学习路线同步更新。来源：Isaac Lab 官方文档与源码、GitHub 讨论区（详见各页更新日志）。
- 2026-08-31：导航重构为"阶段 tab → 技术主题 → 文章"三层（mkdocs.yml nav 与 _Sidebar 同步），tab 数控制为 6 个。
- 2026-08-31：完成 build 第二批 3 页（Manager-Based工作流入门、自定义机器人资产导入、Domain随机化与Sim2Real），build 级全部完成（共 6 页），导航/学习地图/学习路线同步更新。来源：Isaac Lab 官方教程、资产与随机化文档、源码（详见各页更新日志）。
- 2026-08-31：新增 deploy 分级与"部署与性能"tab（第 7 个），完成 3 页（多卡与分布式训练、仿真加速与性能优化、真机部署），四级全部完成（共 17 页）。来源：Isaac Lab Multi-GPU 文档、isaac_ros_deploy、策略部署文档（详见各页更新日志）。
- 2026-08-31：Isaac Sim 专项扩充批（共 4 页）：新增 Isaac Sim架构与核心概念（intro）、USD场景入门与物理仿真设置（setup）、传感器与合成数据（train），并深化 Isaac-Sim是什么（能力地图+对比）；上一页/下一页链同步重排，总页数 17→21。来源：Isaac Sim 官方文档（架构/USD/物理/Replicator），详见各页更新日志。
- 2026-08-31：联动改造 + 双侧深化批（共 5 页 + 全局互链）：新增全景联动页
- 2026-09-01：新增 **setup/版本与API速查** 页（版本/API 速查与 3.0 迁移提示），并把版本说明从 Home 收敛到该页。
- 2026-09-01：新增 **advance 进阶方向** 分级（进阶方向概览、模仿学习与数据采集、RL后端对比与选型、容器化与Docker复现），导航/学习地图/侧边栏同步更新。
- 2026-09-01：**补齐先前缺失的 build 级 9 页**（Direct环境类深入、奖励设计与观测修改、训练调参与调试、Manager-Based工作流入门、Direct与Manager-Based对比迁移、自定义机器人资产导入、Isaac Sim扩展开发入门、Domain随机化与Sim2Real、端到端实战案例），打通 train→build→deploy 学习链；同步修正 Home 学习顺序；升级 build.py / publish-wiki.sh 支持 page/assets 图片管线。来源：Isaac Lab 官方教程与源码（详见各页更新日志，访问于 2026-09-01）。（Isaac-Sim与Isaac-Lab如何协作）、Isaac Sim 深化（Isaac Sim扩展开发入门、渲染与LiDAR感知）、Isaac Lab 深化（Direct与Manager-Based对比迁移、端到端实战案例）；为 build 级 6 页与架构页补"与另一工具的联系"小节并打通双向链接；总页数 21→26。来源：Isaac Sim 扩展/渲染/LiDAR 文档、Isaac Lab 环境设计文档（详见各页更新日志）。

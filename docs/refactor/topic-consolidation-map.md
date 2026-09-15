# Topic 整合与分类审计映射表（Topic Consolidation Map）

> **文档属性**：Wiki 架构重构与横向分析层规范化审计报告  
> **设计依据**：[`skill-wiki-design/references/architecture.md`](../../.agents/skills/skill-wiki-design/references/architecture.md)  
> **核心原则**：  
> 1. Topic 是**横向 cross-validation / engineering analysis 层**，负责跨技术源交叉比对与冲突排查；  
> 2. Topic **不是 Gate 的前置阻断依赖**（Gate 必须直接引用 `Evidence#Part`）；  
> 3. Topic **不是原始事实源**（Topic 的所有分析结论必须反向锚定至 `Evidence#Part`）；  
> 4. 消除按 Milestone 割裂的重复内容，逐步演进为基于技术领域（Domain-based）的规范化 Topic 体系。

---

## 1. Topic 分类体系设计（Topic Taxonomy）

为彻底解决历史遗留的“Topic 随里程碑随意堆叠”、“多篇文档重复定义执行器映射”等问题，本工程将 Topic 划分为两大层级：

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Domain-based Horizontal Topics                      │
│            (全局领域专题：跨源比对、契约定义、全局安全与系统边界)              │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 构件与执行器领域   │ 硬件基线与注册领域 │ 系统安全与运行时领域           │
│ • T-ACT-001       │ • T-HW-REG-001    │ • T01-机器人接口               │
│ • T-ACT-002       │                   │ • T02-实验日志                 │
│                   │                   │ • T03-安全联锁                 │
│                   │                   │ • T04-工程边界                 │
└───────────────────┴───────────────────┴────────────────────────────────┘
                               ▲
                               │ 引用 / 继承领域契约
┌──────────────────────────────┴─────────────────────────────────────────┐
│                    Milestone Analysis Working Views                    │
│            (里程碑工作视图：聚焦特定工程阶段的实施细则与测试操作规程)            │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ M1 硬件物理阶段   │ M2 仿真资产阶段   │ M3~M6 进阶阶段                 │
│ • M1-T01~M1-T06   │ • M2-T01~M2-T08   │ • M3-T01, M4-T01, M5-T01, M6-T01│
└───────────────────┴───────────────────┴────────────────────────────────┘
```

---

## 2. 全库 Topic 审计与整合清单（Topic Audit Matrix）

| Topic 标识与文件名 | 领域分类 (Domain) | 角色定性 (Role) | 引用核心 Evidence#Part | 整合与重构动作 (Action) | 最终状态 (Status) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`T-ACT-001-Canonical-Real-Sim-Component-Identity.md`** | Actuator Topology | **Domain Topic (SSOT)** | `E-HW-002#P01`, `E-FW-003#P03`, `E-SIM-001#P03`, `E-SIM-003#P03`, `E-VAL-001#P01` | **SSOT 确立**：全机 12 执行器规范命名、PCA 通道、代码变量到仿真关节唯一映射源 | `ACTIVE / FROZEN` |
| **`T-ACT-002-Servo-Coordinate-Calibration-Contract.md`** | Actuator Calibration | **Domain Topic (SSOT)** | `E-FW-001#P02-P03`, `E-CAL-001#P01-P05`, `E-SIM-001#P03`, `E-SIM-002#P04` | **NEW**：确立 $u_j = u_{0, j} + s_j \cdot k_j \cdot q_j$ 仿射映射、旋向极性与未决项审计 | `ACTIVE / AUDITED` |
| **`T-HW-REG-001-Controller-Registration-Hardware-Identity.md`** | Hardware Identity | **Domain Topic (SSOT)** | `E-DOC-006#P04`, `E-DOC-007#P05`, `E-FW-008#P01-P05` | **SSOT 确立**：双芯片架构、eFuse MAC 指纹提取与注册码校验链条 | `ACTIVE / FROZEN` |
| **`T01-机器人接口.md`** | Hardware Integration | Domain Topic | `E-DOC-004#P01-P05`, `E-HW-001#P01-P05`, `E-FW-004#P01-P03` | **CONSOLIDATED**：系统电气板垛分层与 CAN/RS485 总线拓扑分析 | `ACTIVE` |
| **`T02-实验日志.md`** | Physical Runtime | Domain Topic | `E-TEST-001#P01-P05`, `E-CAL-001#P01-P05` | **CONSOLIDATED**：实机架空测试日志索引与异常工况回溯 | `ACTIVE` |
| **`T03-安全联锁.md`** | Safety Systems | Domain Topic | `E-DOC-001#P04`, `E-DOC-002#P01`, `E-TEST-001#P03`, `E-CAL-001#P04` | **CONSOLIDATED**：硬件急停、超时看门狗与 Channel 7 物理故障阻断联动 | `ACTIVE` |
| **`T04-工程边界.md`** | Sim2Real Boundaries | Domain Topic | `E-SIM-001#P01-P05`, `E-VAL-002#P01-P05` | **CONSOLIDATED**：闭环约束收敛性、单父树割边与无反馈舵机工程边界 | `ACTIVE` |
| **`M1-T01-硬件基线.md`** | M1 Hardware | Milestone View | `E-DOC-003`, `E-DOC-004`, `E-HW-001`, `E-HW-002` | **REFACTORED**：硬件物料清点与主控选型实施细则 | `ACTIVE` |
| **`M1-T02-执行器映射.md`** | M1 Hardware | Milestone View | `E-FW-001`, `E-FW-002`, `E-CAL-001` | **MERGED & DELEGATED**：移除与 T-ACT-001 重复表格，委托至 T-ACT-001/002，聚焦架空小阶跃测试法 | `ACTIVE / CONSOLIDATED` |
| **`M1-T03-传感器数据.md`** | M1 Hardware | Milestone View | `E-FW-001#P04`, `E-FW-007#P02`, `E-HW-002#P02` | **REFACTORED**：IMU 滤波与磁编码器接口实施细则 | `ACTIVE` |
| **`M1-T04-控制时序.md`** | M1 Hardware | Milestone View | `E-TEST-001#P02-P03`, `E-FW-003#P05` | **REFACTORED**：50Hz PWM 与 1Mbps CAN 总线时延测定 | `ACTIVE` |
| **`M1-T05-尺寸质量测量.md`** | M1 Hardware | Milestone View | `E-DOC-003#P02-P03`, `E-SIM-002#P01-P03` | **REFACTORED**：五连杆连杆长度实测与整机配重 | `ACTIVE` |
| **`M1-T06-空间限制.md`** | M1 Hardware | Milestone View | `E-SIM-001#P03`, `E-CAL-001#P04` | **REFACTORED**：舵机运动极限范围与五杆干涉规程 | `ACTIVE` |
| **`M2-T01-资产来源.md`** | M2 Simulation | Milestone View | `E-DOC-003#P01-P05`, `E-SIM-001#P01` | **REFACTORED**：官方 CAD 模型与 STL 网格版本溯源 | `ACTIVE` |
| **`M2-T02-机械拓扑.md`** | M2 Simulation | Milestone View | `E-SIM-001#P01-P05`, `E-VAL-001#P01-P04` | **REFACTORED**：29 Links 28 Joints 单父树树状拓扑 | `ACTIVE` |
| **`M2-T03-几何装配.md`** | M2 Simulation | Milestone View | `E-SIM-002#P01-P05` | **REFACTORED**：-44.95mm 闭环装配几何不变量推导 | `ACTIVE` |
| **`M2-T04-物理属性.md`** | M2 Simulation | Milestone View | `E-SIM-001#P04`, `E-VAL-001#P01` | **REFACTORED**：连杆质量、质心与正定惯性张量校验 | `ACTIVE` |
| **`M2-T05-仿真行为.md`** | M2 Simulation | Milestone View | `E-VAL-002#P01-P05` | **REFACTORED**：悬空烟囱测试与闭环副残差收敛性 | `ACTIVE` |
| **`M2-T06-实验室接入.md`** | M2 Simulation | Milestone View | `E-VAL-001#P05`, `E-VAL-002#P01` | **REFACTORED**：Isaac Lab 环境注册与资产加载 | `ACTIVE` |
| **`M2-T07-坐标约定.md`** | M2 Simulation | Milestone View | `E-SIM-002#P04`, `E-SIM-001#P03` | **REFACTORED**：底盘对称反射与单平面镜像绕向分析 | `ACTIVE` |
| **`M2-T08-闭环恢复.md`** | M2 Simulation | Milestone View | `E-SIM-003#P01-P05` | **REFACTORED**：PhysX RevoluteJoint 闭环副后处理脚本 | `ACTIVE` |
| **`M3-T01-响应对齐.md`** | M3 Calibration | Milestone View | `E-TEST-001`, `E-CAL-001`, `E-VAL-002` | **REFACTORED**：动力学阶跃对齐与频域响应分析概览 | `ACTIVE` |
| **`M4-T01-运动任务.md`** | M4 Locomotion | Milestone View | `E-FW-003#P04` | **REFACTORED**：Trot 步态解算与强化学习任务空间定义 | `ACTIVE` |
| **`M5-T01-随机化扰动.md`** | M5 Robustness | Milestone View | `E-DOC-003`, `E-SIM-001` | **REFACTORED**：域随机化区间（质量、摩擦、阻尼）规划 | `ACTIVE` |
| **`M6-T01-部署流程.md`** | M6 Sim2Real | Milestone View | `E-DOC-002`, `E-DOC-005`, `E-FW-003` | **REFACTORED**：实机影子模式与真机闭环部署工作流 | `ACTIVE` |

---

## 3. 核心整合结论（Key Consolidation Decisions）

1. **执行器映射 SSOT 收敛**：
   - 历史版本中 `M1-T02` 包含了重复的 12 执行器命名表格与出厂映射定义。本次重构确立 `T-ACT-001` 为全库执行器映射的唯一 SSOT，`M1-T02` 改为显式引用 `T-ACT-001`，其正文精炼为架空小阶跃测试规程。
2. **标定数学契约独立为 `T-ACT-002`**：
   - 新建 `T-ACT-002-Servo-Coordinate-Calibration-Contract.md`，形式化定义仿射映射方程 $u_j = u_{0, j} + s_j \cdot k_j \cdot q_j$，显式记录 8 舵机实测旋向极性、未决极性、出厂预设偏置及 Channel 7 硬件故障对整机标定的阻断影响。
3. **架构解耦确认**：
   - 经审计，Gate 验收准则全部直接指向 `docs/evidence/` 下的 `Evidence#Part`，没有任何 Gate 依赖 Topic 的结论作为 PASS 判定；Topic 严格定位于横向交叉分析层。

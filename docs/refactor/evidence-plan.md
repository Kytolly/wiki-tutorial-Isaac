# 证据重构规划表（Evidence Plan）

> 本文档属于：Wiki Evidence 重构工程（Phase 1）  
> 命名规范：**`E-{field English name}-{文档中文名描述}`**（如 `E-hardware-主控板与舵机IMU电气原理图`、`E-simulation-闭链机器人规范树资产说明` 等）。  
> 核心原则：**Evidence 与 Milestone/Gate 解耦。** 一个 Evidence Part 可以被多个 Gate 引用，不以 Gate 结构限制工程事实的自然归属；允许每个证据项引用文档原图片或截图；每个 Part 必须包含忠实复刻/记录源证据的原始物料块。

---

## 1. 工程主题证据规划总表

| Evidence ID | Title | Source(s) | Engineering Purpose | Proposed Parts | Existing Page | Action |
|---|---|---|---|---|---|---|
| **E-hardware-主控板与舵机IMU电气原理图** | **StackForce 主控与舵机供电电气架构** | `SRC-HW-001`, `SRC-HW-002`, `SRC-HW-004`, `SRC-HW-007` | 明确主控 MCU、PCA9685 I2C 舵机板、CAN 收发电路及供电电压轨电气边界，原图切片忠实呈现 | P01: 主控双板供电与电压轨边界<br>P02: PCA9685 I2C 舵机接口拓扑<br>P03: 板间 TWAI/CAN 电气连接与终端电阻<br>P04: IMU 传感器电气接线与引脚分配 | `M1-T01-硬件基线`, `M1-G01-硬件清点` | **CREATE (PILOT)** |
| **E-hardware-双路无刷轮机驱动原理图** | **双路低压无刷轮机驱动器电气特性** | `SRC-HW-003`, `SRC-HW-007` | 明确 DRV8313 驱动芯片额定电流、低压母线供电与磁编码器接口 | P01: DRV8313 驱动逆变桥电气极限<br>P02: 轮机相电流采样硬件配置<br>P03: SSI 磁编码器通信接口 | `M1-T01-硬件基线`, `M1-G03-执行器映射` | **CREATE** |
| **E-mechanical-双支链五杆机构与几何基线** | **双支链五杆机械拓扑与实测几何基线** | `SRC-REP-003`, `SRC-CFG-001`, `SRC-EVI-002` | 形式化定义真实五杆机构杆长（60/100 mm）、投影间距（40 mm）及轴向装配偏置（-44.950 mm） | P01: 双支链五杆连杆几何与孔距真值<br>P02: 四腿底盘对称性反射矩阵与误差<br>P03: W1/W2 轴向偏置与径向共线残差<br>P04: P2 轴承轴向错位与表面间隙 | `mechanical-model.md`, `geometry-baseline.md` | **REWRITE** |
| **E-firmware-舵机与CAN通信控制固件** | **执行器固件控制协议与时序合同** | `SRC-FW-001`, `SRC-FW-002`, `SRC-FW-003`, `SRC-FW-004` | 审计下位机主循环时序、舵机角度指令映射、轮机扭矩 CAN 帧格式与 STOP 停机逻辑，代码逐行忠实复刻 | P01: 舵机角度指令协议与角度映射 API<br>P02: 轮电机 CAN 协议与控制模式定义<br>P03: 下位机控制主循环时序架构<br>P04: 固件级超时判定与主动停机实现<br>P05: 调试串口输出格式与埋点机制 | `M1-T04-控制时序`, `M1-G05-指令定性` | **CREATE (PILOT)** |
| **E-firmware-出厂遥控器与PPM协议说明** | **出厂遥控器协议与手动操作规范** | `SRC-HW-005`, `SRC-PRC-004` | 记录 2.4G 航模遥控器通道定义、PPM 脉宽范围与步态切换映射 | P01: PPM 通道物理映射与脉宽范围<br>P02: 遥控器拨杆模式切换状态机 | `M1-T04-控制时序` | **CREATE** |
| **E-firmware-BLDC无刷电机驱动固件** | **轮电机 SimpleFOC 底层闭环驱动项目** | `SRC-FW-002`, `SRC-FW-006` | 审计 Device02 固件中 SimpleFOC 矢量控制初始化、PID 循环与力矩执行逻辑 | P01: FOC 磁极对数与相电阻配置<br>P02: 开环速度模式与闭环力矩模式切换 | `M1-G05`, `M3-T01` | **CREATE** |
| **E-simulation-闭链机器人规范树资产说明** | **闭链机器人规范树 Loop-Cut 资产规范** | `SRC-PY-001`, `SRC-PY-002`, `SRC-CFG-001`, `SRC-CFG-002` | 形式化定义 29 links / 28 joints 规范树状 URDF、W2 切断设计及 PhysX 闭环转动副恢复实现，原配置与算法忠实记录 | P01: 严格单父树拓扑规范与构件划分<br>P02: W2 处显式 Loop-Cut 运动学切断<br>P03: 四腿闭环参考系元数据约定<br>P04: PhysX 闭环副独立位姿反算算法<br>P05: 规范 Link-Local 二进制网格与面绕向 | `M2-T08-闭环恢复.md`, `M2-T02-机械拓扑` | **CREATE (PILOT)** |
| **E-simulation-PhysX闭环约束动力学配置** | **PhysX 闭环约束动力学原理与配置** | `SRC-DOC-002`, `SRC-PY-002` | 明确 NVIDIA PhysX 约束求解器对非树状闭环副的处理机制及 `excludeFromArticulation` 关键性 | P01: 笛卡尔约束与 Articulation 求解器隔离<br>P02: 闭环转动副参数配置规范（零摩擦/无驱动/无碰撞） | `M2-T08-闭环恢复.md` | **CREATE** |
| **E-simulation-IsaacLab执行器与RL接入规范** | **Isaac Lab 执行器接口与 RL 接入规范** | `SRC-DOC-001` | 明确 Isaac Lab Manager-Based 工作流对执行器组（Actuator Group）与驱动模型的规范定义 | P01: ActuatorBaseCfg 驱动参数语义<br>P02: 轮足机器人混合动作空间定义规范 | `M2-T06-实验室接入`, `Manager-Based工作流入门` | **CREATE** |
| **E-validation-静态资产自动化门禁校验** | **静态数字资产自动化门禁校验** | `SRC-PY-003` | 提供脱离 Omniverse/GPU 依赖的普通 Python3 静态不变量自动化断言工具与执行证据 | P01: URDF 树状拓扑与唯一根断言验证<br>P02: 闭环参考系径向残差门禁校验<br>P03: 二进制 STL 文件格式与存在性验证 | `page/stackforce/gate/M2-G08-Lab载入` | **CREATE** |
| **E-validation-悬空重力仿真烟囱与负对照测试报告** | **悬空重力物理烟囱测试与负对照验证** | `SRC-PY-004`, `SRC-REP-001`, `SRC-REP-002` | 记录 2400 步 CPU 悬空重力测试下 0.0595 mm 闭环漂移 PASS 证据及禁用闭环副导致 129 mm 漂移崩溃的科学负对照 | P01: 2400 步悬空重力测试协议与位移积分<br>P02: 四腿闭环锚点漂移与轴向角误差实测<br>P03: 闭环禁用负对照崩溃实验与结论<br>P04: 资产未就绪边界（rl_ready = false） | `M2-Simulation-Asset.md` | **CREATE** |
| **E-experiment-架空测试时序延迟与安全停机日志** | **实机架空实验测频、延迟与安全联锁记录** | `SRC-EXP-001`, `SRC-EXP-002`, `SRC-EXP-003`, `SRC-LOG-001`, `SRC-LOG-002` | 记录实机架空实测 IMU 采样频率（175.3 Hz）、控制响应时序、停机恢复验证及 ch7 回中失败故障，原始 CSV 与串口日志忠实复刻 | P01: 实机 IMU 采样周期与抖动统计真值<br>P02: 控制指令延迟与自动停机窗口实测<br>P03: 执行器通道与物理响应定性映射<br>P04: ch7 回中失败事件记录与硬件安全断电联锁 | `T02-实验日志`, `T03-安全联锁`, `M1-现场产物归档` | **CREATE (PILOT)** |
| **E-software-Wiki知识库构建与导航校验** | **Wiki 知识库构建器与导航交叉验证** | `SRC-PY-006`, `SRC-CFG-004` | 验证 Wiki 静态编译流水线、Wikilink 语法支持与自动化索引机制 | P01: Markdown 语法与 Wikilink 解析合同<br>P02: 全库交叉引用编译合法性验证（0 errors） | `README.md`, `_META.md` | **CREATE** |

---

## 2. 试点执行说明（Pilot Execution Status）

按照用户指示：
- **当前阶段重点**：确立标准命名规范 `E-{field English name}-{文档中文名描述}`、支持原始图纸与截图引用、在模板与 Pilot 中落地 `#### Raw Source Faithful Reproduction（原始证据忠实复刻）` 专区；
- **执行纪律**：在得到用户明确确认指示前，不擅自启动全库批量处理；
- 首批 4 个 Pilot 已严格按照该新规范完成样板打磨，待用户指令确认后即可进行后续推进。

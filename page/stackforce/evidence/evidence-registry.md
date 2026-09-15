# 证据注册与索引表（Evidence Index）

> **THIS PAGE IS AN INDEX.**  
> **EVIDENCE DOCUMENTS ARE THE SOURCE OF TRUTH.**  
> 本页面为全库规范化证据条目的**全局只读索引（Index Only）**。本页不定义、不重写具体技术断言（Claims）、实测数值（Results）或工程推论（Conclusions）；所有认识论断言与可复现方法一律以 [`docs/evidence/`](../../docs/evidence/) 下的原子证据文档为唯一真源（SSOT）。  
> 历史旧证据标识符映射字典请参阅：[`docs/refactor/legacy-evidence-id-map.md`](../../docs/refactor/legacy-evidence-id-map.md)。

---

## 1. 核心原子证据全索引表（Canonical Evidence Index Table）

| Evidence ID | 证据文档标题 (Title) | 规范状态 (Status) | 认识论角色 (Epistemic Role) | 领域类别 (Domain) | 包含原子分部 (Parts) | 主要消费方 (Consumers) |
|---|---|---|---|---|---|---|
| **`E-CAL-001`** | 实机执行器单通道动作隔离与故障阻断记录 | **VALID** | `PHYSICAL` | Physical Calibration | `P01`~`P05`: 通道映射、阶跃测试、极性定性、ch7 故障事实、ch8 耦合分析 | `M1-G03`, `M1-G04`, `M1-G05`, `M1-G10`, `T-ACT-001`, `T03` |
| **`E-DOC-001`** | 遥控器原厂操作与对频接线指南 | **VALID** | `DOC_SPEC` | Hardware Document | `P01`~`P04`: 接收机线序、S3 接口接线、对频时序、开机安全位姿 | `M1-G05`, `T-ACT-001`, `T03` |
| **`E-DOC-002`** | StackForce四足狗基本操作说明 | **VALID** | `DOC_SPEC` | Hardware Document | `P01`~`P04`: 开关机规程、拨杆模式真值、摇杆量程、行走自稳条件 | `M1-G05`, `M1-G10`, `M6-G06`~`G08`, `T03` |
| **`E-DOC-003`** | 四足机器人整机机械安装与调试指南 | **VALID** | `DOC_SPEC` | Hardware Document | `P01`~`P05`: 紧固件与轴承、机干主架、五杆组装与防松、调试按键、驱动轮与编码器 | `M1-G01`, `M1-G08`, `M1-G09`, `M2-G01`, `M3-G05` |
| **`E-DOC-004`** | 四足机器人整机电气接线与总线拓扑指南 | **VALID** | `DOC_SPEC` | Hardware Document | `P01`~`P05`: 板垛物理分层、4 路 BLDC 极性分配、8 舵机供电拓扑、电池母线、CAN 总线 120Ω | `M1-G01`, `M1-G03`, `M6-G02` |
| **`E-DOC-005`** | 四足机器人整机固件烧录与出厂联调配置指南 | **VALID** | `DOC_SPEC` | Firmware Document | `P01`~`P05`: 双芯片切换、FOC 极对数自校准、8 舵机零位偏置规程、主从烧录、轮机双闭环标定 | `M1-G04`, `M6-G05` |
| **`E-DOC-006`** | 主控板双芯片操作与例程使用必读说明 | **VALID** | `DOC_SPEC` | Firmware Document | `P01`~`P04`: S1/S3 芯片型号、Type-C 切换按键、硬件复位排布、S1 串口注册码机制 | `M1-G01`, `T-HW-REG-001` |
| **`E-DOC-007`** | 客户注册码获取与Arduino环境配置教程 | **VALID** | `DOC_SPEC` | Firmware Document | `P01`~`P05`: Arduino IDE 2.x 版本、ESP32 Dev Module、CH340K 选定、Flash 烧录、串口监视器提取指纹 | `M1-G01`, `T-HW-REG-001` |
| **`E-FW-001`** | 双足轮腿舵机标定固件项目 | **VALID** | `IMPLEMENTATION` | Embedded Firmware | `P01`~`P05`: PlatformIO 构建、8 舵机交互式标定协议、PCA9685 驱动、MPU6050 互补滤波、FreeRTOS | `M1-G01`~`G04`, `M1-G06`, `T-ACT-001` |
| **`E-FW-002`** | BLDC轮电机驱动固件项目 | **VALID** | `IMPLEMENTATION` | Embedded Firmware | `P01`~`P05`: PlatformIO 目标、逆变器 MCPWM、磁编码器双协议、FOC 初始化与 4 种控制模式、串口协议 | `M1-G01`, `M1-G02`, `M1-G04`~`G06`, `M3-G04` |
| **`E-FW-003`** | 四足轮腿运动解算与总线控制固件项目 | **VALID** | `IMPLEMENTATION` | Embedded Firmware | `P01`~`P05`: ESP32-S3 @ 240MHz 构建、PPM 中断解码、五连杆解析 IK、Trot 步态发生器、1Mbps CAN | `M1-G01`, `M1-G02`, `M1-G05`~`G07`, `T-ACT-001` |
| **`E-FW-004`** | 前从控板CAN节点与轮电机驱动固件项目 | **VALID** | `IMPLEMENTATION` | Embedded Firmware | `P01`~`P05`: 前从控配置、CAN 节点 0x02 通信、16位定点解压、SF_BLDC 串口桥接、调度降频 | `M1-G01`, `M1-G03`, `T01` |
| **`E-FW-005`** | 主控板基础外设与传感器通信例程固件 | **VALID** | `IMPLEMENTATION` | Embedded Firmware | `P01`~`P05`: 基础 GPIO 映射、蜂鸣器/WS2812B、BLE GATT、AS5600 轮询、MT6701 高速 SPI/I2C | `M1-G01`, `M1-G02`, `M6-G01` |
| **`E-FW-006`** | 双路无刷电机FOC控制与电流采样例程固件 | **VALID** | `IMPLEMENTATION` | Embedded Firmware | `P01`~`P05`: 30kHz 开环算法、INA199 相电流差分采样、Mode 4 力矩闭环模式、Mode 1/2 模式、UDP 遥测 | `M1-G05`, `M1-G06`, `M3-G01`, `M3-G04` |
| **`E-FW-007`** | 舵机扩展板PCA9685与MPU6050驱动例程固件 | **VALID** | `IMPLEMENTATION` | Embedded Firmware | `P01`~`P02`: PCA9685 16通道 12-bit PWM 驱动、MPU6050 姿态角与角速度读取 | `M1-G02`, `M1-G06` |
| **`E-FW-008`** | 芯片唯一eFuse硬件信息与设备指纹读取固件 | **VALID** | `IMPLEMENTATION` | Embedded Firmware | `P01`~`P05`: S1 运行时架构、115200 串口通信、64 位 eFuse MAC 提取、硅片元数据、授权闭环校验 | `M1-G01`, `T-HW-REG-001` |
| **`E-HW-001`** | ESP32-S3主控板电气原理图与接口规范 | **VALID** | `DOC_SPEC` | Hardware Schematic | `P01`~`P05`: ESP32-S3-WROOM-1U-N16R2 最小系统、CH440R 复用切换、CH340K 下载、电源树、排针总线 | `M1-G01`, `T01` |
| **`E-HW-002`** | PCA9685多路舵机与MPU6050扩展板原理图 | **VALID** | `DOC_SPEC` | Hardware Schematic | `P01`~`P05`: PCA9685PW 拓扑、MPU6050 传感电路、TPS5450 5A Buck 降压、8 路舵机隔离排针、CN1/CN2 互联 | `M1-G01`, `M1-G02`, `M1-G03`, `M1-G06`, `T-ACT-001` |
| **`E-HW-003`** | 双路无刷轮机驱动器与逆变电路原理图 | **VALID** | `DOC_SPEC` | Hardware Schematic | `P01`~`P05`: DRV8313 驱动逆变拓扑、INA199 电流采样、磁编码器物理接口、TPS5450 稳压、动力端子 | `M1-G01`, `M1-G02`, `M1-G03` |
| **`E-HW-004`** | 板间TWAI-CAN与RS485总线通信板原理图 | **VALID** | `DOC_SPEC` | Hardware Schematic | `P01`~`P05`: SN65HVD230 CAN 收发、SP3485 RS-485 扩展、120Ω 终端电阻、B0505S 隔离电源、TVS 防护 | `M1-G01`, `T01` |
| **`E-SIM-001`** | 闭链四足轮腿机器人单父树URDF资产 | **VALID** | `CONFIGURATION` | Simulation Asset | `P01`~`P05`: 29 Links / 28 Joints 单父树、W2 Loop-Cut 切断策略、驱动维度、惯性张量与 STL 网格、末端轮机 | `M1-G08`, `M1-G09`, `M2-G01`, `M2-G02`, `M2-G05`, `M2-G07`, `T-ACT-001` |
| **`E-SIM-002`** | 双支链闭环几何装配不变量与参考系配置 | **VALID** | `CONFIGURATION` | Simulation Asset | `P01`~`P05`: 轴向偏置 -44.950mm、径向共线残差 < 1.83e-17m、Inner Knee 间隙 0.150mm、底盘对称反射矩阵、闭环重构校验契约 | `M1-G08`, `M2-G03`, `M2-G04` |
| **`E-SIM-003`** | PhysX闭环副自动重构与USD后处理实现 | **VALID** | `IMPLEMENTATION` | Simulation Asset | `P01`~`P05`: Isaac Sim 无头环境、closure_joints 作用域、UsdPhysics.RevoluteJoint 注入、excludeFromArticulation=true、Flatten 导出 | `M2-G07`, `M2-G08` |
| **`E-TEST-001`** | 实机架空通信时序与固件超时停机测定 | **VALID** | `RUNTIME` | Physical Benchmark | `P01`~`P05`: 架空隔离条件、PCA9685 50Hz 脉冲响应、500ms 超时看门狗实测、轮机响应边界、ch7 故障事实记录 | `M1-G06`, `M1-G07`, `M1-G10`, `T02`, `T03` |
| **`E-VAL-001`** | 仿真资产静态执行器与被动关节空间划分校验报告 | **VALID** | `VALIDATION` | Validation Report | `P01`~`P05`: 12 主动驱动与 3 执行器组、8 从动被动关节、4 闭环副隔离断言、12 维动作空间纯洁性、16 项静态校验全绿 | `M1-G09`, `M2-G02`, `M2-G06`, `M2-G08`, `T-ACT-001` |
| **`E-VAL-002`** | 强化学习闭环约束收敛与悬空重力烟囱测试报告 | **VALID** | `VALIDATION` | Validation Report | `P01`~`P05`: 5 节点接触力传感器、复位残差收敛、2400 步重力烟囱测试（漂移 <= 0.0595mm）、阶跃激励、负对照 129mm 崩溃与 rl_ready=false | `M2-G06`, `M2-G08`, `M3-G01`, `M3-G06`, `M4-G01` |

---

## 2. 更新日志

- 2026-09-15：彻底重构为只读索引表（Index Only）；移除非法的本地 Claim 与结果定义，明确所有事实真源归属于 `docs/evidence/` 下的具体原子证据文件；收录全部 26 篇正式原子证据。
- 2026-09-15：严格规范证据状态（生命周期状态统一解耦为 `VALID`，严禁与 PASS/FAIL 混淆），独立明确认识论角色（`Epistemic Role`：`DOC_SPEC`, `IMPLEMENTATION`, `CONFIGURATION`, `RUNTIME`, `PHYSICAL`, `VALIDATION`）。

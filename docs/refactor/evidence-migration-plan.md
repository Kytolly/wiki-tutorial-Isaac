# Evidence 架构规范化与分阶段迁移计划
# Evidence Normalization & Phased Migration Plan

> **规划依据**：[`.agents/skills/skill-wiki-design`](../../.agents/skills/skill-wiki-design/SKILL.md)  
> **规划日期**：2026-09-14  
> **目标**：将 Wiki 中现存的混合证据（Mixed Evidence）、碎片化物料与未审计条目，系统化迁移为纯粹单一认识论角色的原子 Evidence 与横向 Topic 矩阵。  
> **执行约束**：**本计划仅作为待审核方案，当前完全停机，等待人工确认后方可执行具体文件写入与迁移。**

---

## 1. 拟建规范化证据清单（Proposed Evidence Target Architecture）

按照 `skill-wiki-design` 标准命名空间与单一认识论角色原则，全库规划归纳为 16 个标准 Evidence 文档：

### 1.1 文档与官方规程类（Namespace: `E-DOC`，角色: `DOC/SPEC`）
| Target Evidence ID | 规范标题 | 承接原始物料 (Source) | 产生原子 Parts | 落地状态 |
|---|---|---|---|---|
| **E-DOC-001** | 遥控器原厂操作与对频接线指南 | `0整机操作说明/遥控器对频说明.docx` | `P01`: 接收机引脚线序与供电极性<br>`P02`: 40引脚S3接口与扩展板接线<br>`P03`: 10秒内3次通断电对频时序与LED状态机<br>`P04`: 遥控器开机安全位姿约束 | **LANDED** |
| **E-DOC-002** | StackForce四足狗基本操作说明 | `0整机操作说明/StackForce四足狗基本操作说明.docx/.pdf` | `P01`: 开关机安全操作时序规程<br>`P02`: 遥控器三位拨杆控制模式真值表<br>`P03`: 基础控制摇杆量程与机器人运动学响应边界<br>`P04`: 步态行走与自稳模式操作条件与安全限制 | **LANDED** |
| **E-DOC-003** | 四足机器人整机机械安装与调试指南 | `1教程/1安装文档.docx/.pdf` | `P01`: 标准紧固件规格、轴承与关节辅助件清单<br>`P02`: 机身主干机架、舵机外环与金属舵盘固定规范<br>`P03`: 五杆闭链腿部连杆组装与轴向防松阻尼间隙控制<br>`P04`: 双MCU板调试按键功能定义与舵机母线调压限值<br>`P05`: BLDC外转子驱动轮总成、磁铁粘贴与编码器间隙配合 | **LANDED** |
| **E-DOC-004** | 四足机器人整机电气接线与总线拓扑指南 | `1教程/2接线文档.docx/.pdf` | `P01`: 前后双分布式板垛物理分层与功能架构<br>`P02`: 4路BLDC轮电机与磁编码器接口极性分配规范<br>`P03`: 8路舵机供电极性、延长线色谱映射与排针层级定义<br>`P04`: 动力电池1分3母线并联供电拓扑与布线路径<br>`P05`: 双板间TWAI/CAN差分总线拓扑、端口防呆与120Ω终端电阻配置 | **LANDED** |
| **E-DOC-005** | 四足机器人整机固件烧录与出厂联调配置指南 | `1教程/3调试文档 .docx/.pdf` | `P01`: Type-C 硬件排针复用与 S1/S3 双芯片物理切换机制<br>`P02`: BLDC 轮电机 FOC 极对数辨识准则与启动自检校准<br>`P03`: 8 通道舵机机械拆卸安全准则与交互式零位偏置标定规程<br>`P04`: 前后主从双板固件烧录部署与整机遥控动作初检规程<br>`P05`: 轮电机速度反馈极性 (`SpdDir`) 与控制极性 (`Dir`) 双闭环标定规程 | **LANDED** |

### 1.2 硬件设计与电气图纸类（Namespace: `E-HW`，角色: `DOC/SPEC`）
| Target Evidence ID | 规范标题 | 承接原始物料 (Source) | 产生原子 Parts | 落地状态 |
|---|---|---|---|---|
| **E-HW-001** | ESP32-S3 主控板电气原理图与接口规范 | `3全套控制板原理图/StackForce主控板.pdf` | `P01`: ESP32-S3-WROOM-1U-N16R2 核心最小系统与射频接口<br>`P02`: CH440R 与按键双芯片硬件复用切换电路<br>`P03`: CH340K USB 转串口与自动下载电路<br>`P04`: XC6210B332MR 高速低压差稳压器与电源树架构<br>`P05`: 20-Pin 驱动板直连插座与 28-Pin 顶层扩展总线接口 | **LANDED** |
| **E-HW-002** | PCA9685 多路舵机与 MPU6050 扩展板原理图 | `3全套控制板原理图/多路舵机+IMU模块.pdf` | `P01`: PCA9685PW 16通道 12-bit PWM 发生器与 I2C 总线拓扑<br>`P02`: MPU-6050 6轴惯性测量单元传感电路<br>`P03`: TPS5450DDAR 5A 大功率开关稳压降压电路（Buck）<br>`P04`: 8 路舵机专用三针排针总线布局与电源物理隔离<br>`P05`: 堆叠扩展接口 CN1/CN2 与主控板互联拓扑 | **LANDED** |
| **E-HW-003** | 双路无刷轮机驱动器与逆变电路原理图 | `3全套控制板原理图/双路无刷电机小功率驱动.pdf` | `P01`: DRV8313PWPR 双路三相半桥逆变器功率驱动拓扑<br>`P02`: INA199A1DCKR 双向低端分流电流采样电路<br>`P03`: 磁编码器双协议兼容物理接口拓扑（MT6701/AS5600）<br>`P04`: TPS5450DDAR 板级 Buck 稳压回路与精密基准源<br>`P05`: 20-Pin 板垛直连插座与电机三相动力输出端子 | **LANDED** |
| **E-HW-004** | 板间 TWAI/CAN 与 RS485 总线通信板原理图 | `3全套控制板原理图/CAN.pdf` | `P01`: SN65HVD230DR 3.3V 高速 CAN 收发器电路<br>`P02`: SP3485EN 3.3V 半双工 RS-485 工业收发扩展电路<br>`P03`: 120Ω 终端匹配电阻与拨码开关选择网络<br>`P04`: B0505S 隔离电源模块与数字信号隔离网络<br>`P05`: TVS/ESD 工业级瞬态防护与接线端子定义 | **LANDED** |

### 1.3 嵌入式固件实现类（Namespace: `E-FW`，角色: `IMPLEMENTATION`）
| Target Evidence ID | 规范标题 | 承接原始物料 (Source) | 产生原子 Parts | 落地状态 |
|---|---|---|---|---|
| **E-FW-001** | 双足轮腿舵机标定固件项目 | `2程序/bipedal_calibrate/` | `P01`: PlatformIO 工程构建配置与硬件目标平台（ESP32-S3）<br>`P02`: 8通道舵机交互式串口标定协议与基准零位偏置解算<br>`P03`: PCA9685 I2C 舵机驱动器硬件使能与 12-bit PWM 定时器寄存器映射<br>`P04`: MPU6050 六轴惯导零偏校准与一阶互补滤波姿态解算<br>`P05`: BLDC 轮电机多闭环控制数据结构与双核 FreeRTOS 抽象层 | **LANDED** |
| **E-FW-002** | BLDC轮电机驱动固件项目 | `2程序/BLDC_Control/` | `P01`: PlatformIO 构建环境与目标芯片架构（ESP32-WROOM / esp32dev）<br>`P02`: 双三相全桥逆变器 MCPWM 硬件引脚分配与使能架构<br>`P03`: 磁编码器双协议硬件总线接口（MT6701 SPI vs AS5600 I2C）<br>`P04`: FOC 核心初始化、电角度校准电压（3V）与四种控制模式<br>`P05`: 双板间 UART 串口通信协议帧结构与 FreeRTOS 异步任务分发 | **LANDED** |
| **E-FW-003** | 四足轮腿运动解算与总线控制固件项目 | `2程序/SF_serveo_control/` | `P01`: PlatformIO 构建环境与目标平台定义（ESP32-S3 @ 240MHz）<br>`P02`: PPM 脉宽调制接收机硬件中断捕获与一阶滤波通道解码<br>`P03`: 五连杆闭链逆运动学（IK）解析几何方程与物理坐标偏置补偿<br>`P04`: 对角小跑（Trot）步态发生器与姿态误差 PID 闭环补偿<br>`P05`: 1Mbps TWAI/CAN 总线协议、定点数压缩与分布式轮电机驱动 | **LANDED** |
| **E-FW-004** | 前从控板CAN节点与轮电机驱动固件项目 | `2程序/SF_serveo_control_device2/` | `P01`: PlatformIO 构建配置与硬件目标平台（ESP32-S3）<br>`P02`: TWAI/CAN 从节点通信接口与地址拓扑（CAN ID 0x02）<br>`P03`: 16位定点数向浮点物理量解压缩算法与前轮速度目标解析<br>`P04`: `SF_BLDC` 串口桥接、初始化时序与工作模态配置<br>`P05`: 主控制循环降频调度、串口监控输出与协议预留 | **LANDED** |

### 1.4 仿真数字资产与运动学模型类（Namespace: `E-SIM`，角色: `CONFIG` / `IMPLEMENTATION`）
| Target Evidence ID | 规范标题 | 承接原始物料 (Source) | 产生原子 Parts |
|---|---|---|---|
| **E-SIM-001** | 闭链机器人单父树 Loop-Cut 规范 URDF 资产 | `urdf`, `build_asset.py` | `P01`: 29 links, 28 joints 严格单父有向无环树<br>`P02`: 闭环回路切断点选定在 W2（内小腿末端）<br>`P03`: 关节树 Featherstone 动力学拓扑约束 |
| **E-SIM-002** | 双支链闭环几何装配不变量与参考系配置 | `closure_frames.json` | `P01`: W1 与 W2 沿 Y 轴恒定 -44.950 mm 偏置<br>`P02`: 径向共线投影残差小于 1.83e-17 m<br>`P03`: P2 间隙 0.150 mm 与偏置 13.650 mm |
| **E-SIM-003** | PhysX 闭环副自动重构与 USD 后处理实现 | `recover_closed_loops.py` | `P01`: USD PhysicsRevoluteJoint 自动注入<br>`P02`: `excludeFromArticulation=true` 解耦配置 |

### 1.5 实验测试、验证与标定类（Namespace: `E-TEST`, `E-VAL`, `E-CAL`，角色: `RUNTIME` / `PHYSICAL`）
| Target Evidence ID | 规范标题 | 承接原始物料 (Source) | 产生原子 Parts |
|---|---|---|---|
| **E-VAL-001** | 规范资产静态数学拓扑与网格合法性校验报告 | `validate_asset.py` | `P01`: 单父树与关节数量自动化断言输出<br>`P02`: 二进制 STL 网格朝向与无退化面验证 |
| **E-VAL-002** | 2400 步 CPU 悬空重力物理烟囱测试报告 | `simulation_report.json` | `P01`: 2400 步闭环约束最大漂移 0.0595 mm<br>`P02`: 闭环禁用负对照崩溃触发（对比漂移 129 mm） |
| **E-TEST-001** | 实机架空通信时序、指令响应与超时停机测定 | `timing_latency.csv`<br>`physical_session_log.md` | `P01`: IMU 实际刷新率 175.3 Hz 与抖动 0.790 ms<br>`P02`: 固件 501.5~502.5 ms 精确触发停机时间戳 |
| **E-CAL-001** | 执行器单通道动作隔离、极性定性与故障阻断记录 | `actuator_registration.csv`<br>`m1_serial_completion.log` | `P01`: 7 路健康执行器动作隔离与正反转极性<br>`P02`: ch7 物理回中失败持续上抬导致手动断电事实 |

---

## 2. 拟建横向分析专题清单（Proposed Topics）

为了承接跨认识论角色的多源交叉验证与冲突排查，规划以下 6 个核心 Topic：

| Topic ID | 专题标题 | 关联 Evidence 集合 | 核心解决问题与交叉比对 |
|---|---|---|---|
| **T-CONTROL-001** | 遥控链路全协议一致性分析 (Golden Topic) | `E-DOC-001` (DOC)<br>`E-FW-001` (FW)<br>`E-HW-001` (HW) | 对照原厂 DOCX 与固件 PPM 解码逻辑；核验引脚 40 与通道定义的吻合度与模式分歧 |
| **T-KINEMATICS-001**| 五杆闭链机构 CAD 标称值与模型树拓扑对齐 | `E-SIM-001` (SIM)<br>`E-SIM-002` (CONFIG)<br>`E-VAL-001` (VAL) | 交叉检验 CAD 测定杆长、URDF 连杆尺寸与 -44.950 mm 装配间隙数学自洽性 |
| **T-DYNAMICS-001**  | 闭链动力学闭环约束无应力稳定性分析 | `E-SIM-003` (SIM)<br>`E-VAL-002` (VAL) | 比较带闭环重构与禁用闭环的 PhysX 表现，证明约束未产生数值发散 |
| **T-ELEC-001**      | 实机供电电源域划分与高低压物理隔离审计 | `E-HW-001` (HW)<br>`E-HW-002` (HW)<br>`E-HW-003` (HW) | 梳理电池母线、5V 逻辑、3.3V 核心与光耦隔离，排查地回路串扰 |
| **T-ACTUATOR-001**  | 执行器开环指令与物理动作响应边界分析 | `E-FW-002` (FW)<br>`E-TEST-001` (TEST)<br>`E-CAL-001` (CAL) | 彻底阐述 `COMMAND != FEEDBACK`，揭示软件写 90 度与物理实测到位之间的巨大鸿沟 |
| **T-SAFETY-001**    | 软件看门狗与实机硬件失控断电阻断分析 | `E-FW-004` (FW)<br>`E-TEST-001` (TEST)<br>`E-CAL-001` (CAL) | 深度分析固件发出 STOP 但硬件 ch7 依旧失控的物理机理，论证母线物理断电的不可替代性 |

---

## 3. 重点案例迁移实施计划：Golden Example 拆分方案

针对当前已生成的混合证据 `E-control-遥控器对频与接收机接线说明.md`，制定以下拆解实施方案：

```text
[当前现状 - 违规混合]
E-control-遥控器对频与接收机接线说明.md (DOC + CODE 混杂)
         │
         ├── 拆分为 ──► E-DOC-001 (遥控器与接收机原厂操作与接线指南)
         │              ├── P01: 接收机引脚线序与供电 (DOCX 原图原话)
         │              ├── P02: 10秒通断电三次对频时序与LED状态机
         │              └── P03: 遥控器开机安全位姿约束（左摇杆与拨杆置底）
         │
         ├── 拆分为 ──► E-FW-001 (接收机 PPM 中断解码与遥控通道映射固件)
         │              ├── P01: GPIO 40 上升沿外部中断与脉宽计时实现
         │              ├── P02: 8 通道 PPM 脉宽低通滤波算法
         │              └── P03: 遥控器摇杆量程与机器人腿高/翻滚映射
         │
         └── 建立 ────► T-CONTROL-001 (遥控链路全协议一致性分析 Topic)
                        ├── DOC ↔ FW 引脚一致性 (CONSISTENT)
                        ├── DOC ↔ FW 模式切换通道分歧 (CONFLICT / INFERRED)
                        └── 未决通道分析 (UNRESOLVED: 通道 8 实际用途)
```

---

## 4. 迁移实施步骤与检查关卡（Phase Checklist）

- [ ] **Step 1: 用户审核本计划**（等待人工确认，不提前写文件）；
- [ ] **Step 2: 落地 E-DOC-001**（纯原厂操作规范，嵌入 5 张原图）；
- [ ] **Step 3: 落地 E-FW-001**（纯固件代码，逐行复刻 PPM 中断与通道计算）；
- [ ] **Step 4: 落地 T-CONTROL-001**（横向交叉分析专题）；
- [ ] **Step 5: 移除旧混合证据**（安全更替 `E-control-遥控器对频与接收机接线说明.md`）；
- [ ] **Step 6: 依次推进 E-HW, E-SIM, E-TEST, E-CAL 体系**；
- [ ] **Step 7: 建立 Gate 准则精准引用并更新 Milestone 看板**。

---

## 5. 需要人工确认的关键决策项（Open Questions for Human Review）

1. **命名风格偏好确认**：
   - 方案 A（全英文+数字）：`E-DOC-001-remote-controller-manual.md`
   - 方案 B（混合中文语义）：`E-DOC-001-遥控器原厂操作与接线指南.md`
   - *（建议采用方案 B，既保留全局唯一的命名空间检索性，又具有中文直观语义）*。
2. **Topic 存放目录确认**：
   - 方案 A：存放在 `docs/topics/`
   - 方案 B：存放在 `page/stackforce/topic/`
   - *（建议放入 `page/stackforce/topic/`，可直接参与 MkDocs 导航树展示）*。
3. **是否立即启动 Step 2 ~ Step 4（Golden Example 落地与拆分）？**

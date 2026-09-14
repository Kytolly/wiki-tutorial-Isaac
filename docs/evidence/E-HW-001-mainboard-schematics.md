---
evidence_id: E-HW-001
title: StackForce 主控板与舵机/IMU/CAN电气原理图规范
status: VALID
created: 2026-09-14
last_verified: 2026-09-14
sources:
  - source_id: SRC-HW-001
    type: MANUFACTURER_SPEC
    path_or_url: doc/四足机器人-origin/3全套控制板原理图/StackForce主控板.pdf
    revision: 2024-07-05
  - source_id: SRC-HW-002
    type: MANUFACTURER_SPEC
    path_or_url: doc/四足机器人-origin/3全套控制板原理图/多路舵机+IMU模块.pdf
    revision: 2024-07-05
  - source_id: SRC-HW-004
    type: MANUFACTURER_SPEC
    path_or_url: doc/四足机器人-origin/3全套控制板原理图/CAN.pdf
    revision: 2024-07-05
  - source_id: SRC-HW-007
    type: MANUFACTURER_SPEC
    path_or_url: doc/四足机器人-origin/1教程/2接线文档.pdf
    revision: 2024-07-05
---

# E-HW-001 — StackForce 主控板与舵机/IMU/CAN电气原理图规范

> 证据定位：`E-HW-001`  
> 状态：`VALID`（硬件设计图纸真实有效，已完成元器件与网络审计）  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档提炼自原厂电路图纸的电气工程语义，所有硬件参数标记为 `SPECIFIED`。

---

## 1. Scope（工程范围）

- **核心工程问题**：
  1. 机器人主控芯片型号及其核心外设引脚分配（ESP32-S3）是什么？
  2. 8 路舵机驱动模块的控制总线拓扑、驱动芯片（PCA9685）及通道物理映射是什么？
  3. 板载 IMU 传感器型号及其电气通信总线类型是什么？
  4. 板间 CAN/TWAI 总线收发器电路、隔离设计及终端电阻配置是什么？
- **应用范围**：StackForce 四轮足机器人主控电气系统、8 路腿部关节舵机接口、IMU 惯导接口与板间通信总线。
- **非目标**：不涵盖轮毂电机逆变电路（见 `E-HW-002`）、不涵盖实机物理接线磨损与接触电阻测量、不涵盖未通电状态下的动态波形。

---

## 2. Source Summary（技术源清单）

| Source ID | 类型 | 规范便携路径 | 版本 / 签发日期 | 角色与描述 |
|---|---|---|---|---|
| `SRC-HW-001` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/StackForce主控板.pdf` | 2024-07-05 | ESP32-S3 主控板主电路原理图 |
| `SRC-HW-002` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/多路舵机+IMU模块.pdf` | 2024-07-05 | PCA9685 8通道 PWM 与 MPU6050 电路图 |
| `SRC-HW-004` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/CAN.pdf` | 2024-07-05 | CAN/RS485 电气隔离与收发接口原理图 |
| `SRC-HW-007` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/1教程/2接线文档.pdf` | 2024-07-05 | 原厂线束引脚定义与外部供电接口指南 |

---

## 3. Evidence Parts（可独立引用的工程事实）

<a id="p01-mcu-power-domain"></a>
### P01 — ESP32-S3 主控与供电电源域划分

#### Engineering Statement
> [SPECIFIED] 机器人主控制器采用乐鑫 ESP32-S3 系列 MCU，具备逻辑 `3.3V`、主板 `5V`（USB/DC-DC）与外部动力电池电压轨输入。主逻辑系统供电与高压大电流动力电源在原理图上通过独立稳压芯片隔离。

#### Source Observation
- `StackForce主控板.pdf` 包含 `ESP32-S3` 核心最小系统，标注供电网络 `S3_3V3`、`S3_5V`、`USB_5V`、`VIN` 与 `BAT_MEASURE` 分压电阻网络。
- 动力输入端配备反接保护与电池电压采样分压电阻（接入 ADC 输入引脚）。

#### Engineering Interpretation
- 主控 MCU 逻辑与通信外设工作于 3.3V 电平标准；
- 电池分压电阻网络支持主控板通过 ADC 实时读取动力总线电压，为低压软报警与欠压切断策略提供硬件基础；
- USB 5V 与电池输入具备隔离二极管，防止调试烧录时与动力电池倒灌。

#### Limitations
- 原理图标记的 `VIN` 电平不能证明实机当前插入的是 2S 还是 3S 锂电池组（需由实物测量或电池铭牌支撑）；
- 原理图存在不能代表 PCB 覆铜实际过流能力与热损耗已实测达标。

#### Source Trace
- 文件：`doc/四足机器人-origin/3全套控制板原理图/StackForce主控板.pdf`
- 图页 / 模块：Sheet 1 "Power Supply & MCU"
- 关键词：`"ESP32-S3"`, `"BAT_MEASURE"`, `"S3_3V3"`, `"VIN"`

---

<a id="p02-pca9685-servo-topology"></a>
### P02 — PCA9685 8路舵机驱动总线与通道映射

#### Engineering Statement
> [SPECIFIED] 机器人整机 8 个关节舵机由独立的 PCA9685 芯片（12-bit PWM，I2C 接口）集中驱动，通道分配为 `PWM0` 至 `PWM7`，I2C 总线连接至 ESP32-S3 主控。

#### Source Observation
- `多路舵机+IMU模块.pdf` 中 U1 标定为 `PCA9685`，其引脚 `PWM0` ~ `PWM7` 分别引出至 8 组三线（VCC, GND, PWM）舵机接线排针。
- PCA9685 的 `A0`, `A1`, `A2` 地址引脚接地，硬件固定 I2C 7 位基准地址为 `0x40`。
- 控制信号线 `SDA`、`SCL` 接至上拉电阻后引出到主板连接器。

#### Engineering Interpretation
- 8 个舵机完全脱离主控 MCU 的直接硬件 PWM 定时器，由 PCA9685 内部计数器提供稳定的 50 Hz PWM 载波；
- 主控与舵机控制器的交互带宽受限于 I2C 总线物理速率（通常 100 kHz 或 400 kHz）；
- 通道 `PWM0` 至 `PWM7` 为板级物理索引，在固件层必须经过严格通道查找表映射才能转换为机器人左前/右前/左后/右后的具体内外大腿关节。

#### Limitations
- PCA9685 原理图仅证明物理上有 8 个独立 PWM 信号线，**不能证明**实机中哪一根线实际插到了哪一个机械腿的舵机上（必须结合 `E-EXP-001` 或接线记录映射）；
- 舵机插针仅包含控制信号（PWM）与电源，**不存在回读位置传感器反馈引脚**（舵机为开环指令执行）。

#### Source Trace
- 文件：`doc/四足机器人-origin/3全套控制板原理图/多路舵机+IMU模块.pdf`
- 图页 / 模块：Sheet 1 "U1 PCA9685"
- 关键词：`"PWM0"`, `"PWM7"`, `"PCA9685"`, `"SDA"`, `"SCL"`

---

<a id="p03-imu-sensor-interface"></a>
### P03 — 板载 IMU 传感器电气接线与选型

#### Engineering Statement
> [SPECIFIED] 舵机/IMU 复合模块原理图上设计了 `MPU-6050`（或同引脚兼容 ICM 系列）六轴惯性测量单元，通过同一组硬件 I2C 总线与主控 MCU 通信。

#### Source Observation
- `多路舵机+IMU模块.pdf` 中 U2 标注为 `MPU-6050_C24112`。
- 供电引脚接 `S3_3V3`，通信引脚接同一 I2C 网络的 `SDA` 与 `SCL`。
- 外部具备去耦电容与滤波电容。

#### Engineering Interpretation
- 机器人位姿估计的核心传感器物理集成在舵机子板上，随子板固定在车体中心骨架；
- 与 PCA9685 共用 I2C 总线，这意味着主控在同一个物理通信总线上既要周期性写入舵机角度，又要周期性读取 IMU 六轴角速度与加速度。总线仲裁与时序延迟（见 `E-EXP-001`）直接受限于此共享拓扑。

#### Limitations
- 原理图提供的是设计选型，实机贴片物料可能根据供货批次替换为 ICM42688 等引脚兼容芯片（需要固件 WHO_AM_I 寄存器读取或实测日志确证）；
- 不能由原理图推断传感器的实机噪声水平与动态漂移。

#### Source Trace
- 文件：`doc/四足机器人-origin/3全套控制板原理图/多路舵机+IMU模块.pdf`
- 图页 / 模块：Sheet 1 "U2 MPU6050"
- 关键词：`"MPU-6050"`, `"SDA"`, `"SCL"`, `"S3_3V3"`

---

<a id="p04-can-transceiver-topology"></a>
### P04 — 板间 TWAI/CAN 通信与电气隔离

#### Engineering Statement
> [SPECIFIED] 主控板与电机驱动板之间采用 CAN 总线通信，板载 `SN65HVD230DR` 差分收发芯片与 `π121M31` 数字隔离芯片，预留 $120\ \Omega$ 终端匹配电阻及拨码开关。

#### Source Observation
- `CAN.pdf` 中收发器 U1 为 `SN65HVD230DR`（3.3V CAN 收发器），连接差分线 `CAN_H` 与 `CAN_L`。
- 差分总线之间跨接 $120\ \Omega$ 电阻（R1），通过拨码开关 SW14 控制接入。
- 配备 `NUP2105L` ESD 浪涌保护器件。
- 数字信号线 `CAN_TX`、`CAN_RX` 经由 `π121M31` 数字隔离器连接到 ESP32-S3 的 GPIO（S3_IO39 / S3_IO42），隔离端供电采用 `B0505S-1W` 隔离 DC-DC 模块。

#### Engineering Interpretation
- 通信层采用标准物理隔离 CAN 架构，可有效抑制轮电机驱动大电流开关噪声对 ESP32-S3 核心逻辑地平面的传导干扰；
- 终端电阻 $120\ \Omega$ 可根据实际挂载节点配置开闭；
- 传输物理带宽受限于 ESP32-S3 的 TWAI 控制器最大速率（通常配置为 1 Mbit/s）。

#### Limitations
- 原理图的 1 Mbit/s 物理上限不代表应用层指令刷新频率（应用层周期取决于固件轮询/中断调度实现，见 `E-FW-001`）；
- 隔离器件引入了纳秒级的信号传输延迟，但不构成毫秒级控制周期的主要瓶颈。

#### Source Trace
- 文件：`doc/四足机器人-origin/3全套控制板原理图/CAN.pdf`
- 图页 / 模块：Sheet 1 "CAN Transceiver & Isolation"
- 关键词：`"SN65HVD230DR"`, `"π121M31"`, `"B0505S-1W"`, `"120R"`, `"CAN_H"`, `"CAN_L"`

---

## 4. Artifacts（关联产物与机器可读附件）

| 产物名称 | 存储相对路径 | 格式 / 属性 | 角色说明 |
|---|---|---|---|
| 主控板原理图 | `doc/四足机器人-origin/3全套控制板原理图/StackForce主控板.pdf` | PDF (Vector) | 原厂电气主图 |
| 舵机板原理图 | `doc/四足机器人-origin/3全套控制板原理图/多路舵机+IMU模块.pdf` | PDF (Vector) | 舵机与IMU子图 |
| CAN总线原理图 | `doc/四足机器人-origin/3全套控制板原理图/CAN.pdf` | PDF (Vector) | 总线隔离与收发子图 |

---

## 5. Provenance & Reproducibility（溯源与可复现方法）

- **提取方法**：使用 `pdfinfo` 与 `pdftotext` 提取文本网络标号，通过跨文件对照确证网络命名一致性。
- **校验命令**：
  ```bash
  pdftotext doc/四足机器人-origin/3全套控制板原理图/CAN.pdf - | grep -E "SN65HVD230|120R|CAN_H"
  ```
- **预期输出**：终端打印包含收发芯片与终端电阻标号的纯文本记录。

---

## 6. Revision History（修订历史）

- `2026-09-14`：建立 `E-HW-001` 规范 Evidence 文档，从原厂电路图纸中提炼 MCU、PCA9685、IMU 和 CAN 隔离收发四个独立工程事实（P01–P04）。

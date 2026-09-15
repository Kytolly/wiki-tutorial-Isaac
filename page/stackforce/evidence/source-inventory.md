# 来源清单与技术源索引（Source Index）

> **THIS PAGE IS AN INDEX.**  
> **RAW ARTIFACTS AND UPSTREAM SOURCES ARE THE SOURCE OF TRUTH.**  
> 本页面属于 StackForce 机器狗实战的技术源索引（Source Index）。本页不进行门禁决策，亦不重复撰写实验结论。  
> 完整来源覆盖度审计与机器可读映射详见：`_meta/source-inventory.yaml` 与 `docs/refactor/source-inventory.md`。

---

## 1. 原始技术源索引（Canonical Source Index Table）

| Source ID | 类别 (Type) | 路径 / 规约位置 (Path / Spec) | 对应原子证据 (Related Evidence) | 状态 (Status) | 说明 (Notes) |
|---|---|---|---|---|---|
| `SRC-HW-001` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/StackForce主控板.pdf` | `E-HW-001` | **CONFIRMED** | ESP32-S3 主控板最小系统与排针总线 |
| `SRC-HW-002` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/多路舵机+IMU模块.pdf` | `E-HW-002` | **CONFIRMED** | PCA9685 舵机驱动板与 MPU6050 电路 |
| `SRC-HW-003` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/双路无刷电机小功率驱动.pdf` | `E-HW-003` | **CONFIRMED** | DRV8313 驱动逆变桥与相电流采样 |
| `SRC-HW-004` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/CAN.pdf` | `E-HW-004` | **CONFIRMED** | SN65HVD230 CAN 收发与 120Ω 匹配 |
| `SRC-HW-005` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/0整机操作说明/StackForce四足狗基本操作说明.pdf` | `E-DOC-002` | **CONFIRMED** | 开关机操作与遥控器三位拨杆模式 |
| `SRC-HW-006` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/1教程/1安装文档.pdf` | `E-DOC-003` | **CONFIRMED** | 机械安装顺序、轴承配合与轮毂紧固 |
| `SRC-HW-007` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/1教程/2接线文档.pdf` | `E-DOC-004` | **CONFIRMED** | 电气母线拓扑与电机排针连接 |
| `SRC-HW-008` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/1教程/3调试文档 .pdf` | `E-DOC-005` | **CONFIRMED** | 舵机零位微调、FOC 极对数校准规程 |
| `SRC-HW-009` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/0整机操作说明/遥控器对频说明.pdf` | `E-DOC-001` | **CONFIRMED** | PPM 接收机引脚线序与通断电对频 |
| `SRC-HW-010` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/4例程资料/主控板例程/0使用前必看说明/使用说明.docx` | `E-DOC-006` | **CONFIRMED** | S1/S3 硬件切换与串口输出机制 |
| `SRC-HW-011` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/5客户获取注册码/arduino使用教程.docx` | `E-DOC-007` | **CONFIRMED** | Arduino IDE 配置与注册码提取流程 |
| `SRC-FW-001` | `SOURCE_CPP` | `doc/四足机器人-origin/2程序/bipedal_calibrate/` | `E-FW-001` | **IMPLEMENTED** | 8 舵机标定与 MPU6050 互补滤波固件 |
| `SRC-FW-002` | `SOURCE_CPP` | `doc/四足机器人-origin/2程序/BLDC_Control/` | `E-FW-002` | **IMPLEMENTED** | 双路 SimpleFOC 闭环轮机驱动固件 |
| `SRC-FW-003` | `SOURCE_CPP` | `doc/四足机器人-origin/2程序/SF_serveo_control/` | `E-FW-003` | **IMPLEMENTED** | PPM 中断解码、五连杆 IK 与 1Mbps CAN |
| `SRC-FW-004` | `SOURCE_CPP` | `doc/四足机器人-origin/2程序/SF_serveo_control_device2/` | `E-FW-004` | **IMPLEMENTED** | 前从控板 0x02 节点通信与轮机驱动 |
| `SRC-FW-005` | `SOURCE_CPP` | `doc/四足机器人-origin/4例程资料/主控板例程/` | `E-FW-005` | **IMPLEMENTED** | 外设通信例程（AS5600/MT6701/WS2812B） |
| `SRC-FW-006` | `SOURCE_CPP` | `doc/四足机器人-origin/4例程资料/主控板加小电流板/` | `E-FW-006` | **IMPLEMENTED** | Mode 4 力矩控制与相电流差分采样 |
| `SRC-FW-007` | `SOURCE_CPP` | `doc/四足机器人-origin/4例程资料/主控板加舵机板/` | `E-FW-007` | **IMPLEMENTED** | PCA9685 12-bit PWM 舵机驱动例程 |
| `SRC-FW-008` | `SOURCE_CPP` | `doc/四足机器人-origin/5客户获取注册码/getInfo/getInfo.ino` | `E-FW-008` | **IMPLEMENTED** | 64 位 eFuse MAC 提取与设备指纹读取 |
| `SRC-SIM-001` | `ROBOT_ASSET` | `sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf` | `E-SIM-001` | **VERIFIED** | 29 links, 28 joints 规范单父树 URDF |
| `SRC-SIM-002` | `CONFIG` | `sf_quad/.../config/closure_frames.json` | `E-SIM-002` | **VERIFIED** | W1/W2 轴向 -44.950mm 偏置与径向残差元数据 |
| `SRC-SIM-003` | `SOURCE_PYTHON` | `sf_quad/.../scripts/recover_closed_loops.py` | `E-SIM-003` | **VERIFIED** | PhysX RevoluteJoint 闭环副自动重构脚本 |
| `SRC-VAL-001` | `SOURCE_PYTHON` | `sf_quad/.../scripts/validate_asset.py` | `E-VAL-001` | **VERIFIED** | 16 项静态不变量自动化断言工具 |
| `SRC-VAL-002` | `SOURCE_PYTHON` | `sf_quad/.../scripts/simulation_validation.py` | `E-VAL-002` | **VERIFIED** | 2400 步 CPU 悬空重力烟囱测试脚本 |
| `SRC-EXP-001` | `RUNTIME_LOG` | `doc/StackForceDog/artifacts/physical_session_log.md` | `E-TEST-001` | **RECORDED** | 架空台架 500ms 超时看门狗实机测定记录 |
| `SRC-EXP-002` | `PHYSICAL_MEASUREMENT` | `doc/StackForceDog/artifacts/safety_validation.md` | `E-CAL-001` | **RECORDED** | 8 通道阶跃测试、ch7 持续上抬故障与母线断电记录 |

---

## 2. 更新日志

- 2026-09-15：重构为标准技术源只读索引（Source Index Only）；严格遵循 A PATH IS NOT EVIDENCE 原则；对齐全库 26 项核心原始技术物料。

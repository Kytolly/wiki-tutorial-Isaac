# 全量原始技术源清单（Source Inventory）

> 本文档属于：Wiki Evidence 重构工程（Phase 1）  
> 核心原则：**A PATH IS NOT EVIDENCE.** 文件路径存在仅证明资产存在于当前文件系统，不代表其内容已经验证或其工程事实成立。  
> 命名规范：**`E-{field English name}-{文档中文名描述}`**。  
> 用途：系统盘点 StackForce 四轮足机器人与 Isaac 仿真工程中涉及的所有原始图纸、文档、源码、固件、配置、日志、实验报告及已有 Wiki 证据。

---

## 1. 原始技术源分类统计

| Source Type | 数量 | 覆盖范围 |
|---|---:|---|
| `MANUFACTURER_SPEC` | 8 | 官方原理图 PDF、硬件连接图纸、组装调试手册 |
| `OFFICIAL_DOC` | 4 | NVIDIA Isaac Sim / Lab 官方手册、ESP-IDF / SimpleFOC 规范 |
| `SOURCE_CPP` | 7 | 主控板与下位机固件源码、CAN 通信库、PCA9685 驱动 |
| `SOURCE_PYTHON` | 6 | 规范资产生成器、闭环恢复脚本、静态校验器、仿真烟囱测试器 |
| `CONFIG` | 4 | 闭环几何元数据 (`closure_frames.json`)、URDF 描述、PlatformIO 配置 |
| `PROCEDURE` | 4 | 遥控器对频指南、上电检查清单、架空实验流程指南 |
| `RUNTIME_LOG` | 3 | 架空实机串口通信全量日志、固件编译/构建日志 |
| `PHYSICAL_MEASUREMENT` | 3 | 实机测频/延迟 CSV、执行器注册 CSV、安全联锁记录 |
| `GENERATED_REPORT` | 3 | 2400 步 CPU 仿真报告、负对照报告、四腿几何校验报告 |
| `EXISTING_EVIDENCE` | 6 | Wiki 现有 evidence/ 页面与 _meta 元数据配置 |
| **总计** | **48** | **全工程关键证据源全覆盖** |

---

## 2. 全量技术源详细登记表

| Source ID | Type | Path / URL (便携式相对路径) | 简要描述 | Current Wiki References | Proposed Evidence ID | 状态 / 校验边界 |
|---|---|---|---|---|---|---|
| `SRC-HW-001` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/StackForce主控板.pdf` | ESP32-S3 主控板硬件原理图（供电、USB-CDC、CAN 收发器、PCA9685 接口） | `M1-G01`, `M1-T01` | `E-hardware-主控板与舵机IMU电气原理图` | RAW_AVAILABLE（未实机电气测绘验证） |
| `SRC-HW-002` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/多路舵机+IMU模块.pdf` | 8 路舵机驱动板与 MPU6050/ICM IMU 接口原理图 | `M1-G02`, `M1-G03`, `M1-T01` | `E-hardware-主控板与舵机IMU电气原理图` | RAW_AVAILABLE（包含 PCA9685 I2C 拓扑） |
| `SRC-HW-003` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/双路无刷电机小功率驱动.pdf` | 轮毂电机低压驱动板原理图（DRV8313 逆变、采样电阻、SSI 编码器接口） | `M1-G01`, `M1-G03`, `M1-T01` | `E-hardware-双路无刷轮机驱动原理图` | RAW_AVAILABLE |
| `SRC-HW-004` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/3全套控制板原理图/CAN.pdf` | 板间 CAN (TWAI) 通信电气接口与终端电阻定义图纸 | `M1-G01`, `M1-T04` | `E-hardware-主控板与舵机IMU电气原理图` | RAW_AVAILABLE |
| `SRC-HW-005` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/0整机操作说明/StackForce四足狗基本操作说明.pdf` | 官方出厂说明书（整机遥控模式、PPM 通道分配、基础步态说明） | `M1-G05`, `M1-T04` | `E-firmware-出厂遥控器与PPM协议说明` | RAW_AVAILABLE（遥控器通道映射参考） |
| `SRC-HW-006` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/1教程/1安装文档.pdf` | 机械本体装配指南、舵机舵盘零位机械对齐说明 | `M1-G04`, `M1-T05` | `E-mechanical-机械本体装配与零位说明` | RAW_AVAILABLE |
| `SRC-HW-007` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/1教程/2接线文档.pdf` | 电气母线与通信接线说明（主控板至电机驱动板、电池接线） | `M1-G01`, `M1-T01` | `E-hardware-主控板与舵机IMU电气原理图` | RAW_AVAILABLE |
| `SRC-HW-008` | `MANUFACTURER_SPEC` | `doc/四足机器人-origin/1教程/3调试文档 .pdf` | 固件烧录、零位微调与基本串口调试指南 | `M1-G04`, `M1-T02` | `E-firmware-出厂遥控器与PPM协议说明` | RAW_AVAILABLE |
| `SRC-DOC-001` | `OFFICIAL_DOC` | `https://isaac-sim.github.io/IsaacLab/` | NVIDIA Isaac Lab 官方文档（Actuator APIs、Manager-based RL 环境） | `Intro`, `Setup`, `M2-T06` | `E-simulation-IsaacLab执行器与RL接入规范` | UPSTREAM_DOCUMENTATION |
| `SRC-DOC-002` | `OFFICIAL_DOC` | `https://docs.isaacsim.omniverse.nvidia.com/` | NVIDIA Isaac Sim 官方文档（PhysX 约束、RevoluteJoint、Articulation） | `USD入门`, `闭环恢复` | `E-simulation-PhysX闭环约束动力学配置` | UPSTREAM_DOCUMENTATION |
| `SRC-DOC-003` | `OFFICIAL_DOC` | `https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/twai.html` | ESP32-S3 TWAI/CAN 驱动协议与时序参考手册 | `M1-T04` | `E-firmware-舵机与CAN通信控制固件` | UPSTREAM_DOCUMENTATION |
| `SRC-DOC-004` | `OFFICIAL_DOC` | `https://docs.simplefoc.com/` | SimpleFOC 算法库官方文档（BLDCMotor 扭矩/电压控制模式） | `M1-G05`, `M3-T01` | `E-firmware-BLDC无刷电机驱动固件` | UPSTREAM_DOCUMENTATION |
| `SRC-FW-001` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control/src/main.cpp` | Device01 主控板主固件（PPM 解算、IK 姿态、PCA9685 舵机写入、TWAI CAN 发送） | `M1-G03~G07`, `M1-T02` | `E-firmware-舵机与CAN通信控制固件` | IMPLEMENTED_INSPECTED（行号 600, 666 已审计） |
| `SRC-FW-002` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control_device2/src/main.cpp` | Device02 轮电机驱动固件（CAN 接收、SimpleFOC 闭环/开环写入） | `M1-G03~G07`, `M1-T02` | `E-firmware-舵机与CAN通信控制固件` | IMPLEMENTED_INSPECTED（行号 70, 116 已审计） |
| `SRC-FW-003` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control/lib/SF_Servo/SF_Servo.cpp` | PCA9685 I2C 舵机驱动封装实现 | `M1-G06`, `M1-T04` | `E-firmware-舵机与CAN通信控制固件` | IMPLEMENTED_INSPECTED |
| `SRC-FW-004` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control/lib/SF_CAN/SF_CAN.cpp` | TWAI 报文组包、收发与缓冲区实现 | `M1-G06`, `M1-T04` | `E-firmware-舵机与CAN通信控制固件` | IMPLEMENTED_INSPECTED |
| `SRC-FW-005` | `SOURCE_CPP` | `lib/firmware/bipedal_calibrate/src/main.cpp` | 舵机校准与机械限位标定工具固件 | `M1-G04` | `E-firmware-舵机与CAN通信控制固件` | IMPLEMENTED_INSPECTED |
| `SRC-FW-006` | `SOURCE_CPP` | `lib/firmware/BLDC_Control/src/main.cpp` | 独立无刷轮电机速度/位置测试固件 | `M1-G05` | `E-firmware-BLDC无刷电机驱动固件` | IMPLEMENTED_INSPECTED |
| `SRC-FW-007` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control/platformio.ini` | 固件构建目标、晶振配置、编译器优化与依赖库清单 | `M1-T01` | `E-firmware-舵机与CAN通信控制固件` | CONFIGURED |
| `SRC-PY-001` | `SOURCE_PYTHON` | `sf_quad/.../scripts/build_asset.py` | 确定性资产生成器（提取局部 STL、生成 URDF 与 USD） | `M2-G02`, `M2-T01` | `E-simulation-闭链机器人规范树资产说明` | IMPLEMENTED_EXECUTABLE |
| `SRC-PY-002` | `SOURCE_PYTHON` | `sf_quad/.../scripts/recover_closed_loops.py` | PhysX 闭环重构脚本（独立反算 W2 局部位姿，挂载 RevoluteJoint） | `M2-G07`, `闭环恢复` | `E-simulation-闭链机器人规范树资产说明` | IMPLEMENTED_EXECUTED |
| `SRC-PY-003` | `SOURCE_PYTHON` | `sf_quad/.../scripts/validate_asset.py` | 静态资产几何/拓扑不变量断言校验器 | `M2-G08`, `evidence-registry` | `E-validation-静态资产自动化门禁校验` | EXECUTED_VERIFIED（退出码 0） |
| `SRC-PY-004` | `SOURCE_PYTHON` | `sf_quad/.../scripts/simulation_validation.py` | CPU 悬空 2400 步重力仿真烟囱测试与负对照验证脚本 | `M2-Simulation-Asset` | `E-validation-悬空重力仿真烟囱与负对照测试报告` | EXECUTED_VERIFIED |
| `SRC-PY-005` | `SOURCE_PYTHON` | `sf_quad/.../scripts/build_urdf.py` | 早期 Ref B 树状 URDF 构建脚本 | `M2-reverse-engineering` | `E-simulation-闭链机器人规范树资产说明` | SUPERSEDED by `SRC-PY-001` |
| `SRC-PY-006` | `SOURCE_PYTHON` | `script/build.py` | Wiki 静态页面编译器与导航交叉引用校验器 | `_META`, `README` | `E-software-Wiki知识库构建与导航校验` | EXECUTED_VERIFIED（0 errors） |
| `SRC-CFG-001` | `CONFIG` | `sf_quad/.../config/closure_frames.json` | 四腿 W1/W2 闭环坐标、机械转轴方向、-44.950 mm 偏置元数据 | `M2-G04`, `M2-T03` | `E-simulation-闭链机器人规范树资产说明` | VALIDATED（机器可读真源） |
| `SRC-CFG-002` | `CONFIG` | `sf_quad/.../urdf/stackforce_quadrupedal_wheeled_robot.urdf` | 29 links, 28 joints 规范单父树 Loop-cut URDF 描述 | `M2-G02`, `M2-T02` | `E-simulation-闭链机器人规范树资产说明` | VALIDATED（拓扑解析无环） |
| `SRC-CFG-003` | `CONFIG` | `sf_quad/.../ref_b_real_fr/geometry_config.json` | 早期右前腿五杆几何标定配置 | `legacy`, `geometry-baseline` | `E-mechanical-双支链五杆机构与几何基线` | SUPERSEDED by `SRC-CFG-001` |
| `SRC-CFG-004` | `CONFIG` | `script/mkdocs.yml` | Wiki 静态站点导航与渲染配置文件 | 全库 | `E-software-Wiki知识库构建与导航校验` | CONFIGURED |
| `SRC-PRC-001` | `PROCEDURE` | `doc/StackForceDog/artifacts/m1_commands.txt` | 实机架空 Session 1 指令执行脚本与操作序列 | `M1-现场产物归档` | `E-experiment-架空测试时序延迟与安全停机日志` | EXECUTED_ARCHIVED |
| `SRC-PRC-002` | `PROCEDURE` | `doc/StackForceDog/artifacts/m1_completion_commands.txt` | 实机架空 Session 2 闭环补测执行指令序列 | `M1-现场产物归档` | `E-experiment-架空测试时序延迟与安全停机日志` | EXECUTED_ARCHIVED |
| `SRC-PRC-003` | `PROCEDURE` | `doc/StackForceDog/M1_outcome/M1-physical-session-checklist.md` | 架空测试前置安全检查与上电步骤规程 | `M1-G10`, `T03-安全联锁` | `E-experiment-架空测试时序延迟与安全停机日志` | PROCEDURE_DEFINED |
| `SRC-PRC-004` | `PROCEDURE` | `doc/四足机器人-origin/0整机操作说明/遥控器对频说明.docx` | 航模 PPM 接收机对频与通道微调规程 | `M1-T04` | `E-firmware-出厂遥控器与PPM协议说明` | PROCEDURE_DEFINED |
| `SRC-LOG-001` | `RUNTIME_LOG` | `doc/StackForceDog/artifacts/m1_unified_serial.log` | 架空 Session 1 串口原始输出全量记录（启动/IMU/执行器响应） | `M1-T03`, `T02-实验日志` | `E-experiment-架空测试时序延迟与安全停机日志` | RUNTIME_OBSERVED |
| `SRC-LOG-002` | `RUNTIME_LOG` | `doc/StackForceDog/artifacts/m1_unified_serial_completion.log` | 架空 Session 2 串口全量记录（含 ch7 回中失败与超时日志） | `M1-G10`, `M1-T07` | `E-experiment-架空测试时序延迟与安全停机日志` | RUNTIME_OBSERVED（记录 ch7 故障） |
| `SRC-LOG-003` | `RUNTIME_LOG` | `sf_quad/logs/debug/C6_30_four_inner_chains_validation_20260912_234915.log` | 四腿内链对称反射构建过程执行日志 | `C6-registration-history` | `E-simulation-闭链机器人规范树资产说明` | RUNTIME_OBSERVED |
| `SRC-EXP-001` | `PHYSICAL_MEASUREMENT` | `doc/StackForceDog/artifacts/timing_latency.csv` | 实机 IMU 采样周期（175.3 Hz）与控制响应延迟测量数据 | `M1-G06`, `M1-G07` | `E-experiment-架空测试时序延迟与安全停机日志` | MEASURED（实测统计真值） |
| `SRC-EXP-002` | `PHYSICAL_MEASUREMENT` | `doc/StackForceDog/artifacts/actuator_registration.csv` | 实机 8 舵机 + 4 轮电机物理通道、极性与响应定性记录表 | `M1-G03`, `M1-T02` | `E-experiment-架空测试时序延迟与安全停机日志` | MEASURED（实测定性结果） |
| `SRC-EXP-003` | `PHYSICAL_MEASUREMENT` | `doc/StackForceDog/artifacts/safety_validation.md` | 实机停机/超时测试审计记录（记录 ch7 上抬与断电事件） | `M1-G10`, `T03-安全联锁` | `E-experiment-架空测试时序延迟与安全停机日志` | OBSERVED_EVENT |
| `SRC-REP-001` | `GENERATED_REPORT` | `sf_quad/.../validation/simulation_report.json` | 2400 步 CPU 悬空物理测试结果（0.0595 mm 漂移，PASS） | `M2-Simulation-Asset` | `E-validation-悬空重力仿真烟囱与负对照测试报告` | EXECUTED_VERIFIED |
| `SRC-REP-002` | `GENERATED_REPORT` | `sf_quad/.../validation/negative_control_report.json` | 负对照测试报告（禁用闭环导致 129 mm 漂移并在 480 步崩溃） | `M2-Simulation-Asset` | `E-validation-悬空重力仿真烟囱与负对照测试报告` | EXECUTED_VERIFIED |
| `SRC-REP-003` | `GENERATED_REPORT` | `sf_quad/.../ref_b_real_fr/four_inner_chains_validation.json` | 四腿几何对称性与闭环残差报告（对称误差 <= 6.14e-6 mm） | `M2-G03` | `E-mechanical-双支链五杆机构与几何基线` | EXECUTED_VERIFIED |
| `SRC-EVI-001` | `EXISTING_EVIDENCE` | `page/stackforce/evidence/evidence-registry.md` | 便携式证据总注册表 | `Roadmap与里程碑`, `_META` | `E-registry-便携式证据总索引` | VALID_INDEX |
| `SRC-EVI-002` | `EXISTING_EVIDENCE` | `page/stackforce/evidence/mechanical-model.md` | 双支链五杆机械拓扑与几何约定专题 | `M2-T02`, `M2-T03` | `E-mechanical-双支链五杆机构与几何基线` | EXISTING_VALID |
| `SRC-EVI-003` | `EXISTING_EVIDENCE` | `page/stackforce/evidence/geometry-baseline.md` | 早期几何基线度量与孔距记录 | `M1-G08` | `E-mechanical-双支链五杆机构与几何基线` | EXISTING_LEGACY |
| `SRC-EVI-004` | `EXISTING_EVIDENCE` | `page/stackforce/evidence/source-inventory.md` | 早期来源清单快照 | `M2-G01` | 本文档接管 | SUPERSEDED |
| `SRC-EVI-005` | `EXISTING_EVIDENCE` | `_meta/claims.yaml` | 结构化声明元数据配置 | `_META` | `E-registry-便携式证据总索引` | VALID_CONFIG |
| `SRC-EVI-006` | `EXISTING_EVIDENCE` | `_meta/evidence.yaml` | 结构化证据元数据配置 | `_META` | `E-registry-便携式证据总索引` | VALID_CONFIG |

---

## 3. 盘点总结与审计发现

1. **硬件原理图与接线文档完备性**：
   - 官方原厂 PDF 原理图覆盖了主控板、舵机驱动板、无刷轮机驱动板和 CAN 总线；
   - 这些原理图提供了芯片选型（ESP32-S3、PCA9685、MPU6050/ICM、DRV8313）的规格（`MANUFACTURER_SPEC`），但不能直接证明装配后的实机参数与动力学校准结果。
2. **源码与仿真资产完备性**：
   - 固件源码 `SRC-FW-001` 与 `SRC-FW-002` 完整揭示了下位机通信协议与控制时序，但代码里的 `setAngle()` 不等同于实机角度到达（`COMMAND != FEEDBACK`）；
   - 仿真资产生成与恢复链条具备全自动化脚本与测试报告（`SRC-PY-001`~`SRC-PY-004`），具备完备的静态与物理烟囱测试真凭实据。
3. **实验数据真实性**：
   - 实机架空 Session 产生了两份不可篡改的串口日志（`SRC-LOG-001`, `SRC-LOG-002`），客观记录了包括 ch7 物理回中失败在内的全部事实。

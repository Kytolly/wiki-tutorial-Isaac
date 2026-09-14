# Evidence Pilot 重构评估报告（Evidence Pilot Report）

> 本文档属于：Wiki Evidence 重构工程（Phase 1 评估报告）  
> 状态：COMPLETE（首批 4 个重点代表性 Pilot 已落地，规范已闭环）  
> 原则：**A PATH IS NOT EVIDENCE.** 本报告对首批试点 Evidence Document 的转换效果、语义强度、边界处理及未决项进行系统性评估，为后续全库批量迁移提供决策依据。

---

## 1. 试点证据与技术源映射总览（Source → Evidence Mapping）

本次试点严格按照任务要求，从 4 类截然不同的原始技术源中各抽取典型代表，转换为标准的工程证据文档：

| Pilot ID | 标题 | 技术源类型 | 覆盖原始技术源 | 产生工程 Parts | 状态评定 |
|---|---|---|---|---|---|
| **E-HW-001** | StackForce 主控板与舵机/IMU/CAN电气原理图规范 | `MANUFACTURER_SPEC` (PDF图纸) | `StackForce主控板.pdf`<br>`多路舵机+IMU模块.pdf`<br>`CAN.pdf`<br>`2接线文档.pdf` | `P01`: ESP32-S3 主控与供电电源域<br>`P02`: PCA9685 8路舵机驱动总线<br>`P03`: 板载 IMU 传感器选型与I2C接线<br>`P04`: 板间 TWAI/CAN 通信与隔离 | `VALID` |
| **E-SIM-001** | 闭链机器人规范树状 Loop-Cut 数字仿真资产规范 | `SOURCE_PYTHON` / `CONFIG` (仿真资产) | `stackforce_quadrupedal_wheeled_robot.urdf`<br>`closure_frames.json`<br>`build_asset.py`<br>`recover_closed_loops.py`<br>`validate_asset.py` | `P01`: 29 links/28 joints 严格单父树<br>`P02`: 运动学断开点选定在 W2<br>`P03`: 轴向偏置与共线残差不变量<br>`P04`: PhysX 闭环副位姿独立反算<br>`P05`: Link-Local 二进制网格与面绕向 | `VALID` |
| **E-FW-001** | 执行器控制固件协议、时序架构与停机合同 | `SOURCE_CPP` (嵌入式固件) | `SF_serveo_control/src/main.cpp`<br>`device2/src/main.cpp`<br>`SF_Servo.cpp`<br>`SF_CAN.cpp` | `P01`: 舵机开环角度协议与 Degree API<br>`P02`: 轮电机 TWAI/CAN 帧压缩解压<br>`P03`: 主循环控制时序与前后台轮询<br>`P04`: 超时判定与固件主动停机实现 | `VALID` |
| **E-EXP-001** | 实机架空实验时序、控制响应与安全停机测试记录 | `RUNTIME_LOG` / `PHYSICAL_MEASUREMENT` (实机实验) | `timing_latency.csv`<br>`actuator_registration.csv`<br>`safety_validation.md`<br>`m1_unified_serial.log`<br>`m1_unified_serial_completion.log` | `P01`: 实机 IMU 采样周期与抖动真值<br>`P02`: 控制指令延迟与自动停机窗口<br>`P03`: ch7 回中失败事件与断电阻断<br>`P04`: 单执行器激励隔离与极性定性 | `VALID` |

---

## 2. Part 设计与颗粒度评估（Part Design Analysis）

1. **原子化工程事实（Atomic Engineering Statement）**：
   - 每一个 Part 仅陈述一个能够被其 Source 直接证实的技术事实，避免多个维度的推论混杂在同一小节中；
   - 示例：在 `E-SIM-001` 中，将“URDF 29 links / 28 joints 单父树”（P01）与“W2 处切断”（P02）以及“轴向偏置 -44.950 mm”（P03）完全拆分为不同 Part，使得上层 Gate 引用时可以针对性挂载，无需通篇引用。
2. **显式 HTML 锚点（Stable Anchors）**：
   - 每个 Part 均配备形如 `<a id="p01-mcu-power-domain"></a>` 的稳定锚点；
   - 未来无论文档标题或排版如何微调，锚点链接格式保持永固，支持形如 `[[E-HW-001#p02-pca9685-servo-topology]]` 的细粒度机器与人眼追踪。

---

## 3. 语义边界决策（Semantic Boundary Decisions）

在 4 个 Pilot 的编写过程中，严格落实了禁止语义越级（Semantic Elevation）的准则：

| 技术源层面的表达 | 过去容易出现的错误宣称 | 本次 Pilot 采取的严格语义限定 | 涉及 Pilot/Part |
|---|---|---|---|
| 原理图画出 MPU6050 芯片与 I2C 引脚 | “实机 IMU 采样精度高、噪声低” | 标记为 `[SPECIFIED]`，仅代表硬件选型和接线存在；物理性能待实测。 | `E-HW-001#p03` |
| Python 脚本中配置了关节和闭环恢复代码 | “闭链动力学仿真已验证成功” | 标记为 `[IMPLEMENTED]`，仅证明重构代码存在并生成了 USD 属性；动力学有效性必须等待物理运行测试。 | `E-SIM-001#p04` |
| 固件代码中有 `setAngle(num, 90)` | “关节当前角度已到达 90 度” | 标记为 `[IMPLEMENTED]`，明确阐明这仅是开环 PWM 占空比写入（`COMMAND != FEEDBACK`），无位置传感器回读。 | `E-FW-001#p01` |
| 固件代码在超时后调用了主动停机函数 | “系统已安全停机，无失控风险” | 标记为 `[IMPLEMENTED]`，严格与物理执行解耦；并在 `E-EXP-001` 中用实测事实揭示 ch7 虽然收到 STOP 但物理上持续上抬。 | `E-FW-001#p04`<br>`E-EXP-001#p03` |
| 架空测试中测量到 501.5 ms 固件停机时间戳 | “整机端到端物理响应延迟为 501.5 ms” | 标记为 `[MEASURED]`，但明确标注 Limitations：“仅测定固件触发停机时间戳，实际机构减速停转耗时未测”。 | `E-EXP-001#p02` |

---

## 4. 历史记录保护与未决项处理（Historical Integrity & Unresolved Ambiguities）

1. **客观保留历史故障，严禁粉饰太平**：
   - 在 `E-EXP-001#p03` 中，忠实完整地记录了 2026-09-10 实机架空 Session 2 中发生的 **第 7 通道舵机（ch7）物理回中失败并持续上抬事件**；
   - 明确指出固件产生的 `STOP,command_timeout` 信号无法挽救硬件失控，实测结果判定为 `FAILED_PHYSICAL_RETURN`；
   - 该失败记录不仅不被掩盖，反而作为支撑“实机执行器母线必须保持断电隔离，M1 必须判定为 BLOCKED”这一关键安全联锁的核心证据。
2. **规范命名与未决映射（Unresolved Physical Aliases）**：
   - 统一规范名称标准：`FR_Outer_Servo`, `FR_Inner_Servo`, `FR_Wheel` 等；
   - 但在 `E-EXP-001#p04` 与 `E-HW-001#p02` 中，严格声明：**当前技术源中，PCA9685 的 PWM0~7 物理插头与机器人的左右/内外腿对应关系尚未完全通过非破坏性实测证实**；
   - 坚决不做凭空猜测，将通道 8 与轮电机的左右归属如实标记为 `UNRESOLVED`，保留原始别名。

---

## 5. 信息保留与刻意过滤（Information Pruning & Retention）

1. **保留的信息（Preserved）**：
   - 芯片选型（ESP32-S3, PCA9685, MPU6050, SN65HVD230DR, DRV8313）；
   - 电气参数（50 Hz PWM, 120 $\Omega$ 终端匹配电阻, 16-bit 定点压缩公式）；
   - 空间几何参数（-44.950 mm 轴向装配偏置, $< 1.83 \times 10^{-17}\text{ m}$ 径向残差）；
   - 实测统计数值（175.3 Hz IMU 刷新率, 5.704 ms 周期, 0.790 ms 抖动, 501.5–502.5 ms 自动停机响应）；
   - 原始文件校验哈希（SHA256 串）。
2. **刻意不过度外推的信息（Intentionally Not Promoted）**：
   - 滤除了早期调试阶段未经实物标定的主观猜测（如“机器狗自重约 3 kg”、“整机控制带宽 500 Hz”等非证据声明）；
   - 滤除了将纯配置默认值（如 USD 中 importer 自动生成的 `stiffness=0, damping=0`）误称为“动力学标定完成”的虚假描述；
   - 将实机操作说明中的“如何操作遥控器”剥离为 `PROCEDURE`，不混入 `EVIDENCE`。

---

## 6. 证据架构对后续批量重构的指引（Guidelines for Full Migration）

经过 4 个 Pilot 的实战检验，验证了当前 Evidence Architecture 具有高度的严谨性与可行性。后续进入第二阶段批量重构时，建议遵循以下标准模式：

1. **按工程领域持续补充 Evidence Documents**：
   - 补充 `E-HW-002`（无刷电机驱动与编码器电气规范）；
   - 补充 `E-VAL-001`（静态资产自动化校验脚本证据）；
   - 补充 `E-VAL-002`（2400 步 CPU 悬空重力烟囱测试与负对照崩溃证据）；
   - 补充 `E-MECH-001`（完整五杆机构几何真值）。
2. **上层 Gate 的纯语义引用（Gate Traceability）**：
   - 在 Gate 页面中，严禁出现零碎的本地文件绝对路径；
   - Gate 的判定依据统一声明为 Evidence Part 引用，例如：
     `判定依据：[[E-EXP-001#p01-imu-timing-jitter]] (实测 175.3 Hz)`
     `安全阻断：[[E-EXP-001#p03-ch7-failure-event]] (ch7 回中失败，母线断电)`
     `模型资产：[[E-SIM-001#p01-strict-tree-topology]] (29 links / 28 joints 规范单父树)`。

---

## 7. 停机检查与状态声明（Stop Condition Confirmation）

- [x] **`docs/refactor/source-inventory.md`**：完成全量 48 项技术源分类盘点；
- [x] **`docs/refactor/evidence-plan.md`**：完成全局工程主题解耦与迁移矩阵规划；
- [x] **`docs/templates/evidence-template.md`**：完成五分段标准 Evidence 模板构建；
- [x] **4 个代表性 Evidence Pilot**：
  - `docs/evidence/E-HW-001-mainboard-schematics.md` (PDF / Manufacturer Spec)
  - `docs/evidence/E-SIM-001-canonical-loop-cut-asset.md` (Python / Simulation Spec)
  - `docs/evidence/E-FW-001-actuator-control-firmware.md` (C++ / Firmware Implementation)
  - `docs/evidence/E-EXP-001-lifted-timing-safety-session.md` (Runtime Log / Physical Experiment)
- [x] **`docs/refactor/evidence-pilot-report.md`**：完成全面评估报告；
- [x] **未修改** Gate 页面与状态（`page/stackforce/gate/` 未动）；
- [x] **未修改** Milestone 页面与状态（`page/stackforce/milestone/` 未动）；
- [x] **未修改** Roadmap 进度与状态（`Roadmap与里程碑.md` 与 `Home.md` 未动）；
- [x] **未开始** M3 参数拟合。

本阶段工作已全部按约定交付完毕，执行完全停机，静候人工架构审核。

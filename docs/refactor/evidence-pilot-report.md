# Evidence Pilot 重构评估报告（Evidence Pilot Report）

> 本文档属于：Wiki Evidence 重构工程（Phase 1 评估报告）  
> 状态：COMPLETE（首批 4 个重点代表性 Pilot 已落地，规范已闭环）  
> 原则：**A PATH IS NOT EVIDENCE.** 本报告对首批试点 Evidence Document 的转换效果、语义强度、边界处理及未决项进行系统性评估，为后续全库批量迁移提供决策依据。

---

## 1. 试点证据与技术源映射总览（Source → Evidence Mapping）

本次试点严格按照命名规则 `E-{field English name}-{文档中文名描述}`，从 4 类截然不同的原始技术源中各抽取典型代表，转换为标准的工程证据文档，并在每个 Part 中引入**忠实复刻原始技术物料（Raw Source Faithful Reproduction）**小节与原始图片引用能力：

| Pilot ID | 标题 | 技术源类型 | 覆盖原始技术源 | 产生工程 Parts | 状态评定 |
|---|---|---|---|---|---|
| **E-hardware-主控板与舵机IMU电气原理图** | StackForce 主控板与舵机/IMU/CAN电气原理图规范 | `MANUFACTURER_SPEC` (PDF图纸) | `StackForce主控板.pdf`<br>`多路舵机+IMU模块.pdf`<br>`CAN.pdf`<br>`2接线文档.pdf` | `P01`: ESP32-S3 主控与供电电源域<br>`P02`: PCA9685 8路舵机驱动总线<br>`P03`: 板载 IMU 传感器选型与I2C接线<br>`P04`: 板间 TWAI/CAN 通信与隔离 | `VALID` |
| **E-simulation-闭链机器人规范树资产说明** | 闭链机器人规范树状 Loop-Cut 数字仿真资产说明 | `SOURCE_PYTHON` / `CONFIG` (仿真资产) | `stackforce_quadrupedal_wheeled_robot.urdf`<br>`closure_frames.json`<br>`build_asset.py`<br>`recover_closed_loops.py`<br>`validate_asset.py` | `P01`: 29 links/28 joints 严格单父树<br>`P02`: 运动学断开点选定在 W2<br>`P03`: 轴向偏置与共线残差不变量<br>`P04`: PhysX 闭环副位姿独立反算<br>`P05`: Link-Local 二进制网格与面绕向 | `VALID` |
| **E-firmware-舵机与CAN通信控制固件** | 舵机与CAN通信控制固件协议、时序架构与停机合同 | `SOURCE_CPP` (嵌入式固件) | `SF_serveo_control/src/main.cpp`<br>`device2/src/main.cpp`<br>`SF_Servo.cpp`<br>`SF_CAN.cpp` | `P01`: 舵机开环角度协议与 Degree API<br>`P02`: 轮电机 TWAI/CAN 帧压缩解压<br>`P03`: 主循环控制时序与前后台轮询<br>`P04`: 超时判定与固件主动停机实现 | `VALID` |
| **E-experiment-架空测试时序延迟与安全停机日志** | 实机架空实验时序、控制响应与安全停机测试记录 | `RUNTIME_LOG` / `PHYSICAL_MEASUREMENT` (实机实验) | `timing_latency.csv`<br>`actuator_registration.csv`<br>`safety_validation.md`<br>`m1_unified_serial.log`<br>`m1_unified_serial_completion.log` | `P01`: 实机 IMU 采样周期与抖动真值<br>`P02`: 控制指令延迟与自动停机窗口<br>`P03`: ch7 回中失败事件与断电阻断<br>`P04`: 单执行器激励隔离与极性定性 | `VALID` |

---

## 2. 原始技术物料忠实复刻机制（Raw Source Faithful Reproduction）

为了解决“从原始文件到工程事实之间的证据失真与主观推测风险”，本次 Pilot 落地了强约束的 **Raw Source Faithful Reproduction** 机制：
1. **原汁原味摘录（Verbatim Reproduction）**：
   - 源码证据：逐行摘录原版 C++ / Python 函数实现，完整保留变量名、边界条件判定与数值常数；
   - 配置文件：逐字记录 `closure_frames.json` 真实 JSON 键值对，包含浮点残差阶数；
   - 实机实验：逐行呈现 `timing_latency.csv` 测量记录、`safety_validation.md` 检查表行项与串口异常现场日志流；
   - 硬件图纸：字面复刻引脚网络名、外设总线名称与上下拉配置。
2. **支持原始图片与截图嵌入（Image / Screenshot Guidelines）**：
   - 在模板与规范中明确允许并鼓励直接嵌入原理图切片、实物接线照片、示波器波形图与仿真场景截图；
   - 统一存放规范路径，使用带明确技术说明的 Markdown 图片语法。
3. **分权隔离设计（Strict Separation of Concerns）**：
   - `Raw Source Faithful Reproduction`：只负责**如实记录物料本身**，严禁插入主观论述；
   - `Engineering Statement`：提炼**受直接支持的原子工程事实**并加注限定词；
   - `Source Observation`：提炼**关键事实标号**；
   - `Engineering Interpretation`：阐述**对全系统的工程影响**；
   - `Limitations`：划定**本证据绝对不能证明的边界禁区**。

---

## 3. Part 设计与颗粒度评估（Part Design Analysis）

1. **原子化工程事实（Atomic Engineering Statement）**：
   - 每一个 Part 仅陈述一个能够被其 Source 直接证实的技术事实，避免多个维度的推论混杂在同一小节中；
   - 示例：在 `E-simulation-闭链机器人规范树资产说明` 中，将“URDF 29 links / 28 joints 单父树”（P01）与“W2 处切断”（P02）以及“轴向偏置 -44.950 mm”（P03）完全拆分为不同 Part，使得上层 Gate 引用时可以针对性挂载，无需通篇引用。
2. **显式 HTML 锚点（Stable Anchors）**：
   - 每个 Part 均配备形如 `<a id="p01-mcu-power-domain"></a>` 的稳定锚点；
   - 未来无论文档标题或排版如何微调，锚点链接格式保持永固，支持形如 `[[E-hardware-主控板与舵机IMU电气原理图#p02-pca9685-servo-topology]]` 的细粒度机器与人眼追踪。

---

## 4. 语义边界决策（Semantic Boundary Decisions）

在 4 个 Pilot 的编写过程中，严格落实了禁止语义越级（Semantic Elevation）的准则：

| 技术源层面的表达 | 过去容易出现的错误宣称 | 本次 Pilot 采取的严格语义限定 | 涉及 Pilot/Part |
|---|---|---|---|
| 原理图画出 MPU6050 芯片与 I2C 引脚 | “实机 IMU 采样精度高、噪声低” | 标记为 `[SPECIFIED]`，仅代表硬件选型和接线存在；物理性能待实测。 | `E-hardware-主控板与舵机IMU电气原理图#p03` |
| Python 脚本中配置了关节和闭环恢复代码 | “闭链动力学仿真已验证成功” | 标记为 `[IMPLEMENTED]`，仅证明重构代码存在并生成了 USD 属性；动力学有效性必须等待物理运行测试。 | `E-simulation-闭链机器人规范树资产说明#p04` |
| 固件代码中有 `setAngle(num, 90)` | “关节当前角度已到达 90 度” | 标记为 `[IMPLEMENTED]`，明确阐明这仅是开环 PWM 占空比写入（`COMMAND != FEEDBACK`），无位置传感器回读。 | `E-firmware-舵机与CAN通信控制固件#p01` |
| 固件代码在超时后调用了主动停机函数 | “系统已安全停机，无失控风险” | 标记为 `[IMPLEMENTED]`，严格与物理执行解耦；并在实机日志中用实测事实揭示 ch7 虽然收到 STOP 但物理上持续上抬。 | `E-firmware-舵机与CAN通信控制固件#p04`<br>`E-experiment-架空测试时序延迟与安全停机日志#p03` |
| 架空测试中测量到 501.5 ms 固件停机时间戳 | “整机端到端物理响应延迟为 501.5 ms” | 标记为 `[MEASURED]`，但明确标注 Limitations：“仅测定固件触发停机时间戳，实际机构减速停转耗时未测”。 | `E-experiment-架空测试时序延迟与安全停机日志#p02` |

---

## 5. 历史记录保护与未决项处理（Historical Integrity & Unresolved Ambiguities）

1. **客观保留历史故障，严禁粉饰太平**：
   - 在 `E-experiment-架空测试时序延迟与安全停机日志#p03` 中，忠实完整地记录了 2026-09-10 实机架空 Session 2 中发生的 **第 7 通道舵机（ch7）物理回中失败并持续上抬事件**；
   - 明确指出固件产生的 `STOP,command_timeout` 信号无法挽救硬件失控，实测结果判定为 `FAILED_PHYSICAL_RETURN`；
   - 该失败记录不仅不被掩盖，反而作为支撑“实机执行器母线必须保持断电隔离，M1 必须判定为 BLOCKED”这一关键安全联锁的核心证据。
2. **规范命名与未决映射（Unresolved Physical Aliases）**：
   - 统一规范名称标准：`FR_Outer_Servo`, `FR_Inner_Servo`, `FR_Wheel` 等；
   - 但在 `E-experiment-架空测试时序延迟与安全停机日志#p04` 与 `E-hardware-主控板与舵机IMU电气原理图#p02` 中，严格声明：**当前技术源中，PCA9685 的 PWM0~7 物理插头与机器人的左右/内外腿对应关系尚未完全通过非破坏性实测证实**；
   - 坚决不做凭空猜测，将通道 8 与轮电机的左右归属如实标记为 `UNRESOLVED`，保留原始别名。

---

## 6. 信息保留与刻意过滤（Information Pruning & Retention）

1. **保留的信息（Preserved）**：
   - 芯片选型（ESP32-S3, PCA9685, MPU6050, SN65HVD230DR, DRV8313）；
   - 电气参数（50 Hz PWM, 120 Ω 终端匹配电阻, 16-bit 定点压缩公式）；
   - 空间几何参数（-44.950 mm 轴向装配偏置, < 1.83e-17 m 径向残差）；
   - 实测统计数值（175.3 Hz IMU 刷新率, 5.704 ms 周期, 0.790 ms 抖动, 501.5–502.5 ms 自动停机响应）；
   - 原始文件校验哈希（SHA256 串）。
2. **刻意不过度外推的信息（Intentionally Not Promoted）**：
   - 滤除了早期调试阶段未经实物标定的主观猜测（如“机器狗自重约 3 kg”、“整机控制带宽 500 Hz”等非证据声明）；
   - 滤除了将纯配置默认值（如 USD 中 importer 自动生成的 `stiffness=0, damping=0`）误称为“动力学标定完成”的虚假描述；
   - 将实机操作说明中的“如何操作遥控器”剥离为 `PROCEDURE`，不混入 `EVIDENCE`。

---

## 7. 停机检查与状态声明（Stop Condition Confirmation）

- [x] **`docs/refactor/source-inventory.md`**：完成全量 48 项技术源分类盘点与新规范 ID 映射；
- [x] **`docs/refactor/evidence-plan.md`**：完成全局工程主题解耦与新规范 ID 迁移矩阵规划；
- [x] **`docs/templates/evidence-template.md`**：完成双层命名 `E-{field English name}-{文档中文名描述}`、图片引用规范与原始证据忠实复刻（Raw Source Faithful Reproduction）模板构建；
- [x] **4 个代表性 Evidence Pilot**：
  - `docs/evidence/E-hardware-主控板与舵机IMU电气原理图.md` (PDF / Manufacturer Spec)
  - `docs/evidence/E-simulation-闭链机器人规范树资产说明.md` (Python / Simulation Spec)
  - `docs/evidence/E-firmware-舵机与CAN通信控制固件.md` (C++ / Firmware Implementation)
  - `docs/evidence/E-experiment-架空测试时序延迟与安全停机日志.md` (Runtime Log / Physical Experiment)
- [x] **`docs/refactor/evidence-pilot-report.md`**：完成全面评估报告；
- [x] **未修改** Gate 页面与状态（`page/stackforce/gate/` 未动）；
- [x] **未修改** Milestone 页面与状态（`page/stackforce/milestone/` 未动）；
- [x] **未修改** Roadmap 进度与状态（`Roadmap与里程碑.md` 与 `Home.md` 未动）；
- [x] **未开始** M3 参数拟合；
- [x] **严格等待用户指令**：遵照用户“Pilot Execution具体等我指示我们开始。这一轮我确认后可开始 pivot evidence”要求，停机静候用户确认。

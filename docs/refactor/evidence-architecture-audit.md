# Evidence 架构与认识论合规性全面审计报告
# Evidence Architecture & Epistemic Compliance Audit Report

> **审计依据**：[`.agents/skills/skill-wiki-design`](../../.agents/skills/skill-wiki-design/SKILL.md)  
> **审计日期**：2026-09-14  
> **审计范围**：`docs/evidence/`, `page/stackforce/evidence/`, `_meta/evidence.yaml`, `doc/` 原始技术源及历史 Pilot 产物  
> **核心原则**：**A PATH IS NOT EVIDENCE.** 事实与认识论强度完全绑定，严禁跨角色拼凑闭环与语义越级。

---

## 1. 审计统计概览（Executive Summary）

| 审计维度 | 审计发现数量 | 状态判定 | 核心风险与说明 |
|---|---|---|---|
| **全量技术源总数 (Source Inventory)** | 48 项 | 已全量建档 | 分布在 PDF, DOCX, CPP, Python, JSON, CSV, LOG 7 类物料中 |
| **受审证据条目 (Current Evidence Items)** | 14 条 | 待重构迁移 | 包括 `docs/evidence/` 1 条、历史 Pilot 4 条、`_meta/evidence.yaml` 9 条 |
| **混合证据违规 (Mixed-Evidence Violations)** | **4 起** | **高危违规** | DOC+CODE 混写、CONFIG+RUNTIME 混写、SPEC+PHYSICAL 混写 |
| **重复证据定义 (Duplicate Evidence)** | **2 起** | 待合并归一 | 同一 URDF/JSON 在不同命名空间被重复碎片化引用 |
| **语义越级宣称 (Semantic Overclaims)** | **5 起** | 需严格降级 | COMMAND $\to$ FEEDBACK、CONFIGURED $\to$ VALIDATED、SPEC $\to$ MEASURED |
| **出处缺失/弱出处 (Missing Provenance)** | **3 起** | 需补充校验 | 缺少 SHA256 哈希或便携相对路径指向绝对本地路径 |
| **建议拆分证据项 (Proposed Splits)** | **4 个** | 规划就绪 | 拆解为纯粹的单一认识论角色 Evidence |
| **建议新增 Topic 专题 (Proposed Topics)** | **6 个** | 规划就绪 | 承接跨认识论角色的多源交叉验证与冲突分析 |

---

## 2. 混合证据违规深度剖析（Mixed-Evidence Violations）

根据 `skill-wiki-design` 的认识论合并规则：**禁止将不同认识论角色的技术源合并到同一个 Evidence 中。** 审计发现以下典型违规：

### 违规 1：`E-control-遥控器对频与接收机接线说明`（当前落地 Evidence）
- **涉及源**：
  - `SRC-PRC-004`：`遥控器对频说明.docx`（原厂操作指南，认识论角色：`DOC/SPEC`）
  - `SRC-FW-001`：`SF_serveo_control/src/main.cpp`（固件源码，认识论角色：`IMPLEMENTATION`）
- **违规性质**：**DOC + CODE 混合**。
- **问题分析**：
  文档为了“向读者证明引脚与代码闭环”，在 Part P01 中直接将 DOCX 截图与 `main.cpp` 的 `#define PPM_PIN 40` 写入同一段落，在 P03 中将遥控器实物拨杆与固件内部 `filteredPPMValues3` 混写。这使得该 Evidence 既包含了原厂规定的名义事实（`[SPECIFIED]`），又包含了本地代码的实现事实（`[IMPLEMENTED]`）。
- **重构纠正方案**：
  - 拆分为 `E-DOC-001`（原厂遥控器操作与对频接线指南）；
  - 拆分为 `E-FW-001`（ESP32 接收机 PPM 中断解码与通道解算固件）；
  - 将引脚与拨杆的对应关系移至 `T-CONTROL-001` 横向专题进行交叉比对。

---

### 违规 2：`E-simulation-闭链机器人规范树资产说明`（历史 Pilot 2）
- **涉及源**：
  - `SRC-CFG-001` / `SRC-CFG-002`：`closure_frames.json` + `urdf`（认识论角色：`CONFIG`）
  - `SRC-PY-002`：`recover_closed_loops.py`（认识论角色：`IMPLEMENTATION`）
  - `SRC-PY-003`：`validate_asset.py`（自动化运行校验脚本，认识论角色：`RUNTIME / VALIDATED`）
- **违规性质**：**CONFIG + IMPLEMENTATION + RUNTIME 混合**。
- **问题分析**：
  在 P05 中，直接将 `validate_asset.py` 的执行终端输出日志作为 `[VALIDATED]` 事实与静态 URDF 模型树合并在同一文档中。模型定义（静止资产）与测试执行（动态测试）属于不同生命周期。
- **重构纠正方案**：
  - 静态资产（URDF + JSON + recover 代码）归入 `E-SIM-001`；
  - 静态资产自动化门禁检验输出独立归入 `E-VAL-001`（或 `E-TEST-001`）。

---

### 违规 3：`E-hardware-主控板与舵机IMU电气原理图`（历史 Pilot 1）
- **涉及源**：
  - 4 份 PDF 原理图（`DOC/SPEC`）
  - 论述中交叉混入了固件宏定义与通道别名猜测（`IMPLEMENTATION`）
- **违规性质**：**SPEC + IMPLEMENTATION 混合倾向**。
- **重构纠正方案**：
  - 剥离所有固件别名推论，纯粹记录原理图芯片引脚与电气网络（`[SPECIFIED]`）。

---

### 违规 4：`E-experiment-架空测试时序延迟与安全停机日志`（历史 Pilot 4）
- **涉及源**：
  - `timing_latency.csv`（测量数值，`MEASURED`）
  - `actuator_registration.csv`（动作定性，`MEASURED`）
  - `safety_validation.md`（规程检查表，`PROCEDURE`）
  - `m1_unified_serial_completion.log`（异常事件流，`OBSERVED_EVENT`）
- **违规性质**：**MEASURED + PROCEDURE + OBSERVED_EVENT 粗粒度堆叠**。
- **重构纠正方案**：
  - 保持底层原始物料不动，拆分为专门的时序测量证据（`E-TEST-xxx`）与安全停机故障事件证据（`E-TEST-xxx` 或 `E-CAL-xxx`）。

---

## 3. 重复证据与命名空间违规（Duplicate & Namespace Violations）

1. **Gate 耦合命名违规**：
   - `_meta/evidence.yaml` 中存在 `E-M1-OUTCOME-20260910` 与 `E-M1-PHYSICAL-20260910`；
   - **违规原因**：命名中直接硬编码了 `M1`（Milestone 1），破坏了解耦性，导致 M6 阶段在引用相同物理日志时发生语义混乱。
2. **重复模型证据定义**：
   - `evidence-registry.md` 中同时定义了 `E-MECH-002`（关节划分）与 `E-ASSET-001`（单父树 URDF），二者指向完全相同的 `stackforce_quadrupedal_wheeled_robot.urdf`，存在事实重叠与双重维护。
3. **Registry 作为伪 SSOT**：
   - `page/stackforce/evidence/evidence-registry.md` 存放了大量事实正文，而 `docs/evidence/` 目录中却没有对应的独立实体文件，导致 Gate 引用无法跳转至原子文件。

---

## 4. 语义越级宣称清单（Semantic Overclaims Audit）

| 违规定位 | 原始技术源真实表达 | 过去 Wiki/文档中出现的越级宣称 | 真实认识论界限 | 纠正动作 |
|---|---|---|---|---|
| **舵机控制 API** | `SF_Servo.cpp` 中执行 `setPWM(num, 0, off)` | “舵机当前关节角度已到达 90 度” | **`COMMAND != FEEDBACK`**。无角度传感器回读，仅代表占空比下发。 | 降级为 `[IMPLEMENTED]`，在 Limitations 中明确无闭环反馈。 |
| **USD 物理关节属性** | USD 文件中由 Importer 自动生成 `stiffness=0, damping=0` | “四足闭链动力学模型属性配置完成” | **`CONFIGURED != VALIDATED`**。仅为默认零初值，电机特性未标定。 | 降级为 `[CONFIGURED]`，标记 `rl_ready=false`。 |
| **MPU6050 传感器** | 原理图画出 MPU6050 芯片与 I2C 总线 | “板载 IMU 具备低噪声、高精度姿态输出” | **`SPECIFIED != MEASURED`**。原理图只能证明接线存在，噪声必须实测。 | 降级为 `[SPECIFIED]`，物理表现指引至实测日志。 |
| **固件超时停机** | 代码判断超时后调用 `Serial.println("STOP")` 并写 PWM 0 | “系统具备完备的主动停机与故障隔离保护” | **`IMPLEMENTED != PHYSICAL EFFECT`**。代码发出停机不等于硬件执行（ch7 依然上抬）。 | 明确软件停机与硬件断电的隔离，记录 ch7 物理失控。 |
| **仿真脚本存在** | 磁盘存在 `build_asset.py` 与 `recover_closed_loops.py` | “PhysX 闭环仿真已验证通过” | **`PATH EXISTS != EXECUTED / VALIDATED`**。文件存在不等于运行稳定。 | 必须以 2400 步烟囱测试报告为 `[VALIDATED]` 证据。 |

---

## 5. 出处追溯弱项（Missing Provenance Audit）

1. **绝对路径污染**：
   `_meta/evidence.yaml` 中部分条目使用了 `/home/kytolly/Project/IsaacProject/...` 绝对路径，脱离特定机器后无法解析。必须全部规范化为便携式相对路径（`$PROJECT_ROOT/...` 或规范相对路径）。
2. **缺乏防篡改哈希**：
   实机实验的 CSV 文件（如 `timing_latency.csv`）未在 Header 中记录 SHA256 哈希，存在被编辑脚本静默修改的风险。

---

## 6. 审计结论与红线总结

1. **当前单一证据 `E-control-遥控器对频与接收机接线说明.md` 存在明确的 DOC+CODE 混写违规**，必须按照 Golden Example 拆解为 `E-DOC-001` 与 `E-FW-001`，并引入 `T-CONTROL-001` 专题；
2. **全库存在 4 大类混合证据违规与 5 项语义越级**，严禁在未规范化前让 Gate 引用这些混合产物；
3. **必须坚持 EVIDENCE FIRST**：在各纯粹 Evidence 独立入库前，不批量修改 Gate 验收状态。

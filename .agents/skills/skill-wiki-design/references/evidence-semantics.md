# Evidence Epistemics, Semantics & Merge Rules

> 本规范定义 Evidence 认识论分类（Epistemic Roles）、语义限定词（Qualifiers）、防语义越级红线与合并/拆分准则。

---

## 1. 认识论角色分类（Epistemic Roles）

严禁仅按“文件扩展名（.pdf / .py / .log）”机械分类。必须依据证据在认知链条中的**认识论角色（Epistemic Role）**进行严格定性：

| 认识论角色 | 核心回答的工程问题 | 典型原始技术源 | 默认限定词 |
|---|---|---|---|
| **DOC / SPEC** | “原厂规范、官方手册或设计图纸**规定**了什么？” | 芯片 Datasheet, 原理图 PDF, 原厂 DOCX 操作说明, 官方标准 | `[SPECIFIED]` |
| **IMPLEMENTATION** | “当前代码、驱动或配置文件在语法上**实际定义/实现了**什么？” | C/C++ 固件源码, Python 控制逻辑, URDF/USD 配置文件 | `[IMPLEMENTED]`<br>`[CONFIGURED]` |
| **RUNTIME** | “程序在计算节点真实执行时**实际发生了**什么输出？” | 串口输出流, 终端执行 Log, 仿真运行 Trace, 自动化测试退出码 | `[EXECUTED]`<br>`[OBSERVED]` |
| **PHYSICAL** | “物理真实机器的实物状态、实测数值与物理动作**究竟是**什么？” | 悬空架空实验日志, 游标卡尺/万用表测量表, 传感器采集真值, 实物故障断电记录 | `[MEASURED]`<br>`[OBSERVED_EVENT]` |
| **DERIVED / ANALYSIS** | “基于已有原始数据，通过确定性算法**计算推导**得到了什么？” | 离线姿态解算导出的欧拉角时序, 刚体动力学递推计算的惯量矩阵, 傅里叶频域分析谱 | `[DERIVED]`<br>`[ESTIMATED]` |

---

## 2. 标准语义限定词定义（Semantic Qualifiers）

在撰写每个 Part 的 `Engineering Statement` 时，必须且只能使用以下规范限定词作为首个标识：

1. `[SPECIFIED]`：图纸、芯片手册或设计规范所规定的名义参数（如“供电电压标称为 3.3V”）。
2. `[CONFIGURED]`：在配置文件或模型树中显式设定的静态参数（如“URDF 中配置 W2 沿 Y 轴偏置 -0.04495 m”）。
3. `[IMPLEMENTED]`：在软件或固件代码中由具体指令实现的处理逻辑（如“固件实现了 16 位大端整数 CAN 帧压缩”）。
4. `[EXECUTED]`：程序或脚本已在指定环境真实运行完毕（如“自动化门禁脚本已执行并返回退出码 0”）。
5. `[OBSERVED]`：在运行时日志或监控报文中字面捕获到的字符串或波形现象。
6. `[MEASURED]`：通过物理仪器（秒表、卡尺、示波器、传感器回传）在真实机器上实测取得的数据。
7. `[VALIDATED]`：通过封闭数学方程、单元测试断言或自动化回归测试证实的不变量。
8. `[ESTIMATED]`：通过统计模型、滤波算法或间接观测估算取得的状态估计量。
9. `[IDENTIFIED]`：通过参数辨识方法从实验数据拟合出的系统辨识参数。
10. `[DERIVED]`：严格基于公理化物理方程或运动学正逆解从已知数据解析推导出的几何/动力学量。

---

## 3. 严格禁止语义越级（Forbidden Semantic Elevations）

**这是工程证据审计的第一红线。严禁越过原始技术源所能证明的最大认识论强度：**

```text
[红线 1] SPECIFIED → MEASURED
  原理图画出 3.3V LDO 和 120Ω 终端电阻，绝不能陈述为“实测电压 3.3V，总线匹配电阻经实测为 120Ω”。
  （原理图仅能证明电路图纸设计如此，无法证明实物元器件未虚焊或阻值无温漂）。

[红线 2] CONFIGURED → VALIDATED
  在 URDF 中写了 limit velocity="10.0"，绝不能陈述为“关节最大物理转速经验证可达 10.0 rad/s”。
  （配置仅证明文件字面属性，物理极限必须由物理加载实验验证）。

[红线 3] IMPLEMENTED → EXECUTED / PHYSICAL RESPONSE
  固件源码中存在 setAngle(ch, 90) 和 STOP 指令，绝不能陈述为“物理关节已转至 90 度”或“系统已可靠物理停机”。
  （代码存在不等于物理动作到位；COMMAND != FEEDBACK）。

[红线 4] COMMAND → FEEDBACK
  下位机向舵机写入了 PWM 脉宽，绝不能宣称“传感器反馈关节角为某某度”（PCA9685 无角度回读）。

[红线 5] ESTIMATED → IDENTIFIED / MEASURED
  基于粗略质量推算出来的连杆转动惯量，绝不能陈述为“已精准测定转动惯量”。

[红线 6] PATH EXISTS → VALIDATED
  构建目录下存在 usd 文件或脚本，绝不能陈述为“物理仿真已通过验收”。
```

---

## 4. Evidence 合并与拆分规则（Coherent Source Family）

### 核心禁令：禁止拼凑闭环
**绝对严禁将不同认识论角色、不同出处上下文的技术源强行打包进同一个 Evidence 文档。**

- **禁止组合**：
  `原厂 DOCX 指南` + `固件 main.cpp` + `串口 log` + `实机悬空测量 csv` $\to$ **绝对禁止合并为一个 Evidence！**
  这种强行闭环的做法会破坏证据的出处可溯性，导致上层无法清晰定位究竟是图纸问题、实现问题还是硬件故障。

### 允许合并的唯一条件：同一技术源家族（Coherent Source Family）
当且仅当多个 Source 满足以下全部 3 个条件时，允许合并在同一个 Evidence 中：
1. **同属一个技术源家族（Same Source Family）**；
2. **具有相同的出处与上下文（Same Provenance Context）**；
3. **承担完全相同的认识论角色（Same Epistemic Role）**。

#### 正确合并示例
- `SF_Servo.h` 与 `SF_Servo.cpp`：
  同属 ESP32 舵机驱动库源码，同一作者/版本，同属 `IMPLEMENTATION` $\to$ 合并为 `E-FW-xxx`。
- `StackForce主控板.pdf` 与 `多路舵机+IMU模块.pdf`：
  同属 2024-07-05 出厂硬件电气图纸，同属原厂设计，同属 `DOC/SPEC` $\to$ 合并为 `E-HW-xxx`。

#### 强制拆分示例（Golden Rule）
- `遥控器对频说明.docx`（原厂操作指南，`DOC/SPEC`）与 `SF_serveo_control/src/main.cpp`（固件实现，`IMPLEMENTATION`）：
  **必须拆分为两个独立的 Evidence 文档**：
  1. `E-DOC-001`：遥控器与接收机原厂操作/接线说明（记录原厂规定的线序、电压与对频时序）；
  2. `E-FW-001`：ESP32 接收机 PPM 中断解码与控制映射固件实现（记录代码如何定义引脚、中断与通道数学映射）。
  **二者之间的符合度与差异分析，交由横向 Topic（如 `T-CONTROL-001`）负责比对，严禁在 E-DOC 中吞并 E-FW！**

---

## 5. Evidence 状态生命周期（Evidence Status Lifecycle）

Evidence 文档 Frontmatter 中的 `status` 字段用于描述证据自身的生命周期，**严禁使用 PASS/FAIL**：

- `DRAFT`：草稿状态，正在提取工程语义，技术源信息或 Part 划分尚未最终确定。
- `VALID`：经审计确认为真实、客观、来源无误的工程证据。
  - **重要原则**：**失败的实验记录也是 VALID Evidence**（例如 2026-09-10 实测第 7 通道舵机物理回中失败持续上抬事件，作为证据本身真实客观，status 为 `VALID`，其工程结论记录物理故障）。
  - **禁止历史粉饰**：严禁为了迎合项目进度而删除、隐瞒或篡改失败实验证据。
- `SUPERSEDED`：已被更新的物理标定或工程更正版本替代的历史证据（需在 Header 中声明由谁替代）。
- `INVALID`：被证实出处造假、测试受外界非预期严重破坏（如测试仪器损坏导致数据全错）的无效记录。

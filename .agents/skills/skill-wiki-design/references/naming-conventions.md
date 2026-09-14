# Naming Conventions & Canonical Terminology

> 本规范定义 Evidence 命名空间、Topic 命名空间与机器人硬件执行器的规范命名体系（Canonical Terminology）。

---

## 1. 证据命名空间规范（Evidence Namespaces）

证据文档统一存放在 `docs/evidence/` 目录下。

### 命名模式
```text
E-{NAMESPACE}-{中文简明描述}.md
```
或者在全英文规范场景下：
```text
E-{NAMESPACE}-{three-digit-id}-{english-slug}.md
```

### 标准命名空间定义

| 命名空间 | 适用工程领域 | 典型认识论角色 | 示例 |
|---|---|---|---|
| `E-DOC-xxx` | 原厂操作指南、官方标准、用户手册、协议白皮书 | `DOC/SPEC` | `E-DOC-001-遥控器原厂操作与接线说明.md` |
| `E-HW-xxx` | 主控原理图、电机驱动板图纸、PCB Layout、电气引脚表 | `DOC/SPEC` | `E-HW-001-主控板与传感器电气原理图.md` |
| `E-FW-xxx` | 下位机 C/C++ 驱动固件、寄存器配置、中断服务例程 | `IMPLEMENTATION` | `E-FW-001-接收机PPM中断解码固件实现.md` |
| `E-SIM-xxx` | URDF/USD 仿真模型资产、Loop-cut 闭环配置、网格拓扑 | `CONFIG` / `IMPLEMENTATION` | `E-SIM-001-规范树状闭链数字资产说明.md` |
| `E-TEST-xxx` | 嵌入式单元测试、架空通信烟囱测试、串口指令往返测试 | `RUNTIME` | `E-TEST-001-架空指令时序与停机测试.md` |
| `E-CAL-xxx` | 传感器实物偏差标定、执行器机械零位补偿、极性判定 | `PHYSICAL` / `MEASURED` | `E-CAL-001-执行器单通道旋转极性标定.md` |
| `E-VAL-xxx` | 动力学不变量仿真验证、2400步连续重力稳定性报告 | `VALIDATED` / `EXECUTED` | `E-VAL-001-闭链物理仿真无应力校验报告.md` |

### 严禁反模式
- **严禁使用 `E-M1-G02-001`**：禁止在 Evidence ID 中嵌入 Milestone 或 Gate 编号，因为 Evidence 是可跨 Gate/Milestone 被多次引用的客观工程事实。

---

## 2. 横向专题命名空间（Topic Namespaces）

专题文档统一存放在 `docs/topics/` 或 `page/topic/` 目录下，采用 `T-{DOMAIN}-{id/slug}.md` 形式：

- `T-CONTROL-xxx`：遥控、遥测、通讯链路与控制模式切换分析
- `T-KINEMATICS-xxx`：五杆闭链运动学、几何装配偏置与工作空间
- `T-DYNAMICS-xxx`：刚体质量惯量、接触碰撞模型与动力学参数对齐
- `T-ELEC-xxx`：电源网络、总线抗干扰、隔离收发与硬件安全互锁
- `T-SIM2REAL-xxx`：实机运行数据与物理仿真环境的跨域对齐与拟合

---

## 3. 执行器规范命名体系（Canonical Actuator Terminology）

为消除跨固件、仿真模型与实操指南中的名称混淆，本项目确立以下标准命名（Canonical Name）：

### 8 路关节舵机规范名
- 前右外侧大腿关节：`FR_Outer_Servo`
- 前右内侧支撑关节：`FR_Inner_Servo`
- 前左外侧大腿关节：`FL_Outer_Servo`
- 前左内侧支撑关节：`FL_Inner_Servo`
- 后右外侧大腿关节：`RR_Outer_Servo`
- 后右内侧支撑关节：`RR_Inner_Servo`
- 后左外侧大腿关节：`RL_Outer_Servo`
- 后左内侧支撑关节：`RL_Inner_Servo`

### 4 路驱动轮电机规范名
- 前右轮电机：`FR_Wheel`
- 前左轮电机：`FL_Wheel`
- 后右轮电机：`RR_Wheel`
- 后左轮电机：`RL_Wheel`

### 历史遗留别名（Legacy Aliases）与未决映射规则
在历史源码、CAD 图纸或早期测试日志中常见的遗留命名：
- `M1`, `M2`, `M3`, `M4`
- `servoRightFront`, `servoLeftFront`, `servoRightRear`, `servoLeftRear`
- `alpha`, `beta`, `joint_1`, `joint_2`
- `PWM0` ~ `PWM7`

**处理红线**：
1. **保留历史现场，不做破坏性全局替换**：原始代码和原始 log 中的变量名必须原汁原味保留；
2. **严禁根据变量字面猜测内外腿对应关系**：
   例如不能仅因为代码写了 `servoRightFront` 就臆测它是 Outer 还是 Inner；
3. **未决必须标为 `UNRESOLVED`**：
   在尚未完成非破坏性单关节物理激励与实测拍照前，映射关系表格中必须明确填写 `UNRESOLVED`，禁止伪造“已对齐”。

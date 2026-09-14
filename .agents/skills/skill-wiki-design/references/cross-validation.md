# Cross-Validation & Topic Synthesis

> 本规范定义横向工程分析层（Topic）的多源交叉验证（Triangulation）、冲突分析（Conflict Analysis）与未决问题（Unresolved Questions）追踪方法论。

---

## 1. 交叉验证的四维矩阵（The Triangulation Dimensions）

在复杂的机器人机电与物理仿真系统中，单一维度的证据往往存在片面性或认知偏差。Topic 通过建立多维对照矩阵，穿透表面现象：

```text
               ┌────────────────┐
               │    DOC / SPEC  │
               └───────┬────────┘
                       │ DOC ↔ IMPLEMENTATION
                       ▼
┌────────────────┐            ┌────────────────┐
│   PHYSICAL     │◄──────────►│ IMPLEMENTATION │
└───────┬────────┘  SPEC ↔    └───────┬────────┘
        │          PHYSICAL           │ IMPLEMENTATION ↔
        │                             │ RUNTIME
        │ REAL ↔ SIM                  ▼
        │                      ┌────────────────┐
        └─────────────────────►│    RUNTIME     │
                               └────────────────┘
```

1. **DOC ↔ IMPLEMENTATION（图纸与代码对照）**：
   - 检查代码是否忠实实现了设计规范（例如图纸规定 PPM 接入 GPIO 40，固件中宏定义是否确为 `#define PPM_PIN 40`）。
2. **IMPLEMENTATION ↔ RUNTIME（逻辑与运行对照）**：
   - 检查代码逻辑在真实运行时是否被执行（例如固件实现了超时停机逻辑，串口实际是否在 500 ms 超时后输出了 `"STOP,command_timeout"`）。
3. **SPEC ↔ PHYSICAL（标称与实物对照）**：
   - 检查名义标称参数与物理器件的真实响应（例如标称舵机转速与实测无负载角速度差异，标称 120Ω 终端电阻在实板上的万用表实测值）。
4. **REAL ↔ SIM（实机与数字孪生对照）**：
   - 检查物理仿真动力学响应与真机物理实验曲线的一致度（例如悬空自由落体阻尼、触地冲量反弹峰值、步态跟踪误差）。

---

## 2. 关系判定语义状态（Relationship Statuses）

在 Topic 的比对矩阵中，各维度比对结论只能赋予以下四种标准状态：

- `CONSISTENT`：两项或多项 Evidence 之间完全吻合，无数学冲突或逻辑矛盾。
- `CONFLICT`：Evidence 之间存在明确的数据冲突、逻辑矛盾或物理违背。
  - **原则**：**冲突必须公开保留**。严禁在 Topic 中为了得出“统一结论”而私自删改某一方的数据。
- `MISSING`：某一维度尚未提供经过审计的 Evidence（例如有代码但缺乏实机运行测量）。
- `VERIFIED`：经过两个以上不同认识论角色的独立 Evidence 闭环证实（例如代码配置为 44.95 mm 且 CAD 与实物网格对齐残差小于容差）。

---

## 3. Topic 规范文档结构

每个 Topic 文档必须建立在 `page/topic/` 或 `docs/topics/` 目录下，采用 `T-{DOMAIN}-{slug}` 规范命名，结构如下：

```markdown
# T-CONTROL-001 — 遥控器输入链路与下位机控制接口一致性分析

> 专题编号：`T-CONTROL-001`  
> 状态：`ANALYZED` | `UNRESOLVED`  
> 范围：出厂遥控器发射机、PPM 接收机与主控固件接口全链路一致性。

---

## 1. Engineering Question（核心工程问题）
清晰定义本 Topic 旨在回答的技术一致性疑问（如“遥控器各通道拨杆在物理上的动作定义，是否与固件中接收解算的变量物理含义严格一致？”）。

---

## 2. Evidence Set（引用证据集合）
按认识论角色显式罗列参与分析的 Evidence#Part：

### Documentation / Specification
- [[E-DOC-001#p01-receiver-wiring-pinout]] — 原厂规定的接收机接线与引脚分配
- [[E-DOC-001#p03-safe-arming-interlock]] — 原厂规定的拨杆初始安全位姿

### Implementation
- [[E-FW-001#p01-ppm-pin-definition]] — 固件 GPIO 40 中断接收实现
- [[E-FW-001#p04-channel-teleop-mapping]] — 固件各通道物理量映射逻辑

### Runtime / Physical (若有)
- [[E-EXP-001#p02-command-latency-window]] — 架空测试指令延迟与停机

---

## 3. Cross-Validation Matrix（交叉验证矩阵）

| 对照维度 | 涉及证据 Part | 比对状态 | 分析与工程说明 |
|---|---|---|---|
| DOC ↔ FW (引脚连接) | `E-DOC-001#p01` vs `E-FW-001#p01` | CONSISTENT | 图纸 40 引脚与代码 `PPM_PIN 40` 完全一致 |
| DOC ↔ FW (通道定义) | `E-DOC-001#p03` vs `E-FW-001#p04` | CONFLICT | 原厂指引称左拨杆切模式，固件代码将通道7作为双足/四足切换但通道5控制车轮模式，存在双重模式定义分歧 |
| FW ↔ PHYSICAL (安全停机) | `E-FW-001#p04` vs `E-EXP-001#p03` | CONFLICT | 固件输出停机字符串，但实机 ch7 物理失控未停转，证明纯软件停机对硬件短路无效 |

---

## 4. Engineering Conclusion（工程学结论）
对该系统的当前工程认识，必须严格按确定性分级输出：
- **SUPPORTED（有充分证据支持的事实）**：遥控接收机必须由 3.3V 供电并接至 GPIO 40。
- **INFERRED（合理工程推断）**：操作手册中部分模式切换说明对应早期版本固件，当前固件扩展了更多通道。
- **UNRESOLVED（当前未决项）**：通道 8 在固件中被映射但原厂文档未提及其实际物理用途。

---

## 5. Conflicts & Open Questions（冲突与未决问题清单）
- **C-01 [CONFLICT]**：...
- **Q-01 [OPEN QUESTION]**：...
```

---

## 4. 处理未决问题与冲突的铁律

1. **不得私自抹平冲突**：
   如果原厂文档规定接 5V，而固件与原理图写着 3.3V，必须显式在 Topic 中立项记录为 `[CONFLICT]`，并在结论中提醒硬件工程师防烧毁风险，绝不能悄悄改动原厂文档的摘录。
2. **三态结论严谨性**：
   - 严禁将 `INFERRED`（推论）冒充为 `SUPPORTED`（实证）；
   - 面对证据不全的情况，坚决输出 `UNRESOLVED`，不要臆造“已对齐”。

---
evidence_id: E-{field English name}-{文档中文名描述}
title: 简明工程证据标题
status: DRAFT
created: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources:
  - source_id: SRC-XXX-001
    type: MANUFACTURER_SPEC | OFFICIAL_DOC | SOURCE_PYTHON | SOURCE_CPP | CONFIG | PROCEDURE | RUNTIME_LOG | PHYSICAL_MEASUREMENT | GENERATED_REPORT | IMAGE | DATASET | EXISTING_EVIDENCE
    path_or_url: $PROJECT_ROOT/...
    revision: git-hash-or-version
---

# E-{field English name}-{文档中文名描述}

> 证据编号：`E-{field English name}-{文档中文名描述}`  
> 状态：`DRAFT` | `VALID` | `SUPERSEDED` | `INVALID`（注：禁止使用 PASS/FAIL 评定证据本身状态）  
> 原则：**A PATH IS NOT EVIDENCE.** 本文档提供从原始技术源（Raw Source）提炼出的可审计工程语义层与忠实原始物料记录。

---

## 证据命名规范（Naming Convention）

每个证据项采用双层命名语义：
```text
E-{field English name}-{文档中文名描述}
```
- **field English name**（领域英文名）：`hardware`、`mechanical`、`control`、`firmware`、`simulation`、`experiment`、`validation`、`software` 等。
- **文档中文名描述**：清晰反映工程实体与产物性质，例如 `主控板与舵机IMU电气原理图`、`闭链机器人规范树资产说明`、`舵机与CAN通信控制固件`、`架空测试时序延迟与安全停机日志`、`BLDC无刷电机驱动固件`、`仿真测试报告` 等。

---

## 原始物料图片与截图引用规范（Image / Screenshot Guidelines）

- 允许且推荐在证据中直接嵌入原始图纸切片、实物照片、上位机示波器波形截图或终端运行抓图。
- 图片资源统一存放在相对路径：`docs/assets/images/{evidence_id}/` 或与证据文件并列的资产目录。
- 引用格式采用标准 Markdown 语法，必须配备清晰的图片说明：
  ```markdown
  ![图示说明：主控板 CAN 收发电路与隔离芯片原理图切片](../../docs/assets/images/E-hardware-主控板与舵机IMU电气原理图/can_isolation_schematic.png)
  ```

---

## 1. Scope（工程范围）

- **核心工程问题**：本 Evidence 旨在回答什么具体的物理、架构、电气、控制或仿真问题？
- **应用范围**：适用于机器人的哪些构件、子系统、仿真流程或硬件通道？
- **非目标**：本 Evidence 明确不涵盖或不能推论哪些领域？

---

## 2. Source Summary（技术源清单）

| Source ID | 类型 | 规范便携路径 / URL | 版本 / 提交哈希 | 角色与描述 |
|---|---|---|---|---|
| `SRC-XXX-001` | `MANUFACTURER_SPEC` | `<path>` | `rev` | 硬件原理图 / 数据手册 / 官方文档 |
| `SRC-XXX-002` | `SOURCE_CPP` | `<path>` | `git-sha` | 固件实现源码 |

---

## 3. Evidence Parts（可独立引用的工程事实）

每个 Part 必须是一个具备独立可引用性、论证完整的原子工程事实，并使用永久稳定的显式 HTML 锚点 `<a id="p01-slug"></a>`。

<a id="p01-part-slug"></a>
### P01 — [Part Title: 独立工程事实标题]

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> **本节严禁添加任何主观推断、修饰或语义升降级，必须字面完整、原汁原味地复刻或记录原始技术物料。**
> 
> 可以包含以下一种或多种形式：
> 1. **原始原理图切片 / 截图**：
>    `![电路图局部截图](相对图片路径)`
> 2. **原始源码逐行摘录**（保持行号与完整上下文）：
>    ```cpp
>    // 原始代码原样摘录，不修改变量名，不省略关键条件
>    ```
> 3. **原始数据表 / CSV 真实行**：
>    ```csv
>    // 原始测量行与列头原貌
>    ```
> 4. **原始终端串口日志流切片**：
>    ```text
>    [时间戳] 原始串口字符串输出，原样保留报错与状态码
>    ```
> 5. **原厂文档 / 数据手册原文切片**。

#### Engineering Statement（工程事实陈述）
> 直接由上述 Raw Source 支持的工程事实。严格使用语义限定词标注：
> `[SPECIFIED]` / `[MEASURED]` / `[OBSERVED]` / `[CONFIGURED]` / `[IMPLEMENTED]` / `[EXECUTED]` / `[VALIDATED]` / `[ESTIMATED]` / `[IDENTIFIED]` / `[DERIVED]`。

#### Source Observation（技术源字面观察）
> 提炼原始证据中的关键观察点（例如关键芯片标号、引脚连接网络、数组初值、数值极值或断言退出码）。

#### Engineering Interpretation（工程学解释）
> 该 Observation 对本工程（StackForce 四轮足 / Isaac 物理仿真与实机系统）的具体技术含义、参数约束或设计影响。

#### Limitations（证据局限性与禁区）
> 本 Part **不能证明什么**。明确列出边界条件、未测变量、环境依赖或潜在假设（严防语义越级，例如原理图不能证明实测性能、固件写命令不能证明物理反馈到位）。

#### Source Trace（溯源定位）
- **文件 / URL**：`$PROJECT_ROOT/...`
- **定位符**：Line / Function / Section / Page / Schematic Sheet
- **检索关键词**：`"keyword"`

---

<a id="p02-part-slug"></a>
### P02 — [Part Title: 第二个独立工程事实]

#### Raw Source Faithful Reproduction（原始证据忠实复刻）

#### Engineering Statement

#### Source Observation

#### Engineering Interpretation

#### Limitations

#### Source Trace

---

## 4. Artifacts（关联产物与机器可读附件）

| 产物名称 | 存储相对路径 | SHA256 / 格式 | 生成方式 / 校验命令 |
|---|---|---|---|
| 原始配置 / 日志 / 图片 | `$PROJECT_ROOT/...` | `<hash>` | 原始抓取 / 自动化生成 / 屏幕截图 |

---

## 5. Provenance & Reproducibility（溯源与可复现方法）

- **提取环境**：提取该证据所需的工具链、解析器或实验设备环境。
- **复现 / 校验命令**：
  ```bash
  # 确定性的机器校验、代码检索或日志比对命令
  ```
- **预期观测特征**：执行上述命令时应当观察到的特定退出码、数值、图片显示或日志标记。

---

## 6. Revision History（修订历史）

- `YYYY-MM-DD`：初始化本 Evidence Document，提取 P01–Pxx。

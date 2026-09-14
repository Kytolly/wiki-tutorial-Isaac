---
evidence_id: E-XXX-000
title: Standard Engineering Evidence Title
status: DRAFT
created: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources:
  - source_id: SRC-XXX-001
    type: MANUFACTURER_SPEC | OFFICIAL_DOC | SOURCE_PYTHON | SOURCE_CPP | CONFIG | PROCEDURE | RUNTIME_LOG | PHYSICAL_MEASUREMENT | GENERATED_REPORT | IMAGE | DATASET | EXISTING_EVIDENCE
    path_or_url: $PROJECT_ROOT/...
    revision: git-hash-or-version
---

# Evidence Title

> 证据定位：`E-XXX-000`  
> 状态：`DRAFT` | `VALID` | `SUPERSEDED` | `INVALID`（注：禁止使用 PASS/FAIL 评定证据本身状态）  
> 原则：**A PATH IS NOT EVIDENCE.** 本文档提供从原始技术源（Raw Source）提炼出的可审计工程语义层。

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

<a id="p01-part-slug"></a>
### P01 — [Part Title: 独立工程事实标题]

#### Engineering Statement
> 直接支持的工程事实。严格使用语义限定词：`SPECIFIED` / `MEASURED` / `OBSERVED` / `CONFIGURED` / `IMPLEMENTED` / `EXECUTED` / `VALIDATED` / `ESTIMATED` / `IDENTIFIED` / `DERIVED`。

#### Source Observation
> 原始技术源中字面观察到的内容（摘录电路图器件标号、引脚连接、代码片段、日志行或报表数值，不添加推断）。

#### Engineering Interpretation
> 该 Observation 对本工程（StackForce 四轮足 / Isaac 仿真与实机）的具体技术含义、参数约束或设计影响。

#### Limitations
> 本 Part **不能证明什么**。明确列出边界条件、未测变量、环境依赖或潜在假设（严防语义越级与过度外推）。

#### Source Trace
- **文件 / URL**：`$PROJECT_ROOT/...`
- **定位符**：Line / Function / Section / Page / Schematic Sheet
- **关键词**：`"keyword"`

---

<a id="p02-part-slug"></a>
### P02 — [Part Title: 第二个独立工程事实]

#### Engineering Statement

#### Source Observation

#### Engineering Interpretation

#### Limitations

#### Source Trace

---

## 4. Artifacts（关联产物与机器可读附件）

| 产物名称 | 存储相对路径 | SHA256 / 格式 | 生成方式 / 校验命令 |
|---|---|---|---|
| 原始配置 / 日志 | `$PROJECT_ROOT/...` | `<hash>` | 原始抓取 / 自动化生成 |

---

## 5. Provenance & Reproducibility（溯源与可复现方法）

- **提取环境**：提取该证据所需的工具链、解析器或实验设备环境。
- **复现 / 校验命令**：
  ```bash
  # 确定性的机器校验或检索命令
  ```
- **预期观测特征**：执行上述命令时应当观察到的特定退出码、数值或日志标记。

---

## 6. Revision History（修订历史）

- `YYYY-MM-DD`：初始化本 Evidence Document，提取 P01–Pxx。

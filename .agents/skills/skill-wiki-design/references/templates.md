# Information Architecture Templates

> 本规范提供标准 Evidence、Topic 及 Gate Traceability 的标准 Markdown 模板。

---

## 1. 标准 Evidence 模板

```markdown
---
evidence_id: E-{NAMESPACE}-{ID/SLUG}
title: 简明工程证据标题
status: DRAFT | VALID | SUPERSEDED | INVALID
created: YYYY-MM-DD
last_verified: YYYY-MM-DD
sources:
  - source_id: SRC-XXX-001
    type: MANUFACTURER_SPEC | OFFICIAL_DOC | SOURCE_PYTHON | SOURCE_CPP | CONFIG | PROCEDURE | RUNTIME_LOG | PHYSICAL_MEASUREMENT | GENERATED_REPORT | DATASET
    path_or_url: relative/path/or/url
    revision: git-hash-or-date
    sha256: sha256-string (可选)
---

# E-{NAMESPACE}-{ID/SLUG} — 简明工程证据标题

> 证据编号：`E-{NAMESPACE}-{ID/SLUG}`  
> 状态：`VALID`  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档提炼自原始技术源的工程语义层与忠实物料记录。

---

## 1. Scope（工程范围）

- **核心工程问题**：本 Evidence 旨在回答什么具体的物理、架构、电气、控制或仿真问题？
- **应用范围**：适用于机器人的哪些构件、子系统、仿真流程或硬件通道？
- **非目标**：本 Evidence 明确不涵盖或不能推论哪些领域？

---

## 2. Source Summary（技术源清单）

| Source ID | 类型 | 规范便携路径 / URL | 版本 / 提交哈希 | 角色与描述 |
|---|---|---|---|---|
| `SRC-XXX-001` | `TYPE` | `path/to/source` | `rev` | 简短描述 |

---

## 3. Evidence Parts（可独立引用的工程事实）

<a id="p01-slug-name"></a>
### P01 — [Part Title: 独立原子工程事实标题]

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> **本节严禁添加任何主观推断、修饰或语义升降级，必须字面完整、原汁原味地复刻或记录原始技术物料。**
> 
> 可以包含以下一种或多种形式：
> 1. 原理图切片 / 截图：
>    `![图示说明](../../docs/assets/images/{evidence_id}/sample.png)`
> 2. 原始源码逐行摘录（保持行号与完整上下文）：
>    ```cpp
>    // 原始代码原样摘录，不修改变量名，不省略关键条件
>    ```
> 3. 原始数据表 / CSV 真实行：
>    ```csv
>    // 原始测量行与列头原貌
>    ```
> 4. 原始终端串口日志流切片：
>    ```text
>    [时间戳] 原始串口字符串输出，原样保留报错与状态码
>    ```

#### Engineering Statement
> [SPECIFIED] / [IMPLEMENTED] / [MEASURED] / [CONFIGURED] / [VALIDATED]
> 直接由上述 Raw Source 支持的原子工程事实，以强语义限定词起始。

#### Source Observation
> 提炼原始证据中的关键观察点（例如关键芯片标号、引脚连接网络、数组初值、数值极值或断言退出码）。

#### Engineering Interpretation
> 该 Observation 对本工程（StackForce 四轮足 / Isaac 物理仿真与实机系统）的具体技术含义、参数约束或设计影响。

#### Limitations
> 本 Part **不能证明什么**。明确列出边界条件、未测变量、环境依赖或潜在假设（严防语义越级）。

#### Source Trace
- 文件：`path/to/source`
- 行号 / 章节：`L123` / `第 2 节`
- 关键检索符：`"search_keyword"`

---

## 4. Provenance & Artifacts（出处与衍生资产）

- **原始物理文件**：`path/to/file`
- **校验哈希 (SHA256)**：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **关联嵌入媒体**：
  - `docs/assets/images/{evidence_id}/sample.png`
```

---

## 2. 标准 Topic 模板

```markdown
# T-{DOMAIN}-{ID/SLUG} — [横向工程分析专题标题]

> 专题编号：`T-{DOMAIN}-{ID/SLUG}`  
> 状态：`ANALYZED` | `UNRESOLVED`  
> 范围：...

---

## 1. Engineering Question（核心工程问题）
清晰定义本专题旨在解答的跨物料、跨领域一致性疑问。

---

## 2. Evidence Set（引用证据集合）

### Documentation / Specification
- [[E-DOC-001#p01-slug]] — ...

### Implementation
- [[E-FW-001#p01-slug]] — ...

### Runtime / Physical
- [[E-TEST-001#p01-slug]] — ...

---

## 3. Cross-Validation Matrix（交叉验证矩阵）

| 对照维度 | 涉及证据 Part | 比对状态 | 分析与工程说明 |
|---|---|---|---|
| DOC ↔ FW | `E-DOC-001#p01` vs `E-FW-001#p01` | CONSISTENT | ... |
| FW ↔ PHYSICAL | `E-FW-001#p04` vs `E-TEST-001#p03` | CONFLICT | ... |

*状态候选：`CONSISTENT` / `CONFLICT` / `MISSING` / `VERIFIED`*

---

## 4. Engineering Conclusion（工程学结论）

- **SUPPORTED（有充分证据支持的事实）**：...
- **INFERRED（合理工程推断）**：...
- **UNRESOLVED（当前未决项）**：...

---

## 5. Conflicts（冲突清单）
- **C-01 [CONFLICT]**：详细记录不同证据之间的数值或逻辑矛盾，注明各方出处。

---

## 6. Missing Evidence & Open Questions（缺失证据与未决问题）
- **M-01 [MISSING EVIDENCE]**：缺少哪一类物理测试或运行时日志。
- **Q-01 [OPEN QUESTION]**：后续需要通过何种实验解决的核心技术疑问。
```

---

## 3. Gate 准则追溯表模板（Gate Traceability Table）

```markdown
### Acceptance Criteria（验收准则）

| 准则编号 | 验收准则描述 | 属性 | 依据证据 (Evidence#Part) | 准则状态 | 说明 |
|---|---|---|---|---|---|
| C01 | 主控与接收机电气接口及供电规范明确 | Required | [[E-DOC-001#p01-receiver-wiring-pinout]] | PASS | 3.3V GPIO 40 |
| C02 | 遥控器安全初始位姿在固件中闭环建立 | Required | [[E-FW-001#p03-safe-teleop-mapping]] | PASS | 腿高初始置底 |
| C03 | 遥控链路超时无信号时触发物理安全停机 | Required | [[E-EXP-001#p03-ch7-failure-event]] | FAIL | 实机 ch7 失控上抬断电 |

*准则状态候选：`PASS` / `FAIL` / `MISSING` / `BLOCKED` / `N/A`*  
*Gate 最终状态候选：`TODO` / `IN PROGRESS` / `BLOCKED` / `PASS`*
```

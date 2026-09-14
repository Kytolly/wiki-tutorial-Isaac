# Information Architecture & Layered Hierarchy

> 本规范定义本工程 Wiki 的全局信息架构（Information Architecture）。
> 核心原则：**A PATH IS NOT EVIDENCE.** 文件存在不代表工程事实成立，工程事实成立不代表验收通过。

---

## 1. 核心五层分级与横向分析层

本工程 Wiki 严格划分为 5 个垂直层级与 1 个横向分析层：

```text
Layer 0: Raw Source / Artifact (原始物料/事实源)
           ↓
Layer 1: Evidence Document (工程证据文档)
           ↓
Layer 2: Evidence#Part (原子工程事实小节，具稳定锚点)
           ↓
Layer 3: Gate Acceptance Criterion (门禁验收准则，直接引用 Part)
           ↓
Layer 4: Milestone (里程碑阶段管理，聚合 Gates)
```

**横向分析层（Horizontal Analysis Layer）**：
```text
Evidence#Part ─┐
Evidence#Part ─┼─→ Topic (横向工程分析：交叉验证 / 冲突排查 / 综合解释)
Evidence#Part ─┘
```

---

## 2. 各层级职责与边界定义

### Layer 0: Raw Source / Artifact（技术源物料）
- **实体形态**：PDF 原理图、DOCX 操作手册、原厂芯片 Datasheet、官方网页、Python 源码、C/C++ 固件、URDF/USD 仿真资产、JSON/CSV 配置文件、运行时日志流（.log）、实物测量输出、自动化校验报告、实物照片与截图。
- **角色约束**：
  - Source 是不可变或受版本控制的原始事实材料。
  - **A PATH IS NOT EVIDENCE**：一个文件在磁盘上存在（Path exists），仅代表其作为物料存在，绝不能直接等同于功能实现或性能达标。
  - 严禁因为“源码或配置文件存在”直接宣称 Gate PASS。

### Layer 1: Evidence Document（工程证据文档）
- **实体形态**：存放于 `docs/evidence/` 下的标准 Markdown 文件，拥有稳定编号（如 `E-DOC-xxx`, `E-HW-xxx`, `E-FW-xxx`, `E-SIM-xxx` 等）。
- **角色约束**：
  - Evidence 是对 Source 的工程语义化记录与忠实复刻。
  - 必须具备完整 Provenance（出处溯源：文件路径、版本/提交哈希/SHA256、签发日期）。
  - **Evidence ID 与 Gate 完全解耦**：严禁将证据命名为 `E-M1-G02-001` 这类绑定 Gate 的名字，因为同一份工程事实（如实测 IMU 采样频率）可被多个 Gate、Topic 或 Milestone 共同复用。
  - Evidence 状态只能是 `DRAFT` / `VALID` / `SUPERSEDED` / `INVALID`，**禁止使用 PASS/FAIL 评定证据本身状态**。

### Layer 2: Evidence#Part（可独立引用的原子工程事实）
- **实体形态**：Evidence 文档内部带有永久稳定 HTML 锚点的段落（如 `<a id="p01-servo-command"></a>`，配合 `### P01 — [Title]`）。
- **角色约束**：
  - 每个 Part 必须是一个自包含、论证完整、具有独立可引用性的原子工程事实。
  - 包含强制性 Dedicated Section：`#### Raw Source Faithful Reproduction（原始证据忠实复刻）`，字面摘录原始数据、真实代码、图片切片或串口日志。
  - 明确标注限定词（`[SPECIFIED]`, `[IMPLEMENTED]`, `[MEASURED]` 等）、字面观察（Observation）、工程解释（Interpretation）以及证据局限（Limitations）。
  - Part 锚点一经发布，后续无论排版或标题字面如何微调，锚点名称永固不变。

### Layer 3: Gate Acceptance Criterion & Gate（门禁验收层）
- **实体形态**：存放于 `page/stackforce/gate/` 下的验收门禁页面。
- **角色约束**：
  - Gate 只负责**严格验收**，不保存或复制原始事实细节。
  - Gate 页面结构定义：Objective（目标）、Acceptance Criteria（准则表）、Required/Optional 属性、Evidence#Part 显式链接、Criterion 状态、Gate 最终状态。
  - 准则追踪矩阵推荐格式：
    ```markdown
    | Criterion ID | 验收准则描述 | 属性 | 依据证据 (Evidence#Part) | 准则状态 |
    |---|---|---|---|---|
    | C01 | 主控与舵机驱动通信建立 | Required | [[E-HW-001#p02-pca9685-servo-topology]] | PASS |
    | C02 | 架空指令超时停机硬件保护 | Required | [[E-EXP-001#p03-ch7-failure-event]] | FAIL |
    ```
  - **Criterion 状态**：`PASS` / `FAIL` / `MISSING` / `BLOCKED` / `N/A`。
  - **Gate 状态**：`TODO` / `IN PROGRESS` / `BLOCKED` / `PASS`。
  - **绝对禁止反向污染**：Gate 只能引用 `Evidence#Part`，不得复制 Evidence 的大段长文或原始数据。

### Layer 4: Milestone（里程碑与路线图管理）
- **实体形态**：存放于 `page/stackforce/milestone/` 及全局 `Roadmap与里程碑.md`。
- **角色约束**：
  - Milestone 只负责**阶段进度聚合与方向规划**。
  - Milestone 汇总其管辖的所有 Gate 状态，计算交付百分比，呈现 Current Focus 与 Next Action。
  - **严禁越级存储**：Milestone 页面不得直接记录 Ground Truth 物理测量值、原始调试日志或嵌入复杂代码片段。

---

## 3. 横向分析层：Topic（横向工程专题）

### Topic 的定位
Topic 是平行于垂直层级的**横向工程分析层**，用于解决跨物料、跨领域、跨阶段的综合技术分析。

### Topic 的核心职责
1. **交叉验证（Cross-Validation）与多源互证（Triangulation）**：
   - 比较设计图纸与实现源码（`DOC ↔ IMPLEMENTATION`）；
   - 比较实现代码与运行时实测（`IMPLEMENTATION ↔ RUNTIME`）；
   - 比较名义指标与物理实物（`SPEC ↔ PHYSICAL`）；
   - 比较实机物理响应与物理仿真（`REAL ↔ SIM`）。
2. **一致性与冲突分析（Consistency & Conflict Analysis）**：
   - 对比各 Evidence#Part，客观标记 `CONSISTENT` / `CONFLICT` / `MISSING` / `VERIFIED`。
   - 绝不掩盖或抹杀冲突事实。
3. **工程综合解释（Engineering Synthesis & Interpretation）**：
   - 给出当前技术理解阶段的 Working Engineering Conclusion。
4. **未决问题追踪（Unresolved Questions Tracking）**：
   - 记录当前证据链不完备之处，指引下一步实验或测定。

---

## 4. 严禁反向依赖与反模式（Anti-Patterns）

```text
[禁止反模式 1]: Gate → Topic → Evidence
  Gate 不得以 Topic 的分析结论作为 PASS 的替代依赖。
  Gate 必须且只能直接穿透引用原子级 Evidence#Part！

[禁止反模式 2]: Topic 替代 Evidence
  Topic 不能成为事实来源（SSOT），Topic 中的每一句论断必须反向追踪至 Evidence#Part。

[禁止反模式 3]: Evidence Registry 作为 SSOT
  Evidence Registry 只能是只读检索索引（INDEX），事实真源位于各独立的 Evidence 文件中。

[禁止反模式 4]: 语义升级跨层穿透
  严禁将原理图（DOC）直接作为 Gate PASS 的实测性能依据。
```

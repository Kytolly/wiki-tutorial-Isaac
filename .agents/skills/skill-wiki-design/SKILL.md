---
name: skill-wiki-design
description: StackForce / Isaac Wiki 严谨工程证据架构（Evidence Architecture）、认识论分类、多源交叉验证、Gate/Milestone 状态解耦与规范重构指南。适用于整理 Wiki、重构证据、审查门禁与里程碑、分析技术物料及 Sim2Real 审计。
---

# skill-wiki-design: Engineering Evidence & Wiki Information Architecture

> 本 Skill 是本工程 Wiki 的**核心信息架构与认识论控制平面（Control Plane）**。
> 核心原则：**A PATH IS NOT EVIDENCE.** 文件在磁盘上存在不代表功能成立，代码写了不代表物理已执行，仿真跑通不代表实机达标。

---

## 1. 核心架构：五层垂直流与横向分析层

本项目的工程事实与进度追踪严格遵循以下层级单向流，杜绝倒置与语义污染：

```text
Layer 0: Raw Source / Artifact (图纸/代码/资产/日志/实物测量)
           ↓
Layer 1: Evidence Document (E-DOC / E-HW / E-FW / E-SIM / E-TEST / E-CAL / E-VAL)
           ↓
Layer 2: Evidence#Part (原子工程事实，稳定锚点，忠实复刻)
           ↓
Layer 3: Gate Acceptance Criterion (直接引用 Evidence#Part，计算准则 PASS/FAIL)
           ↓
Layer 4: Milestone (聚合 Gate，进度看板与路线图推进)
```

**横向分析层（Horizontal Layer）**：
```text
Evidence#Part ─┐
Evidence#Part ─┼─→ Topic (T-CONTROL / T-KINEMATICS / T-DYNAMICS / T-SIM2REAL ...)
Evidence#Part ─┘   (跨源交叉验证 / 冲突排查 / 综合工程解释 / 未决问题追踪)
```

**绝对禁止**：
- `Gate → Topic → Evidence`（Gate 不得以 Topic 结论替代原子证据）；
- 将 Topic 当作事实源（Topic 的结论必须反向追踪至 Evidence#Part）。

---

## 2. 规则参考导航（Reference Sitemap）

当执行具体任务时，Agent **必须查阅** 对应的专用参考规范：

| 任务场景 | 必读参考文件 | 核心内容与规则 |
|---|---|---|
| **理解全局层级与角色边界** | [`references/architecture.md`](references/architecture.md) | 5 层垂直流、Topic 横向定位、Gate/Milestone 解耦、4 大反模式 |
| **判定认识论角色与语义限定词** | [`references/evidence-semantics.md`](references/evidence-semantics.md) | 5 类认识论角色、10 个语义限定词、6 条防语义越级红线、同一家族合并准则、Evidence 状态生命周期（严禁PASS/FAIL） |
| **多源交叉验证与冲突排查** | [`references/cross-validation.md`](references/cross-validation.md) | 四维互证矩阵（DOC↔FW, FW↔RUNTIME, SPEC↔PHYSICAL, REAL↔SIM）、CONSISTENT/CONFLICT/MISSING/VERIFIED 判定、三态结论（SUPPORTED, INFERRED, UNRESOLVED） |
| **重构工作流与安全审计红线** | [`references/refactor-workflow.md`](references/refactor-workflow.md) | 六阶段流程（E0盘点 $\to$ E1分类 $\to$ E2提取 $\to$ E3规范 $\to$ E4审计 $\to$ E5门禁 $\to$ E6看板）、六大重构安全红线（严禁删原始物料、严禁掩盖故障、严禁臆测电机映射） |
| **命名规范与执行器标准术语** | [`references/naming-conventions.md`](references/naming-conventions.md) | `E-DOC/HW/FW/SIM/TEST/CAL/VAL` 命名空间、12 执行器 Canonical Terminology、历史别名与未决项处理 |
| **撰写 Evidence / Topic / Gate** | [`references/templates.md`](references/templates.md) | 标准 Evidence 模板（含原始物料复刻小节）、标准 Topic 模板、Gate 验收准则表、图片资产嵌入语法 |

---

## 3. Agent 行为准则与操作清单（Operational Checklist）

当被要求“整理 Wiki”、“审计 Evidence”、“更新 Gate/Milestone”时，必须依次执行：

1. **识别 Source**：定位原始物料（文件路径、提交哈希或物理测量来源）；
2. **确认认识论角色**：判断属于 DOC/SPEC、IMPLEMENTATION、RUNTIME 还是 PHYSICAL；
3. **检查已有 Evidence 库**：避免重复创建，判断是 KEEP / REWRITE / SPLIT / MERGE 还是 SUPERSEDE；
4. **同家族审查（严格拆分红线）**：
   - 严禁将不同认识论角色（如原厂 DOCX 与固件 CPP）合并在一个 Evidence 内；
   - 强制拆分为 `E-DOC-xxx` 与 `E-FW-xxx`，并在 `T-xxx` Topic 中比对；
5. **提取原子事实并写入 Part**：
   - 使用规范限定词（`[SPECIFIED]`, `[IMPLEMENTED]`, `[MEASURED]` 等）；
   - 强制撰写 `#### Raw Source Faithful Reproduction（原始证据忠实复刻）`；
   - 给出 Observation、Interpretation、Limitations 与 Source Trace；
6. **建立多源交叉验证（若涉及跨源分析）**：创建或更新 Topic，客观记录 CONSISTENT 或 CONFLICT；
7. **挂载 Gate 准则**：在 Evidence 稳定后，再在 Gate 页面建立 `[[E-xxx#p01-slug]]` 准则链接；
8. **更新看板**：最后汇总更新 Milestone 与 Roadmap。
9. **面对未决事实**：坚决标记 `MISSING`、`UNRESOLVED` 或 `CONFLICT`，绝不凭空臆造！

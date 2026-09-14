# Evidence-First Refactoring Workflow & Safety Rules

> 本规范定义对既有工程资料、旧版 Wiki 及原始物料进行系统化重构的标准工作流与安全红线。
> 核心原则：**EVIDENCE FIRST, NOT MILESTONE FIRST.** 先审计事实证据，再更新门禁与路线图。

---

## 1. 重构的六阶段标准流程（Phased Workflow）

```text
Phase E0: Source Inventory (全量技术源盘点)
   ↓
Phase E1: Source Classification (认识论角色与家族分类)
   ↓
Phase E2: Engineering Semantic Extraction (工程语义与事实提取)
   ↓
Phase E3: Evidence Normalization (证据规范化入库，含忠实复刻)
   ↓
Phase E4: Evidence Audit (自洽性、多源拆分与反越级审计)
   ↓
Phase E5: Gate Traceability (门禁准则引用对齐)
   ↓
Phase E6: Milestone & Roadmap Rebuild (里程碑与进度聚合重建)
```

### Phase E0 — Source Inventory（全量物料盘点）
- 扫描工程目录（如 `doc/`, `sf_quad/`, `lib/firmware/`, `artifacts/` 等），建立不可被删除的原始技术源清单。
- 记录便携相对路径、文件类型、SHA256 哈希值与修改日期。
- 产出：`docs/refactor/source-inventory.md`。

### Phase E1 — Source Classification（认识论与家族分类）
- 为每个 Source 判定认识论角色：`DOC/SPEC`、`IMPLEMENTATION`、`RUNTIME`、`PHYSICAL`、`DERIVED`。
- 划分技术源家族（Source Family）。
- 确认是否属于同一家族，若不同角色则强制标记为拆分任务。

### Phase E2 — Engineering Semantic Extraction（工程语义提取）
- 审查原始技术源内容，提取具备工程约束力的硬事实：
  - 引脚分配、电压域、阻抗、波特率；
  - 连杆偏置距离、轴向法向量、惯量矩阵；
  - 控制循环周期、滤波公式、报文压缩格式；
  - 实测延迟、采样抖动、故障事件序列。
- 严禁加入任何主观猜测或未经证实的推论。

### Phase E3 — Evidence Normalization（证据规范化撰写）
- 按标准模板撰写 Evidence 文件至 `docs/evidence/`。
- 提取并保存原始截图、图纸切片至 `docs/assets/images/{evidence_id}/`。
- 每个 Part 必须包含 `Raw Source Faithful Reproduction` 小节，完整复刻关键代码、配置或原图。
- 显式声明 `[SPECIFIED]`, `[IMPLEMENTED]`, `[MEASURED]` 等限定词。

### Phase E4 — Evidence Audit（自洽性与多源拆分审计）
- 审查是否存在多认识论角色混写（如 DOC 吞并 FW）；
- 审查是否存在语义越级（如将配置写成已实测验证）；
- 审查 Provenance 是否完备（哈希与版本是否缺失）；
- 对多源比较任务，创建或更新 `docs/topics/` 专题。

### Phase E5 — Gate Traceability（门禁准则链条挂载）
- 在 Evidence 稳定入库后，更新对应 Gate（`page/stackforce/gate/`）；
- 将验收准则的证据依赖精确指定为 `[[E-xxx#p01-slug]]`；
- 根据 Evidence Part 的真实结果客观评定准则状态（PASS/FAIL/BLOCKED/MISSING）。

### Phase E6 — Milestone & Roadmap Rebuild（路线图与看板更新）
- 聚合 Gate 验收结果，更新 Milestone 进度百分比与状态；
- 同步主页 `Home.md` 与 `Roadmap与里程碑.md`。

---

## 2. 重构安全守则与底线红线（Safety Rules）

在重构过程中，任何 Agent 必须严格遵守以下纪律：

1. **绝对禁止无映射的大规模删除**：
   重构旧文档前，必须建立 `Source → Old Document → New Evidence` 映射表。凡未被新证据完全承接的技术事实，旧文档不得删除。
2. **绝对禁止删除或篡改原始产物（Raw Artifacts）**：
   原始 CSV 测量文件、二进制 USD 资产、固件 ELF 文件、带有 SHA256 的串口日志文件必须原样保留在工程目录中。
3. **绝对禁止删除或隐瞒历史失败记录（Historical Failures）**：
   硬件故障（如 ch7 回中失败持续上抬导致手动断电）是系统的核心安全阻断依据，绝不能因为要让看板变绿而篡改历史或粉饰太平。
4. **绝对禁止为了通过而降低验收准则（Criteria Lowering）**：
   不能因为实机硬件当前无法通过闭环自平衡，就悄悄将 Gate 准则从“实机闭环平衡”修改为“仿真通过即可”。
5. **绝对禁止在证据不足时妄猜执行器物理映射**：
   未决映射必须保留 `UNRESOLVED` 状态，严禁凭空指定电机通道。
6. **先盘点再实施（Inventory Before Modifying）**：
   严禁跳过 Phase E0/E1 直接修改 Gate 或 Milestone。

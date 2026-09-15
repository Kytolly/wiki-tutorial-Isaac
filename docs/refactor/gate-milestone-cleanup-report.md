# Gate–Milestone Traceability & Wiki Cleanup Final Report
# 门禁–里程碑全链路追溯与知识库重构终报

> **报告依据**：`skill-wiki-design` 与用户指令规范要求。  
> **报告日期**：2026-09-15  
> **重构目标**：收口 Wiki 上层追溯链条为 `Milestone → Gate → Acceptance Criterion → Evidence#Part → Source / Artifact`，解耦 Topic 为横向分析层，消除历史过期阻断与歧义命名，确立全库唯一状态 SSOT。

---

## 1. Architecture Result（最终知识库层次架构）

重构后，全库确立了严格清晰的单向验收主链与横向交叉分析层：

```text
[Upstream Source / Physical Artifact]
         │
         ▼
[Atomic Evidence Document] (docs/evidence/E-*.md, 共 27 篇)
         │
         ▼
[Evidence#Part] (如 E-SIM-001#P01, E-CAL-001#P04)
         │
         ▼ (直接单向引用)
[Acceptance Criterion] (如 M1-G01-C01, M2-G02-C01)
         │
         ▼ (判定推导：全部 Required Criteria 为 PASS 或 N/A)
[Gate Page] (page/stackforce/gate/Mx-Gxx.md, 共 44 个)
         │
         ▼ (聚合推导)
[Milestone Page] (page/stackforce/milestone/Mx-*.md, 共 6 个)
         │
         ▼ (顶层呈现)
[Roadmap 与 Home 视图] (page/stackforce/Roadmap与里程碑.md, page/Home.md)
```

**横向分析层（Horizontal Analysis Layer）**：
```text
Evidence#Part ◄──► Topic (page/stackforce/topic/T-*.md) ◄──► Evidence#Part
```
- **核心定位**：Topic 负责跨证据的多源交叉验证（Cross-validation）、一致性三角核验（Triangulation）、物理冲突排查与未决问题跟踪，**严禁作为 Gate PASS 的唯一依据，亦不阻断 Gate 到 Evidence#Part 的直接追溯链**。

---

## 2. Gate Migration（门禁重构与验收准则明细）

- **重构门禁总数**：全量 **44 个 Gate** 均已按标准结构重写（`# Mx-Gxx — Gate Title`、`## Status`、`## Objective`、`## Acceptance Criteria`、`## Related Topics`、`## Changelog`）。
- **验收准则（Criteria）总数**：共 **118 条原子验收准则**。
  - **PASS**：**48 条**（M1: 27 条，M2: 21 条）。
  - **MISSING / Evidence Debt**：**5 条**（M1 实机回归复测与精细标定准则）。
  - **IN PROGRESS**：**2 条**（M3-G01 激励协议准则）。
  - **TODO**：**63 条**（M3~M6 未就绪准则）。
  - **BLOCKED**：**0 条**（已清除全部虚假硬阻断）。
- **直接追溯矩阵**：详见 [`docs/refactor/gate-evidence-traceability.md`](gate-evidence-traceability.md)。

---

## 3. Milestone Status（六大里程碑最新状态与进度）

全库状态唯一机器可读 SSOT（`_meta/status.yaml`）、Milestone 页面、Roadmap 与 Home 视图已 100% 对齐：

| Milestone | 阶段名称 | 门禁数 | PASS | IN PROGRESS | TODO | 当前状态 | 核心焦点与推进说明 |
|---|---|---:|---:|---:|---:|---|---|
| **M1** | Hardware Ground Truth | 10 | 7 | 3 | 0 | **IN PROGRESS** | 硬件/固件/时序基线关闭；ch7 已修复，待回归复测与 8 舵机物理零位标定 |
| **M2** | Simulation Asset | 8 | 8 | 0 | 0 | **PASS** | 29 Links/28 Joints 单父树与 PhysX 闭环副验证全绿；明确 `rl_ready = false` 边界 |
| **M3** | Dynamics Calibration | 6 | 0 | 1 | 5 | **IN PROGRESS** | **当前核心推进阶段**。基础映射与数字资产已具备，待实机采样与系统辨识 |
| **M4** | Locomotion | 6 | 0 | 0 | 6 | **TODO** | 等待 M3 动力学参数就绪后解除 `rl_ready = false` 锁定 |
| **M5** | Robustness | 6 | 0 | 0 | 6 | **TODO** | 待 M4 基础步态与自稳策略收敛后开展域随机化 |
| **M6** | Sim-to-Real | 8 | 0 | 0 | 8 | **TODO** | 待 M1 硬件安全解封与 M5 策略导出后开展真机联调 |
| **总计** | **Project Macro Total** | **44** | **15** | **4** | **25** | **IN PROGRESS** | **宏观进度 15 / 44 Closed** |

---

## 4. M1 Changes（硬件基线重算与安全解耦）

1. **消除 Stale ch7 Blocker**：
   - 历史事实：Channel 7（右后内侧舵机）在架空实验中曾发生 `STOP` 指令后持续上抬失控，该历史事实已在 `E-CAL-001#P04` 与 `E-TEST-001#P05` 中永久留存。
   - 当前物理真值：经实机硬件检修，物理硬件故障已排除修复，不再作为阻止全项目的外部永久性硬阻断。
   - 剩余要求：在 `M1-G03-C04` 与 `M1-G10-C04` 中标记为 `MISSING`（待补修复后回归复测数据），状态置为 `IN PROGRESS`。
2. **M1 状态重新推导**：
   - 摒弃旧版硬编码的 `7/10 BLOCKED`。
   - G01, G02, G05, G06, G07, G08, G09 为 `PASS`；G03, G04, G10 为 `IN PROGRESS`。
   - M1 Milestone 状态由 `BLOCKED` 更新为 **`IN PROGRESS`**。
3. **注册码认识论边界（Registration Code Provenance）**：
   - 严格落实 Level A~E 分层：机制存在（A）与固件提取规程（B）不等于当前特定物理机身注册码（D/E）。
   - 创建 `T-HW-REG-001` 专题，解耦源码占位常量与真机实体指纹。

---

## 5. M2 Changes（规范资产保持 8/8 PASS 与构件命名）

1. **8/8 PASS 严格保持**：M2 为项目已冻结交付物，严禁无故重开；全量 G01~G08 全部维持 `PASS`。
2. **规范构件命名（Canonical Component Naming）全面替代旧代号**：
   - 全面消除正文中混用的 `M1/M2/P1/P2/W1/W2` 作为当前构件标识。
   - 统一使用：
     - **12 Actuated Tree Joints**：`4 Outer Hip Joints` + `4 Inner Hip Joints` + `4 Wheel Joints`。
     - **8 Passive Tree Joints**：`4 Outer Knee Joints` + `4 Inner Knee Joints`。
     - **4 Closure Joints**：`{LEG}_Closure_Joint`（在 Inner Calf 末端切断，PhysX 中以 `excludeFromArticulation=true` 注入）。
3. **Legacy Evidence ID 迁移**：旧 `E-ASSET-*`、`E-MECH-*`、`E-PHYS-*`、`E-RL-*` 均已在 Gate 中替换为原子 `E-SIM-*` 与 `E-VAL-*`。

---

## 6. M3 Changes（修正当前现实与依赖基础）

1. **状态更新为 IN PROGRESS**：移除非法过期的“M2 尚未冻结资产”阻断（M2 已 8/8 PASS），M3 状态更新为 **`IN PROGRESS (0/6 PASS)`**。
2. **已具备基础（Current Foundation）**：
   - Canonical Actuator Identity：可用（`T-ACT-001`）。
   - PCA ↔ Servo Identity：可用（`PCA1~PCA8` 对应确定）。
   - Servo ↔ Sim Hip Joint Identity：可用。
   - M2 Simulation Asset：已 8/8 PASS 冻结，具备 2400 步重力下沉稳定基线。
3. **真机依赖保留**：明确声明 Servo u0 机械零位、指令物理符号、比例因子、轮机 FOC 动力学参数与地面摩擦角尚未实测，继续标记为 `WAITING_REAL_DATA / TODO`，严禁主观编造。

---

## 7. Topic Consolidation（横向分析专题重构与收口）

- **KEEP (保留与规范化)**：
  - `T-ACT-001-Canonical-Real-Sim-Component-Identity.md`：**Golden Topic**，全项目跨阶段构件映射唯一权威分析。
  - `T01-机器人接口.md`：软件抽象接口与适配器分析。
  - `T02-实验日志.md`：高频遥测 CSV 标准格式分析。
  - `T03-安全联锁.md`：软硬件安全联锁与断电保护分析。
  - `T04-工程边界.md`：负知识排错与五大反模式分析。
  - `M1-T01`, `M1-T03`~`M1-T06`, `M2-T01`~`M2-T08`, `M3-T01`, `M4-T01`, `M5-T01`, `M6-T01`。
- **NEW (新建全局专题)**：
  - `T-HW-REG-001-Controller-Registration-Hardware-Identity.md`：解耦注册码机制、源码宏与实机指纹。
- **MERGE (合并吸收)**：
  - `M1-T02-执行器映射.md`：构件映射真值合并指向 `T-ACT-001`，正文聚焦 PCA9685 板级接线与小阶跃测试规程。
- **ARCHIVE (移入归档)**：
  - `M1-现场产物归档.md` $\rightarrow$ 移入 `page/stackforce/archive/`。

---

## 8. Evidence Index Changes（证据注册表降级为纯索引）

- **降级为只读索引**：`page/stackforce/evidence/evidence-registry.md` 顶部明确标明：
  `THIS PAGE IS AN INDEX. EVIDENCE DOCUMENTS ARE THE SOURCE OF TRUTH.`
- **去除重复声明**：移除原页面中内嵌的 Claim、Result、Engineering Conclusion，正文仅维护包含 27 篇证据的只读索引表。
- **来源索引标准化**：`page/stackforce/evidence/source-inventory.md` 重构为规范技术源只读索引（`Source Index`），与 `_meta/source-inventory.yaml` 严格吻合。

---

## 9. Legacy Evidence IDs（历史证据编号映射）

建立了全局映射文件 [`docs/refactor/legacy-evidence-id-map.md`](legacy-evidence-id-map.md)：
- 全库 11 个旧 ID（`E-MECH-001/002`, `E-ASSET-001~004`, `E-PHYS-001/002`, `E-RL-001`, `E-HW-001 (Legacy)`, `E-CANON-001`）已 100% 映射至当前原子证据。
- Current Gate / Milestone / Roadmap / Home 中已全面清除 Legacy ID。

---

## 10. Files Deleted（安全删除文件清单与理由）

共删除 **10 个文件**（经全局检索，入度引用均为 0，无任何独特事实丢失）：
1. `archive/legacy/M1-01-硬件清单与传感器.md`（已吸收至 M1-T01 / M1-T03）
2. `archive/legacy/M1-02-Joint-Map与单执行器.md`（已吸收至 M1-T02 / T-ACT-001）
3. `archive/legacy/M1-03-控制接口与频率延迟.md`（已吸收至 M1-T04 / T01）
4. `archive/legacy/M1-04-机械参数与重量.md`（已吸收至 M1-T05）
5. `archive/legacy/M1-T07-接口安全日志.md`（已吸收至 T02 / T03）
6. `archive/legacy/M1-硬件吃透.md`（早期草稿，已被规范 Roadmap 取代）
7. `archive/legacy/M2-资产检查.md`（已吸收至 M2-T01 / M2-T02）
8. `archive/legacy/legacy-Roadmap与里程碑.md`（早期草稿，已被规范 Roadmap 取代）
9. `page/stackforce/topic/闭环恢复架构与产物映射.md`（重构为标准简短名 `M2-T08-闭环恢复.md`）
10. `page/stackforce/topic/T04-参考工程边界.md`（重构为标准简短名 `T04-工程边界.md`）

---

## 11. Files Archived（历史归档文件清单）

所有保留历史价值的文件均已移入 `page/stackforce/archive/` 并添加 `STATUS: ARCHIVED / NOT A CURRENT SOURCE OF TRUTH` 标头：
1. `page/stackforce/archive/M1-现场产物归档.md`（2026-09-10 实机调试产物清单）
2. `page/stackforce/archive/mechanical-model.md`（重构前机械模型总结，替代页：`M2-T02` 与 `E-SIM-001`）
3. `page/stackforce/archive/geometry-baseline.md`（重构前几何基线总结，替代页：`M2-T03` 与 `E-SIM-002`）
4. `page/stackforce/archive/C6-registration-history.md`（历史 C6 注册探索记录）
5. `page/stackforce/archive/M2-reverse-engineering.md`（历史逆向工程记录）
6. `page/stackforce/archive/重构迁移索引.md`（历史迁移索引）

---

## 12. Remaining Ambiguities（未决问题与 REVIEW_REQUIRED 项）

以下事项已显式列入跟踪，不借重构主观假设：
1. **REVIEW_REQUIRED: RR-Inner 修复后回归测试**：`M1-G03-C04` 与 `M1-G10-C04` 待实机再次架空上电，取得无失控、正常复位的量化遥测日志后正式关闭。
2. **REVIEW_REQUIRED: 8 舵机机械零位 u0 与尺度 Scale**：`M1-G04-C02` 与 `M1-G04-C04` 需实物量角器/台架物理测定，严禁从镜像反射或固件偏移推导。
3. **REVIEW_REQUIRED: 轮电机物理反馈极性**：`T-ACT-001` 中标记轮电机旋转反馈方向需在 `M3-G04` 实机采集中核验。

---

## 13. Validation Results（全库一致性与构建验证）

1. **构建测试**：
   - `python3 script/build.py`：全库页面扁平化与 WikiLink 转换顺利完成。
   - `mkdocs build -f script/mkdocs.yml`：**Exit Code 0**，文档站点构建成功，零死链。
2. **状态一致性**：
   - `_meta/status.yaml` $\leftrightarrow$ `Roadmap与里程碑.md` $\leftrightarrow$ `Home.md` $\leftrightarrow$ 6 个 `Milestone` $\leftrightarrow$ 44 个 `Gate` 计数完全吻合（15 PASS, 4 IN PROGRESS, 25 TODO）。
3. **构件命名一致性**：
   - 全库统一使用 `{LEG}_{BRANCH}_Servo`、`{LEG}_Wheel_Motor`、`{LEG}_{BRANCH}_Hip_Joint`、`{LEG}_{BRANCH}_Knee_Joint`、`{LEG}_Wheel_Joint`、`{LEG}_Closure_Joint`，消除了歧义代号。

---

## 14. 当前项目唯一 Next Action（Next Action for Project）

> **唯一推荐下一步**：  
> **推进 `M3-Dynamics-Calibration` 下的 `M3-G01-激励冻结` 与 `M3-G02-实机采样`**：连接真实四足轮腿机器人架空台架，执行阶跃与正弦激励实验，录制标准 CSV 遥测数据集，为执行器刚度/阻尼辨识提供数据输入。

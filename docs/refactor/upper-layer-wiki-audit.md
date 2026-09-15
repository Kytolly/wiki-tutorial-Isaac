# Upper-Layer Wiki Audit Report
# 上层 Wiki 架构与文件角色全面审计

> **审计依据**：`skill-wiki-design`，执行 Phase A 规范。  
> **审计日期**：2026-09-15  
> **核心目标**：全面盘点 Milestone、Gate、Topic、Evidence、Index、Roadmap、Home 及历史归档文件，明确其当前角色、目标角色、入度引用、重复关系、过期状态及重构动作。  
> **约束**：本阶段为纯审计与规划，不对文件执行实际删除。

---

## 1. 架构角色重构定义

根据目标架构：
```text
Source / Artifact
    ↓
Evidence Document (docs/evidence/E-*.md)
    ↓
Evidence#Part (e.g. E-SIM-001#P01)
    ↓
Acceptance Criterion (e.g. M2-G02-C01)
    ↓
Gate (page/stackforce/gate/Mx-Gxx.md)
    ↓
Milestone (page/stackforce/milestone/Mx-*.md)
```

横向分析层：
```text
Evidence#Part ◄──► Topic (page/stackforce/topic/T-*.md) ◄──► Evidence#Part
```

---

## 2. 全库上层文件审计总表（Upper-Layer File Audit Table）

| File | Current Role | Intended Role | Incoming References | Duplicate Of | Stale? | Action |
|---|---|---|---|---|---|---|
| **Milestone Pages** | | | | | | |
| `page/stackforce/milestone/M1-Hardware-Ground-Truth.md` | Milestone Spec (含硬编码 7/10 BLOCKED 与冗余总结) | Pure Milestone (只引用 G01~G10，移除旧 blocker，更新为 IN PROGRESS) | 7 refs (`Home.md`, `_Sidebar.md`, etc.) | None | Yes (硬编码旧状态) | **REWRITE** |
| `page/stackforce/milestone/M2-Simulation-Asset.md` | Milestone Spec (含 8/8 PASS，内含 Legacy Evidence ID) | Pure Milestone (8/8 PASS 保持，规范化引用 G01~G08) | 6 refs (`Home.md`, `_Sidebar.md`, etc.) | None | Yes (含旧 ID/旧构件代号) | **REWRITE** |
| `page/stackforce/milestone/M3-Dynamics-Calibration.md` | Milestone Spec (标记为 TODO，内含过期 M2 未完成断言) | Pure Milestone (更新为 IN PROGRESS，基础完备，待实机数据) | 6 refs (`Roadmap与里程碑.md`, etc.) | None | Yes (M2 已冻结，阻断过期) | **REWRITE** |
| `page/stackforce/milestone/M4-Locomotion.md` | Milestone Spec (标记为 IN PROGRESS，但底层 M3 尚未完成) | Pure Milestone (修正状态为 TODO / BLOCKED by M3) | 6 refs (`Roadmap与里程碑.md`, etc.) | None | Yes (时序倒置) | **REWRITE** |
| `page/stackforce/milestone/M5-Robustness.md` | Milestone Spec (TODO) | Pure Milestone (TODO, 只引用 G01~G06) | 5 refs | None | No | **REWRITE** |
| `page/stackforce/milestone/M6-Sim-to-Real.md` | Milestone Spec (TODO) | Pure Milestone (TODO, 只引用 G01~G08) | 5 refs | None | No | **REWRITE** |
| **M1 Gate Pages (G01 ~ G10)** | | | | | | |
| `page/stackforce/gate/M1-G01-硬件清点.md` | Gate (混杂旧 outcome 路径) | Pure Gate (Criterion 表直接引 E-DOC/E-HW#Part) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M1-G02-传感器映射.md` | Gate (引旧 Topic/Outcome) | Pure Gate (Criterion 直接引 E-HW-002/E-FW-005#Part) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M1-G03-执行器映射.md` | Gate (标为 BLOCKED by ch7) | Pure Gate (ch7 标为硬件已修复，缺回归测试证据，IN PROGRESS) | 4 refs | None | Yes (stale blocker) | **REWRITE** |
| `page/stackforce/gate/M1-G04-关节标定.md` | Gate (标为 BLOCKED by ch7) | Pure Gate (更新为 IN PROGRESS / MISSING) | 3 refs | None | Yes (stale blocker) | **REWRITE** |
| `page/stackforce/gate/M1-G05-指令定性.md` | Gate (PASS with evidence debt) | Pure Gate (直接引 E-CAL-001/E-FW-001#Part) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M1-G06-控制测频.md` | Gate (PASS with evidence debt) | Pure Gate (直接引 E-TEST-001#P02) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M1-G07-延迟测量.md` | Gate (PASS with evidence debt) | Pure Gate (直接引 E-TEST-001#P02, P03) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M1-G08-尺寸测量.md` | Gate (PASS with evidence debt) | Pure Gate (直接引 E-SIM-002#P01, P03) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M1-G09-质量测量.md` | Gate (PASS with evidence debt) | Pure Gate (直接引 E-SIM-001#P04) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M1-G10-停机验证.md` | Gate (标为 BLOCKED by ch7) | Pure Gate (历史事实归档，当前置为 IN PROGRESS，引 E-TEST-001#P03) | 3 refs | None | Yes (stale blocker) | **REWRITE** |
| **M2 Gate Pages (G01 ~ G08, 保持 8/8 PASS)** | | | | | | |
| `page/stackforce/gate/M2-G01-来源冻结.md` | Gate (PASS, 引旧文档) | Pure Gate (PASS, 直接引 E-DOC-003, E-SIM-001#P01) | 3 refs | None | Yes (旧路径) | **REWRITE** |
| `page/stackforce/gate/M2-G02-拓扑对齐.md` | Gate (PASS, 仍有 legacy 代号) | Pure Gate (PASS, 采用规范构件名，引 E-SIM-001#P01) | 3 refs | None | Yes (名称非标准) | **REWRITE** |
| `page/stackforce/gate/M2-G03-几何对齐.md` | Gate (PASS, 仍含旧说明) | Pure Gate (PASS, 直接引 E-SIM-002#P01, P02) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M2-G04-坐标对齐.md` | Gate (PASS, 引旧 Outcome) | Pure Gate (PASS, 直接引 E-SIM-002#P04) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M2-G05-惯性完备.md` | Gate (PASS, 引旧配置) | Pure Gate (PASS, 直接引 E-SIM-001#P04) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M2-G06-碰撞可用.md` | Gate (PASS, 引旧报告) | Pure Gate (PASS, 直接引 E-VAL-001#P03, P04) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M2-G07-关节可动.md` | Gate (PASS, 含旧代号) | Pure Gate (PASS, 直接引 E-SIM-003#P03, P04) | 3 refs | None | Yes (名称非标准) | **REWRITE** |
| `page/stackforce/gate/M2-G08-Lab载入.md` | Gate (PASS, 引旧报告) | Pure Gate (PASS, 直接引 E-VAL-001#P05, E-VAL-002#P03) | 3 refs | None | Yes | **REWRITE** |
| **M3 ~ M6 Gate Pages** | | | | | | |
| `page/stackforce/gate/M3-G01-激励冻结.md` | Gate (TODO / IN PROGRESS) | Pure Gate (IN PROGRESS, 规范化准则表) | 3 refs | None | Yes | **REWRITE** |
| `page/stackforce/gate/M3-G02-实机采样.md` | Gate (TODO) | Pure Gate (TODO / WAITING_REAL_DATA) | 3 refs | None | No | **REWRITE** |
| `page/stackforce/gate/M3-G03-舵机标定.md` | Gate (TODO) | Pure Gate (TODO / WAITING_REAL_DATA) | 3 refs | None | No | **REWRITE** |
| `page/stackforce/gate/M3-G04-轮机标定.md` | Gate (TODO) | Pure Gate (TODO / WAITING_REAL_DATA) | 3 refs | None | No | **REWRITE** |
| `page/stackforce/gate/M3-G05-接触标定.md` | Gate (TODO) | Pure Gate (TODO) | 3 refs | None | No | **REWRITE** |
| `page/stackforce/gate/M3-G06-响应对齐.md` | Gate (TODO) | Pure Gate (TODO) | 3 refs | None | No | **REWRITE** |
| `page/stackforce/gate/M4-G01 ~ M4-G06` | Gate Pages (TODO) | Pure Gate (统一准则表规范) | 3 refs each | None | No | **REWRITE** |
| `page/stackforce/gate/M5-G01 ~ M5-G06` | Gate Pages (TODO) | Pure Gate (统一准则表规范) | 3 refs each | None | No | **REWRITE** |
| `page/stackforce/gate/M6-G01 ~ M6-G08` | Gate Pages (TODO) | Pure Gate (统一准则表规范) | 3 refs each | None | No | **REWRITE** |
| **Evidence / Source Indexes** | | | | | | |
| `page/stackforce/evidence/evidence-registry.md` | Mixed SSOT Registry (含正文与声明) | Pure Evidence Index (只含索引表与消费方，明确非 SSOT) | 12 refs | docs/evidence/* | Yes (内容冗余) | **INDEX_ONLY** |
| `page/stackforce/evidence/source-inventory.md` | 27行简短来源表 | Pure Source Index (与 _meta/source-inventory.yaml 一致) | 3 refs | docs/refactor/source-inventory.md | Yes (过简) | **INDEX_ONLY** |
| `page/stackforce/evidence/geometry-baseline.md` | 混合事实总结 | Cross-validation 合并入 M2-T03 与 E-SIM-002，归档 | 3 refs | E-SIM-002, M2-T03 | Yes | **ARCHIVE** |
| `page/stackforce/evidence/mechanical-model.md` | 混合事实总结 | Cross-validation 合并入 M2-T02 与 E-SIM-001，归档 | 3 refs | E-SIM-001, M2-T02 | Yes | **ARCHIVE** |
| **Topic Pages** | | | | | | |
| `page/stackforce/topic/T-ACT-001-Canonical-Real-Sim-Component-Identity.md` | Canonical 构件映射 Topic (Golden Topic) | 跨阶段横向构件映射标准 Topic (唯一 SSOT) | 6 refs | M1-T02 | No | **KEEP** |
| `page/stackforce/topic/M1-T01-硬件基线.md` | M1 硬件审计 Topic | 横向硬件架构 Topic | 6 refs | None | No | **KEEP** |
| `page/stackforce/topic/M1-T02-执行器映射.md` | M1 执行器映射 Topic (与 T-ACT-001 重复) | 合并至 T-ACT-001，精简为硬件接线与标定步骤 | 13 refs | T-ACT-001 | Yes (映射重复) | **MERGE** |
| `page/stackforce/topic/M1-T03-传感器数据.md` | 传感器标定 Topic | 横向传感器工程分析 Topic | 6 refs | None | No | **KEEP** |
| `page/stackforce/topic/M1-T04-控制时序.md` | 控制总线与时序 Topic | 横向总线通信与时钟分析 Topic | 8 refs | None | No | **KEEP** |
| `page/stackforce/topic/M1-T05-尺寸质量测量.md` | 物理测量 Topic | 横向尺寸与质量分析 Topic | 6 refs | None | No | **KEEP** |
| `page/stackforce/topic/M1-T06-空间限制.md` | 实验空间说明 | 横向工程测试约束 Topic | 3 refs | None | No | **KEEP** |
| `page/stackforce/topic/M1-现场产物归档.md` | 现场文件索引 | 移入 archive 作为历史归档 | 7 refs | None | Yes | **ARCHIVE** |
| `page/stackforce/topic/M2-T01-资产来源.md` | 资产来源分析 Topic | 横向 CAD/URDF 溯源 Topic | 3 refs | None | No | **KEEP** |
| `page/stackforce/topic/M2-T02-机械拓扑.md` | 机械拓扑分析 Topic | 吸收 mechanical-model 内容，作为横向拓扑分析 Topic | 9 refs | mechanical-model.md | No | **KEEP** |
| `page/stackforce/topic/M2-T03-几何装配.md` | 几何装配分析 Topic | 吸收 geometry-baseline 内容，作为横向几何分析 Topic | 5 refs | geometry-baseline.md | No | **KEEP** |
| `page/stackforce/topic/M2-T04-物理属性.md` | 惯性与材质 Topic | 横向刚体参数分析 Topic | 5 refs | None | No | **KEEP** |
| `page/stackforce/topic/M2-T05-仿真行为.md` | 动力学行为 Topic | 横向仿真烟囱分析 Topic | 4 refs | None | No | **KEEP** |
| `page/stackforce/topic/M2-T06-实验室接入.md` | Isaac Lab 配置 Topic | 横向 Lab 环境集成 Topic | 5 refs | None | No | **KEEP** |
| `page/stackforce/topic/M2-T07-坐标约定.md` | 参考系转换 Topic | 横向坐标系统一 Topic | 4 refs | None | No | **KEEP** |
| `page/stackforce/topic/M2-T08-闭环恢复.md` | 闭环副重构 Topic | 横向闭环约束工程实现 Topic | 6 refs | None | No | **KEEP** |
| `page/stackforce/topic/M3-T01-响应对齐.md` | 动力学标定规划 Topic | 横向 Real↔Sim 动力学对齐 Topic | 10 refs | None | No | **KEEP** |
| `page/stackforce/topic/M4-T01-运动任务.md` | 步态与强化学习任务 Topic | 横向 Locomotion 训练任务分析 Topic | 12 refs | None | No | **KEEP** |
| `page/stackforce/topic/M5-T01-随机化扰动.md` | 域随机化分析 Topic | 横向鲁棒性扰动空间 Topic | 10 refs | None | No | **KEEP** |
| `page/stackforce/topic/M6-T01-部署流程.md` | 真机部署流程 Topic | 横向 Sim2Real 部署与安全审计 Topic | 8 refs | None | No | **KEEP** |
| `page/stackforce/topic/T01-机器人接口.md` | 软件控制抽象 Topic | 横向 API 设计规范 Topic | 8 refs | None | No | **KEEP** |
| `page/stackforce/topic/T02-实验日志.md` | 遥测与日志格式 Topic | 横向数据记录标准 Topic | 8 refs | None | No | **KEEP** |
| `page/stackforce/topic/T03-安全联锁.md` | 安全防护机制 Topic | 横向软硬件联锁分析 Topic | 10 refs | None | No | **KEEP** |
| `page/stackforce/topic/T04-工程边界.md` | 负知识与边界 Topic | 横向边界与反模式排错 Topic | 3 refs | None | No | **KEEP** |
| **Top-Level Views & Meta** | | | | | | |
| `page/stackforce/Roadmap与里程碑.md` | 宏观规划与里程碑总表 | 仅作为 Summary / View，反映最新真实 Gate/Milestone 状态 | 12 refs | None | Yes (含旧数字) | **REWRITE** |
| `page/Home.md` | 门户首页 | 仅作为 Summary / View，严谨描述主从架构，不内嵌真值 | 15 refs | None | Yes (含旧架构描述) | **REWRITE** |
| `page/_Sidebar.md` | 全局侧边栏导航 | 侧边栏导航链接 | 1 ref | None | Yes | **REWRITE** |
| `page/_META.md` | Wiki 元数据与政策 | 明确单一认识论原则与 Evidence 规范 | 2 refs | None | No | **KEEP** |
| `_meta/status.yaml` | 机器可读状态 SSOT | 唯一机器可读状态真源，与 Gate 完全对齐 | 3 refs | None | Yes (旧数据) | **REWRITE** |
| **Historical Archive & Refactor Docs** | | | | | | |
| `page/stackforce/archive/C6-registration-history.md` | 历史注册尝试记录 | Historical Archive | 2 refs | None | No | **KEEP** |
| `page/stackforce/archive/M2-reverse-engineering.md` | 历史逆向推导记录 | Historical Archive | 2 refs | None | No | **KEEP** |
| `page/stackforce/archive/重构迁移索引.md` | 历史迁移记录 | Historical Archive | 2 refs | None | No | **KEEP** |
| `page/stackforce/refactor/*` | 重构过程产物 | 归档 / 移入 docs/refactor 统一维护 | 4 refs | docs/refactor/* | Yes | **ARCHIVE** |

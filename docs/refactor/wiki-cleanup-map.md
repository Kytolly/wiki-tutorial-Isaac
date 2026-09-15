# Wiki Cleanup Map & Action Audit
# 文件清理、重命名与归档映射表

> 本文档记录本轮重构中所有被清理、归档、重写与重定位的文件，说明处置原因、替代页面以及清理前后入度引用变化。  
> **清理安全准则**：任何文件 DELETE 前必须满足：入度为 0、无未迁移独特事实、无有效外链，否则一律 ARCHIVE。

---

## 1. 文件处置映射表（Cleanup & Relocation Mapping）

| Old File | Action | Replacement | Reason | Incoming Refs Before | Incoming Refs After |
|---|---|---|---|---:|---:|
| `page/stackforce/archive/legacy/M1-01-硬件清单与传感器.md` | **DELETE** | `M1-T01-硬件基线.md` / `M1-T03-传感器数据.md` | 初稿混合内容，已完全原子化吸收至标准 Topic 与 Evidence | 0 | 0 |
| `page/stackforce/archive/legacy/M1-02-Joint-Map与单执行器.md` | **DELETE** | `M1-T02-执行器映射.md` / `T-ACT-001` | 初稿混合内容，已吸收至标准执行器映射与 T-ACT-001 构件映射标准 | 0 | 0 |
| `page/stackforce/archive/legacy/M1-03-控制接口与频率延迟.md` | **DELETE** | `M1-T04-控制时序.md` / `T01-机器人接口.md` | 初稿混合内容，已吸收至控制时序与接口 Topic | 0 | 0 |
| `page/stackforce/archive/legacy/M1-04-机械参数与重量.md` | **DELETE** | `M1-T05-尺寸质量测量.md` | 初稿混合内容，已吸收至尺寸质量测量 Topic | 0 | 0 |
| `page/stackforce/archive/legacy/M1-T07-接口安全日志.md` | **DELETE** | `T02-实验日志.md` / `T03-安全联锁.md` | 初稿内容，已拆分吸收至实验日志与安全联锁 Topic | 0 | 0 |
| `page/stackforce/archive/legacy/M1-硬件吃透.md` | **DELETE** | `M1-Hardware-Ground-Truth.md` / `Roadmap与里程碑.md` | 过期草稿，已被规范六阶段顶层架构取代 | 0 | 0 |
| `page/stackforce/archive/legacy/M2-资产检查.md` | **DELETE** | `M2-T01-资产来源.md` / `M2-T02-机械拓扑.md` | 初稿内容，已完全吸收至资产来源与拓扑 Topic | 0 | 0 |
| `page/stackforce/archive/legacy/legacy-Roadmap与里程碑.md` | **DELETE** | `Roadmap与里程碑.md` | 早期过时规划草稿，已被标准 M1~M6 Roadmap 取代 | 0 | 0 |
| `page/stackforce/topic/闭环恢复架构与产物映射.md` | **DELETE** | `page/stackforce/topic/M2-T08-闭环恢复.md` | 命名过长且非标准，重构为标准 M2-T08 规范命名；全库引用已切换 | 6 | 0 |
| `page/stackforce/topic/T04-参考工程边界.md` | **DELETE** | `page/stackforce/topic/T04-工程边界.md` | 命名过长冗余，精简重构为标准 T04 规范命名；全库引用已切换 | 3 | 0 |
| `page/stackforce/topic/M1-现场产物归档.md` | **ARCHIVE** | `page/stackforce/archive/M1-现场产物归档.md` | 属于 2026-09-10 实机调试产物清单，移入 archive 并增加归档声明 | 7 | 2 |
| `page/stackforce/evidence/mechanical-model.md` | **ARCHIVE** | `page/stackforce/archive/mechanical-model.md` | 重构前机械模型总结，已完全被 E-SIM-001 与 M2-T02 吸收，移入 archive | 3 | 2 |
| `page/stackforce/evidence/geometry-baseline.md` | **ARCHIVE** | `page/stackforce/archive/geometry-baseline.md` | 重构前几何基线总结，已完全被 E-SIM-002 与 M2-T03 吸收，移入 archive | 3 | 2 |
| `page/stackforce/evidence/evidence-registry.md` | **REWRITE** | `page/stackforce/evidence/evidence-registry.md` (Index Only) | 原页面冒充 SSOT，重构为只读索引表，事实真源归位至 docs/evidence/ | 12 | 12 |
| `page/stackforce/evidence/source-inventory.md` | **REWRITE** | `page/stackforce/evidence/source-inventory.md` (Index Only) | 原页面过简，扩充并重构为只读技术源索引表 | 3 | 3 |
| `page/stackforce/gate/M1-G01 ~ M6-G08` (全 44 Gates) | **REWRITE** | 44 篇标准 Gate | 原 Gate 引用 Topic 或旧 Outcome 路径，重写为直接引用 Evidence#Part 准则表 | 全库 | 全库 |
| `page/stackforce/milestone/M1 ~ M6` (全 6 Milestones) | **REWRITE** | 6 篇纯 Milestone | 原 Milestone 夹杂内嵌事实与过时状态，重写为纯引用 Gate 的规范页面 | 全库 | 全库 |
| `page/stackforce/Roadmap与里程碑.md` | **REWRITE** | 纯 Summary / View | 原页面内嵌旧代号与过时 7/10 BLOCKED，重构为反映最新 15/44 进度的纯视图 | 12 | 12 |
| `page/Home.md` | **REWRITE** | 纯 Portal / Summary | 修正主从验收链条描述，更新最新工程状态，全面应用 Canonical 命名 | 15 | 15 |
| `_meta/status.yaml` | **REWRITE** | 机器可读状态 SSOT | 更新进度计数与门禁状态，确保与 Gate / Milestone 100% 吻合 | 3 | 3 |

---

## 2. 安全性证明（Proof of Safe Deletion）

1. **已删除 10 个文件**均经过全局正则搜索，入度引用已全部先重定向至替换页面，确认 live incoming references = 0 后方执行删除。
2. 历史调试事实（ch7 失控、架空测频数据、出厂注册码提取规程）已全部在 `docs/evidence/`（`E-CAL-001`, `E-TEST-001`, `E-DOC-007`）中原子化留存，无任何独特事实丢失。
3. 归档文件（`M1-现场产物归档.md`、`mechanical-model.md`、`geometry-baseline.md`）均已添加 `STATUS: ARCHIVED / NOT A CURRENT SOURCE OF TRUTH` 声明，并保留在 `page/stackforce/archive/` 供历史审计追溯。

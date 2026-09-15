# 最终语义收敛、M3 门禁能力重构与 Wiki 架构正式冻结报告
## (Final Semantic Cleanup, Capability-Oriented M3 Gates & Architecture Freeze Report)

> **报告发布日期**：2026-09-16  
> **执行依据**：[`skill-wiki-design`](../../.agents/skills/skill-wiki-design/SKILL.md) 全套规范  
> **核心结论**：全库语义清理、认识论解耦、执行器规范命名收口、横向 Topic 整合与 M3 动力学校验能力门禁重构已全面完成。文档体系结构稳定，即日起**正式冻结 Wiki 信息架构（Wiki Architecture Frozen）**，转入日常增量维护阶段。

---

## 1. 架构执行总览（Executive Summary）

本轮重构严格在已确立的五层垂直流与横向分析层信息架构下执行，彻底完成了全库最后一公里的语义收敛与认识论规范化：

```text
Layer 0: Raw Source / Artifact (图纸 / 代码 / 资产 / 测量表 / 物理日志)
           ↓
Layer 1: Evidence Document (docs/evidence/ 下全部 26 篇规范化事实文件)
           ↓
Layer 2: Evidence#Part (原子工程事实，强制 Raw Source Faithful Reproduction)
           ↓
Layer 3: Gate Acceptance Criterion (134 项准则，100% 直接引用 Evidence#Part)
           ↓
Layer 4: Milestone (聚合 Gate，进度看板与路线图推进，当前 15 / 44 Gates PASS)

横向分析层（Horizontal Layer）：
Evidence#Part ─┐
Evidence#Part ─┼─→ Topic (全局领域契约 T-ACT-001/002, T-HW-REG-001 及阶段工作视图)
Evidence#Part ─┘   (跨源交叉比对 / 契约定义 / 冲突审计；非 Gate 准则前置依赖)
```

---

## 2. 证据状态与认识论角色解耦（Evidence Status & Epistemic Role Normalization）

### 2.1 生命周期状态与认识论角色彻底解耦
依据 `skill-wiki-design/references/evidence-semantics.md`，彻底纠正了此前将“验证结果”或“实现定性”错填入 `status` 字段的非规范行为：
- **`status` 规范化**：全库 26 篇 Evidence 的生命周期状态严格限定为 `VALID`（经工程审计真实、客观、出处可溯的正式证据）。失败的实验记录（如 `E-CAL-001` 记录 Channel 7 失控）同样属于 `VALID` 证据，不粉饰历史。
- **`epistemic_role` 独立定性**：在 Frontmatter 及索引表中独立设立 `epistemic_role`，严格按认知强度划分为 6 大标准角色：
  - `DOC_SPEC`：原厂图纸与规范指南（`E-DOC-001`~`007`, `E-HW-001`~`004`，共 11 篇）；
  - `IMPLEMENTATION`：固件代码与自动化后处理实现（`E-FW-001`~`008`, `E-SIM-003`，共 9 篇）；
  - `CONFIGURATION`：刚体拓扑与几何装配配置（`E-SIM-001`~`002`，共 2 篇）；
  - `RUNTIME`：台架测试运行与通信测频（`E-TEST-001`，共 1 篇）；
  - `PHYSICAL`：实机动作隔离与故障阻断记录（`E-CAL-001`，共 1 篇）；
  - `VALIDATION`：动静态模型校验与烟囱测试（`E-VAL-001`~`002`，共 2 篇）。

### 2.2 索引表升级
更新 [`page/stackforce/evidence/evidence-registry.md`](../../page/stackforce/evidence/evidence-registry.md)，确立其为只读索引（Index Only），明确各分部（Parts）与上层 Gate 消费关系。

---

## 3. 横向 Topic 整合与标定契约确立（Topic Consolidation）

### 3.1 领域专题与阶段工作视图分层
依据 [`docs/refactor/topic-consolidation-map.md`](topic-consolidation-map.md)，正式将 Topic 划分为：
1. **Domain-based Horizontal Topics（全局领域专题）**：
   - **`T-ACT-001`**：全机 12 执行器规范命名、PCA 通道、代码变量到仿真关节唯一映射源（SSOT）；
   - **`T-ACT-002`**：**[NEW]** 形式化确立舵机坐标映射仿射方程 $u_j = u_{0, j} + s_j \cdot k_j \cdot q_j$、8 舵机实测/未决旋向极性、出厂预设偏置与 Channel 7 硬件故障阻断审计；
   - **`T-HW-REG-001`**：双芯片架构、S1 注册码获取机制与 eFuse MAC 设备指纹提取链路；
   - **`T01`~`T04`**：机器人接口、实验日志、安全联锁与工程边界。
2. **Milestone Analysis Working Views（里程碑工作视图）**：
   - `M1-T01`~`M1-T06`、`M2-T01`~`M2-T08`、`M3-T01` 等聚焦各里程碑具体测试规程与实施细节。

### 3.2 `M1-T02` 消除重复与 SSOT 委托
- 移除 `M1-T02` 中与 `T-ACT-001` 重复的命名表格与映射字典；
- 在 `M1-T02` 头部明确将构件映射委托至 `T-ACT-001`、将标定契约委托至 `T-ACT-002`；
- `M1-T02` 正文完全聚焦于 Stack B PCA9685PW 板级接线与架空单执行器微步阶跃测试金字塔规程。

---

## 4. 彻底清除残留模糊构件术语（Canonical Terminology Enforcement）

### 4.1 当前工程正文全面规范化
对全库工程 prose 进行穷尽式审计与清理：
- 严格杜绝在当前工程描述中使用模糊代号（如 `M1/M2` 混用舵机/里程碑、`P1/P2` 混用膝关节、`W1/W2` 代替闭环副）；
- 全面统一使用冻结的规范命名：
  - **8 腿部舵机**：`{LEG}_{BRANCH}_Servo`（如 `FR_Outer_Servo`, `FL_Inner_Servo`）；
  - **4 轮电机**：`{LEG}_Wheel_Motor`（如 `FR_Wheel_Motor`）；
  - **12 主动驱动关节**：`{LEG}_{BRANCH}_Hip_Joint`, `{LEG}_Wheel_Joint`；
  - **8 被动膝关节**：`{LEG}_{BRANCH}_Knee_Joint`（`PASSIVE`）；
  - **4 闭环约束副**：`{LEG}_Closure_Joint`（`LOOP_CLOSURE`，PhysX RevoluteJoint）。

### 4.2 原始物料与出处代号的审慎保留
- 在原始图纸、固件代码逐行摘录、日志原样复刻及 CAD 几何配置（如 `closure_frames.json` 中定义的三维参考系 `refa:W1`, `refb:W2`, `P1`, `P2`）中，严格保留原始物料字面原貌，并在其旁标注规范构件对照；
- 明确区分工程里程碑代号（`Milestone M1`, `M2`, `M1–M6`）与历史构件代号。

---

## 5. M3 门禁准则能力导向重构（Capability-Oriented M3 Gates）

针对此前 M3 门禁存在“过度规定模型具体实现数学形式”（如强行限定一阶传递函数、硬编码相电阻/力矩常数、限定库仑摩擦角）的学术化缺陷，依据物理辨识与强化学习真实需求，将 M3-G01～G06 重构为纯**能力导向（Capability-Oriented）**验收准则：

### 5.1 M3-G01 激励冻结（15 项全要素实验契约）
- `C01`~`C03`：执行器身份、闭链仿真基线、仿射映射方程形式冻结（**PASS**）；
- `C04`~`C07`：舵机动态激励协议、安全量程限制（`TBD_SAFE_RANGE`）、轮机 Mode 4 纯力矩指令语义与转速饱和保护协议冻结；
- `C08`~`C12`：确定性复位规程、微秒级实机遥测 Schema、仿真 SI 单位 Schema、镜像坐标约定与 500ms 看门狗紧急停机联锁协议冻结；
- `C13`~`C15`：定量评估指标（RMSE / Peak Lag）、70%/30% 辨识与留出切分策略、原始数据不可篡改存证（SHA-256）规程冻结。
- **状态**：`IN PROGRESS`。

### 5.2 M3-G02 实机采样（高保真数据集准则）
- `C01`~`C05`：物理台架环境可复现记录、微秒级多源时间戳对齐与极低丢包率（<0.1%）、原始文件只读不可篡改哈希存证、严格划分辨识集与留出集、仿真对应轨迹并行生成对齐。
- **状态**：`TODO`。

### 5.3 M3-G03 舵机动力学（有效预测模型准则）
- `C01`~`C04`：在有效工作区间内建立具备充分预测能力的动态响应模型（不限模型形式）；独立样本交叉验证杜绝过拟合；形式化归档开环特性、缺乏编码器回读与速度饱和等物理局限；Isaac Lab 执行器配置注入与数值解算稳定。
- **状态**：`TODO`。

### 5.4 M3-G04 轮机动力学（Mode 4 力矩响应准则）
- `C01`~`C04`：建立从输入指令到力矩/角加速度/转速的有效预测模型；严格维持 Mode 4 直接力矩控制语义（杜绝降级为速度源）；准确刻画转子等效惯量与反电动势阻尼；准确映射母线电压跌落与饱和限制。
- **状态**：`TODO`。

### 5.5 M3-G05 接触动力学（轮地交互响应准则）
- `C01`~`C03`：测定并对齐法向支撑刚度、滑移发生临界条件与牵引力演化趋势（不局限于单一库仑摩擦）；材质交互模型准确预测附着力转化；着地冲击过渡数值稳定无异常穿透。
- **状态**：`TODO`。

### 5.6 M3-G06 响应对齐（Hold-out 系统级终验准则）
- `C01`~`C03`：候选参数集在验证前全局锁定；在未见过的留出激励轨迹（Unseen Traces）下综合误差优于门禁阈值；出具动力学资质报告，并基于全栈证据独立重新评估 `rl_ready` 状态（杜绝盲目放行）。
- **状态**：`TODO`。

---

## 6. 文件系统与归档规范化（File Cleanup & Reorganization）

1. **消除冗余临时目录**：
   - 清理已完成过渡使命的 `page/stackforce/refactor/` 目录；
   - 构件迁移过程资产移入 `page/stackforce/archive/canonical-migration/` 安全归档；
   - 确保 `page/` 目录内仅包含正式面向用户的 Wiki 文档与归档物料。
2. **新增工程视图工件**：
   - 创建 [`page/stackforce/topic/M3-TODO-view.md`](../../page/stackforce/topic/M3-TODO-view.md)，四象限清晰解耦：
     - `[DONE]`：12 执行器命名、M2 资产、映射契约等已固化基线；
     - `[OFFLINE TODO]`：仿真端激励发生脚本、定量评估算法、参数化配置模板（可立即离线开发）；
     - `[REAL-ROBOT TODO]`：**Channel 7 故障检修（TOP BLOCKER）**、架空阶跃测试、极性与零位实测、高频数据采集；
     - `[WAITING FOR DATA]`：舵机/轮机/接触模型参数辨识与 Hold-out 终验。

---

## 7. 全局验证与指标统计（Verification & Validation Metrics）

- **构建与链接检查**：
  - `python3 script/build.py` 执行成功，页面拍平构建正常；
  - `mkdocs build -f script/mkdocs.yml` 编译成功，退出码为 `0`；
  - 站点本地预览与导航树无死链、无坏链。
- **门禁与里程碑宏观指标**：
  - **总里程碑数量**：6 个（M1–M6）
  - **总门禁数量**：44 个
  - **门禁状态分布**：
    - `M1 Hardware Ground Truth`：**7 / 10 PASS (IN PROGRESS)**（受 Channel 7 硬件故障阻断）
    - `M2 Simulation Asset`：**8 / 8 PASS (PASS)**（单父树闭链资产完全冻结）
    - `M3 Dynamics Calibration`：**0 / 6 PASS (IN PROGRESS)**（实验契约冻结中）
    - `M4 Locomotion`：**0 / 6 PASS (TODO)**
    - `M5 Sim-to-Real Robustness`：**0 / 6 PASS (TODO)**
    - `M6 Deployment & Verification`：**0 / 8 PASS (TODO)**
    - **全系统总进度**：**15 / 44 Gates PASS**
  - **总验收准则数量**：134 项（100% 单向直接追溯至 `Evidence#Part`，零 Topic 依赖倒置）。

---

## 8. 架构正式冻结声明（Declaration of Architecture Freeze）

经本轮严格审查与语义收口：
1. **证据架构完全冻结**：垂直流 `Source → Evidence → Evidence#Part → Gate Criteria → Gate → Milestone` 严密闭环，禁止倒置；
2. **构件命名完全冻结**：12 执行器、12 主动关节、8 被动膝关节与 4 闭环约束副的规范英文术语为工程唯一真值；
3. **认识论定性完全冻结**：证据状态生命周期严格采用 `DRAFT / VALID / SUPERSEDED / INVALID`，认识论角色严格采用 `DOC_SPEC / IMPLEMENTATION / CONFIGURATION / RUNTIME / PHYSICAL / VALIDATION`；
4. **M3 门禁重构完成**：全面升级为能力导向准则，消除了过早的技术实现假设。

**即日起，StackForce / Isaac Wiki 信息架构正式冻结（Wiki Architecture Frozen）。后续工程工作全面聚焦于实机 Channel 7 故障排查修复、高频遥测数据采集与 M3 动力学参数辨识执行！**

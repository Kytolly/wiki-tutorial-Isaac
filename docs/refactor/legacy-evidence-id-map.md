# Legacy Evidence ID Migration Map

> 本文档根据 Wiki 架构规范重构，建立历史 Evidence 标识符（`E-MECH-*`, `E-ASSET-*`, `E-PHYS-*`, `E-RL-*` 等）向当前标准原子证据（`E-DOC-*`, `E-HW-*`, `E-FW-*`, `E-SIM-*`, `E-VAL-*`, `E-TEST-*`, `E-CAL-*`）的映射字典。  
> **使用约束**：Current Gate / Milestone / Roadmap / Home 严禁继续引用 Legacy ID，必须直接引用 Current Evidence#Part。Legacy ID 仅保留于历史归档与本迁移字典中。

---

## 1. 核心映射表（Legacy Evidence ID Mapping）

| Legacy ID | 历史声明与主题 | Current Evidence ID | Target Evidence Document | Target Part | Migration Status | Notes |
|---|---|---|---|---|---|---|
| `E-MECH-001` | 双支链五杆闭链机构基线与杆长真值（60/100/40mm） | `E-SIM-002` | 双支链闭环几何装配不变量与参考系配置 | `P01`, `P03`, `P04` | **MIGRATED** | CAD/Metrology 装配公差与底盘对称镜像变换已在 E-SIM-002 中原子化。 |
| `E-MECH-002` | 20 树关节 / 12 主动驱动 / 8 被动铰接 / 4 闭环约束 | `E-VAL-001`<br>`E-SIM-001` | 仿真资产静态执行器与被动关节空间划分校验报告<br>闭链机器人单父树 Loop-Cut 规范 URDF 资产 | `E-VAL-001#P01`<br>`E-VAL-001#P02`<br>`E-SIM-001#P01`<br>`E-SIM-001#P03` | **MIGRATED** | 拓扑驱动/被动划分、动作空间纯洁性由 E-VAL-001 断言，URDF 树由 E-SIM-001 记录。 |
| `E-ASSET-001` | 单父树 Loop-Cut 规范 URDF（29 links, 28 joints） | `E-SIM-001` | 闭链四足轮腿机器人单父树URDF资产 | `P01`, `P02` | **MIGRATED** | 严格单父有向无环树与 W2 处显式 loop-cut 切断。 |
| `E-ASSET-002` | 闭环参考系几何元数据（closure_frames.json） | `E-SIM-002` | 双支链闭环几何装配不变量与参考系配置 | `P01`, `P02` | **MIGRATED** | 包含 W1/W2 轴向偏置 $-44.950\text{ mm}$ 与径向残差 $< 1.83 \times 10^{-17}\text{ m}$。 |
| `E-ASSET-003` | PhysX 闭环转动副重构算法与生成 USD | `E-SIM-003` | PhysX闭环副自动重构与USD后处理实现 | `P01`, `P03`, `P04` | **MIGRATED** | `UsdPhysics.RevoluteJoint` 注入与 `excludeFromArticulation=true` 配置。 |
| `E-ASSET-004` | 静态资产自动化门禁校验器（validate_asset.py） | `E-VAL-001` | 仿真资产静态执行器与被动关节空间划分校验报告 | `P05` | **MIGRATED** | 16 项自动化静态断言全部通过（Exit code 0）。 |
| `E-PHYS-001` | 2400 步 CPU 悬空下沉重力验证报告 | `E-VAL-002` | 强化学习闭环约束收敛与悬空重力烟囱测试报告 | `P02`, `P03` | **MIGRATED** | 2400 步（10.0s）仿真位移 $0.0906\text{ m}$，漂移 $\le 0.0595\text{ mm}$。 |
| `E-PHYS-002` | 负对照实验（禁用闭环副导致 129mm 漂移崩溃） | `E-VAL-002` | 强化学习闭环约束收敛与悬空重力烟囱测试报告 | `P05` | **MIGRATED** | 禁用闭环副在 480 步触发 `RuntimeError` 崩溃，确证约束物理有效性。 |
| `E-RL-001` | 强化学习未就绪边界（rl_ready = false） | `E-VAL-002` | 强化学习闭环约束收敛与悬空重力烟囱测试报告 | `P01`, `P05` | **MIGRATED** | 驱动器动力学/阻尼未标定，碰撞与接触未通过动力学验收。 |
| `E-HW-001` (Legacy) | 实机架空审计与 Channel 7 安全断电门禁 | `E-CAL-001`<br>`E-TEST-001` | 实机执行器单通道动作隔离与故障阻断记录<br>实机架空通信时序与固件超时停机测定 | `E-CAL-001#P04`<br>`E-CAL-001#P05`<br>`E-TEST-001#P05` | **MIGRATED** | 旧名称与硬件原理图 `E-HW-001` 重名冲突；历史故障事实已移入 E-CAL-001 与 E-TEST-001。 |
| `E-CANON-001` | Canonical component identity migration | `E-SIM-001`<br>`E-VAL-001` | 闭链四足轮腿机器人单父树URDF资产<br>仿真资产静态执行器与被动关节空间划分校验报告 | `E-SIM-001#P01`<br>`E-VAL-001#P01` | **MIGRATED** | 构件命名确定性映射规范，详见 `_meta/canonical_actuator_map.yaml`。 |

---

## 2. 消费方迁移指引（Consumer Migration Checklist）

- [x] 所有 Gate 验收准则（Criteria）已切换为引用 Current Evidence#Part（如 `E-SIM-001#P01`）。
- [x] Milestone 页面仅引用 Gate，不再直接挂载 Legacy ID。
- [x] Evidence Registry 已降级为只读索引（`Evidence Index`），移除非标准 Legacy 词条。
- [x] 当前工程正文全面消除 Legacy ID。

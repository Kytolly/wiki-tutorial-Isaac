# M2-G08 — Lab 载入

## Status

PASS

## Objective

在 Isaac Sim / Lab 环境完成自动化门禁校验与 2400 步 CPU 悬空重力烟囱测试。

## Acceptance Criteria

| Criterion ID | Requirement | Required | Evidence#Part | Status | Notes |
|---|---|---:|---|---|---|
| `M2-G08-C01` | 16 项静态自动化校验工具全绿通过（Exit Code 0） | Yes | `E-VAL-001#P05` | **PASS** | 树拓扑、网格存在性与闭环残差校验全绿。 |
| `M2-G08-C02` | 2400 步 CPU 悬空重力烟囱测试通过（最大锚点漂移 <= 0.0595mm） | Yes | `E-VAL-002#P02`<br>`E-VAL-002#P03` | **PASS** | 10 秒连续重力下沉无发散，远优于 1mm 门禁标准。 |
| `M2-G08-C03` | 禁用闭环副负对照组在 480 步漂移 129mm 崩溃并抛出异常 | Yes | `E-VAL-002#P05` | **PASS** | 确凿证实闭环保持力源于 PhysX 约束而非初始位姿巧合。 |
| `M2-G08-C04` | 明确资产未完成驱动器动力学标定边界（rl_ready = false） | Yes | `E-VAL-002#P01`<br>`E-VAL-002#P05` | **PASS** | 约束完备但不具备强化学习直接训练就绪状态。 |

## Related Topics

- [[M2-T06-实验室接入]] — M2-T06-实验室接入
- [[M2-T08-闭环恢复]] — M2-T08-闭环恢复
- [[T04-工程边界]] — T04-工程边界

## Changelog / 更新日志

- 2026-09-15：重构为标准 Gate 规范；直接引用 Evidence#Part 原子凭证；解耦 Related Topics；严格依据 Acceptance Criteria 重算 Gate 状态。

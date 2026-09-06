# M5 — Robustness

## Goal

让运动策略在定义范围内的模型误差、观测误差、延迟和外部扰动下仍然有效。

## Progress

- [ ] [[M5-G01-范围冻结]] — TODO
- [ ] [[M5-G02-参数随机]] — TODO
- [ ] [[M5-G03-观测扰动]] — TODO
- [ ] [[M5-G04-延迟注入]] — TODO
- [ ] [[M5-G05-推扰恢复]] — TODO
- [ ] [[M5-G06-泛化达标]] — TODO

Progress: 0 / 6 Gates PASS

## Current TODO

- [ ] 用 M1/M3 数据确定质量、摩擦、执行器、噪声和延迟范围。
- [ ] 将随机化和扰动配置纳入可复现训练与评测。
- [ ] 在未见参数组合上建立独立测试集。

## Blockers

- M3 未提供经过校准的 nominal 参数与误差范围。
- 当前没有鲁棒性评测结果。

## Exit Criteria

- 六个 Gate 全部 PASS。
- 在冻结的不确定性范围内，策略达到 M4 的运动性能阈值。
- 训练和评测随机种子、范围、指标及结果均已归档。

## Status

TODO

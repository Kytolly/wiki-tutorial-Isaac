# M6 — Sim-to-Real

## Goal

让仿真训练策略安全、稳定地运行在真实 StackForce 机器人上，并完成定义好的目标任务。

## Progress

- [ ] [[M6-G01-观测对齐]] — BLOCKED
- [ ] [[M6-G02-动作对齐]] — BLOCKED
- [ ] [[M6-G03-安全联锁]] — TODO
- [ ] [[M6-G04-影子推理]] — TODO
- [ ] [[M6-G05-悬空执行]] — TODO
- [ ] [[M6-G06-实机站立]] — TODO
- [ ] [[M6-G07-实机平衡]] — TODO
- [ ] [[M6-G08-实机运动]] — TODO

Progress: 0 / 8 Gates PASS

## Current TODO

- [ ] 定义同构的 observation/action 接口和版本。
- [ ] 实现独立于策略的限幅、超时、倾倒保护和急停。
- [ ] 按影子推理、悬空、站立、平衡、低速运动逐级测试。

## Blockers

- M1 尚未冻结实机观测和动作语义。
- M4/M5 尚未提供可部署且经过鲁棒性评测的策略。

## Exit Criteria

- 八个 Gate 全部 PASS。
- 策略在真实机器人上完成目标运动任务。
- 每一级实机测试都有日志、限幅和可回退方案。

## Status

TODO

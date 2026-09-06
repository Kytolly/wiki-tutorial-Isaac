# M1 — Hardware Ground Truth

## Goal

建立能够准确、可复现描述真实 StackForce 机器人的硬件基线。

## Progress

- [ ] [[M1-G01-硬件清点]] — IN PROGRESS
- [ ] [[M1-G02-传感器映射]] — IN PROGRESS
- [ ] [[M1-G03-执行器映射]] — IN PROGRESS
- [ ] [[M1-G04-关节标定]] — TODO
- [ ] [[M1-G05-指令定性]] — IN PROGRESS
- [ ] [[M1-G06-控制测频]] — TODO
- [ ] [[M1-G07-延迟测量]] — TODO
- [ ] [[M1-G08-尺寸测量]] — TODO
- [ ] [[M1-G09-质量测量]] — TODO
- [ ] [[M1-G10-停机验证]] — TODO

Progress: 0 / 10 Gates PASS

## Current TODO

- [ ] 将源码级结论与实体设备逐项核对。
- [ ] 完成 U01–U17 实机验证并把结果写入基线。
- [ ] 记录尺寸、质量、控制频率、延迟和抖动。

## Blockers

- U01–U10 未解决前，关节坐标、传感器坐标和动作量程不能冻结。
- 当前没有实机测量记录，无法把源码事实升级为完整 Ground Truth。

## Exit Criteria

- 十个 Gate 全部 PASS。
- 所有硬件、传感器、执行器和通信字段都有来源或测量证据。
- U01–U17 不再有未归属的 UNKNOWN。

## Status

IN PROGRESS

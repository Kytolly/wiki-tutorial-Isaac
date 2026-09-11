# M1 — Hardware Ground Truth

## Goal

建立能够准确、可复现描述真实 StackForce 机器人的硬件基线。

## Progress

- [x] [[M1-G01-硬件清点]] — PASS / CLOSED
- [x] [[M1-G02-传感器映射]] — PASS / CLOSED
- [ ] [[M1-G03-执行器映射]] — BLOCKED（ch7 failure；sign table 不完整）
- [ ] [[M1-G04-关节标定]] — BLOCKED（ch7 物理回中失败）
- [x] [[M1-G05-指令定性]] — PASS WITH EVIDENCE DEBT
- [x] [[M1-G06-控制测频]] — PASS WITH EVIDENCE DEBT
- [x] [[M1-G07-延迟测量]] — PASS WITH EVIDENCE DEBT
- [x] [[M1-G08-尺寸测量]] — PASS WITH EVIDENCE DEBT
- [x] [[M1-G09-质量测量]] — PASS WITH EVIDENCE DEBT
- [ ] [[M1-G10-停机验证]] — BLOCKED（ch7 hardware/mechanical return failure）

Progress: 7 / 10 Gates closed

## Evidence Snapshot

M1 已完成两次可审计的架空现场 session：硬件/firmware、IMU、command、timing、代表性 latency 与首版 kinematic geometry 均形成可用合同；ch7 回中异常使 powered actuation 仍被禁止。

| Gate | 已完成的静态证据 | 仍需关闭的验收项 |
|---|---|---|
| [[M1-G01-硬件清点]] | 双控制栈身份、S1/S3 firmware、注册码、build/flash/boot 与恢复路径 | rear S1 独立可复现 build 仍是 recovery debt |
| [[M1-G02-传感器映射]] | IMU frame/sign/units；175.3 Hz timing；feedback availability | 已关闭 |
| [[M1-G03-执行器映射]] | 8 servo identity/offset；ch4/5/6=CW/CCW/CW；代表性 wheel movement | 修复 ch7/8；补齐 servo/wheel sign 与 rear feedback sign |
| [[M1-G04-关节标定]] | degree API、PCA mapping、本机 offset、70–150 mm task-space region | ch7/ch8 return validation；精确极限延后 |
| [[M1-G05-指令定性]] | servo position-style、wheel torque-mode、CAN/feedback boundary | wheel SI scale 未标定 |
| [[M1-G06-控制测频]] | IMU mean 5.704 ms / 175.3 Hz，jitter 0.790 ms | Device02/Serial2/PPM 精确 rate 未测 |
| [[M1-G07-延迟测量]] | 0.5 s response bound；501.535–502.498 ms automatic stop | 精确 onset 与逐通道分布未测 |
| [[M1-G08-尺寸测量]] | real five-bar graph；60/100/100/60/40 mm nominal geometry | exact assembled metrology 未做 |
| [[M1-G09-质量测量]] | prior/unknown 分类和 fidelity impact 已冻结 | real mass/inertia/CoM/dynamics 未标定 |
| [[M1-G10-停机验证]] | current-source freshness/timeout；baseline restore；实机 stop evidence | ch7 在 firmware return/STOP 后仍上抬 |

G06–G10 的横向结论见 [[M1-G06-G10-static-summary]]。

## Current TODO

- [x] 完成 G01–G10 的源码级静态合同与验收边界审计。
- [x] 冻结目标 firmware 的构建、烧录、启动和恢复基线。
- [x] 完成 IMU 注册、timing 与代表性 actuator response/stop 测量。
- [ ] 隔离、维修 ch7/ch8，并通过 unloaded/installed tiny return test。
- [ ] 安全恢复后补齐 servo/wheel polarity 与 feedback sign。

## Blockers

- ch7 在 firmware return 与显式 STOP 后仍持续上抬；ch8 可能受闭链被动带动。
- actuator rail 必须保持断电，禁止真机 RL、落地 locomotion 或扩大动作范围。
- 最终 real-action adapter 仍缺 servo/wheel polarity 与 feedback sign。

## Exit Criteria

- 十个 Gate 全部 PASS。
- 所有硬件、传感器、执行器和通信字段都有来源或测量证据。
- U01–U17 不再有未归属的 UNKNOWN。

## Status

BLOCKED

## 更新日志

- 2026-09-11：同步两次 2026-09-10 架空 session；M1 更新为 7/10 closed，并以 ch7 安全异常保持 BLOCKED。
- 2026-09-08：新增逐 Gate Evidence Snapshot，汇总静态交付和剩余实机验收项。
- 2026-09-08：同步 M1-G01–G10 静态审计；总 PASS 保持 0/10，并记录 G10 P0 安全缺口。

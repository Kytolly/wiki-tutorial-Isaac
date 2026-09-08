# M1 — Hardware Ground Truth

## Goal

建立能够准确、可复现描述真实 StackForce 机器人的硬件基线。

## Progress

- [ ] [[M1-G01-硬件清点]] — IN PROGRESS
- [ ] [[M1-G02-传感器映射]] — IN PROGRESS
- [ ] [[M1-G03-执行器映射]] — BLOCKED（静态合同完成，待真机 identity）
- [ ] [[M1-G04-关节标定]] — BLOCKED（静态合同完成，待 firmware baseline 与真机标定）
- [ ] [[M1-G05-指令定性]] — IN PROGRESS
- [ ] [[M1-G06-控制测频]] — IN PROGRESS（静态时序完成）
- [ ] [[M1-G07-延迟测量]] — IN PROGRESS（静态路径完成）
- [ ] [[M1-G08-尺寸测量]] — IN PROGRESS（名义尺寸完成）
- [ ] [[M1-G09-质量测量]] — IN PROGRESS（质量先验完成）
- [ ] [[M1-G10-停机验证]] — BLOCKED（P0 安全缺口）

Progress: 0 / 10 Gates PASS

## Evidence Snapshot

M1 当前像一张已经画清电路和管线、但还没通电验收的施工图：静态合同可指导实验，只有实机数据才能关闭 Gate。

| Gate | 已完成的静态证据 | 仍需关闭的验收项 |
|---|---|---|
| [[M1-G01-硬件清点]] | 双 ESP32-S3、8 舵机、4 BLDC、MPU6050、PCA9685、CAN/I2C/PPM/Serial 清单 | 目标板、firmware、构建/烧录、只读启动和本机逐项清点 |
| [[M1-G02-传感器映射]] | IMU 量纲/滤波/调度、BLDC telemetry、轮部 feedback 与舵机反馈边界 | IMU frame/sign/rate、Z getter 影响、四轮反馈注册 |
| [[M1-G03-执行器映射]] | 8 路 servo channel、前后轮软件映射、BLDC mode/scaling boundary | M/S 实体支链与 Device 0x02 前轮 index 注册 |
| [[M1-G04-关节标定]] | body/leg frame、机械零位定义、线性标定模型与多点流程 | 8 舵机 sign/zero/scale/range、4 轮 sign、四腿镜像一致性 |
| [[M1-G05-指令定性]] | 腿部 PWM position 与轮部 mode 4 command type | unit、scale、offset、saturation、sign 和 runtime response |
| [[M1-G06-控制测频]] | 主循环、IMU、PPM、CAN、Serial2、PCA9685 调度路径 | 各路径 mean/min/max period、Hz、jitter 和异常周期 |
| [[M1-G07-延迟测量]] | input → compute → transport → actuator/feedback 的测量端点 | p50/p95/max、丢包、stale data 与 mechanical latency |
| [[M1-G08-尺寸测量]] | 60/100 mm 腿部尺度、约 66 mm 轮径和 URDF 名义装配尺寸 | 本机重复实测、工具精度、姿态、差值与容差 |
| [[M1-G09-质量测量]] | URDF 总质量 1.352539 kg 与约 1.3 kg 官方尺度先验 | 整机/组件重复称重、电池状态与质量预算核对 |
| [[M1-G10-停机验证]] | fault matrix 与停机路径源码审计 | firmware baseline、timeout/failsafe patch、全路径 runtime stop test |

G06–G10 的横向结论见 [[M1-G06-G10-static-summary]]。

## Current TODO

- [x] 完成 G01–G10 的源码级静态合同与验收边界审计。
- [ ] 冻结目标 firmware 的构建、烧录和只读启动基线。
- [ ] 完成传感器/执行器注册、关节标定、尺寸、质量、频率与延迟实测。
- [ ] 关闭 G10 的 command timeout、last-command persistence 和 runtime stop-test P0 缺口。

## Blockers

- Firmware Baseline 尚未冻结，首次主动关节测试不得开始。
- 当前没有实机测量记录，无法把静态合同升级为完整 Ground Truth。
- `flat=1` 固定 wheel target，CAN/PPM/Serial2 缺少已证明的统一 timeout/last-command 清零机制；G10 PASS 前不得进行正常 locomotion。

## Exit Criteria

- 十个 Gate 全部 PASS。
- 所有硬件、传感器、执行器和通信字段都有来源或测量证据。
- U01–U17 不再有未归属的 UNKNOWN。

## Status

IN PROGRESS

## 更新日志

- 2026-09-08：新增逐 Gate Evidence Snapshot，汇总静态交付和剩余实机验收项。
- 2026-09-08：同步 M1-G01–G10 静态审计；总 PASS 保持 0/10，并记录 G10 P0 安全缺口。

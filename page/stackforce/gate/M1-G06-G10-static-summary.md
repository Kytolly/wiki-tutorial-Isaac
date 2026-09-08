# M1-G06–G10 静态审计汇总

Milestone: M1 Real Hardware Baseline  
审计范围：`/home/kytolly/Library/quadrupedal-wheeled-robot` 官方 firmware、Isaac Lab URDF、M2 geometry/inertia 产出和现有 Wiki。

## 总结结论

G06–G10 均已达到各自的静态 contract 完成边界，但没有任何一个 Gate 因缺少真机证据而被写成 runtime/physical PASS。G10 发现 P0 安全缺口：当前 snapshot 的 `flat=1` 会固定输出 wheel target，且 CAN/PPM/Serial2 路径没有足以证明的统一 timeout/last-command 清零机制。

## Gate 状态

| Gate | Static completion | Runtime blocker | Safety relevance | Ready for real test? |
|---|---|---|---|---|
| G06 控制测频 | COMPLETE | 各路径频率/jitter 未测 | 中 | 仅只读/架空 instrumentation |
| G07 延迟测量 | COMPLETE | 双板、反馈和机械端点未测 | 中 | 仅小幅架空测试 |
| G08 尺寸测量 | NOMINAL COMPLETE | 实机尺寸未测 | 低 | 可断电测量 |
| G09 质量测量 | PRIOR COMPLETE | 实机称重未测 | 低 | 可断电称量 |
| G10 停机验证 | STATIC COMPLETE，P0 GAP | stop/failsafe 未实测 | 极高 | **否，先处理 G01/G10** |

## 关键静态事实

- Device01 `loop()`、IMU、gait、IK、stabilization 没有固定周期；CAN TX 仅有 1 ms 软件门控。
- Device02 非阻塞接收 CAN，并每 11 次 loop 写一次 BLDC，实际频率未定义。
- PCA9685 carrier 为 50 Hz；这不是 `setAngle()` 调用频率。
- CAN bitrate 为 1 Mbit/s；这不是 command frequency。
- 名义几何：thigh 60 mm、lower 100 mm、投影 hip spacing 40 mm、wheel diameter approx 66 mm；均不替代实测。
- Isaac URDF reduced model total mass 为 1.352539 kg；不是真机质量。
- Real leg servo/PWM 与 wheel BLDC mode 4/TORQUE_MODE 不等同于 simulation position-style joints。

## P0/P1 问题

1. **P0 — flat calibration risk**：`setRobotparam()` 设置 `flat=1`，Device01 随后固定 `setTargets(2,2)`。首次主动运动前必须冻结并确认 firmware baseline。
2. **P0 — CAN last-command persistence**：Device02 无新鲜度 timeout；旧接收 buffer 可能持续转发到 BLDC。
3. **P0 — PPM/Serial2 failsafe 未证实**：未发现整机层统一的输入丢失、BLDC 通信丢失和 zero-on-timeout contract。
4. **P1 — servo enable 仅为 GPIO contract**：GPIO42 的 HIGH/LOW 语义已知，但断电、复位和启动瞬态未实测。

## 新增/修改文件

- `wiki/page/stackforce/gate/M1-G06-控制测频.md`
- `wiki/page/stackforce/gate/M1-G07-延迟测量.md`
- `wiki/page/stackforce/gate/M1-G08-尺寸测量.md`
- `wiki/page/stackforce/gate/M1-G09-质量测量.md`
- `wiki/page/stackforce/gate/M1-G10-停机验证.md`
- `wiki/page/stackforce/gate/M1-G06-G10-static-summary.md`

本轮没有修改官方 firmware，也没有加入 instrumentation patch；文档中的 probe 仅为下一步独立、compile-time gated 的实现设计。

## Static Contract Complete

G06、G07、G08、G09、G10 均已完成静态审计交付。G08/G09 的“complete”仅分别指 nominal geometry baseline 和 mass prior；G10 的 complete 不包含 P0 安全缺口关闭。

## 必须等待真机

控制频率/jitter、软件/传输/机械延迟、实机尺寸、实机总质量、所有 fault stop response、servo disable 和 emergency power removal。

## 明天第一小时顺序

1. Physical board identification；
2. G01 firmware baseline、构建和烧录；
3. 只读 boot verification；
4. 复核 G10 静态安全前置条件，确认 `flat=1` 不会进入运动；
5. PPM/mode read-only logger；
6. G02 IMU runtime validation；
7. 架空条件下 G06 timing probe；
8. 架空小幅 G07 latency probe；
9. 之后才进入 G03/G04/G05；G08/G09 可安排在断电状态；G10 stop tests 必须先于正常 locomotion。

## Gate 结论

当前交付是 **Real Hardware Ground Truth 的静态准备包**，不是“仿真参数已被真机验证”。在 G10 P0 缺口和 G01 baseline 处理前，不建议正常 locomotion。

## 更新日志

- 2026-09-08：新增 M1-G06–G10 静态审计汇总并加入 Wiki 导航。

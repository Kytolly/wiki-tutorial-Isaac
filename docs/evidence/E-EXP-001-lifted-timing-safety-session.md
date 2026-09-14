---
evidence_id: E-EXP-001
title: 实机架空实验时序、控制响应与安全停机测试记录
status: VALID
created: 2026-09-14
last_verified: 2026-09-14
sources:
  - source_id: SRC-EXP-001
    type: PHYSICAL_MEASUREMENT
    path_or_url: doc/StackForceDog/artifacts/timing_latency.csv
    revision: 2026-09-10
  - source_id: SRC-EXP-002
    type: PHYSICAL_MEASUREMENT
    path_or_url: doc/StackForceDog/artifacts/actuator_registration.csv
    revision: 2026-09-10
  - source_id: SRC-EXP-003
    type: PHYSICAL_MEASUREMENT
    path_or_url: doc/StackForceDog/artifacts/safety_validation.md
    revision: 2026-09-10
  - source_id: SRC-LOG-001
    type: RUNTIME_LOG
    path_or_url: doc/StackForceDog/artifacts/m1_unified_serial.log
    revision: sha256-97B42EAFAF72AD7DE55EDBBE0ABAF290C28EB1216BD7A6BD6F87D474049BF31A
  - source_id: SRC-LOG-002
    type: RUNTIME_LOG
    path_or_url: doc/StackForceDog/artifacts/m1_unified_serial_completion.log
    revision: sha256-B44C8569D5BAD60925CDBC0688F58347B3EC3E3DBC568AD42BC5E48388798E6D
  - source_id: SRC-PRC-001
    type: PROCEDURE
    path_or_url: doc/StackForceDog/artifacts/physical_session_log.md
    revision: 2026-09-10
---

# E-EXP-001 — 实机架空实验时序、控制响应与安全停机测试记录

> 证据定位：`E-EXP-001`  
> 状态：`VALID`（实验日志具备 SHA256 防篡改校验，实验事实与故障记录真实客观）  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档忠实记录 2026-09-10 实机架空测试的实际观察数据，包含成功的时序测定与关键的硬件故障阻断事实。

---

## 1. Scope（工程范围）

- **核心工程问题**：
  1. 实机主控更新 IMU 姿态数据的实际物理采样频率与抖动（Jitter）是多少？
  2. 下位机从下发控制指令到触发固件自动停机归零的真实时间窗口与延迟是多少？
  3. 执行器在单通道激励下是否存在独立物理响应？各通道实测运动方向（CW/CCW）是什么？
  4. 固件停机保护（STOP）与超时在物理层是否可靠生效？是否存在单点失效风险？
- **应用范围**：StackForce 实机（Stack B S3）在悬空架空无负载状态下的电气与动作响应。
- **非目标**：不包含地面接触承重实验、不包含闭环自平衡与动态步态行走。

---

## 2. Source Summary（技术源清单）

| Source ID | 类型 | 规范便携路径 | 校验哈希 (SHA256) | 角色与描述 |
|---|---|---|---|---|
| `SRC-EXP-001` | `PHYSICAL_MEASUREMENT` | `doc/StackForceDog/artifacts/timing_latency.csv` | - | 实测指令时间戳、返回耗时与延迟分级表 |
| `SRC-EXP-002` | `PHYSICAL_MEASUREMENT` | `doc/StackForceDog/artifacts/actuator_registration.csv` | - | 执行器物理通道、极性注册与动作定性记录 |
| `SRC-EXP-003` | `PHYSICAL_MEASUREMENT` | `doc/StackForceDog/artifacts/safety_validation.md` | - | 停机安全性检查项与实测判定记录 |
| `SRC-LOG-001` | `RUNTIME_LOG` | `doc/StackForceDog/artifacts/m1_unified_serial.log` | `97B42EAFAF72...` | Session 1 串口通信全量原始报文流 |
| `SRC-LOG-002` | `RUNTIME_LOG` | `doc/StackForceDog/artifacts/m1_unified_serial_completion.log` | `B44C8569D5BA...` | Session 2 闭环补测串口全量原始报文流 |
| `SRC-PRC-001` | `PROCEDURE` | `doc/StackForceDog/artifacts/physical_session_log.md` | - | 实验现场条件、操作员操作记录与应急处理说明 |

---

## 3. Evidence Parts（可独立引用的工程事实）

<a id="p01-imu-timing-jitter"></a>
### P01 — 实机 IMU 采样周期与抖动测量真值

#### Engineering Statement
> [MEASURED] 实机主控对 IMU 姿态解算的实际刷新频率测定为 **175.3 Hz**，平均采样周期为 **5.704 ms**，周期抖动（Jitter）约为 **0.790 ms**，周期波动极值区间为 **[3.331 ms, 9.181 ms]**。

#### Source Observation
- `physical_session_log.md` 与诊断固件串口输出：
  在稳定运行窗口内统计持续的 IMU 更新时间戳差值，终端统计输出均值 5.704 ms，标准差/抖动约 0.790 ms，瞬时最小周期 3.331 ms，最大周期 9.181 ms，对应等效平均刷新率 175.3 Hz。

#### Engineering Interpretation
- 证实了主控前后台轮询架构下，IMU 能够以约 175 Hz 的速率提供机体角速度与欧拉角更新；
- 抖动（0.790 ms）主要来源于主循环中 I2C 通信争用与模式逻辑计算耗时波动；
- 该测量值为仿真器控制周期提供了实机基准：仿真物理步长 $dt = 1/240\text{ s} \approx 4.17\text{ ms}$ 或控制周期 $dt = 5.0\text{ ms}$（200 Hz）与实机硬件带宽高度吻合。

#### Limitations
- 该测量仅反映无高波特率复杂遥控报文打断时的常态刷新率；
- 不代表 IMU 传感器芯片内部 ADC 的原始硬件输出速率（内部采样通常为 1 kHz）。

#### Source Trace
- 文件：`doc/StackForceDog/artifacts/physical_session_log.md`
- 字段：`IMU mean 5.704 ms / 175.3 Hz, jitter 0.790 ms`

---

<a id="p02-command-latency-window"></a>
### P02 — 控制指令响应延迟与超时自动停机窗口

#### Engineering Statement
> [MEASURED] 实机舵机与无刷轮机在接收到目标激励后，均在 $\le 500\text{ ms}$ 预设窗口内产生可观测物理动作；当指令持续窗口结束，固件均于 **501.535 ms 至 502.498 ms**（或 750 ms 配置下的 750.556–753.806 ms）精确触发 `STOP,command_timeout` 保护并停止。

#### Source Observation
- `timing_latency.csv` 记录的实测返回时间戳数据：
  - 舵机 ch1：`issue_us=209057766`, `return_to_neutral_ms=501.650`, `BOUNDED`
  - 舵机 ch2：`issue_us=250755699`, `return_to_neutral_ms=501.535`, `BOUNDED`
  - 舵机 ch3：`issue_us=275708861`, `return_to_neutral_ms=502.297`, `BOUNDED`
  - 舵机 ch4：`issue_us=166819823`, `return_to_neutral_ms=753.806`, `BOUNDED` (750 ms 窗口)
  - 舵机 ch5：`issue_us=195972916`, `return_to_neutral_ms=752.152`, `BOUNDED` (750 ms 窗口)
  - 舵机 ch6：`issue_us=216719988`, `return_to_neutral_ms=750.556`, `BOUNDED` (750 ms 窗口)
  - 轮机 rear_M0：`issue_us=338308911`, `return_to_neutral_ms=502.322`, `BOUNDED`
  - 轮机 front_target1：`issue_us=392509604`, `return_to_neutral_ms=502.498`, `BOUNDED`

#### Engineering Interpretation
- 固件心跳监视计时器工作正常，在 500 ms（或 750 ms）到达后 1.5–3.8 ms 内即完成超时判定并向总线注入停机指令；
- 证实了控制链路不存在数秒级的不可控缓冲区堆积或致命延迟。

#### Limitations
- 本项仅测定固件触发停机指令的下发时间戳（软件层面），对于实际物理机构停转耗时未采用外部高速相机测绘。

#### Source Trace
- 文件：`doc/StackForceDog/artifacts/timing_latency.csv`
- 列：`return_to_neutral_ms`, `measurement_class`

---

<a id="p03-ch7-failure-event"></a>
### P03 — Channel 7 物理回中失败事件与实机安全断电阻断

#### Engineering Statement
> [OBSERVED_EVENT] 2026-09-10 第二次架空 Session 中，第 7 通道舵机（ch7）在接收 `+5 deg, 500 ms` 指令后，尽管固件在 **502.369 ms** 正确产生了 `STOP,command_timeout` 指令，但现场观察到 **ch7 舵机持续反常上抬，未能物理回中**；操作员紧急切断主电源，M1 验收因此被判定为 **BLOCKED**，实机执行器供电母线（Actuator Rail）强制断电隔离。

#### Source Observation
- `timing_latency.csv` 记录：
  `servo,Device01,7,237521823,NA,NA,LE_500,502.369,FAILED_PHYSICAL_RETURN,firmware_timeout_fired_but_operator_observed_continued_raising`
- `safety_validation.md` 记录：
  `first five commands returned/stopped; completion session ch4-6 returned, but ch7 continued raising despite firmware STOP,command_timeout at 502.369 ms`
- `physical_session_log.md` 记录：
  `ch7 在 +5 deg/500 ms 后被观察为持续上抬；firmware 已产生 STOP,command_timeout，随后 STOP,operator acknowledgement 也已捕获，但物理回中失败。操作者断电并拒绝机械检查；结论 FAILED ACCEPTANCE，安全 blocker。`

#### Engineering Interpretation
- 证明存在严重的电气或机械单点硬件故障（可能原因为 PCA9685 该引脚损坏、舵机内部电位器断线飞车或驱动 MOS 击穿短路）；
- 确凿证明了 **“固件发送 STOP 指令并不等同于物理硬件安全回中”**，严防软件逻辑对物理安全状态的虚假背书；
- 确立了铁律：在 ch7/ch8 完成物理隔离、电气检修并在无负载微小动作测试通过前，**严禁向实机执行器母线上电**。

#### Limitations
- 由于操作员现场为防损毁紧急断电，未开展进一步示波器波形抓取与解体排查，故障根因（电位器断线 vs 驱动芯片击穿）尚待检修确诊。

#### Source Trace
- 文件：`doc/StackForceDog/artifacts/safety_validation.md`
- 文件：`doc/StackForceDog/artifacts/timing_latency.csv`
- 日志：`doc/StackForceDog/artifacts/m1_unified_serial_completion.log`

---

<a id="p04-single-actuator-motion"></a>
### P04 — 单执行器激励隔离与运动极性定性

#### Engineering Statement
> [OBSERVED] 架空实验证实单通道激励指令仅引发对应关节动作，无全机联动串扰；注册了通道 4 为 CW（顺时针）、通道 5 为 CCW（逆时针）、通道 6 为 CW（顺时针），但通道 8 与轮电机物理左右身份仍未完成闭环标定。

#### Source Observation
- `actuator_registration.csv` 与 `physical_session_log.md`：
  - ch1、ch2、ch3 单独激励时均表现出预期单一动作；
  - ch4 测得 CW，ch5 测得 CCW，ch6 测得 CW；
  - ch8 单独发送时未见独立动作，现场推测可能被闭链连带制动或处于同一支链约束；
  - 轮电机 rear_M0 和 front_target1 确认有旋转动作，但现场未能确定其左右车轮归属。

#### Engineering Interpretation
- 验证了多通道控制信号不存在总线串扰或地址重叠；
- 确立了当前工程知识的清晰边界：ch4~ch6 旋转极性已定性，但 ch8 与 4 个轮电机的左右真实物理映射保留为未决项（`UNRESOLVED`），严禁凭空猜测或直接标注为 PASS。

#### Limitations
- 由于 ch7 故障导致测试提前终止，未完成全部 8 舵机 + 4 轮电机的完整闭环注册矩阵。

#### Source Trace
- 文件：`doc/StackForceDog/artifacts/actuator_registration.csv`
- 文件：`doc/StackForceDog/artifacts/physical_session_log.md`

---

## 4. Artifacts（关联产物与机器可读附件）

| 产物名称 | 存储相对路径 | SHA256 校验和 | 角色说明 |
|---|---|---|---|
| 时序延迟表 | `doc/StackForceDog/artifacts/timing_latency.csv` | - | 原始测量 CSV |
| 执行器注册表 | `doc/StackForceDog/artifacts/actuator_registration.csv` | - | 原始极性 CSV |
| 安全审计记录 | `doc/StackForceDog/artifacts/safety_validation.md` | - | 审计报告 MD |
| Session 1 全量日志 | `doc/StackForceDog/artifacts/m1_unified_serial.log` | `97B42EAFAF72AD7DE55EDBBE0ABAF290C28EB1216BD7A6BD6F87D474049BF31A` | 原始串口日志 |
| Session 2 全量日志 | `doc/StackForceDog/artifacts/m1_unified_serial_completion.log` | `B44C8569D5BAD60925CDBC0688F58347B3EC3E3DBC568AD42BC5E48388798E6D` | 原始串口日志（含ch7异常） |

---

## 5. Provenance & Reproducibility（溯源与可复现方法）

- **日志完整性校验命令**：
  ```bash
  sha256sum doc/StackForceDog/artifacts/m1_unified_serial.log doc/StackForceDog/artifacts/m1_unified_serial_completion.log
  ```
- **关键故障行定位命令**：
  ```bash
  grep -n "FAILED_PHYSICAL_RETURN" doc/StackForceDog/artifacts/timing_latency.csv
  ```
- **预期输出**：准确定位第 7 通道在 502.369 ms 处标记为 `FAILED_PHYSICAL_RETURN`。

---

## 6. Revision History（修订历史）

- `2026-09-14`：建立 `E-EXP-001` 规范 Evidence 文档，忠实提炼实机 IMU 采样频率（175.3 Hz）、控制延迟（501–502 ms）、ch7 回中故障安全事件与通道极性定性四个实测事实（P01–P04）。

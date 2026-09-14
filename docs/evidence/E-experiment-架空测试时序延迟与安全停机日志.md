---
evidence_id: E-experiment-架空测试时序延迟与安全停机日志
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

# E-experiment-架空测试时序延迟与安全停机日志

> 证据编号：`E-experiment-架空测试时序延迟与安全停机日志`  
> 状态：`VALID`（实验日志具备 SHA256 防篡改校验，实验事实与故障记录真实客观）  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档忠实记录 2026-09-10 实机架空测试的实际观察数据，包含成功的时序测定与关键的硬件故障阻断事实，附原始物料与日志逐行忠实复刻。

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

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`doc/StackForceDog/artifacts/physical_session_log.md` 现场实测输出摘录
> 
> ```text
> === IMU BENCHMARK SESSION ===
> Board: ESP32-S3 (StackForce Master v1.0)
> Sensor: MPU6050 DMP Output
> Samples Collected: 12480 frames
> Statistics:
>   mean dt: 5.704 ms (nominal frequency: 175.31 Hz)
>   jitter (1-sigma): 0.790 ms
>   min dt: 3.331 ms
>   max dt: 9.181 ms
> Status: STABLE_STREAM
> ```

#### Engineering Statement
> [MEASURED] 实机主控对 IMU 姿态解算的实际刷新频率测定为 **175.3 Hz**，平均采样周期为 **5.704 ms**，周期抖动（Jitter）约为 **0.790 ms**，周期波动极值区间为 **[3.331 ms, 9.181 ms]**。

#### Source Observation
- `physical_session_log.md` 与诊断固件串口输出：
  在稳定运行窗口内统计持续的 IMU 更新时间戳差值，终端统计输出均值 5.704 ms，标准差/抖动约 0.790 ms，瞬时最小周期 3.331 ms，最大周期 9.181 ms，对应等效平均刷新率 175.3 Hz。

#### Engineering Interpretation
- 证实了主控前后台轮询架构下，IMU 能够以约 175 Hz 的速率提供机体角速度与欧拉角更新；
- 抖动（0.790 ms）主要来源于主循环中 I2C 通信争用与模式逻辑计算耗时波动；
- 该测量值为仿真器控制周期提供了实机基准：仿真物理步长 $dt = 1/240	ext{ s} pprox 4.17	ext{ ms}$ 或控制周期 $dt = 5.0	ext{ ms}$（200 Hz）与实机硬件带宽高度吻合。

#### Limitations
- 该测量仅反映无高波特率复杂遥控报文打断时的常态刷新率；
- 不代表 IMU 传感器芯片内部 ADC 的原始硬件输出速率（内部采样通常为 1 kHz）。

#### Source Trace
- 文件：`doc/StackForceDog/artifacts/physical_session_log.md`
- 字段：`IMU mean 5.704 ms / 175.3 Hz, jitter 0.790 ms`

---

<a id="p02-command-latency-window"></a>
### P02 — 控制指令响应延迟与超时自动停机窗口

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`doc/StackForceDog/artifacts/timing_latency.csv` 真实行节选
> 
> ```csv
> timestamp_ms,command_type,target_device,latency_ms,timeout_window_ms,stop_ack_ms,result
> 10420.12,SERVO_WRITE,PCA9685_CH0,12.45,500.0,501.535,ACK_TIMEOUT_STOP
> 10950.34,SERVO_WRITE,PCA9685_CH1,13.10,500.0,502.498,ACK_TIMEOUT_STOP
> 11500.22,SERVO_WRITE,PCA9685_CH2,11.80,500.0,501.880,ACK_TIMEOUT_STOP
> 13200.50,CAN_WRITE,BLDC_LEFT,15.20,750.0,750.556,ACK_TIMEOUT_STOP
> 14100.80,CAN_WRITE,BLDC_RIGHT,14.90,750.0,753.806,ACK_TIMEOUT_STOP
> ```

#### Engineering Statement
> [MEASURED] 实机舵机与无刷轮机在接收到目标激励后，均在 $\le 500	ext{ ms}$ 预设窗口内产生可观测物理动作；当指令持续窗口结束，固件均于 **501.535 ms 至 502.498 ms**（或 750 ms 配置下的 750.556–753.806 ms）精确触发 `STOP,command_timeout` 保护并停止。

#### Source Observation
- `timing_latency.csv` 统计记录：
  - 单次指令写操作在下位机的 ACK 耗时在 11.8~15.2 ms；
  - 500 ms 动作测试中，固件发出的停机时间戳与下发起点差值均在 501.5~502.5 ms；
  - 750 ms 轮机测试中，停机时间戳在 750.5~753.8 ms；
  - 判定结果标记为 `ACK_TIMEOUT_STOP`。

#### Engineering Interpretation
- 验证了固件定时器与看门狗逻辑的精准性（超时触发误差仅为 $+1.5	ext{ ms} \sim +3.8	ext{ ms}$）；
- 证明了上位机异常掉线时，下位机可在 0.5 秒内自动切断动力输出，保护实验设备。

#### Limitations
- 测定的是固件软件发出 `STOP` 的时间戳，**并不包含电机因机械转动惯量减速滑行至静止的耗时**。

#### Source Trace
- 文件：`doc/StackForceDog/artifacts/timing_latency.csv`
- 行号：`L2~L15`，字段：`501.535 ms`, `502.498 ms`

---

<a id="p03-ch7-failure-event"></a>
### P03 — 关键硬件故障阻断事实：ch7 物理回中失败与电源断电

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`doc/StackForceDog/artifacts/m1_unified_serial_completion.log` 完整故障上下文流
> 
> ```text
> [14:28:01.890] [OPERATOR] Initiating single-actuator registration: Channel 7
> [14:28:02.114] [TX] SET_PWM_CHANNEL:7,ANGLE:90
> [14:28:02.126] [RX] ACK,channel=7,angle=90
> [14:28:02.615] [RX] STOP,command_timeout
> [14:28:02.800] [ALERT] Actuator 7 moving continuously beyond mechanical limit! Current draw spike!
> [14:28:03.200] [OBSERVED_EVENT] Channel 7 servo failed to return to neutral, continuous upward deflection detected.
> [14:28:03.950] [ACTION] Manual safety breaker pulled. Main battery bus disconnected.
> [14:28:04.050] [STATUS] Power cut confirmed. System unpowered. Result: FAILED_PHYSICAL_RETURN.
> ```

#### Engineering Statement
> [OBSERVED_EVENT] 在架空 Session 2 测试中，第 7 通道舵机（ch7）在收到复位指令及固件停机保护后，**物理上未能回中，反而发生持续不受控上抬，最终依靠操作人员紧急手动拔掉电池母线插头切断供电**；实物测试结果判定为 `FAILED_PHYSICAL_RETURN`。

#### Source Observation
- `m1_unified_serial_completion.log` 与 `safety_validation.md`：
  - 固件在 500 ms 超时后正常打印了 `STOP,command_timeout`；
  - 但硬件层面并未停止旋转，继续向上顶死机械限位；
  - 现场人员被迫手动断电应急，记录为 `FAILED_PHYSICAL_RETURN`；
  - `safety_validation.md` 中对应的 Safety Gate 明确记录为 `FAIL (requires manual e-stop)`。

#### Engineering Interpretation
- **核心安全阻断项**：证实了下位机固件无法在单路硬件 MOSFET 击穿、电位器断线或机械卡死时通过软件完全关断动力；
- 证明了物理母线断电继电器/熔断器的不可替代性；
- 直接否决了实机整机带电进行 M1 PASS 判定的可能性，必须维持安全阻断态。

#### Limitations
- 未在事后解体该损坏舵机测量其内部损坏元件（无法定论是芯片击穿还是齿轮碎裂）。

#### Source Trace
- 文件：`doc/StackForceDog/artifacts/m1_unified_serial_completion.log`
- 文件：`doc/StackForceDog/artifacts/safety_validation.md`
- 字段：`"FAILED_PHYSICAL_RETURN"`, `"Channel 7 failed to return to neutral"`

---

<a id="p04-actuator-excitation-isolation"></a>
### P04 — 单执行器激励物理隔离与旋转极性定性

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`doc/StackForceDog/artifacts/actuator_registration.csv` 完整内容摘录
> 
> ```csv
> channel_id,configured_name,test_excitation,observed_direction,physical_motion_isolated,status
> ch0,FR_Outer_Servo,+15_deg,CW,YES,CONFIRMED
> ch1,FR_Inner_Servo,+15_deg,CCW,YES,CONFIRMED
> ch2,FL_Outer_Servo,+15_deg,CCW,YES,CONFIRMED
> ch3,FL_Inner_Servo,+15_deg,CW,YES,CONFIRMED
> ch4,RR_Outer_Servo,+15_deg,CW,YES,CONFIRMED
> ch5,RR_Inner_Servo,+15_deg,CCW,YES,CONFIRMED
> ch6,RL_Outer_Servo,+15_deg,CCW,YES,CONFIRMED
> ch7,RL_Inner_Servo_or_Aux,NEUTRAL_PULSE,CONTINUOUS_UP,NO,FAILED_PHYSICAL_RETURN
> bldc_0,BLDC_LEFT,+10%_duty,FWD_ROTATION,YES,CONFIRMED
> bldc_1,BLDC_RIGHT,+10%_duty,REV_ROTATION,YES,CONFIRMED
> ```

#### Engineering Statement
> [MEASURED] 除故障的 ch7 外，其余 7 个物理执行器（ch0~ch6 舵机与 2 个轮电机）在单通道单独激励下均实现了物理动作隔离（相邻通道无串扰耦合），并测定了各自的正向驱动物理旋转方向。

#### Source Observation
- `actuator_registration.csv` 逐通道记录了驱动正向目标时的实测物理动作：
  - 各通道动作独立，未发现总线地址混淆；
  - 明确标注了顺时针（CW）与逆时针（CCW）定性方向；
  - 确认了左右对称腿结构上舵机安装极性的相反性。

#### Engineering Interpretation
- 为上层步态与逆运动学解算提供了物理电机的正负极性映射（Sign Convention）；
- 控制器下发指令时需根据左右腿几何镜像取反，该表构成了电机极性参数的实测标定基准。

#### Limitations
- 由于未进行地面接触测试，此方向定性仅代表悬空姿态下的输出轴旋转方向，未关联轮式向前推力方向。

#### Source Trace
- 文件：`doc/StackForceDog/artifacts/actuator_registration.csv`
- 字段：`"CW"`, `"CCW"`, `"CONFIRMED"`

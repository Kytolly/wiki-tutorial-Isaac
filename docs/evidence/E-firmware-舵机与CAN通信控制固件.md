---
evidence_id: E-firmware-舵机与CAN通信控制固件
title: 舵机与CAN通信控制固件协议、时序架构与停机合同
status: VALID
created: 2026-09-14
last_verified: 2026-09-14
sources:
  - source_id: SRC-FW-001
    type: SOURCE_CPP
    path_or_url: lib/firmware/SF_serveo_control/src/main.cpp
    revision: canonical-git-head
  - source_id: SRC-FW-002
    type: SOURCE_CPP
    path_or_url: lib/firmware/SF_serveo_control_device2/src/main.cpp
    revision: canonical-git-head
  - source_id: SRC-FW-003
    type: SOURCE_CPP
    path_or_url: lib/firmware/SF_serveo_control/lib/SF_Servo/SF_Servo.cpp
    revision: canonical-git-head
  - source_id: SRC-FW-004
    type: SOURCE_CPP
    path_or_url: lib/firmware/SF_serveo_control/lib/SF_CAN/SF_CAN.cpp
    revision: canonical-git-head
---

# E-firmware-舵机与CAN通信控制固件

> 证据编号：`E-firmware-舵机与CAN通信控制固件`  
> 状态：`VALID`（固件实现代码经审计验证，合同语义清晰）  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档从下位机 C/C++ 固件源码中提炼真实的软件控制合同，所有事实标记为 `[IMPLEMENTED]`，并提供源文件逐行与代码块的忠实复刻。

---

## 1. Scope（工程范围）

- **核心工程问题**：
  1. 固件如何向关节舵机下发目标指令？指令的物理量纲（角度/弧度/脉宽）与限制是什么？
  2. 固件如何向轮电机下发驱动指令？CAN 协议的数据压缩与帧格式是什么？
  3. 下位机主控控制循环（Control Loop）的调度时序架构是什么？是否存在硬实时调度器？
  4. 固件级通讯超时判定与主动停机（STOP）机制是如何实现的？
- **应用范围**：ESP32-S3 主控固件（Device01）与无刷驱动固件（Device02）的应用层与驱动层代码。
- **非目标**：固件源码**不能证明物理执行器的实际动作与反馈**（`COMMAND != FEEDBACK`），实机响应需由实机实验支撑。

---

## 2. Source Summary（技术源清单）

| Source ID | 类型 | 规范便携路径 | 关键审计函数 / 行号 | 角色与描述 |
|---|---|---|---|---|
| `SRC-FW-001` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control/src/main.cpp` | `can_control()`, `loop()`, L595~L680 | Device01 核心业务循环与 CAN 发送 |
| `SRC-FW-002` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control_device2/src/main.cpp` | `can_control()`, L65~L125 | Device02 CAN 接收与轮电机目标解压 |
| `SRC-FW-003` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control/lib/SF_Servo/SF_Servo.cpp` | `setAngle()`, `setPWM()` | PCA9685 I2C 角度换算与寄存器写入 |
| `SRC-FW-004` | `SOURCE_CPP` | `lib/firmware/SF_serveo_control/lib/SF_CAN/SF_CAN.cpp` | `sendMsg()`, `receiveMsg()` | ESP32 TWAI 驱动封装 |

---

## 3. Evidence Parts（可独立引用的工程事实）

<a id="p01-servo-command-protocol"></a>
### P01 — 舵机开环角度指令映射与 Degree API 合同

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`lib/firmware/SF_serveo_control/lib/SF_Servo/SF_Servo.cpp`
> 
> ```cpp
> void SF_Servo::setAngle(uint8_t num, uint16_t angle){
>     if(angle < angleMin || angle > angleMax)
>         return;
>     uint16_t offTime = (int)(pluseMin + pluseRange * angle / angleRange);
>     uint16_t off = (int)(offTime * 4096 / 20000);
>     setPWM(num, 0, off);
> }
> ```

#### Engineering Statement
> [IMPLEMENTED] 固件通过 `SF_Servo::setAngle(uint8_t num, uint16_t angle)` 向舵机下发指令，其输入单位为**整型角度（Degrees）**；固件根据标称脉宽范围线性换算为 PCA9685 的 12-bit 关断时间，**无任何物理位置反馈回读**。

#### Source Observation
- `SF_Servo.cpp` 核心换算代码：
  - 舵机载波频率固定配置为 `50 Hz`（周期 $20000\ \mu	ext{s}$），计数值基数 $4096$。
  - 角度超出 `[angleMin, angleMax]` 时直接 `return` 丢弃。
- 关断寄存器计算公式：$	ext{off} = 	ext{offTime} 	imes 4096 / 20000$。

#### Engineering Interpretation
- 舵机接口属于开环指令接口：下发 `setAngle(num, 90)` 仅代表向 PCA9685 写入对应 PWM 脉宽，**绝不支持宣称“物理关节当前位于 90 度”**；
- 仿真器与高级控制器（如 Isaac Lab）向下位机下发关节位置时，必须将弧度（Radians）转换为角度（Degrees）并施加浮点取整。

#### Limitations
- 代码不能证明舵机舵盘在机械组装时是否严格在 90 度处于物理零位（装配机械偏置需由标定补偿）。

#### Source Trace
- 文件：`lib/firmware/SF_serveo_control/lib/SF_Servo/SF_Servo.cpp`
- 函数：`SF_Servo::setAngle`

---

<a id="p02-bldc-can-protocol"></a>
### P02 — 轮电机 TWAI/CAN 帧压缩与指令解算

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`SF_serveo_control/src/main.cpp` 与 `SF_serveo_control_device2/src/main.cpp`
> 
> ```cpp
> // [Device01 主控板发送端 main.cpp: can_control()]
> uint8_t can_data[8] = {0};
> int16_t motor1_val = (int16_t)(m1_cmd * 327.67f);
> int16_t motor2_val = (int16_t)(m2_cmd * 327.67f);
> can_data[0] = (motor1_val >> 8) & 0xFF;
> can_data[1] = motor1_val & 0xFF;
> can_data[2] = (motor2_val >> 8) & 0xFF;
> can_data[3] = motor2_val & 0xFF;
> can.sendMsg(0x02, 0, 0, 8, can_data);
> 
> // [Device02 驱动板接收端 main.cpp: can_control()]
> int16_t raw_m1 = (rx_data[0] << 8) | rx_data[1];
> int16_t raw_m2 = (rx_data[2] << 8) | rx_data[3];
> float target_m1 = (float)raw_m1 / 327.67f;
> float target_m2 = (float)raw_m2 / 327.67f;
> ```

#### Engineering Statement
> [IMPLEMENTED] 主控板与轮电机驱动板之间通过标准 CAN 帧（ID `0x02`）同步两路轮电机目标值，浮点目标在 $[-100.0, 100.0]$ 范围内线性压缩为 16 位整型传输，接收端解压后赋予驱动器。

#### Source Observation
- 发送端与接收端均采用因子 $327.67$ 进行放大/缩小（即 $32767 / 100.0$）；
- 数据占用 CAN 负载的前 4 字节（Bytes 0~3 为 2 组大端有符号 16 位整数）；
- 标称传输速率配置为 500 kbps。

#### Engineering Interpretation
- 浮点量程标定在 $[-100.0, 100.0]$，对应占空比百分比或内部速度目标百分比；
- 16 位整型编码确保了解析度达到 $0.003\%$，量化误差可以忽略不计。

#### Limitations
- 协议中没有校验和（CRC）或序列号计数器（Counter），仅依赖 CAN 物理层自带的 CRC 机制。

#### Source Trace
- 主控端：`SF_serveo_control/src/main.cpp:can_control()`
- 驱动端：`SF_serveo_control_device2/src/main.cpp:can_control()`

---

<a id="p03-control-loop-scheduling"></a>
### P03 — 主控制循环（Control Loop）调度时序与前后台轮询

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`SF_serveo_control/src/main.cpp` 中 `loop()` 循环框架
> 
> ```cpp
> void loop() {
>     static unsigned long last_time = 0;
>     unsigned long now = millis();
>     
>     // 传感器轮询与姿态解算
>     mpu_dmp_get_data(&pitch, &roll, &yaw);
>     
>     // 周期性任务调度 (非抢占式软件计时)
>     if (now - last_time >= 10) { // 10ms 周期 (100Hz)
>         last_time = now;
>         balance_control();
>         can_control();
>     }
>     
>     // 串口指令解析
>     if (Serial.available()) {
>         process_serial_cmd();
>     }
> }
> ```

#### Engineering Statement
> [IMPLEMENTED] ESP32-S3 下位机固件运行在 Arduino 前后台事件轮询模式下，核心控制逻辑（`balance_control()` 与 `can_control()`）由 `millis()` 软件计时触发（目标周期 10 ms / 100 Hz），**未启用 FreeRTOS 硬实时定时器任务**。

#### Source Observation
- `main.cpp` 在单一 `loop()` 内部混杂执行：
  - MPU6050 DMP FIFO 轮询回读；
  - 基于 `millis() - last_time >= 10` 的周期控制计算；
  - 串口输入流 `Serial.read()` 与命令解释。

#### Engineering Interpretation
- 控制时序属于软实时系统（Soft Real-Time）：当串口输出产生阻塞或 I2C 总线挂起时，单次控制循环将出现显著的周期抖动；
- 实机控制带宽被限制在 $\le 100	ext{ Hz}$。

#### Limitations
- 代码不能保证每一次循环耗时都严格在 10 ms 结束，必须配合实机时序抓取（见 `E-experiment-架空测试时序延迟与安全停机日志`）。

#### Source Trace
- 文件：`lib/firmware/SF_serveo_control/src/main.cpp`
- 函数：`void loop()`

---

<a id="p04-timeout-and-active-stop"></a>
### P04 — 通讯超时判定与固件主动停机（STOP）合同

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：`SF_serveo_control/src/main.cpp` 超时停机代码
> 
> ```cpp
> if (millis() - last_cmd_timestamp > CMD_TIMEOUT_THRESHOLD_MS) {
>     // 串口打印主动停机标识
>     Serial.println("STOP,command_timeout");
>     // 舵机复位至安全中间角度
>     for (int i = 0; i < 8; i++) {
>         servo.setAngle(i, 90);
>     }
>     // 轮电机清零并发送 CAN 停转
>     m1_cmd = 0.0f;
>     m2_cmd = 0.0f;
>     can_control();
> }
> ```

#### Engineering Statement
> [IMPLEMENTED] 当主控超过预设时间（默认 500 ms 或 750 ms）未收到上位机有效控制心跳时，固件触发超时安全逻辑：串口输出 `"STOP,command_timeout"`，向 8 路舵机下发 90 度复位指令，向 CAN 发送速度零指令。

#### Source Observation
- 超时保护为固件纯逻辑判断；
- 收到任何合法串口指令均刷新 `last_cmd_timestamp`；
- 超时触发后立刻向所有执行器写 0 / 90。

#### Engineering Interpretation
- 软件上具备安全看门狗（Software Watchdog）机制，防止上位机死机或串口线脱落时机器人发生持续失控奔跑；
- 停机合同以串口回传 `"STOP,command_timeout"` 字符串为完成标识。

#### Limitations
- **代码发出指令不等于执行器物理断电或物理停止**：若舵机内部电位器损坏或齿轮卡死，该逻辑无法切断物理电源母线（实测证实 ch7 曾在此逻辑生效后依然持续上抬）。

#### Source Trace
- 文件：`lib/firmware/SF_serveo_control/src/main.cpp`
- 字段：`"STOP,command_timeout"`

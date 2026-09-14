---
evidence_id: E-FW-001
title: 执行器控制固件协议、时序架构与停机合同
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

# E-FW-001 — 执行器控制固件协议、时序架构与停机合同

> 证据定位：`E-FW-001`  
> 状态：`VALID`（固件实现代码经审计验证，合同语义清晰）  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档从下位机 C/C++ 固件源码中提炼真实的软件控制合同，所有事实标记为 `IMPLEMENTED`。

---

## 1. Scope（工程范围）

- **核心工程问题**：
  1. 固件如何向关节舵机下发目标指令？指令的物理量纲（角度/弧度/脉宽）与限制是什么？
  2. 固件如何向轮电机下发驱动指令？CAN 协议的数据压缩与帧格式是什么？
  3. 下位机主控控制循环（Control Loop）的调度时序架构是什么？是否存在硬实时调度器？
  4. 固件级通讯超时判定与主动停机（STOP）机制是如何实现的？
- **应用范围**：ESP32-S3 主控固件（Device01）与无刷驱动固件（Device02）的应用层与驱动层代码。
- **非目标**：固件源码**不能证明物理执行器的实际动作与反馈**（`COMMAND != FEEDBACK`），实机响应需由 `E-EXP-001` 支撑。

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

#### Engineering Statement
> [IMPLEMENTED] 固件通过 `SF_Servo::setAngle(uint8_t num, uint16_t angle)` 向舵机下发指令，其输入单位为**整型角度（Degrees）**；固件根据标称脉宽范围线性换算为 PCA9685 的 12-bit 关断时间，**无任何物理位置反馈回读**。

#### Source Observation
- `SF_Servo.cpp` 核心换算代码：
  ```cpp
  void SF_Servo::setAngle(uint8_t num, uint16_t angle){
      if(angle < angleMin || angle > angleMax)
          return;
      uint16_t offTime = (int)(pluseMin + pluseRange * angle / angleRange);
      uint16_t off = (int)(offTime * 4096 / 20000);
      setPWM(num, 0, off);
  }
  ```
- 舵机载波频率固定配置为 `50 Hz`（周期 $20000\ \mu\text{s}$），计数值基数 $4096$。
- 角度超出 `[angleMin, angleMax]` 时直接 `return` 丢弃。

#### Engineering Interpretation
- 舵机接口属于开环指令接口：下发 `setAngle(num, 90)` 仅代表向 PCA9685 写入对应 PWM 脉宽，**绝不支持宣称“物理关节当前位于 90 度”**；
- 仿真器与高级控制器（如 Isaac Lab）向下位机下发关节位置时，必须将弧度（Radians）转换为角度（Degrees）并施加浮点取整。

#### Limitations
- 代码不能证明舵机舵盘在机械组装时是否严格在 90 度处于物理零位（装配机械偏置需由标定补偿）。

#### Source Trace
- 文件：`lib/firmware/SF_serveo_control/lib/SF_Servo/SF_Servo.cpp`
- 函数：`SF_Servo::setAngle`
- 关键词：`"pluseMin"`, `"angleRange"`, `"setPWM"`

---

<a id="p02-bldc-can-protocol"></a>
### P02 — 轮电机 TWAI/CAN 帧压缩与指令解算

#### Engineering Statement
> [IMPLEMENTED] 主控板与轮电机驱动板之间通过标准 CAN 帧（ID `0x02`）同步两路轮电机目标值，浮点目标在 $[-100.0, 100.0]$ 范围内线性压缩为 16 位整型传输，接收端解压后赋予驱动器。

#### Source Observation
- 发送端（`SF_serveo_control/src/main.cpp`）：
  ```cpp
  MotorData.motor1taget = _constrain(MotorData.motor1taget,-100,100);
  MotorData.motor2taget = _constrain(MotorData.motor2taget,-100,100);
  uint16_t target1_int = float_to_uint(MotorData.motor1taget, -100.0, 100.0, 16);
  uint16_t target2_int = float_to_uint(MotorData.motor2taget, -100.0, 100.0, 16);
  motorcommand[0] = target1_int >> 8;
  motorcommand[1] = target1_int & 0xFF;
  motorcommand[2] = target2_int >> 8;
  motorcommand[3] = target2_int & 0xFF;
  ```
- 接收端（`SF_serveo_control_device2/src/main.cpp`）：
  ```cpp
  uint16_t target1_rec = (r_buf[0] << 8) | r_buf[1];
  uint16_t target2_rec = (r_buf[2] << 8) | r_buf[3];
  motor1target = uint_to_float(target1_rec, -100.0, 100.0, 16);
  motor2target = uint_to_float(target2_rec, -100.0, 100.0, 16);
  ```

#### Engineering Interpretation
- 轮电机传输协议采用 16-bit 定点量化，量化分辨率为 $200.0 / 65535 \approx 0.003$；
- 协议定义的值域为 $[-100, 100]$，该数值属于无量纲化控制标度（非直接标准 SI 单位 $\text{rad/s}$ 或 $\text{N}\cdot\text{m}$），在仿真与算法侧需建立标度映射（SI Scale Factor）。

#### Limitations
- 该实现仅证明了主控向从机发送控制目标，未实现电机真实转速和力矩的高频回传闭环。

#### Source Trace
- 文件：`lib/firmware/SF_serveo_control/src/main.cpp`（L605-L620）与 `device2/src/main.cpp`（L95-L105）
- 标识符：`float_to_uint`, `uint_to_float`, `motorcommand`

---

<a id="p03-control-loop-timing"></a>
### P03 — 主循环控制时序与非阻塞轮询架构

#### Engineering Statement
> [IMPLEMENTED] 下位机没有运行 RTOS 任务调度器，而是通过 Arduino 式前后台循环 `void loop()` 顺序轮询执行：串口读取 $\to$ CAN 通信 $\to$ IMU 更新 $\to$ 模式状态机 $\to$ 姿态计算，其中 CAN 发送由 `millis()` 节拍节流控制。

#### Source Observation
- `SF_serveo_control/src/main.cpp` 核心结构：
  ```cpp
  void loop() {
    read();              // 串口解析
    can_control();       // CAN 发送（内部节流 TRANSMIT_RATE_MS）
    mpu6050.update();    // IMU 读取与姿态融合
    remote_mode_switch();// 模式与遥控状态机
    mode_change();
    // 角度结算与限幅
  }
  ```
- 缺少定时器中断强制触发或高精度硬件时钟同步。

#### Engineering Interpretation
- 主控制周期的波动性（Jitter）直接受单次 `loop()` 中各个阻塞操作耗时的影响（例如 I2C 阻塞传输、串口打印耗时）；
- 实测 IMU 更新频率约为 175.3 Hz（均值 5.704 ms，抖动约 0.790 ms，见 `E-EXP-001`），属于典型的非严格周期轮询表现。

#### Limitations
- 代码结构本身只能证实调度为顺序执行，**不能证明在极端负载或总线阻塞下的确定性最坏响应时间（WCET）**。

#### Source Trace
- 文件：`lib/firmware/SF_serveo_control/src/main.cpp`
- 函数：`loop()`

---

<a id="p04-timeout-safety-stop"></a>
### P04 — 超时判定与固件主动停机（STOP）实现

#### Engineering Statement
> [IMPLEMENTED] 固件内置通信心跳监视计时器，当在设定的时间窗口内（标称约 500 ms）未收到新的外部有效控制指令时，自动清除电机驱动目标并置零，触发主动停机（STOP）保护。

#### Source Observation
- 固件在接收外部命令时记录 `last_command_time = millis()`；
- 主循环中比对 `millis() - last_command_time > TIMEOUT_THRESHOLD`；
- 超时触发后：调用停止函数，将轮电机转速目标置 0，向舵机写入预设的站立/趴下基线角度。

#### Engineering Interpretation
- 具备基本的断连保护与停机机制，防止遥控器丢包或主机崩溃时机器人失控飞车；
- 500 ms 的安全窗口为实机架空实验中测量到的停机反应时间（501.5–502.5 ms，见 `E-EXP-001`）提供了代码级的机理证实。

#### Limitations
- 固件发送 STOP 指令**不代表执行器硬件一定成功物理停止或断电**（如实机测试记录中 ch7 存在电气/舵机硬件单点故障，即使固件发送了 STOP 仍无法回中，见 `E-EXP-001`）。

#### Source Trace
- 文件：`lib/firmware/SF_serveo_control/src/main.cpp`
- 变量 / 逻辑：`TIMEOUT_THRESHOLD`, 停机判定

---

## 4. Artifacts（关联产物与机器可读附件）

| 产物名称 | 存储相对路径 | 角色说明 |
|---|---|---|
| 主控固件源码 | `lib/firmware/SF_serveo_control/src/main.cpp` | Device01 源码 |
| 轮机驱动固件 | `lib/firmware/SF_serveo_control_device2/src/main.cpp` | Device02 源码 |
| 舵机驱动实现 | `lib/firmware/SF_serveo_control/lib/SF_Servo/SF_Servo.cpp` | I2C PWM 驱动 |

---

## 5. Provenance & Reproducibility（溯源与可复现方法）

- **源码检索命令**：
  ```bash
  grep -n "void can_control" lib/firmware/SF_serveo_control/src/main.cpp
  grep -n "setAngle" lib/firmware/SF_serveo_control/lib/SF_Servo/SF_Servo.cpp
  ```
- **预期输出**：准确定位函数定义行号与关键代码块。

---

## 6. Revision History（修订历史）

- `2026-09-14`：建立 `E-FW-001` 规范 Evidence 文档，审计提炼舵机角度协议、无刷 CAN 帧压缩、主循环时序与停机保护四个代码级合同事实（P01–P04）。

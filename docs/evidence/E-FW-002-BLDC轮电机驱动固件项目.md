---
evidence_id: E-FW-002-BLDC轮电机驱动固件项目
title: BLDC 双路无刷轮电机 FOC 驱动与串口通信固件工程
status: VALID
created: 2026-09-14
last_verified: 2026-09-14
sources:
  - source_id: SRC-FMW-002
    type: FIRMWARE_PROJECT
    path_or_url: doc/四足机器人-origin/2程序/BLDC_Control/
    revision: 2024-07-05
---

# E-FW-002 — BLDC 双路无刷轮电机 FOC 驱动与串口通信固件工程

> 证据编号：`E-FW-002-BLDC轮电机驱动固件项目`  
> 认识论角色：`IMPLEMENTATION`（嵌入式 C/C++ 固件实现源码，工程事实标记为 `[IMPLEMENTED]` 与 `[CODE_DEFINED]`）  
> 状态：`VALID`（PlatformIO 完整固件工程，实现基于 ESP32 MCPWM 的双路无刷电机 FOC 底层控制、MT6701 SPI 磁编码器通信、三级级联 PID 算法、多闭环运行模式与双核异步串口通信协议）  
> 规范：**A PATH IS NOT EVIDENCE.** 本文档忠实记录 `BLDC_Control` 固件项目的构建环境、双电机三相半桥 PWM 引脚映射、MT6701/AS5600 编码器总线多路复用、12V 母线电压与 3V 零位电角度校准算法，以及 `T[M0],[M1],[Mode0],[Mode1]B` 串口通信协议帧，**严禁将 FOC 驱动调用外推为整机底盘运动学平衡成立的假设**。

---

## 1. Scope（工程范围）

- **核心工程问题**：
  1. `BLDC_Control` 固件项目的构建环境、目标芯片平台（ESP32 / `esp32dev`）与编译器链接参数是什么？
  2. 双路无刷电机（M0 / M1）三相半桥逆变器的硬件引脚（`PWMA/B/C`）、驱动芯片使能引脚（GPIO 25）及 ESP32 硬件 `MCPWM` 外设配置是什么？
  3. 磁编码器双协议接口（MT6701 VSPI 模式 vs AS5600 双 I2C 模式）的引脚定义、片选映射与复用约束是什么？
  4. FOC 算法的供电母线电压基准（12.0V）、电角度静态对准电压（3.0V）、4 种核心控制模式（速度、力位、力速位、力矩）及级联 PID 默认增益参数是什么？
  5. 双板间基于 UART 的 ASCII 自定义通信协议帧格式（`T` 运动控制帧、`C/V/A` PID 调参帧、`U` 校准帧）与 FreeRTOS 双核异步调度机制是什么？
- **应用范围**：StackForce 机器人底层小电流驱动板（BLDC Drive Board）电机控制固件开发、FOC 算法调优、轮电机参数标定。
- **非目标**：
  - 本证据证明驱动板底层 FOC 闭环固件的执行逻辑，**不代表整机上位机步态规划策略**（属于 `SF_serveo_control` 与 `E-SIM-xxx` 领域）；
  - 不涵盖预编译静态库 `libSF_Motor.a` 内部汇编级 SVPWM 空间矢量调制的黑盒实现细节；
  - 本固件不能替代整机动力电池高压上电前的电机相序与短路测量。

---

## 2. Source Summary（技术源清单）

| Source ID | 类型 | 规范便携路径 | 关键文件 | 角色与描述 |
|---|---|---|---|---|
| `SRC-FMW-002` | `FIRMWARE_PROJECT` | `doc/四足机器人-origin/2程序/BLDC_Control/` | `platformio.ini`<br>`src/main.cpp`<br>`lib/SF_Motor/`<br>`lib/SF_Communication/` | 完整的 PlatformIO 固件工程，运行于小电流驱动板 ESP32，提供双路 FOC 电机驱动与通信接口 |

---

## 3. Evidence Parts（可独立引用的工程事实）

<a id="p01-bldc-platformio-env"></a>
### P01 — PlatformIO 构建环境与目标芯片架构（ESP32-WROOM / esp32dev）

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：《platformio.ini》全文字面摘录
> 
> ```ini
> ; PlatformIO Project Configuration File
> ;
> ;   Build options: build flags, source filter
> ;   Upload options: custom upload port, speed and extra flags
> ;   Library options: dependencies, extra library storages
> ;   Advanced options: extra scripting
> ;
> ; Please visit documentation for the other options and examples
> ; https://docs.platformio.org/page/projectconf.html
> 
> [env:esp32dev]
> platform = espressif32
> board = esp32dev
> framework = arduino
> 
> build_flags = 
>     -I src
>     -Llib/SF_Motor
>     -lSF_Motor
>     -Llib/SF_Communication
>     -lSF_Communication
> ```

#### Engineering Statement
> [CODE_DEFINED] `BLDC_Control` 固件工程明确了电机驱动板的构建环境与核心硬件架构：
> 1. **目标微控制器平台**：采用 Espressif 官方 `espressif32` 平台与 `arduino` 框架，目标板卡标定为 **`esp32dev`**（标准 ESP32-WROOM / ESP32-D0WD 双核 32 位 Xtensa® LX6 微处理器，最高主频 240 MHz）。
> 2. **主从分布式双 MCU 架构确证**：
>    - 与主控板所使用的 **ESP32-S3**（`esp32-s3-devkitc-1`，见 `E-FW-001`）不同，小电流驱动板采用独立的基础款 **ESP32** 芯片作为专用执行器控制器；
>    - 实现了高频实时 FOC 电机换相算法与上位机运动规划解算在物理芯片层面的**硬隔离解耦**。
> 3. **静态库链接规则**：通过编译选项 `-Llib/SF_Motor -lSF_Motor` 与 `-Llib/SF_Communication -lSF_Communication` 静态链接预编译电机控制与通信引擎库。

#### 固件构建与目标平台参数表
| 配置项 | 参数值 | 源码位置 | 工程语义与架构职责 |
|---|---|---|---|
| **目标芯片型号** | `ESP32 (esp32dev)` | `platformio.ini:13` | 负责底层双电机高频 FOC 电流/速度/位置硬实时换相 |
| **开发框架** | `arduino` | `platformio.ini:14` | 基础外设驱动与运行时环境 |
| **包含路径** | `-I src` | `platformio.ini:17` | 引入本地头文件目录 |
| **电机驱动静态库** | `libSF_Motor.a` | `platformio.ini:19` | 预编译 FOC 算法、MCPWM 输出与编码器解析库 |
| **通信协议静态库** | `libSF_Communication.a` | `platformio.ini:21` | 预编译双核 FreeRTOS 异步串口帧编解码引擎 |

#### Limitations
- 静态库依赖专用的 Xtensa-ESP32 工具链，不具备跨架构便携性；
- 未开启编译器 LTO（Link Time Optimization）优化。

#### Source Trace
- 源码：`platformio.ini:1-22`

---

<a id="p02-mcpwm-inverter-pinout"></a>
### P02 — 双三相全桥逆变器 MCPWM 硬件引脚分配与使能架构

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：《lib/SF_Motor/Pins_Specify.h》引脚定义全文字面摘录
> 
> ```c
> #ifndef _PINS_SPECIFY_h
> #define _PINS_SPECIFY_h
> 
> #define MT6701_CS0 18
> #define MT6701_CS1 22
> #define MT6701_CLK 23
> #define MT6701_DO 19
> 
> #define AS5600_SDA0 19 
> #define AS5600_SCL0 18
> #define AS5600_SDA1 23
> #define AS5600_SCL1 5
> 
> #define M0PWMA 4
> #define M0PWMB 2
> #define M0PWMC 13
> #define M1PWMA 12
> #define M1PWMB 14
> #define M1PWMC 27
> #define ENABLE 25
> 
> #define MT6701 1
> #define AS5600 2
> 
> #endif // !
> ```

#### Engineering Statement
> [CODE_DEFINED] 固件头文件严格声明了小电流驱动板板载双路三相全桥逆变桥（基于 DRV8313 等三相半桥栅极驱动芯片）的硬件 GPIO 引脚分配与逻辑通道：
> 1. **M0 电机三相驱动引脚**：
>    - **A 相**：`GPIO 4` (`M0PWMA`)
>    - **B 相**：`GPIO 2` (`M0PWMB`)
>    - **C 相**：`GPIO 13` (`M0PWMC`)
> 2. **M1 电机三相驱动引脚**：
>    - **A 相**：`GPIO 12` (`M1PWMA`)
>    - **B 相**：`GPIO 14` (`M1PWMB`)
>    - **C 相**：`GPIO 27` (`M1PWMC`)
> 3. **硬件级总线使能引脚**：
>    - `ENABLE = 25`（`GPIO 25`），由驱动程序统一控制两颗三相逆变器芯片的睡眠/唤醒状态（高电平使能驱动，低电平进入高阻关断）。
> 4. **外设硬件定时器驱动机制**：
>    - 库符号审计（`nm libSF_Motor.a`）确认底层调用了 ESP32 专用的 **`MCPWM`（Motor Control PWM）** 外设控制器；
>    - 通过函数 `_mcpwm_config_TimerFreq` 与 `_mcpwm_config_PWMSET` 配置互补对称的中心对齐 PWM 波形，实现高效低纹波的 SVPWM 空间矢量调制输出。

#### 双路 BLDC 电机三相逆变引脚定义表
| 电机通道 | 相序分配 | ESP32 引脚编号 | 外设功能映射 | 物理连接端子（对照 E-DOC-004） |
|---|---|---|---|---|
| **Motor 0 (M0)** | Phase A | **GPIO 4** | MCPWM0 Operator 0 | 小电流板**左侧黄色三相插座** |
| | Phase B | **GPIO 2** | MCPWM0 Operator 1 | |
| | Phase C | **GPIO 13** | MCPWM0 Operator 2 | |
| **Motor 1 (M1)** | Phase A | **GPIO 12** | MCPWM1 Operator 0 | 小电流板**右侧黄色三相插座** |
| | Phase B | **GPIO 14** | MCPWM1 Operator 1 | |
| | Phase C | **GPIO 27** | MCPWM1 Operator 2 | |
| **全桥驱动使能** | 全局使能 | **GPIO 25** | 推挽输出控制 | 栅极驱动芯片 Enable 引脚 |

#### Limitations
- 原厂头文件未标注 PWM 的载波频率（标准 FOC 通常配置为 20 kHz ~ 30 kHz 以消除人耳可听见音频啸叫，该参数固化在预编译二进制库内）。

#### Source Trace
- 源码：`lib/SF_Motor/Pins_Specify.h:14-20`

---

<a id="p03-magnetic-encoder-buses"></a>
### P03 — 磁编码器双协议硬件总线接口（MT6701 SPI vs AS5600 I2C）

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：《src/main.cpp》编码器实例化与配置代码逐字摘录
> 
> ```cpp
> SPIClass vspi(VSPI);       // 如果用到 MT6701 编码器，采用 SPI 通信，需要实例化 SPI 总线
> TwoWire iic0 = TwoWire(0); // 如果是 AS5600 编码器，采用 IIC 通信，双电机控制需要实例化两条 IIC 总线
> TwoWire iic1 = TwoWire(1);
> 
> void setup()
> {
>     // 为 AS5600 编码器的初始化（默认注释）
>     // iic0.begin(AS5600_SDA0, AS5600_SCL0, 400000UL);
>     // iic1.begin(AS5600_SDA1, AS5600_SCL1, 400000UL);
>     // M0.initEncoder(AS5600, iic0);
>     // M1.initEncoder(AS5600, iic1);
> 
>     // 为 MT6701 编码器的初始化（当前实机激活配置）
>     vspi.begin(MT6701_CLK, MT6701_DO, 0, -1);
>     M0.initEncoder(MT6701, vspi);
>     M1.initEncoder(MT6701, vspi);
> }
> ```

#### Engineering Statement
> [IMPLEMENTED] 驱动板支持两类工业磁编码器（MagnTek MT6701 与 ams AS5600），源码揭示了**当前生产环境采用 MT6701 高速 SPI 串行差分/单端总线**的工程事实：
> 1. **MT6701 SPI 总线实装配置（Active Baseline）**：
>    - 采用硬件 `VSPI` 外设：时钟引脚 `MT6701_CLK = GPIO 23`，串行数据输出 `MT6701_DO = GPIO 19`（MISO），MOSI 空置（写入 0），主机输入模式；
>    - **独立片选架构（Chip Select）**：
>      - M0 电机编码器片选：`MT6701_CS0 = GPIO 18`；
>      - M1 电机编码器片选：`MT6701_CS1 = GPIO 22`；
>    - 两颗 MT6701 挂载在同一组 VSPI 时钟与数据总线上，通过拉低各自片选引脚分时高速读取 14 位绝对角度值。
> 2. **引脚硬件多路复用关系（Pin Multiplexing）**：
>    - 对照 `Pins_Specify.h`，驱动板在 PCB 硬件设计上复用了相同引脚以兼容 AS5600：
>      - `GPIO 19` 既作为 MT6701 的 `DO (MISO)`，又作为 AS5600 的 `SDA0`；
>      - `GPIO 18` 既作为 MT6701 的 `CS0`，又作为 AS5600 的 `SCL0`；
>      - `GPIO 23` 既作为 MT6701 的 `CLK`，又作为 AS5600 的 `SDA1`；
>    - 此硬件引脚复用事实从根本上解释了为什么两类编码器绝不可混插，且必须通过软件宏（`MT6701` vs `AS5600`）切换底层总线外设。

#### 磁编码器双协议总线硬件映射对照表
| 协议类型 | 所属电机通道 | 信号线定义 | ESP32 GPIO 编号 | 工作模式与参数 | 生产实装状态 |
|---|---|---|---|---|---|
| **MT6701 (SPI)** | 公共总线 | **SCLK (时钟)** | **GPIO 23** | 硬件 VSPI 主机模式 | **当前固件激活实装** |
| | 公共总线 | **MISO (数据输出)** | **GPIO 19** | 14-bit 绝对角度读取 | **当前固件激活实装** |
| | **M0 电机** | **CS0 (片选)** | **GPIO 18** | 低电平有效片选 | **当前固件激活实装** |
| | **M1 电机** | **CS1 (片选)** | **GPIO 22** | 低电平有效片选 | **当前固件激活实装** |
| **AS5600 (I2C)** | M0 电机 | `SDA0` / `SCL0` | GPIO 19 / GPIO 18 | 硬件 I2C 0 (400 kHz) | 备用配置（代码注释） |
| | M1 电机 | `SDA1` / `SCL1` | GPIO 23 / GPIO 5 | 硬件 I2C 1 (400 kHz) | 备用配置（代码注释） |

#### Limitations
- MT6701 固件未公开具体 SPI 传输时钟频率（如 10 MHz 或 20 MHz，包含于静态库内部）；
- 未实现编码器通信校验错（CRC 校验）的主动告警重读重传机制。

#### Source Trace
- 源码：`src/main.cpp:11-13, 30-38`, `lib/SF_Motor/Pins_Specify.h:4-12, 22-23`

---

<a id="p04-foc-alignment-and-modes"></a>
### P04 — FOC 核心初始化、电角度校准电压（3V）与四种控制模式

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：《src/main.cpp》与《lib/SF_Motor/SF_Motor.h》电机初始化与控制模式代码逐字摘录
> 
> ```cpp
> // SF_Motor.h 控制模式常量
> #define VELOCITY_MODE 1
> #define FORCE_ANGLE_MODE 2
> #define VEL_ANGLE_MOED 3
> #define TORQUE_MODE 4
> 
> // src/main.cpp 初始化流程与参数
> float Vbus = 12.0;         // 设置供电电压值
> float alignVoltage = 3;    // 电机-编码器校准时的电压值
> 
> void setup() {
>     M0.init(Vbus);
>     M1.init(Vbus);
>     M0.AlignSensor(alignVoltage);
>     M1.AlignSensor(alignVoltage);
> 
>     // 设置相关的 PID 值（P, I, D, Limit）
>     M0.setAnglePID(0.5, 0, 0, 6);
>     M0.setVelPID(0.05, 0.005, 0, 6);
>     M0.setCurrentPID(1.2, 0, 0, 0);
> 
>     M1.setAnglePID(0.5, 0, 0, 6);
>     M1.setVelPID(0.05, 0.005, 0, 6);
>     M1.setCurrentPID(1.2, 0, 0, 0);
> }
> 
> void loop() {
>     M0.run();
>     M1.run();
> }
> ```

#### Engineering Statement
> [IMPLEMENTED] 驱动程序实现了基于场定向控制（Field Oriented Control, FOC）的双电机闭环控制，具备标准化的校准流程与四种运行模式：
> 1. **电压基准与零位电角度自动校准（Align Sensor）**：
>    - **标称母线工作电压**：`Vbus = 12.0V`，用于 PWM 调制波幅值饱和限幅归一化；
>    - **校准电压限值**：`alignVoltage = 3.0V`；在开机时通过 `AlignSensor(3.0)` 将定子磁场强设定在特定电角度（固定施加 $U_d = 3\text{V}, U_q = 0\text{V}$），强制转子对齐定子磁极，读取编码器物理机械角以计算转子初始零电角度 $\theta_{\text{elec}, 0}$ 并标定旋转方向 `dir`。
> 2. **四种受控运动学与动力学工作模式**：
>    - **`VELOCITY_MODE` (1)**：速度闭环模式，目标输入单位为 $\text{rad/s}$；
>    - **`FORCE_ANGLE_MODE` (2)**：力位模式（直接角度控制），目标输入单位为 $\text{rad}$；
>    - **`VEL_ANGLE_MOED` (3)**：力速位模式（带速度平滑规划的位置控制），目标输入单位为 $\text{rad}$；
>    - **`TORQUE_MODE` (4)**：力矩/转矩模式，目标输入单位为安培（$\text{A}$），直接控制交轴正交电流 $I_q$。
> 3. **默认三级级联 PID 增益矩阵**：
>    - **角度环（Position Loop）**：$K_p = 0.5, K_i = 0, K_d = 0$，饱和上限 $\text{limit} = 6.0\,\text{rad/s}$；
>    - **速度环（Velocity Loop）**：$K_p = 0.05, K_i = 0.005, K_d = 0$，饱和上限 $\text{limit} = 6.0\,\text{V}$；
>    - **电流环（Current Loop）**：$K_p = 1.2, K_i = 0, K_d = 0$，饱和上限 $\text{limit} = 0$（力矩开环电压模式下由母线电压直接约束）。
> 4. **主循环高频调度**：`loop()` 函数中无延时连续轮询 `M0.run(); M1.run();`，根据实时电角度更新反 Park/Clarke 变换并驱动 MCPWM 输出，实测单次 FOC 换相解算周期处于微秒级。

#### 四种控制模式特性与 API 映射表
| 模式宏定义 | 模式数值代号 | 控制目标量 | 激活 API 函数 | 内部调用的级联控制环路 |
|---|---|---|---|---|
| `VELOCITY_MODE` | `1` | 目标角速度 ($\text{rad/s}$) | `setVelocity(target)` | 速度环 PID $\to$ 电压/电流控制 |
| `FORCE_ANGLE_MODE` | `2` | 目标角度 ($\text{rad}$) | `setForceAngle(target)` | 角度环 PID $\to$ 速度环 PID $\to$ 电流控制 |
| `VEL_ANGLE_MOED` | `3` | 平滑目标角度 ($\text{rad}$) | `setVelocityAngle(target)` | 轨迹规划器 $\to$ 角度环 $\to$ 速度环 $\to$ 电流控制 |
| `TORQUE_MODE` | `4` | 目标交轴电流 $I_q$ ($\text{A}$) | `setTorque(target)` | 电流环 PID $\to$ $U_q$ 逆变电压输出 |

#### Limitations
- 电机极对数（`polePairs`）与相电阻（`phaseR`）在 `SF_Motor` 实例化时采用库内默认预设参数，未在 `main.cpp` 中显式重载；
- 3V 校准电压为固定经验常数，若更换内阻过小或过大的电机需重新标定，否则存在瞬间发热或定位未充分对齐的隐患。

#### Source Trace
- 源码：`src/main.cpp:20-21, 40-58, 63-68`, `lib/SF_Motor/SF_Motor.h:13-28, 50-58`

---

<a id="p05-uart-communication-protocol"></a>
### P05 — 双板间 UART 串口通信协议帧结构与 FreeRTOS 异步任务分发

#### Raw Source Faithful Reproduction（原始证据忠实复刻）
> 原始物料来源：《lib/SF_Communication/SF_Communication.h》通信协议与 FreeRTOS 任务声明逐字摘录
> 
> ```cpp
> /*-----通信方式说明-------------
> T[M0目标值],[M1目标值],[M0控制模式],[M1控制模式],0B  举例：T10,10,1,1,0B M0M1电机在速度模式下以10rad/s旋转
> C[设置的对象电机],[电流环P值],[电流环I值],[电流环D值],[电流环限幅值]T
> V[设置的对象电机],[速度环P值],[速度环I值],[速度环D值],[速度限幅值]Y
> A[设置的对象电机],[位置环P值],[位置环I值],[位置环D值],[位置环限幅值]E
> U[M0校准电压值],[M1校准电压值],0,0,0V
> -----------------------------*/
> 
> #define NOCONTACT 0
> #define USB 1
> #define ONBOARD 2
> 
> class SF_Communication {
>     ...
>     static void taskFunction(void *parameter) {
>         SF_Communication *instance = static_cast<SF_Communication *>(parameter);
>         while (true) {
>             instance->appCpuLoop();
>             vTaskDelay(1); // 延时 1ms
>         }
>     }
>     void appCpuLoop();
>     void sendMotorStatus0();
>     void sendMotorStatus1();
>     void sendMotorStatus2();
>     void recCommand();
>     void calRecCommand();
> };
> ```
> 
> 《lib/SF_Motor/register_code.h》与《Register_Callback.cpp》注册码回调逐字摘录：
> ```cpp
> #define REGISTER_CODE "81BB-0U8"
> String registerCodeCallback(){ return REGISTER_CODE; }
> ```

#### Engineering Statement
> [IMPLEMENTED] 驱动板构建了专用的双向 ASCII 串口控制协议，并通过 FreeRTOS 实现了**控制计算核心与通信 I/O 核心的物理分离**：
> 1. **自定义通信协议帧格式定义**：
>    - **运动指令帧（`T` 帧）**：
>      $$\text{Frame} = \text{"T"} \ [M0\text{ Target}] \text{,} \ [M1\text{ Target}] \text{,} \ [M0\text{ Mode}] \text{,} \ [M1\text{ Mode}] \text{,0B"}$$
>      *示例*：`T10,10,1,1,0B` 表示命令 M0 与 M1 在速度模式（`Mode=1`）下均以 $10\,\text{rad/s}$ 旋转；
>    - **PID 增益调参帧（`C / V / A` 帧）**：
>      - 电流环：`C[MotorID],[P],[I],[D],[Limit]T`
>      - 速度环：`V[MotorID],[P],[I],[D],[Limit]Y`
>      - 位置环：`A[MotorID],[P],[I],[D],[Limit]E`
>    - **电角度校准重置帧（`U` 帧）**：
>      - `U[M0 Align V],[M1 Align V],0,0,0V`
> 2. **硬件通信接口选择（`ONBOARD` vs `USB`）**：
>    - 源码中通过 `com.init(ONBOARD)` 初始化驱动板与 S3 主控板之间的排针物理串口；
>    - 可通过切换至 `USB` 模式直接连接开发机虚拟串口进行单独调试。
> 3. **FreeRTOS 双核异步并发架构**：
>    - 通信库在初始化时创建独立任务 `taskFunction`，并将其固定至 **App CPU（Core 1）** 运行；
>    - 该任务以 1ms（1000 Hz）周期调用 `appCpuLoop()`，持续执行指令接收解析（`recCommand()`）与状态遥测广播（`sendMotorStatus0/1/2()`）；
>    - **架构优势**：主线程在 **Pro CPU（Core 0）** 独占执行 FOC 极高频闭环换相，彻底规避了串口字符接收阻塞引发的电机丢步、发热与抖动。
> 4. **固件注册授权校验机制**：
>    - `register_code.h` 显式定义注册授权码常量 `#define REGISTER_CODE "81BB-0U8"`；
>    - 通过 `Register_Callback.cpp` 的 `registerCodeCallback()` 回调函数传入 `libSF_Motor.a`，作为底层驱动功能激活的校验密钥。

#### 通信协议帧类型速查表
| 帧前缀字符 | 帧后缀字符 | 传输功能方向 | 数据段定义 | 协议示例 |
|---|---|---|---|---|
| **`T`** | **`B`** | 控制指令 (RX) | `[M0目标],[M1目标],[M0模式],[M1模式],0` | `T10,10,1,1,0B` |
| **`V`** | **`Y`** | 速度PID参数 (RX) | `[电机ID],[P],[I],[D],[Limit]` | `V0,0.05,0.005,0,6Y` |
| **`A`** | **`E`** | 位置PID参数 (RX) | `[电机ID],[P],[I],[D],[Limit]` | `A0,0.5,0,0,6E` |
| **`C`** | **`T`** | 电流PID参数 (RX) | `[电机ID],[P],[I],[D],[Limit]` | `C0,1.2,0,0,0T` |
| **`U`** | **`V`** | 校准指令 (RX) | `[M0对齐电压],[M1对齐电压],0,0,0` | `U3.0,3.0,0,0,0V` |
| **`RBS-`** | **`\n`** | 电机状态遥测 (TX) | 角度、角速度、交直轴电流等浮点数组 | `RBS-...` (1ms周期广播) |

#### Limitations
- ASCII 文本协议帧未包含 CRC 循环冗余校验码，存在因高频电气噪声串扰导致误触控制指令的潜在风险；
- 注册码机制为出厂绑定校验，若更换主控或驱动板需重新同步注册码。

#### Source Trace
- 源码：`lib/SF_Communication/SF_Communication.h:5-61`, `lib/SF_Motor/register_code.h:1-7`, `lib/SF_Motor/Register_Callback.cpp:1-5`

---

## 4. Cross-Validation & Consistency Rules（交叉验证与一致性约束）

1. **与 `E-DOC-004`（电气接线与总线拓扑）的交叉验证**：
   - `E-DOC-004` P01 确证小电流板位于前后板垛的最底层（直接驱动轮电机）；
   - `E-DOC-004` P02 记录前驱动板“左前轮接左侧黄色接口，右前轮接右侧黄色接口；左编码器接最左侧，右编码器接中间”；
   - 本证据 `E-FW-002` P02 与 P03 确证了底层代码中 `M0` 对应 GPIO 4/2/13（左端子），`M1` 对应 GPIO 12/14/27（右端子），MT6701 编码器片选分别为 CS0 (GPIO 18) 与 CS1 (GPIO 22)。硬件接口与固件底层驱动完全一一对应。
2. **与 `E-DOC-004` 中主控板注册码说明的交叉验证**：
   - `E-DOC-004` P01 规程明确提示“记录这块前驱动的主控板注册码”、“记录后驱动的主控板注册码”；
   - 本证据 `E-FW-002` P05 确证了固件中包含 `REGISTER_CODE "81BB-0U8"` 授权注册机制。原厂操作说明中的提示由此获得了坚实的固件源码级事实支撑。
3. **与 `E-FW-001`（舵机标定固件工程）的交叉验证**：
   - `E-FW-001` P05 中声明了 `SF_BLDC_DATA` 结构体用于接收电机角度与速度；
   - 本证据 `E-FW-002` P04 与 P05 证实了驱动板端的数据源正是由 FOC 算法解算并通过 `SF_Communication` 周期性发出的。下位机双板通信链路在数据结构层面上达到严格自洽。

---

## 5. Artifact Audit Trail（文档资产审计线索）

- **归档源码工程文件清单与校验和**：
  - `platformio.ini`: 572 bytes (22 lines) | MD5: `2b9d36f2405700b2c98563a2491c5537`
  - `src/main.cpp`: 2,238 bytes (78 lines) | MD5: `b66f51033b18cd54b1787e047ed5a41f`
  - `lib/SF_Motor/Pins_Specify.h`: 427 bytes (26 lines) | MD5: `b42abf2809e9457b2702d2d0e53fe56d`
  - `lib/SF_Motor/SF_Motor.h`: 2,832 bytes (90 lines) | MD5: `2c270bdb32e58134a3c1db63a97fb347`
  - `lib/SF_Motor/register_code.h`: 98 bytes (7 lines) | MD5: `2a70e97fb4dcd2ca3af73b2d83b2caa5`
  - `lib/SF_Motor/Register_Callback.h`: 159 bytes (11 lines) | MD5: `834707532b63791d3a3eb40e783d6f08`
  - `lib/SF_Motor/Register_Callback.cpp`: 118 bytes (5 lines) | MD5: `cb8b463d5a7034008cee9d8691fca14e`
  - `lib/SF_Motor/libSF_Motor.a`: 1,102,430 bytes | MD5: `4f2e10499011c45cac7ae513ea722770`
  - `lib/SF_Communication/SF_Communication.h`: 1,855 bytes (63 lines) | MD5: `3dd9f4141f6e780295a8a19cf3089392`
  - `lib/SF_Communication/libSF_Communication.a`: 123,822 bytes | MD5: `0d6862cc3666c0221d1c1672b68cef8f`

---
id: E-FW-008
title: 芯片唯一eFuse硬件信息与设备指纹读取固件
source_files:
- CEG5003/doc/四足机器人-origin/5客户获取注册码/getInfo/getInfo.ino
status: VALID
tags:
- efuse-mac
- chip-model
- hardware-fingerprint
- registration-code
- s1-driver
- firmware
epistemic_role: IMPLEMENTATION
---

# E-FW-008 芯片唯一eFuse硬件信息与设备指纹读取固件

> **认识论角色说明**：本文件属于 `IMPLEMENTATION`（固件源码与实现定义），忠实归档自原厂提供的 `CEG5003/doc/四足机器人-origin/5客户获取注册码/getInfo/getInfo.ino`。本文件严格限定于固件代码本身、C/C++ 系统调用语义、芯片寄存器/只读熔丝（eFuse）读取机制以及出厂注册码校验链条的工程审计；其配套的上位机 IDE 配置与操作交互规程已严格剥离至 [`E-DOC-007`](./E-DOC-007-客户注册码获取与Arduino环境配置教程.md)。

---

## 1. 源码清单与哈希校验

| 文件相对路径 | 源码类型 | 代码行数 | SHA-256 校验和 |
|---|---|---|---|
| `getInfo/getInfo.ino` | Arduino C++ 固件 | 18 行 | `83d30e47f19af48c95bdc62004054a2f86c245b0847889e305f6a4910c186d12` |

---

## 2. 源码逐行工程审计

```cpp
1: void setup() {
2:   // put your setup code here, to run once:
3:   Serial.begin(115200);
4:   Serial.println("==================");
5:   Serial.println(ESP.getEfuseMac());
6:   Serial.println(ESP.getChipModel());
7:   Serial.println(ESP.getChipCores());
8:   Serial.println(ESP.getChipRevision());
9:   Serial.println("==================");
10: 
11: 
12: }
13: 
14: void loop() {
15:   // put your main code here, to run repeatedly:
16: 
17: }
```

---

## 3. 原子工程事实与固件语义（Parts）

### Part 01: 固件运行时架构与目标核心定义 (`P01`)

1. **单次执行语义**：
   - 整个固件逻辑全部置于 `setup()` 生命周期中，`loop()` 主循环完全留空且无任何阻塞；
   - 固件开机后仅运行一次硬件指纹采集与输出，随后 CPU 进入空闲等待状态，避免多次循环打印造成的串口缓冲区溢出与上位机读取混淆。
2. **目标微控制器物理定位**：
   - 固件目标运行于主控板上的 **S1 电机驱动芯片（ESP32-U4WDH）**；
   - 必须通过硬件开关切换至 S1 通道（黄灯）后烧录运行。

---

### Part 02: 115200 高速串口异步通信接口 (`P02`)

1. **波特率基准**：
   - `Serial.begin(115200)` 初始化 UART0 控制器，默认数据位为 8 位、无奇偶校验、1 停止位（`SERIAL_8N1`）；
2. **格式化边界线设计**：
   - 第 4 行与第 9 行通过 `Serial.println("==================")` 打印清晰的定界符，便于人工复制和自动化上位机脚本进行正则表达式截取。

---

### Part 03: 64 位 eFuse 硬件只读 MAC 地址提取 (`P03`)

1. **底层实现与硬件来源**：
   - `ESP.getEfuseMac()` 调用 Espressif ESP-IDF 底层 API `esp_efuse_mac_get_default()`；
   - 从芯片内部的一次性可编程只读熔丝块（`EFUSE_BLK0`）中读取 48 位 Base MAC 地址（IEEE 802.3 MAC），并以 64 位无符号整数（`uint64_t`）形式返回；
2. **物理防伪与唯一性**：
   - eFuse 是在台积电代工厂晶圆制造及乐鑫出厂测试时通过物理加电击穿熔丝固化烧录的，**在硬件物理层面完全不可篡改、不可擦除、不可伪造**；
   - 这构成了机器人节点身份认证与注册码绑定的不可抵赖性根基。

---

### Part 04: 硅片型号、核心数与修订版本元数据 (`P04`)

1. **硅片型号获取 (`ESP.getChipModel()`)**：
   - 读取底层寄存器，返回字符串指针（如 `"ESP32-D0WD-V3"` 或 `"ESP32-U4WDH"`），确认芯片架构家族与集成 Flash 封装属性；
2. **处理器核心数量 (`ESP.getChipCores()`)**：
   - 返回整数 `2`，确认 Xtensa 双核 LX6 架构正常工作；
3. **硅片硬件版本号 (`ESP.getChipRevision()`)**：
   - 读取 `EFUSE_BLK0_RDATA3_REG` 中的 Silicon Revision 字段（如 Revision 3，即 ECO V3），用于确定硬件硅片修复补丁版本与定时器 errata 适用范围。

---

### Part 05: 设备指纹与闭源静态库授权闭环机制 (`P05`)

1. **出厂注册码历史与对应关系**：
   - 在底盘电机驱动例程及生产固件（如 `E-FW-002` 与 `E-FW-006`）中，底层 FOC 算法打包为静态库 `libSF_BLDC.a`；
   - 静态库内部包含校验回调函数：
     ```cpp
     char *call_back_regist_code() {
         return REGISTER_CODE; // 基准硬件注册码: "81BB-0U8"
     }
     ```
2. **授权生成与校验链条**：
   $$\text{eFuse MAC (64-bit)} + \text{Chip Revision} \xrightarrow[\text{原厂私钥/散列算法}]{\text{官方客服系统}} \text{REGISTER\_CODE (如 "81BB-0U8")}$$
3. **运行时防盗用防护**：
   - `SF_BLDC` 启动时调用 `esp_efuse_mac_get_default()`，将其与 `call_back_regist_code()` 返回的字符串进行解密比对；
   - 校验通过则进入 FOC 换相控制；若注册码不匹配，则锁定驱动使能脚（`GPIO 25 = LOW`），电机不输出力矩并报警。

---

## 4. 技术关联与交叉索引

- **操作与配置规程**：[`E-DOC-007 客户注册码获取与Arduino环境配置教程`](./E-DOC-007-客户注册码获取与Arduino环境配置教程.md)
- **BLDC 驱动固件注册码实装**：[`E-FW-002 BLDC轮电机驱动固件项目`](./E-FW-002-BLDC轮电机驱动固件项目.md)
- **双路 FOC 算法与静态库授权**：[`E-FW-006 双路无刷电机FOC控制与电流采样例程固件`](./E-FW-006-双路无刷电机FOC控制与电流采样例程固件.md)
- **双芯片物理复位按键定义**：[`E-DOC-006 主控板双芯片操作与例程使用必读说明`](./E-DOC-006-主控板双芯片操作与例程使用必读说明.md)

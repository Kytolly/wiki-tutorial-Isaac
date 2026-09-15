---
id: E-CAL-001
title: 实机执行器单通道动作隔离与故障阻断记录
source_files:
- /home/kytolly/Project/IsaacProject/doc/StackForceDog/artifacts/actuator_registration.csv
- /home/kytolly/Project/IsaacProject/doc/StackForceDog/artifacts/safety_validation.md
status: VALID
tags:
- actuator-registration
- fault-isolation
- emergency-cutoff
- physical-experiment
- ground-truth
epistemic_role: PHYSICAL
---

# E-CAL-001 实机执行器单通道动作隔离与故障阻断记录

> **认识论角色说明**：本文件属于 `PHYSICAL / CAL`（物理标定与异常故障记录），忠实归档自 `/home/kytolly/Project/IsaacProject/doc/StackForceDog/artifacts/actuator_registration.csv` 与 `safety_validation.md`。本文件严格限定于真机单通道执行器隔离动作测试、正反转极性定性、出厂偏置角与现场发生的真实通道失控断电事故记录；其通信时序测定数据见 [`E-TEST-001`](./E-TEST-001-实机架空通信时序与固件超时停机测定.md)。

---

## 1. 标定记录清单与哈希校验

| 数据记录文件 | 记录类型 | 标定通道数 | SHA-256 校验和 |
|---|---|---|---|
| `actuator_registration.csv` | CSV 单执行器隔离标定表 | 12 路执行器通道 | `23caa62add6c2d9b343e5a58153bc6e6e96aac8286d6d05cc9f31ecb4080db22` |

---

## 2. 真实物理执行器通道标定状态全景表

| 通道号 | 物理关节名 | 执行器代号 | 出厂偏置角 | 激励测试指令 | 持续时窗 | 观测旋转方向 | 正向运动语义 | 回中判定 | 现场异常记录 | 证据类别 |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | FR 外侧大腿 | FR-OM | $-4^\circ$ | $+5^\circ$ | 500 ms | 发生位移 | 未知方向 | **YES** | 无 | `HARDWARE_MEASURED` |
| **2** | FR 内侧大腿 | FR-IM | $-5^\circ$ | $+5^\circ$ | 500 ms | 发生位移 | 未知方向 | **YES** | 无 | `HARDWARE_MEASURED` |
| **3** | FL 内侧大腿 | FL-IM | $+5^\circ$ | $+5^\circ$ | 500 ms | 发生位移 | 未知方向 | **YES** | 无 | `HARDWARE_MEASURED` |
| **4** | FL 外侧大腿 | FL-OM | $-7^\circ$ | $+5^\circ$ | 750 ms | **顺时针 (CW)** | CW | **YES** | 无 | `HARDWARE_MEASURED` |
| **5** | RL 外侧大腿 | RL-OM | $-3^\circ$ | $+5^\circ$ | 750 ms | **逆时针 (CCW)** | CCW | **YES** | 无 | `HARDWARE_MEASURED` |
| **6** | RL 内侧大腿 | RL-IM | $-5^\circ$ | $+5^\circ$ | 750 ms | **顺时针 (CW)** | CW | **YES** | 无 | `HARDWARE_MEASURED` |
| **7** | RR 内侧大腿 | RR-IM | $-8^\circ$ | $+5^\circ$ | 500 ms | **持续异常上抬** | 未知方向 | <span style="color:red">**NO**</span> | **机械或伺服异常持续上抬** | `HARDWARE_MEASURED` |
| **8** | RR 外侧大腿 | RR-OM | $+8^\circ$ | $+5^\circ$ | 500 ms | 未独立测试 | 未知方向 | 未知 | **疑似受通道7动作机械联动耦合** | `HARDWARE_MEASURED` |
| **rear_M0** | RL 轮电机 | RL | 无 | $+0.5\,\text{rad/s}$ | 500 ms | 物理旋转 | 未知方向 | **YES** | 无 | `HARDWARE_MEASURED` |
| **rear_M1** | RR 轮电机 | RR | 无 | $+0.5\,\text{rad/s}$ | 500 ms | 本轮次未测 | 未知方向 | 推断 | 共享超时保护路径 | `INFERRED` |
| **target1** | 前置轮电机 1 | 前轮 | 无 | $+0.5\,\text{rad/s}$ | 500 ms | 物理旋转 | 未知方向 | **YES** | 无 | `HARDWARE_MEASURED` |
| **target2** | 前置轮电机 2 | 前轮 | 无 | $+0.5\,\text{rad/s}$ | 500 ms | 本轮次未测 | 未知方向 | 推断 | 共享超时保护路径 | `INFERRED` |

---

## 3. 原子工程事实与物理标定分析（Parts）

### Part 01: 8 路舵机物理拓扑通道映射与出厂偏置向量 (`P01`)

1. **通道与关节严格映射**：
   - 通道 1: `FR-OM`（前右外大腿，偏置 $-4^\circ$）；
   - 通道 2: `FR-IM`（前右内大腿，偏置 $-5^\circ$）；
   - 通道 3: `FL-IM`（前左内大腿，偏置 $+5^\circ$）；
   - 通道 4: `FL-OM`（前左外大腿，偏置 $-7^\circ$）；
   - 通道 5: `RL-OM`（后左外大腿，偏置 $-3^\circ$）；
   - 通道 6: `RL-IM`（后左内大腿，偏置 $-5^\circ$）；
   - 通道 7: `RR-IM`（后右内大腿，偏置 $-8^\circ$）；
   - 通道 8: `RR-OM`（后右外大腿，偏置 $+8^\circ$）；
2. **与出厂标定向量对比**：
   - 现场测得零位偏置向量为 $[-4, -5, 5, -7, -3, -5, -8, 8]^\top$；与出厂固件 `servo_off[8]` 宏 $[3, 5, -5, -7, 3, -5, -8, 8]^\top$ 相比，前几通道存在符号反转，反映了物理机器重新装配舵盘后的新零位。

---

### Part 02: 单通道隔离阶跃激励测试机制 (`P02`)

1. **测试规程**：
   - 严禁多关节同时下发运动，每次测试仅激活单一通道，其他通道置零锁定；
   - 注入微小微幅角位移 $+5^\circ$，持续固定脉冲时窗（$500\,\text{ms}$ 或 $750\,\text{ms}$）；
   - 人工架设高速摄像并近距肉眼核查物理舵机转轴旋转方向与复位行为。

---

### Part 03: 健康通道极性定性与复位确定性 (`P03`)

1. **旋向定性确立**：
   - 通道 4（`FL-OM`）在正向激励下沿顺时针（CW）旋转；
   - 通道 5（`RL-OM`）在正向激励下沿逆时针（CCW）旋转；
   - 通道 6（`RL-IM`）在正向激励下沿顺时针（CW）旋转；
2. **复位闭环确定性**：
   - 通道 1~6 在脉冲时窗结束后，均能可靠停止运动并精准返回初始平衡中位，回中判定均为 `YES`。

---

### Part 04: 通道 7 (RR-IM) 持续异常上抬与失控阻断事实 (`P04`)

1. **现场物理故障事实**：
   - 对通道 7（后右内侧关节）下发 $+5^\circ$ 激励；
   - 舵机动作后**并未在 500ms 窗口结束时停止，而是持续不断单向向上抬起（CONTINUED_RAISING）**；
   - 固件发出中位指令后该舵机无视指令，持续输出堵转级最大力矩；
2. **根因工程定性**：
   - 判定为该通道舵机内部电位器齿轮滑脱、反馈信号开路或驱动 H 桥烧穿导致的单向失控；
3. **安全断电阻断操作**：
   - 操作员在舵机抬至机械极限碰撞机身前，迅速手动拔除总动力电源插头实施硬断电，成功阻断了机架断裂或扫齿灾难。

---

### Part 05: 通道 8 (RR-OM) 联动耦合疑云与安全未决状态 (`P05`)

1. **连带受累现象**：
   - 由于通道 7 出现持续上抬故障并紧急切断电源，通道 8（`RR-OM`）未能完成单通道独立纯净测试；
   - 现场观察到在通道 7 动作期间通道 8 伴随微小晃动，怀疑五连杆末端刚性约束传递了被动力矩，或内部电路存在总线供电串扰；
2. **认识论状态冻结**：
   - 按照科学事实记录原则，通道 8 状态冻结为 `COUPLED_MOTION_FROM_CHANNEL7_SUSPECTED`，必须在更换通道 7 故障执行器后重新实施独立物理复测。

---

## 4. 技术关联与交叉索引

- **实机架空通信与看门狗测定**：[`E-TEST-001 实机架空通信时序与固件超时停机测定`](./E-TEST-001-实机架空通信时序与固件超时停机测定.md)
- **舵机交互式标定固件**：[`E-FW-001 双足轮腿舵机标定固件项目`](./E-FW-001-双足轮腿舵机标定固件项目.md)
- **整机机械装配指南**：[`E-DOC-003 四足机器人整机机械安装与调试指南`](./E-DOC-003-四足机器人整机机械安装与调试指南.md)

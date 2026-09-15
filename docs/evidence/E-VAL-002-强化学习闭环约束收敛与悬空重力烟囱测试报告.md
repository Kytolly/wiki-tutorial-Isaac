---
id: E-VAL-002
title: 强化学习闭环约束收敛与悬空重力烟囱测试报告
source_files:
- /home/kytolly/Project/IsaacProject/sf_quad/validation/rl_qualification.json
status: VALID
tags:
- rl-qualification
- chimney-test
- closure-residual
- contact-sensors
- validation-report
epistemic_role: VALIDATION
---

# E-VAL-002 强化学习闭环约束收敛与悬空重力烟囱测试报告

> **认识论角色说明**：本文件属于 `RUNTIME / TEST`（验证与测试报告），忠实归档自 `/home/kytolly/Project/IsaacProject/sf_quad/validation/rl_qualification.json`。本文件严格限定于机器人闭环 USD 资产在 Isaac Lab 物理仿真环境下的动态接触力张量、闭环副残差收敛性、单腿激励跟随以及悬空重力下 240 步烟囱测试事实的审计；其静态执行器划分见 [`E-VAL-001`](./E-VAL-001-仿真资产静态执行器与被动关节空间划分校验报告.md)。

---

## 1. 产物清单与哈希校验

| 校验报告文件 | 任务环境标识 | 物理参数就绪状态 | SHA-256 校验和 |
|---|---|---|---|
| `rl_qualification.json` | `Template-Sf-Quad-Direct-v0` | `ESTIMATED_PLACEHOLDER` | `e8114adb6fc96251f7745881beff5489491456a799c230ee0b2e318ab17e3c26` |

---

## 2. 动态测试套件概览

| 测试项代号 | 测试目标 | 判定准则 | 实测数据 | 结果 |
|---|---|---|---|---|
| `contact_sensor_audit` | 5 个接触力传感器绑定 | 形状 `[1, 1, 3]` 无丢帧 | `base_link` + 4足端全部成功绑定 | **PASS** |
| `reset_closure` | 复位瞬间闭环残差 | 锚点 $<1.0\,\text{mm}$，角度 $<0.01\,\text{rad}$ | 锚点最大 $0.691\,\text{mm}$，角度 $3.92\times 10^{-7}\,\text{rad}$ | **PASS** |
| `zero_command` | 悬空重力 240 步积分 | `nan_count == 0`，无数值发散 | 240 步平稳完成，NaN 计数为 0 | **PASS** |
| `FR_M1_excitation` | 大腿外侧舵机阶跃响应 | 被动连杆平滑跟随 | 主动峰值 $0.077\,\text{rad}$，小腿跟随 $0.059\,\text{rad}$ | **PASS** |
| `FR_M2_excitation` | 大腿内侧舵机阶跃响应 | 被动连杆平滑跟随 | 主动峰值 $0.072\,\text{rad}$，内臂跟随 $0.053\,\text{rad}$ | **PASS** |
| `passive_action_negative` | 越界控制指令拦截 | 拒绝对被动关节下发指令 | 严格拦截并返回拒斥提示 | **PASS** |
| `ground_settle` | 地面着陆平衡接触 | 240 步接触无自激抖动 | 闭环锚点最大误差 $0.215\,\text{mm}$ | **PASS** |

---

## 3. 原子工程事实与测试审计（Parts）

### Part 01: 5 节点接触力传感器张量审计 (`P01`)

1. **传感器绑定刚体**：
   - 包含 1 个机身刚体 `base_link` 与 4 个轮端接触连杆 `FR_foot_Link`, `FL_foot_Link`, `RL_foot_Link`, `RR_foot_Link`；
2. **张量输出维度对齐**：
   - 所有 5 处传感器采集张量形状均为标准三维力向量 `[num_envs=1, num_bodies=1, 3]`，精确输出法向力与切向切应力，无内存泄漏与数据丢失。

---

### Part 02: 初始复位闭环副残差精度收敛 (`P02`)

1. **测试条件与容差限**：
   - 容差门限：锚点平移误差 $\le 1.0\,\text{mm}$，轴向旋转误差 $\le 0.01\,\text{rad}$ ($0.57^\circ$)；
2. **四腿实测闭环残差**：
   - `FR_W2_closure_joint`: 锚点误差 $0.639\,\text{mm}$，轴向误差 $2.10 \times 10^{-7}\,\text{rad}$；
   - `FL_W2_closure_joint`: 锚点误差 $0.601\,\text{mm}$，轴向误差 $3.92 \times 10^{-7}\,\text{rad}$；
   - `RL_W2_closure_joint`: 锚点误差 $0.691\,\text{mm}$，轴向误差 $1.74 \times 10^{-7}\,\text{rad}$；
   - `RR_W2_closure_joint`: 锚点误差 $0.638\,\text{mm}$，轴向误差 $2.68 \times 10^{-7}\,\text{rad}$；
   - 证明闭环副重构具有极高的几何精度，初始装配应力微乎其微。

---

### Part 03: 悬空重力 240 步烟囱测试 (`P03`)

1. **测试机制**：
   - 将机器人悬浮于仿真空间，12 路执行器全部下发 0 力矩指令（自由下垂状态），在标准重力场（$-9.81\,\text{m/s}^2$）下持续推进 240 个物理仿真步长（$\Delta t = 0.005\,\text{s}$，总计 1.2 秒）；
2. **判定事实**：
   - 整个仿真推进周期内 `nan_count = 0`，未出现关节速度发散或物理坐标溢出，通过了严苛的数值稳定性基线考核。

---

### Part 04: M1/M2 阶跃动态激励与机构响应 (`P04`)

1. **FR_M1 阶跃激励实测**：
   - 目标关节 `FR_thigh_joint` 响应峰值达 $0.0771\,\text{rad}$，角速度达 $1.409\,\text{rad/s}$；
   - 从动小腿 `FR_calf_joint` 产生 $0.0591\,\text{rad}$ 运动跟随，被动副施加控制力矩为 $0.0\,\text{N}\cdot\text{m}$；闭环副锚点误差减小至 $0.229\,\text{mm}$；
2. **FR_M2 阶跃激励实测**：
   - 目标关节 `FR_M2_joint` 响应峰值达 $0.0723\,\text{rad}$，角速度达 $1.340\,\text{rad/s}$；
   - 内侧连杆 `FR_P2_joint` 产生 $0.0531\,\text{rad}$ 平滑偏转，闭环副残差进一步收敛至 $0.0925\,\text{mm}$。

---

### Part 05: 越界动作指令拦截与负对照断言 (`P05`)

1. **越界指令下发测试**：
   - 向被动连杆 `FR_P2_joint` 尝试注入策略动作；
2. **安全防护断言生效**：
   - 框架通过 `passive_action_negative` 判定为 `rejected = True`，拦截原因记录为 `"FR_P2_joint is not addressable in the 12-dimensional policy action."`，证实强化学习策略与底层被动机构实现了严格的软硬件防呆隔离。

---

## 4. 技术关联与交叉索引

- **静态执行器划分报告**：[`E-VAL-001 仿真资产静态执行器与被动关节空间划分校验报告`](./E-VAL-001-仿真资产静态执行器与被动关节空间划分校验报告.md)
- **PhysX 闭环副定义**：[`E-SIM-003 PhysX闭环副自动重构与USD后处理实现`](./E-SIM-003-PhysX闭环副自动重构与USD后处理实现.md)
- **几何装配参考系契约**：[`E-SIM-002 双支链闭环几何装配不变量与参考系配置`](./E-SIM-002-双支链闭环几何装配不变量与参考系配置.md)

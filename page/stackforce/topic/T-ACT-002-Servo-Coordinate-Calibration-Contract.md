# T-ACT-002 — Servo Coordinate & Calibration Contract

> 专题编号：`T-ACT-002`  
> 状态：`ANALYZED` / `UNRESOLVED_HARDWARE`  
> 范围：仿真关节弧度空间 $q_{\text{sim}}$ 到实机舵机 PWM 脉宽/角度空间 $u_{\text{cmd}}$ 的数学映射契约、机械零位 $u_0$、旋向极性 $s$、量程安全边界与实机未决项审计。

---

## 1. Engineering Question（核心工程问题）

仿真模型中的 8 维腿部髋关节位置 $q_{\text{sim}} \in [q_{\min}, q_{\max}]$（单位：rad，基于单父树 URDF 关节坐标系）如何确定性、无歧义地映射至实机 Stack B PCA9685PW 驱动器的输出指令 $u_{\text{cmd}}$（单位：$\mu\text{s}$ 或 0–300°），如何标定各执行器的机械零位偏置 $u_0$ 与旋向符号 $s$，以及在 Channel 7 物理故障未除的现状下，如何界定当前系统的安全约束？

---

## 2. Evidence Set（引用证据集合）

### Specification / Firmware Implementation
- `[[E-FW-001#P02]]` — 双足轮腿固件 8 舵机交互式标定协议与出厂预设偏移数组 `servo_off[8]`。
- `[[E-FW-001#P03]]` — PCA9685PW 50Hz PWM 发生器驱动，500–2500 $\mu\text{s}$ 线性映射至 0–300°。
- `[[E-DOC-005#P03]]` — 出厂联调指南中规定的舵机机械水平零位对齐规程。

### Physical Calibration / Ground Truth
- `[[E-CAL-001#P01-P03]]` — 实机单通道动作隔离测试、FL/RL 舵机旋向定性（CW / CCW）实测数据。
- `[[E-CAL-001#P04-P05]]` — Channel 7（`RR_Inner_Servo`）持续异常上抬物理故障事实与闭链牵连分析。
- `[[E-TEST-001#P02]]` — PCA9685 50Hz 周期更新与 20ms 帧时序。

### Simulation Assets & Invariants
- `[[E-SIM-001#P03]]` — 单父树 URDF 中 8 髋关节的旋转轴向量 $\mathbf{a}_j = [0, \pm 1, 0]$ 与位置限位 $[-1.047, 1.047]$ rad。
- `[[E-SIM-002#P04]]` — 底盘左右对称反射矩阵与镜像轴旋向变换。

---

## 3. Mathematical Mapping Contract（数学映射契约）

### 3.1 标定映射方程
对于任意合法关节 $j \in \{\text{FL\_Outer, FL\_Inner, FR\_Outer, FR\_Inner, RL\_Outer, RL\_Inner, RR\_Outer, RR\_Inner}\}$，仿真关节弧度 $q_j$ 与实机舵机目标指令 $u_j$ 满足如下仿射变换：

$$
u_j = u_{0, j} + s_j \cdot k_j \cdot q_j
$$

其中：
- $q_j$：仿真髋关节旋转弧度（rad），以机构装配中位为 0；
- $u_{0, j}$：该舵机的实机机械零位偏置（Mechanical Zero Offset），对应仿真 $q_j = 0$ 时的实机指令值；
- $s_j \in \{+1, -1\}$：旋向符号因子（Polarity / Direction Sign），确保仿真正旋转方向与实机物理正旋转严格同义；
- $k_j$：刻度缩放系数（Scale Factor），由舵机脉宽/角度灵敏度决定：
  $$
  k_j = \frac{2000\,\mu\text{s}}{300^\circ \times (\pi / 180^\circ\,\text{rad/deg})} \approx 381.97\,\mu\text{s/rad} \quad \left(\text{或 } \frac{180}{\pi} \approx 57.2958\,^\circ/\text{rad}\right)
  $$

---

## 4. Cross-Validation Matrix（交叉验证矩阵）

| Canonical Actuator | PCA 通道 | 驱动主动关节 | 标定偏移 $u_0$（出厂预设） | 旋向符号 $s$（实测） | 比对状态 | 状态说明与未决事实 |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| `FR_Outer_Servo` | PCA1 | `FR_Outer_Hip_Joint` | -4° (`0xFB`) | `TBD` | **UNRESOLVED** | 架空测试受 ch7 故障中断，尚未实测极性 |
| `FR_Inner_Servo` | PCA2 | `FR_Inner_Hip_Joint` | -5° (`0xFA`) | `TBD` | **UNRESOLVED** | 架空测试受 ch7 故障中断，尚未实测极性 |
| `FL_Inner_Servo` | PCA3 | `FL_Inner_Hip_Joint` | +5° (`0x05`) | `TBD` | **UNRESOLVED** | 架空测试受 ch7 故障中断，尚未独立定标 |
| `FL_Outer_Servo` | PCA4 | `FL_Outer_Hip_Joint` | -7° (`0xF9`) | `+1` (CW) | **VERIFIED** | 实测 +5° 触发 CW 旋转（`E-CAL-001#P02`） |
| `RL_Outer_Servo` | PCA5 | `RL_Outer_Hip_Joint` | -3° (`0xFD`) | `-1` (CCW) | **VERIFIED** | 实测 +5° 触发 CCW 旋转（`E-CAL-001#P02`） |
| `RL_Inner_Servo` | PCA6 | `RL_Inner_Hip_Joint` | -5° (`0xFA`) | `+1` (CW) | **VERIFIED** | 实测 +5° 触发 CW 旋转（`E-CAL-001#P02`） |
| `RR_Inner_Servo` | PCA7 | `RR_Inner_Hip_Joint` | -8° (`0xF8`) | `FAIL` | **CONFLICT** | ⚠️ **硬件异常持续上抬失控，物理阻断** |
| `RR_Outer_Servo` | PCA8 | `RR_Outer_Hip_Joint` | +8° (`0x08`) | `TBD` | **BLOCKED** | ⚠️ **受 ch7 五杆闭链机械牵连，无法独立测试** |

---

## 5. Engineering Conclusion（工程学结论）

- **SUPPORTED（有充分证据支持的事实）**：
  1. 映射关系遵循仿射线性模型 $u_j = u_{0, j} + s_j \cdot k_j \cdot q_j$；
  2. PCA9685PW 输出频率固定为 50Hz，脉宽区间 `[500, 2500]` $\mu\text{s}$ 对应线性区间 `[0, 300]` 度；
  3. `FL_Outer_Servo`、`RL_Outer_Servo` 与 `RL_Inner_Servo` 的相对旋向已在实机架空下证实（`E-CAL-001#P02`）。
- **INFERRED（合理工程推断）**：
  1. 左右侧大腿与小腿在底盘坐标系下呈镜像对称，其符号因子 $s_j$ 理论上应与 `E-SIM-002#P04` 反射矩阵一致，但必须由实机测试闭环证实；
  2. 固件中硬编码的 `servo_off` 仅为原厂组装粗调偏置，不能替代高精度激光或卡尺机械零位真值。
- **UNRESOLVED（当前未决项）**：
  1. `FR_Outer_Servo`、`FR_Inner_Servo`、`FL_Inner_Servo` 尚未完成独立极性实测；
  2. `RR_Inner_Servo` 存在硬件故障，导致右后腿完全无法进行零位或极性标定；
  3. 整机 8 舵机在未检修复测前，全局运动范围必须严格限制在 `TBD_SAFE_RANGE`。

---

## 6. Conflicts & Open Questions（冲突与未决问题）

- **C-01 [HARDWARE FAULT]**：PCA7 通道舵机（`RR_Inner_Servo`）在 `E-CAL-001#P04` 中被证实持续上抬失控，无法执行回中命令，导致实机零位标定链路中断。
- **M-01 [MISSING EVIDENCE]**：缺少修复 Channel 7 后的 8 通道全机小阶跃极性测量与高精度机械零位测量 CSV 数据。
- **Q-01 [OPEN QUESTION]**：待实机硬件检修完成后，必须严格执行架空逐通道单步测试，测定全部 8 个通道的 $u_0$ 与 $s$，输出正式标定证据并解除 `TBD_SAFE_RANGE` 锁定。

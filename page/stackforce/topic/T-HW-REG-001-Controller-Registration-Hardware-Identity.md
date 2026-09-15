# T-HW-REG-001 — Controller Registration & Hardware Identity

> 专题编号：`T-HW-REG-001`  
> 状态：`ANALYZED`  
> 核心任务：解耦并严格审计 ESP32 控制器硬件注册码、eFuse 芯片指纹、官方出厂固件授权机制与真实机器物理身份（Hardware Identity）的论证边界，杜绝证据越级（Overclaim）。

---

## 1. Engineering Question（工程分析问题）

在 StackForce 嵌入式固件体系中，注册码获取机制、固件源码中的宏常量与当前实验室内真机的实际硬件注册码之间，是否存在一一对应关系？如何建立严格的认知证据链？

---

## 2. Evidence Set（证据集合）

- `E-DOC-006#P04` — S1 芯片硬件复位串口输出注册码机制（文档规程）。
- `E-DOC-007#P05` — 串口监视器监听与向官方客服提取注册码规程（流程事实）。
- `E-FW-008#P03` — 64 位 eFuse 硬件只读 MAC 地址提取代码（源码事实）。
- `E-FW-008#P04` — 芯片型号、核心数与修订版本元数据（源码事实）。
- `E-FW-008#P05` — 设备指纹与闭源静态库授权校验闭环机制（源码机制）。
- `E-DOC-007#P05` — 历史会话中提取到的两组出厂注册码记录（`DFI9-VML1` / `6A49-1SK1`）。

---

## 3. Provenance Stratification（认识论分层原则）

项目组确立以下五层严格区分原则，禁止跨层等价推导：

```text
Level A: Registration mechanism exists (硬件授权机制存在)
    ↓ (不等价)
Level B: Registration retrieval procedure exists (注册码提取规程存在)
    ↓ (不等价)
Level C: Firmware source contains REGISTER_CODE (开源/示例源码中包含注册码字符串)
    ↓ (不等价)
Level D: Current physical Front controller registration code (当前真机前控制板物理注册码)
    ↓ (不等价)
Level E: Current physical Rear controller registration code (当前真机后控制板物理注册码)
```

### 严格论证准则

1. **A/B/C 不证明 D/E**：固件源码中存在 `REGISTER_CODE = "..."` 仅证明“该代码库包含此默认常量”，不能证明“实验室当前这台真机的前后板一定烧录并接受该注册码”。
2. **物理指纹唯一性**：ESP32 的出厂注册码基于芯片唯一 eFuse MAC 地址（64-bit）生成。不同物理板垛的 eFuse 必不相同。
3. **真实机身当前状态**：
   - 现场已测出并验证 Front 对应 `DFI9-VML1`，Rear 对应 `6A49-1SK1`。
   - 必须记录为“特定物理批次机器实测提取”，而不作为全项目普适的泛化先验。

---

## 4. Cross-Validation Matrix（交叉验证矩阵）

| 对照维度 | 涉及证据 Part | 判定状态 | 详细分析说明 |
|---|---|---|---|
| 机制存在性 ↔ 提取规程 | `E-DOC-006#P04` vs `E-DOC-007#P05` | **CONSISTENT** | 官方文档与例程均指明 S1 芯片启动时通过 115200 串口输出硬件校验码。 |
| 源码算法 ↔ eFuse 物理层 | `E-FW-008#P03` vs `E-FW-008#P05` | **VERIFIED** | 源码通过读取底层 `esp_efuse_mac_get_default()` 获取硬件唯一标识。 |
| 示例常量 ↔ 真机实体码 | 示例代码 vs 实机提取码 | **DISTINCT** | 示例代码中出现的测试码仅为占位符；真机实体码必须经由实测串口读取提取。 |
| 当前机身 Stack A/B 绑定 | 实机测试记录 vs `E-DOC-007#P05` | **RECORDED** | 前板（Stack A / Device 0x02）绑定 `DFI9-VML1`；后板（Stack B / Device 0x01）绑定 `6A49-1SK1`。 |

---

## 5. Engineering Conclusion（工程结论）

- **SUPPORTED**：主控板双芯片架构中，S1 运行授权校验与底层驱动，其注册码绑定机制由硬件 eFuse 保证物理唯一性。
- **SUPPORTED**：当前实验室真机的出厂注册码已归档至 `E-DOC-007#P05`（`DFI9-VML1` | `6A49-1SK1`），可用于后续固件重新编译与烧录。
- **UNRESOLVED**：未来若更换主板或更换控制器芯片，旧注册码立即失效，必须重新按 `E-DOC-007` 规程提取新芯片硬件指纹并向官方换取新注册码。

---

## 6. 更新日志

- 2026-09-15：创建标准控制器注册与硬件身份分析 Topic；规范 Level A~E 认识论分层；明确区分源码常量与实机物理注册码。

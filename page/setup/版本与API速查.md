# 版本与API速查

> 本页属于：setup 环境与 Demo（版本/迁移速查）
> 前置知识：[[安装与环境配置]]
> 预计阅读时间：10 分钟

## 🎯 为什么需要这一页？

Isaac Sim / Isaac Lab 迭代快，网上教程常对不上号：有的用 4.x 独立版、有的用 5.x/6.x pip、API 名字也在变（如 `AppLauncher`、`SimulationCfg`）。本页集中放**本讲义采用的版本组合**、**常见搭配**、以及 **3.0 迁移提示**，当作"查版本"的速查表。

## 🐍 当前版本状况（截至 2026-09-01）

| 组件 | 本讲义采用 | 说明 |
|------|-----------|------|
| **Isaac Sim** | pip 路线 `5.1.0`（官方最新 pip `6.x`） | pip 版是官方主推；独立桌面版最后一代 4.5.0，Omniverse Launcher 2025-10 起逐步弃用 |
| **Isaac Lab** | v2.3.2（稳定）/ 3.0-beta（可选） | 官方最稳 build；3.0 系列处于 beta，迁移有 API 变化 |
| **Python** | 3.11 | 2.x 教程常用 3.11；Isaac Sim 6.x 起多要求 Python 3.12 |
| **PyTorch** | 2.7.0（cu128） | 与 Isaac Sim 5.x/6.x 配套 |
| **CUDA** | 12.8 | cu128 对应的 PyTorch/CUDA 档位 |

> 判断原则：**跟随官方 Quickstart 的"已验证组合"**，别混用不同版本的命令。想尝鲜 3.0 就整套按 3.0 文档装，别在 2.3.2 环境里混 3.0 代码。

## 📝 两条安装组合（二选一）

| 组合 | 安装对象 | 适合 |
|------|----------|------|
| **组合 A（本讲义主推）** | Isaac Sim 5.1.0 + Isaac Lab 源码（v2.3.2）+ PyTorch 2.7.0(cu128) + Python 3.11 | 稳定、教程命令齐、可复现 |
| **组合 B（尝鲜 3.0 / Sim 6.x）** | Isaac Sim 6.x + Isaac Lab 3.0-beta + Python 3.12 | 想用新特性（新 CLI `isaaclab train`、视觉/Newton 集成等） |

> 组合 B 的具体安装以官方 3.0 安装文档为准（见下方链接）；本讲义其余页面的命令主要按组合 A 编写。

## 🗺️ 关键 API 的版本提示

| API / 入口 | 2.x 常见写法 | 3.0 提示 |
|-----------|-------------|----------|
| 启动 App | `AppLauncher(...)` | 3.0 的启动/CLI 与 headless 行为有调整，见迁移文档 |
| 训练入口 | `python scripts/.../train.py --task ...` | 3.0 新 CLI：`./isaaclab.sh train --rl_library rsl_rl --task ...`（或 `uv run isaaclab train ...`） |
| 环境配置 | `SimulationCfg` / `ManagerBasedRLEnvCfg` | 3.0 部分配置字段/默认值变化，迁移后先核对 |
| 观测/奖励 | `ObservationTermCfg` / `RewardTermCfg` | 3.0 保留管理器模型，细节以文档为准 |

> 用得上 Beta 前，建议先读官方 **Migrating to Isaac Lab 3.0**（见下方），并按你要用的版本把命令/API 逐个对齐。

## 🗒️ 常见问题 FAQ

**Q1：我该用 2.x 还是 3.0？**
新手/求稳用 2.x（v2.3.2）跑通全流程；想用新特性、并愿意处理迁移坑再上 3.0-beta。本讲义主体按 2.x。

**Q2：看到教程用 `4.5.0 独立版`，和 5.1.0 pip 冲突吗？**
不冲突，但独立版与 pip 版是两套；**别混用**。本讲义一律用 pip 版路线（见 [[安装与环境配置]]）。

**Q3：能只升级 Isaac Sim 不动 Isaac Lab？**
不建议。Isaac Sim 与 Isaac Lab 版本有配套关系；升级 Sim 也要核对 Lab 是否兼容，否则传感器/物理 API 可能对不上。

**Q4：某 API 在 3.0 报错？**
按官方 3.0 迁移文档（下方链接）改；核心思路：入口用 `isaaclab train`、常用配置类大多保留，但字段/默认值以 3.0 文档为准。

## ✏️ 小练习

**1.** 想跟着本讲义学，最稳的版本组合是？

<details>
<summary>查看答案</summary>

Isaac Sim 5.1.0（pip）+ Isaac Lab v2.3.2（源码）+ PyTorch 2.7.0(cu128) + Python 3.11。
</details>

**2.** 3.0 新训练入口命令行和 2.x 有什么不同？

<details>
<summary>查看答案</summary>

2.x 常用 `python scripts/reinforcement_learning/<backend>/train.py --task ...`；3.0 可用 `./isaaclab.sh train --rl_library <backend> --task ...`（或 uv run isaaclab train ...）。
</details>

**3.** 为什么不要去"只升级 Sim 不升级 Lab"？

<details>
<summary>查看答案</summary>

Sim 与 Lab 有配套版本关系；Sim 升级后部分 API/物理/传感器默认值可能变化，Lab 不匹配会报错或行为异常。应整套装一套已验证组合。
</details>

## 本章小结

- 版本速查：本讲义按 Isaac Sim 5.1.0 + Isaac Lab v2.3.2 + PyTorch 2.7.0(cu128)/Python 3.11。
- 3.0 是 beta，新 CLI、API 有变化；想尝鲜就整套按 3.0 装。
- 遇到版本/API 对不上，先回本页核对，再按官方迁移文档对齐。

## 下一步

- 上一页：[[物理仿真设置]]
- 下一页：[[强化学习核心概念]]（进入训练理论）
- 返回：[[Home]]

## 更新日志

- 2026-09-01：新增本页（版本与 API 速查）。来源：Isaac Lab 安装/Release Notes（<https://isaac-sim.github.io/IsaacLab/v2.3.2/source/setup/quickstart.html>、<https://isaac-sim.github.io/IsaacLab/release/3.0.0-beta2/source/setup/installation/pip_installation.html>）、Migrating to Isaac Lab 3.0（<https://isaac-sim.github.io/IsaacLab/develop/source/migration/migrating_to_isaaclab_3-0.html>）（访问于 2026-09-01）。

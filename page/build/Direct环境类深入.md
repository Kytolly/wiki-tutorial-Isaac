# Direct环境类深入

> 本页属于：build 自建环境进阶
> 前置知识：[[第一个训练任务]]、[[渲染与LiDAR感知]]
> 预计阅读时间：20 分钟

## 🎯 为什么需要这个？

[[第一个训练任务]] 里你用 `./isaaclab.sh --new` 生成了一个 Direct 工作流模板，但它是**黑盒**：为什么环境类是 `DirectRLEnv`？`decimation` 到底怎么决定决策频率？`_get_rewards()` 里的 `rew_scale_*` 又是在哪一步被算出来的？

本页把 Direct 环境类的**生命周期**拆开讲清楚——你看懂了这 5 个方法，模板就不再是魔法，而是"哪一步该写什么"的填空。

## 💡 一个类比

把 Direct 环境想成一个**带剧本的循环**：每一集（episode）里，导演（策略）给出动作 → 剧组（物理引擎）推进一 "决策周期" → 场记（观测）记录 → 评委（奖励函数）打分 → 如果演砸了就重开一场（reset）。

```
策略给动作 → 环境推进物理(decimation步) → 记录观测 → 算奖励 → 结束/重置
```

## 🐍 最小必要知识

| 概念 | 是什么 | 类比 |
|------|--------|------|
| **`DirectRLEnv`** | 直接手写环境循环的基类，所有逻辑都在一个类里 | 一体成型的小剧场（自己调度一切） |
| **`DirectRLEnvCfg`** | 它的配置类（`@configclass`），定义 sim/scene/decimation 等 | 剧场的"排班表" |
| **`decimation`** | 每个决策周期内推进几个物理步；决策频率 = 物理频率 ÷ decimation | 导演每看几帧才喊一次"act" |
| **生命周期方法** | `_setup_scene/_pre_physics_step/_apply_action/_get_observations/_get_rewards/_reset_idx` | 剧本里必须写的固定桥段 |
| **`self.scene` / `self.robot`** | 场景与机器人资产对象 | 舞台与主角 |
| **向量化** | `num_envs` 份环境并行，所有张量第 0 维是"环境数" | 同时开 N 个考场 |

## 🖼️ 图解：Direct 环境一个决策周期

图 1 Direct 环境一 step 的生命周期（来源：自绘 Mermaid，本地预览渲染；GitHub Wiki 上以代码块显示；访问于 2026-09-01）

```mermaid
flowchart TD
    A[env.step(action)] --> B[_pre_physics_step: 把 action 写进关节/执行器目标]
    B --> C[推进 decimation 个物理步<br/>SimulationCfg.dt × decimation]
    C --> D[_get_observations: 读机器人/传感器状态]
    D --> E[_get_rewards: 按奖励公式算 reward]
    E --> F{terminated / truncated?}
    F -- 是 --> G[_reset_idx: 重开对应环境]
    G --> H[返回 obs, reward, terminated, ..., info]
    F -- 否 --> H
```

## 📝 逐方法拆解（以 Direct 倒立摆/四足为参考）

下面把 5 个骨架方法逐个讲，括号里是你要填"该环节想干什么"。

### 1. `_setup_scene()`：搭舞台

```python
def _setup_scene(self):
    # 1. 添加地面与灯光（GroundPlaneCfg / 默认光照）
    self.scene.ground = GroundPlaneCfg(prim_path="{ENV_REGEX_NS}/Ground").class_type(self)
    # 2. 添加机器人资产（ArticulationCfg：USD 路径 + 关节 + 执行器）
    self.robot = ArticulationCfg(prim_path="{ENV_REGEX_NS}/Robot", spawn=UsdFileCfg(usd_path=...)).class_type(self)
    # 3. 添加传感器（CameraCfg/RayCasterCfg...）
    self.scene.ray_caster = RayCasterCfg(...).class_type(self)
    # 4. 关键：必须调用，否则场景不生效
    self.scene.clone_environments(copy_from_source=False)
    self.scene.filter_collisions(global_prim_paths=[...])
```

### 2. `_pre_physics_step(actions)`：把动作变成指令

```python
def _pre_physics_step(self, actions):
    # actions 形状 (num_envs, action_dim)
    self.actions = actions                     # 存起来给 _apply_action 用
    # 若用关节位置控制：
    self.robot.set_joint_position_target(self.actions * self.cfg.action_scale)
```

### 3. `_apply_action()`：真正执行（Direct 里通常就在 pre_physics 里设置完成，这里可留空或做前馈）

```python
def _apply_action(self):
    # Direct 里动作已在 _pre_physics_step 中写入执行器目标，本方法常用于占位/后处理
    pass
```

### 4. `_get_observations()`：回报观测

```python
def _get_observations(self):
    # 返回可被 RL 库消费的张量或 dict（名 → (num_envs, obs_dim)）
    obs = torch.cat([self.robot.data.joint_pos, self.robot.data.joint_vel], dim=1)
    return {"policy": obs, "critic": obs}      # policy 给策略，critic 可选特权观测
```

### 5. `_get_rewards()`：打赏

```python
def _get_rewards(self):
    # 示例：一直活着 +1，杆子倾斜扣分（用关节角/速度计算）
    alive = torch.ones_like(self.robot.data.joint_pos[:, 0])
    tilt_penalty = -torch.abs(self.robot.data.joint_pos[:, 0]) * self.cfg.rew_scale_tilt
    return alive + tilt_penalty
```

### 6. `_reset_idx(env_ids)`：重开

```python
def _reset_idx(self, env_ids):
    # 只重置指定这几份环境（部分重置），不必整批重开
    self.robot.reset(env_ids)
    self.robot.write_joint_state_to_sim(
        self.robot.data.default_joint_pos[env_ids],
        self.robot.data.default_joint_vel[env_ids],
        env_ids=env_ids,
    )
```

> 关键习惯：**所有张量都带环境维**（`num_envs`），并按 `env_ids` 做**部分重置**——Direct 环境下，场景克隆后各环境相互独立，批量接口都是这样按 id 操作。

## 🗒️ 常见问题 FAQ

**Q1：`decimation` 和 `dt` 谁决定频率？**
决策频率 = 物理频率 ÷ decimation。`SimulationCfg(dt=1/120)` + `decimation=2` ≈ 每 60Hz 做一次决策；`decimation` 越大，策略看得越"稀疏"，控制越糙但越省算力。

**Q2：Direct 和 Manager 的区别一句话？**
Direct：所有环节手写在类里（直观、路径短）；Manager：把动作/观测/奖励/事件拆成可替换的"管理器"模块（模块化、易复用）。

**Q3：`_reset_idx` 为什么只重置部分环境？**
RL 里各环境回合结束时间不同。部分重置让已结束的环境立即重开、其余继续跑，保证并行度不因"扎堆结束"而掉下来。

**Q4：怎么让策略看到传感器？**
在 `_setup_scene` 加 `RayCasterCfg`/`CameraCfg`，然后 `_get_observations` 里拼 `self.scene.ray_caster.data.distances` 或 `self.camera.data.output["rgb"]`。

**Q5：模板里 `state_space` 和 `observation_space` 区别？**
`state_space` 是"上帝知道的全状态"（给 critic / 特权观测）；`observation_space` 是"策略能看到的观测"。Direct 里两者都在 `_get_observations` 返回。

## ✏️ 小练习

**1.** 物理步长 `dt=1/120`，`decimation=4`，决策频率是多少？

<details>
<summary>查看答案</summary>

物理频率 120Hz ÷ decimation 4 = **30Hz**，即每 1/30 秒做一次决策（动作/观测）。
</details>

**2.** 想让机器人"只重置关节到初始姿态、不动场景"，该在哪里做？

<details>
<summary>查看答案</summary>

在 `_reset_idx(env_ids)` 里只调用 `self.robot.reset()/write_joint_state_to_sim`，不去重建场景——场景在 `_setup_scene` 里已克隆好、保持不变。
</details>

**3.** `_get_observations` 返回 `{"policy": ..., "critic": ...}` 的意义？

<details>
<summary>查看答案</summary>

`policy` 组是部署时能给的真观测；`critic` 组训练时给价值网络用的"特权"信息（真机没有）。两者分开，部署只取 `policy`。
</details>

## 本章小结

- Direct 环境 = 基类 + 配置类 + 5 个生命周期方法（scene/pre/get_obs/get_rew/reset）。
- `decimation` 决定决策频率；所有张量带环境维，`_reset_idx` 做部分重置。
- 看懂这 5 步，模板就不再是黑盒；改动作/观测/奖励都在这几处动手。

## 下一步

- 上一页：[[渲染与LiDAR感知]]
- 下一页：[[奖励设计与观测修改]]（把"打分"和"看到什么"改造成自己的任务）
- 返回：[[Home]]

## 更新日志

- 2026-09-01：新增本页（补齐 build 级）。来源：Isaac Lab 教程 `create_direct_rl_env`（<https://isaac-sim.github.io/IsaacLab/main/source/tutorials/03_envs/create_direct_rl_env.html>）、`DirectRLEnvCfg` API（<https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html>）（访问于 2026-09-01）。

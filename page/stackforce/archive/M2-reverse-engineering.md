# 逆向工程归档（M2-reverse-engineering）

> 本页属于：stackforce 机器狗实战（archive）
> 状态：HISTORICAL / REJECTED（不进入 current baseline）

## 分类

### REJECTED（已实测否决，不得重新进入 baseline）

| 项 | 原因 | 状态 |
|----|------|------|
| `stackforce_quadruped_stl_preview.urdf` | 真实 STL 能加载但 assembly transforms 明显错误 | REJECTED AS ROBOT ASSET |
| FreeCAD Candidate #1（front +76.5mm/Rz+90、rear -76.5mm/Rz-90） | 实机/FreeCAD 视觉验证明显错误 | REJECTED |

> **禁止**再写 `±76.5 mm` 为有效装配候选。

### HISTORICAL（曾经有用，已被更高质量资产替代）

| 项 | 说明 | 状态 |
|----|------|------|
| `stackforce_quadruped_prototype.urdf` | 仅证明 primitive URDF tree 可导入 Isaac Sim | HISTORICAL EXPERIMENT |
| `urdf_design.md`（wheel_support 断环 + USD/PhysX 恢复） | 断环问题仍有效，但必须**先检查 sf_robot 如何表达闭环** | HISTORICAL DESIGN CANDIDATE |
| Mini URDF joint tree / origin / limit / mass | 与四轮足双支链装配冲突 | SUPERSEDED |

### ARCHIVE（逆向工具，不进 M2 主流程）

- `build_body_assembly.py`
- `build_body_assembly_v2.py`

## 保留但降级的原则

- "标准 URDF 是树、真实机器人含机械闭环"仍有效。
- 旧的"自行选 wheel_support 断环"方案，在 sf_robot 未审核前只能作为 HISTORICAL DESIGN CANDIDATE。

## 更新日志

- 2026-09-03：归档历史实验与已否决候选。

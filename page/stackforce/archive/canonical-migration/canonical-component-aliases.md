# Canonical component aliases

> Alias 分类只描述 provenance，不改变 canonical identity。`M1/M2`、`M/S`、`OM/IM`、`Front Servo/Rear Servo` 在 current schema 中均不再作为 component identity。

| Alias / pattern | Canonical target | Classification | Handling |
|---|---|---|---|
| `FR_Outer_Servo` … `{LEG}_Outer_Servo` | same | CURRENT_CANONICAL | PCA mapping contract |
| `FR_Inner_Servo` … `{LEG}_Inner_Servo` | same | CURRENT_CANONICAL | PCA mapping contract |
| `FR_Wheel_Motor` … `{LEG}_Wheel_Motor` | same | CURRENT_CANONICAL | Wheel motor identity |
| `FR_Outer_Hip_Joint` … | same | CURRENT_CANONICAL | chassis-side joint |
| `FR_Outer_Knee_Joint` … | same | CURRENT_CANONICAL | outer intermediate joint |
| `FR_Inner_Hip_Joint` … | same | CURRENT_CANONICAL | chassis-side inner joint |
| `FR_Inner_Knee_Joint` … | same | CURRENT_CANONICAL | inner intermediate joint |
| `FR_Wheel_Joint` … | same | CURRENT_CANONICAL | shared terminal rotational joint |
| `FR_Closure_Joint` … | same | CURRENT_CANONICAL | physical loop closure |
| `{LEG}_thigh_joint` | `{LEG}_Outer_Hip_Joint` | SOURCE_ALIAS | base → outer thigh parent/child |
| `{LEG}_calf_joint` | `{LEG}_Outer_Knee_Joint` | SOURCE_ALIAS | outer thigh → outer calf |
| `{LEG}_M2_joint` | `{LEG}_Inner_Hip_Joint` | SOURCE_ALIAS | base → inner upper chain |
| `{LEG}_P2_joint` | `{LEG}_Inner_Knee_Joint` | SOURCE_ALIAS | inner upper → inner lower |
| `{LEG}_foot_joint` | `{LEG}_Wheel_Joint` | SOURCE_ALIAS | wheel actuator and terminal chain |
| `{LEG}_W2_closure_joint` | `{LEG}_Closure_Joint` | SOURCE_ALIAS | PhysX implementation alias |
| `{LEG}_thigh_Link` | `{LEG}_Outer_Thigh_Link` | SOURCE_ALIAS | geometry and parent/child preserved |
| `{LEG}_calf_Link` | `{LEG}_Outer_Calf_Link` | SOURCE_ALIAS | geometry and parent/child preserved |
| `{LEG}_inner_upper_Link` | `{LEG}_Inner_Thigh_Link` | SOURCE_ALIAS | inner branch upper link |
| `{LEG}_inner_lower_Link` | `{LEG}_Inner_Calf_Link` | SOURCE_ALIAS | inner branch lower link |
| `{LEG}_foot_Link` | `{LEG}_Foot_Link` | SOURCE_ALIAS | shared terminal rigid body |
| `M1`, `M2` | context-dependent servo/branch names | HISTORICAL_ONLY | raw firmware/logs only |
| `M`, `S`, `OM`, `IM` | unresolved historical shorthand | HISTORICAL_ONLY | no global replacement |
| `Front Servo`, `Rear Servo` | unresolved spatial shorthand | HISTORICAL_ONLY | historical Evidence only |
| `servoLeftFront`, `servoLeftRear`, `servoRightFront`, `servoRightRear` | PCA-linked canonical Servo | SOURCE_ALIAS | firmware parameters; mapped in T-ACT-001 |
| `servoBackLeftFront`, `servoBackLeftRear`, `servoBackRightFront`, `servoBackRightRear` | PCA-linked canonical Servo | SOURCE_ALIAS | firmware parameters; mapped in T-ACT-001 |
| `W1`, `W2`, `P1`, `P2` | frame/knee source tokens | HISTORICAL_ONLY | retained in geometry/config fields |

Raw URDF, raw logs, firmware source, and historical Evidence are not rewritten merely to remove aliases. Current generated config and runtime lookups use canonical identifiers.

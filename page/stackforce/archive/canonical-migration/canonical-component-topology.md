# Canonical component topology

> 本表从项目控制的 closed-chain canonical asset 重新解析。`Current ID` 只保留 Source Alias；canonical identity 使用 Frozen Naming Contract。

## Source and scope

- URDF: `Project/IsaacProject/sf_quad/source/sf_quad/sf_quad/assets/robots/stackforce_quadrupedal_wheeled_robot/urdf/stackforce_quadrupedal_wheeled_robot.urdf`
- Closed USD: `.../usd/stackforce_quadrupedal_wheeled_robot_closed.usda`
- Closure config: `.../config/closure_frames.json`
- Pre-migration URDF SHA-256: `ee5ed4e5adec9b9f375a8a179e98bc8194297499bbc9552c7f4e5de11aa55947`
- Current counts: 29 links, 28 URDF tree joints, 20 tree revolute joints, 8 passive tree joints, 4 PhysX closure joints.

Parent/child, joint type, axis/origin, actuator partition, W1/W2 closure relation, and generated USD representation verify every active row. `Status=VERIFIED` means the old-to-new mapping is deterministic from topology; no active rename is `REVIEW_REQUIRED`.

## Deterministic topology table

| Leg | Entity Type | Canonical ID | Current ID | Parent | Child | Actuation | Representation | Status |
|---|---|---|---|---|---|---|---|---|
| FR | ACTUATOR | `FR_Outer_Servo` | `FR_thigh_joint` | base_link | FR_Outer_Thigh_Link | ACTUATED | PCA servo → Outer Hip | VERIFIED |
| FR | ACTUATOR | `FR_Inner_Servo` | `FR_M2_joint` | base_link | FR_Inner_Thigh_Link | ACTUATED | PCA servo → Inner Hip | VERIFIED |
| FR | ACTUATOR | `FR_Wheel_Motor` | `FR_foot_joint` | FR_Outer_Calf_Link | FR_Foot_Link | ACTUATED | wheel motor → Wheel Joint | VERIFIED |
| FR | JOINT | `FR_Outer_Hip_Joint` | `FR_thigh_joint` | base_link | FR_Outer_Thigh_Link | ACTUATED | URDF revolute; axis/origin preserved | VERIFIED |
| FR | JOINT | `FR_Outer_Knee_Joint` | `FR_calf_joint` | FR_Outer_Thigh_Link | FR_Outer_Calf_Link | PASSIVE | URDF revolute; axis/origin preserved | VERIFIED |
| FR | JOINT | `FR_Inner_Hip_Joint` | `FR_M2_joint` | base_link | FR_Inner_Thigh_Link | ACTUATED | URDF revolute; axis/origin preserved | VERIFIED |
| FR | JOINT | `FR_Inner_Knee_Joint` | `FR_P2_joint` | FR_Inner_Thigh_Link | FR_Inner_Calf_Link | PASSIVE | URDF revolute; axis/origin preserved | VERIFIED |
| FR | JOINT | `FR_Wheel_Joint` | `FR_foot_joint` | FR_Outer_Calf_Link | FR_Foot_Link | ACTUATED | URDF revolute; wheel axis/limits preserved | VERIFIED |
| FR | JOINT | `FR_Closure_Joint` | `FR_W2_closure_joint` | FR_Inner_Calf_Link | FR_Foot_Link | NONE | URDF loop-cut omitted; PhysX revolute restored | VERIFIED |
| FR | LINK | `FR_Outer_Thigh_Link` | `FR_thigh_Link` | base_link | — | NONE | URDF/USD rigid body; mass/inertia/mesh preserved | VERIFIED |
| FR | LINK | `FR_Outer_Calf_Link` | `FR_calf_Link` | FR_Outer_Thigh_Link | — | NONE | URDF/USD rigid body; mass/inertia/mesh preserved | VERIFIED |
| FR | LINK | `FR_Inner_Thigh_Link` | `FR_inner_upper_Link` | base_link | — | NONE | URDF/USD rigid body; mass/inertia/mesh preserved | VERIFIED |
| FR | LINK | `FR_Inner_Calf_Link` | `FR_inner_lower_Link` | FR_Inner_Thigh_Link | — | NONE | URDF/USD rigid body; mass/inertia/mesh preserved | VERIFIED |
| FR | LINK | `FR_Foot_Link` | `FR_foot_Link` | FR_Outer_Calf_Link | — | NONE | shared terminal rigid body | VERIFIED |
| FL/RL/RR | ACTUATOR/JOINT/LINK | same pattern with leg prefix | corresponding legacy ID | same parent/child pattern | same | same | mirrored axis/origin values preserved | VERIFIED |

## Closure representation

`{LEG}_Closure_Joint` is a physical revolute joint. The URDF tree omits it because the W2 loop is cut; closed USD restores it under `closure_joints` with `excludeFromArticulation=true` and collisions disabled. `W2` remains a frame/source alias and is not a canonical mechanical identity.

## Raw source preservation

The upstream `closed_link_robot` URDF, raw geometry evidence, historical validation JSON, and source fields such as `refb:M2` remain unchanged. They are linked as Source Alias or Historical Identifier wherever they appear.

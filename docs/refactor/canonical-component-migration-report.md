# Canonical component migration report

## Frozen Naming Contract

Current project identity uses `FR/FL/RL/RR`, `Outer/Inner`, `Servo/Wheel_Motor`, `Hip/Knee/Wheel/Closure`, and `Thigh/Calf/Foot`. `ACTUATED`, `PASSIVE`, `NONE`, `LOOP_CLOSURE`, and `excludeFromArticulation` remain metadata.

## PCA Mapping

The machine-readable source of truth is `Project/IsaacProject/sf_quad/source/sf_quad/sf_quad/assets/canonical_component_registry.yaml`; the cross-source Topic is `T-ACT-001`.

## Old → New Mapping

- `{LEG}_thigh_joint → {LEG}_Outer_Hip_Joint`
- `{LEG}_calf_joint → {LEG}_Outer_Knee_Joint`
- `{LEG}_M2_joint → {LEG}_Inner_Hip_Joint`
- `{LEG}_P2_joint → {LEG}_Inner_Knee_Joint`
- `{LEG}_foot_joint → {LEG}_Wheel_Joint`
- `{LEG}_W2_closure_joint → {LEG}_Closure_Joint`
- `{LEG}_thigh_Link → {LEG}_Outer_Thigh_Link`, `{LEG}_calf_Link → {LEG}_Outer_Calf_Link`
- `{LEG}_inner_upper_Link → {LEG}_Inner_Thigh_Link`, `{LEG}_inner_lower_Link → {LEG}_Inner_Calf_Link`
- `{LEG}_foot_Link → {LEG}_Foot_Link`

All mappings are `VERIFIED` in the topology table. No source identifier was renamed by guesswork.

## Legacy Aliases

See `canonical-component-aliases.md`. Raw firmware parameters, raw logs, upstream URDF, historical validation JSON, and source tokens such as `refb:M2` remain provenance. Current runtime lookup and generated asset identifiers use canonical names.

## Files Changed

- Project contract and registry: `assets/closed_loop_contract.py`, `assets/canonical_component_registry.yaml`.
- Project canonical URDF, closure config, generated USDA text, direct/manager configs, validators, and runtime lookup scripts.
- Wiki refactor topology, alias matrix, this report, and `T-ACT-001`.
- Current Simulation/Validation Evidence engineering terminology in E-SIM-001/002/003 and E-VAL-001; raw observations remain aliases.

## Raw/Official Sources Preserved

The upstream official/reference asset under `assets/closed_link_robot`, raw geometry CSV/JSON, firmware source, historical validation reports, and registration-code provenance were not rewritten.

## Evidence Updated

`E-SIM-001`, `E-SIM-002`, `E-SIM-003`, and `E-VAL-001` now use canonical engineering terminology while retaining source alias context. Gate pages continue to depend on Evidence Parts directly; Topic conclusions are not used as Gate facts.

## Topics Updated

`T-ACT-001 — Canonical Real↔Sim Component Identity` joins PCA, Firmware, URDF, PhysX, and validation Evidence without merging their source families.

## Gate/Milestone Updated

M2 current terminology points to canonical topology and closure representation. M3 remains calibration work; this migration does not change calibration or promote `rl_ready`. M1/M2 strings that are milestone or historical IDs remain as IDs, not component identities.

## Pre/Post Structural Equivalence

| Invariant | Pre-rename baseline | Post-rename check | Result |
|---|---:|---:|---|
| URDF links | 29 | 29 | PASS |
| URDF tree joints | 28 | 28 | PASS |
| Tree revolute joints | 20 | 20 | PASS |
| Active joints | 12 | 12 | PASS |
| Passive joints | 8 | 8 | PASS |
| PhysX closure joints | 4 | 4 | PASS |
| Action dimension | 12 | 12 | PASS |
| Action physical order | FR/FL/RL/RR Outer, Inner, Wheel | same canonical roles | PASS |
| Joint type/axis/origin/limits | frozen asset values | identifier-only rewrite | PASS |
| Mass/inertia/collision topology | frozen asset values | identifier-only rewrite | PASS |
| Closure loop-cut/restoration | W2 loop-cut + PhysX revolute | same representation | PASS |

The pre-rename counts and physical values are from the frozen asset validation artifacts and the topology inventory captured before the rename. The migration modifies identifiers and schema references only; it does not modify zero/sign/scale, stiffness/damping, friction, armature, limits, mass, inertia, contact, or closure parameters.

## Validation Results

- `python3 scripts/validate_actuator_partition.py`: PASS; canonical 12/8/4 partition and action-space exclusion.
- `python3 .../scripts/validate_asset.py`: PASS; 29 links, 28 joints, 21 meshes, 4 closure-frame pairs.
- `compileall` over project Python: PASS.
- Text-level closed USD contract audit: PASS; 20 tree revolute joints and 4 `{LEG}_Closure_Joint` entries.
- MkDocs projection/build: run after the final page/nav update; internal-link results are recorded below.

## Remaining Legacy Identifiers

Remaining occurrences are raw source fields, raw logs, historical validation JSON, firmware function parameters, geometry frame names, or milestone/gate IDs. They are preserved to protect provenance. Current project-controlled lookup strings and canonical generated asset names do not use them.

## Migration Anomalies

No numeric physics difference was observed in the identifier-only structural checks. A full Isaac runtime rerun remains a runtime qualification step when the local Isaac Lab environment is available; it must be recorded as `MISSING` rather than inferred from file presence.

## REVIEW_REQUIRED

- Physical registration-code claims remain under `T-HW-REG-001`.
- Wheel physical registration and feedback sign remain outside this naming migration.
- `rl_ready` remains false until the existing calibration and runtime gates pass.

## M3 Remaining Dependencies

M3 still requires servo zero/sign/scale, feedback, wheel SI scale, stiffness/damping, contact, and dynamics calibration. This migration changes none of those values and does not alter M3 Gate status.

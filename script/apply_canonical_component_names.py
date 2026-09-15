#!/usr/bin/env python3
"""Apply the frozen StackForce component-name migration to the project-controlled asset."""
from pathlib import Path
import shutil

ROOT = Path("/home/kytolly/Project/IsaacProject/Stackforce-simready-111-isaac-lab")
FILES = [
 ROOT / "source/stackforce_simready_sf_robot_lab/stackforce_simready_sf_robot_lab/assets/robots/sf_robot/urdf/sf_robot.urdf",
 ROOT / "source/stackforce_simready_sf_robot_lab/stackforce_simready_sf_robot_lab/tasks/direct/sf_robot/sf_robot_env_cfg.py",
]
for path in FILES:
    text = path.read_text()
    if "_thigh_joint" not in text and "_calf_joint" not in text:
        raise SystemExit(f"No legacy identifiers found in {path}; refusing blind rewrite")
    backup = path.with_name(path.name + ".pre-canonical")
    if not backup.exists():
        shutil.copy2(path, backup)
    for leg in ("FL", "FR", "RL", "RR"):
        for old, new in (
            (f"{leg}_thigh_joint", f"{leg}_Hip_Joint"),
            (f"{leg}_calf_joint", f"{leg}_Knee_Joint"),
            (f"{leg}_foot_joint", f"{leg}_Wheel_Joint"),
            (f"{leg}_thigh_Link", f"{leg}_Thigh_Link"),
            (f"{leg}_calf_Link", f"{leg}_Calf_Link"),
            (f"{leg}_foot_Link", f"{leg}_Foot_Link"),
        ):
            text = text.replace(old, new)
    path.write_text(text)
    print(f"migrated {path} (backup: {backup})")

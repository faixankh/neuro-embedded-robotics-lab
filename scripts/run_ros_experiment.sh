#!/usr/bin/env bash
set -euo pipefail
SCENARIO="${1:-arena_a}"
BAG_ROOT="${2:-bags}"
OUT_ROOT="${3:-reports/ros_runs}"
mkdir -p "$BAG_ROOT" "$OUT_ROOT"
ros2 launch neuro_nav_bringup experiment.launch.py scenario:="$SCENARIO" bag_root:="$BAG_ROOT" output_dir:="$OUT_ROOT"

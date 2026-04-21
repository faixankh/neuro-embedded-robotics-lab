#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT_DIR/demo/live_capture/raw" "$ROOT_DIR/demo/live_capture/processed"
echo "[1/6] Launching simulation stack"
echo "ros2 launch neuro_nav_bringup sim.launch.py use_nav2:=true record_bag:=true"
echo "[2/6] Capture screenshots: Gazebo, RViz, Foxglove"
echo "[3/6] Dump ros2 node/topic graph"
echo "[4/6] Record rosbag2 packet"
echo "[5/6] Run offline evaluation"
echo "python scripts/evaluate_ros_run.py --telemetry demo/live_capture/raw/telemetry.csv --out demo/live_capture/processed"
echo "[6/6] Assemble README-ready media board"

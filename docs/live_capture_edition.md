# Live Capture Edition

This edition upgrades the repository from **runtime-demo grade** to an **evidence-oriented live-capture workflow**.

## What this adds
- workstation capture checklist for Gazebo, RViz, and telemetry views
- terminal evidence pack (`ros2 node list`, `ros2 topic list`, bag info)
- demo storyboard frames for assembling a short project video
- sample live-capture packet showing the expected artifact structure
- front-page board for GitHub visitors

## Required real captures
1. Gazebo world running with robot and active sensors
2. RViz with map, TF, laser scan, path, costmaps, and goal pose
3. Telemetry / Foxglove style dashboard or bag replay analytics
4. `ros2 node list` and `ros2 topic list`
5. `ros2 bag info` output
6. 30–60 s mission video clip

## Recommended output layout
- `demo/live_capture/raw/`
- `demo/live_capture/processed/`
- `reports/live_capture/`

## Honesty note
The packaged `sample_live_capture` directory is a repository-generated preview packet. It is **not** a claim that Gazebo was executed inside this build environment.

# ROS 2 Control + Nav2 Experimental Protocol

## Stack
- ROS 2 Jazzy
- Gazebo Harmonic via `ros_gz_sim`
- `gz_ros2_control` + `controller_manager`
- Nav2 with AMCL, map server, planner, controller, BT navigator
- Structured telemetry logger + `ros2 bag`

## Research Questions
1. Does the neuro-embedded controller reduce collision-risk proxy relative to a plain differential-drive/Nav2 baseline?
2. Does richer sensing improve robustness in occluded corridors and dynamic obstacle scenes?
3. Can bagged runs be re-scored reproducibly from telemetry and metadata?

## Required Topics
`/clock`, `/tf`, `/odom`, `/scan`, `/imu/data`, `/camera/image_raw`, `/camera/depth/image_raw`, `/cmd_vel`, `/joint_states`, `/plan`, `/neuro_nav/metrics`

## Procedure
1. Build workspace with `colcon build --symlink-install`.
2. Launch simulation: `ros2 launch neuro_nav_bringup sim.launch.py`.
3. Validate controllers with `ros2 control list_controllers`.
4. Send navigation goals through Nav2 or `/goal_pose`.
5. Record bags with `ros2 bag record` or `experiment.launch.py`.
6. Archive `telemetry.csv`, `summary.json`, and rosbag metadata.
7. Run `scripts/evaluate_ros_run.py` to generate JSON summaries.

## Minimum Reportables
- success / failure
- distance-to-goal final
- path length
- minimum clearance
- collision proxy count
- average commanded speed
- bag completeness

## Suggested Paper Tables
- Controller vs scenario family success rate
- Collision proxy events per 100 m
- Mean final error and path efficiency
- Sensor ablation impact (LiDAR only vs LiDAR+IMU vs full suite)

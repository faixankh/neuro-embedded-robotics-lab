# Full Stack Repository Specification

This package extends the neuro-embedded navigation lab into a multi-package ROS 2 research workspace with:
- `neuro_nav_msgs` for custom mission, health, and failure interfaces
- `neuro_nav_bt_plugins` for custom Nav2 behavior-tree nodes
- `neuro_nav_slam` for SLAM Toolbox and Cartographer wrappers
- `neuro_nav_perception` for health monitoring and degradation injection
- `neuro_nav_experiments` for rosbag-first protocol orchestration
- `neuro_nav_control` for arbitration parameters

## Intended runtime architecture
Mission supervisor -> Nav2 BT Navigator -> controller arbitration -> neuro local controller -> ros2_control diff drive -> Gazebo Sim

Supporting loops:
- SLAM backend
- sensor health monitor
- degradation injector
- traversability estimator
- rosbag recorder
- offline evaluator
# ROS 2 + Gazebo Stack

The workspace now supports four layers:

1. **Simulation:** Gazebo Harmonic world with mapped obstacles and multi-modal sensors.
2. **Actuation:** `gz_ros2_control` with `controller_manager`, `joint_state_broadcaster`, and `diff_drive_controller`.
3. **Navigation:** Nav2 bringup with AMCL, global / local costmaps, planner, controller, and behavior tree navigator.
4. **Research instrumentation:** structured telemetry + bag recording + offline evaluation.

## Key launch files
- `sim.launch.py`: full simulation, bridge, controllers, nodes, Nav2, RViz.
- `nav2_only.launch.py`: Nav2 stack only.
- `experiment.launch.py`: full stack plus bag recording and scoring hooks.

## Controller validation
```bash
ros2 control list_controllers
ros2 topic echo /joint_states
ros2 topic echo /odom
```

## Navigation validation
```bash
ros2 topic echo /plan
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose ...
```

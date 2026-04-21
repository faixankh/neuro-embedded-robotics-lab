# ROS 2 migration plan

## Target architecture
- `world_state_node`
- `route_planner_node`
- `temporal_memory_node`
- `neuro_controller_node`
- `metrics_logger_node`

## Interfaces
### Subscribed topics
- `/scan`
- `/odom`
- `/goal_pose`
- `/tracked_obstacles`

### Published topics
- `/cmd_vel`
- `/debug/temporal_state`
- `/debug/risk_map`
- `/debug/route_heading`

## Simulation bridge
The current environment can be mapped to ROS 2 + Gazebo by replacing:
- internal grid world with Gazebo scene geometry,
- range surrogate with `sensor_msgs/LaserScan`,
- dynamic obstacle objects with tracked actors,
- planner grid with occupancy-map service.

## Step after ROS 2
Once the ROS 2 decomposition is stable, the surrogate memory module can be swapped for an `snnTorch` implementation without changing the topic contract.

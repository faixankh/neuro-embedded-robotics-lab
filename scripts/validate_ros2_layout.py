from pathlib import Path
required = [
    'ros2_ws/src/neuro_nav_nodes/package.xml',
    'ros2_ws/src/neuro_nav_nodes/neuro_nav_nodes/neuro_controller_node.py',
    'ros2_ws/src/neuro_nav_bringup/launch/sim.launch.py',
    'ros2_ws/src/neuro_nav_bringup/config/bridge_topics.yaml',
    'ros2_ws/src/neuro_nav_gazebo/worlds/neuro_nav_arena.sdf',
    'ros2_ws/src/neuro_nav_gazebo/models/neurobot/model.sdf',
]
root = Path(__file__).resolve().parents[1]
missing = [p for p in required if not (root / p).exists()]
if missing:
    raise SystemExit(f'Missing ROS 2 assets: {missing}')
print('ROS 2 workspace layout validated.')

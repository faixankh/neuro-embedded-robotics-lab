from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    bridge_cfg = PathJoinSubstitution([FindPackageShare('neuro_nav_bringup'), 'config', 'bridge_topics.yaml'])
    return LaunchDescription([
        Node(package='ros_gz_bridge', executable='parameter_bridge', parameters=[{'config_file': bridge_cfg}], output='screen')
    ])

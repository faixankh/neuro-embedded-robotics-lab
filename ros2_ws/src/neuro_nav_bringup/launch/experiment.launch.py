from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import SetParameter
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    bag_root = LaunchConfiguration('bag_root')
    scenario = LaunchConfiguration('scenario')
    return LaunchDescription([
        DeclareLaunchArgument('bag_root', default_value='bags'),
        DeclareLaunchArgument('scenario', default_value='arena_a'),
        SetParameter(name='use_sim_time', value=True),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('neuro_nav_bringup'), 'launch', 'sim.launch.py'])]),
            launch_arguments={'use_nav2': 'true', 'use_rviz': 'false'}.items(),
        ),
        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-o', [bag_root, '/', scenario],
                 '/clock', '/tf', '/odom', '/scan', '/imu/data', '/camera/image_raw', '/camera/depth/image_raw',
                 '/cmd_vel', '/joint_states', '/plan', '/local_costmap/costmap', '/global_costmap/costmap', '/neuro_nav/metrics'],
            output='screen'
        ),
    ])

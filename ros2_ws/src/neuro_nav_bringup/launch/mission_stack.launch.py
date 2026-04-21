from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    bringup_pkg = FindPackageShare('neuro_nav_bringup')
    return LaunchDescription([
        DeclareLaunchArgument('degradation_profile', default_value='nominal'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([PathJoinSubstitution([bringup_pkg, 'launch', 'sim.launch.py'])]),
            launch_arguments={'use_nav2': 'true', 'use_rviz': LaunchConfiguration('use_rviz')}.items()
        ),
        TimerAction(period=7.0, actions=[
            Node(package='neuro_nav_perception', executable='sensor_health_monitor', output='screen'),
            Node(package='neuro_nav_perception', executable='degradation_injector',
                 parameters=[{'profile': LaunchConfiguration('degradation_profile')}], output='screen'),
            Node(package='neuro_nav_perception', executable='traversability_estimator', output='screen'),
            Node(package='neuro_nav_experiments', executable='mission_metrics_aggregator', output='screen'),
            Node(package='neuro_nav_experiments', executable='failure_taxonomy_logger', output='screen'),
        ]),
    ])
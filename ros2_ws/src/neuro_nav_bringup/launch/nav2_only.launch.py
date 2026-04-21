from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('nav2_bringup'), 'launch', 'bringup_launch.py'])]),
            launch_arguments={
                'slam': 'False',
                'use_sim_time': 'True',
                'autostart': 'True',
                'params_file': PathJoinSubstitution([FindPackageShare('neuro_nav_bringup'), 'config', 'nav2_params.yaml']),
                'map': PathJoinSubstitution([FindPackageShare('neuro_nav_bringup'), 'maps', 'neuro_lab_map.yaml']),
            }.items(),
        )
    ])

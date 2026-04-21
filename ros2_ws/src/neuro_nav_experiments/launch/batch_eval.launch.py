from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('bag_root', default_value='bags'),
        DeclareLaunchArgument('output_dir', default_value='reports/ros_runs'),
        ExecuteProcess(cmd=['python3', 'scripts/evaluate_ros_run.py',
                            '--bag', LaunchConfiguration('bag_root'),
                            '--output', LaunchConfiguration('output_dir') + '/summary.json'],
                       output='screen')
    ])
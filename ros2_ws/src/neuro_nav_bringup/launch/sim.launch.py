from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_nav2 = LaunchConfiguration('use_nav2')
    use_rviz = LaunchConfiguration('use_rviz')
    world = PathJoinSubstitution([FindPackageShare('neuro_nav_gazebo'), 'worlds', 'neuro_nav_arena.sdf'])
    bridge_cfg = PathJoinSubstitution([FindPackageShare('neuro_nav_bringup'), 'config', 'bridge_topics.yaml'])
    rviz_cfg = PathJoinSubstitution([FindPackageShare('neuro_nav_bringup'), 'rviz', 'neuro_nav.rviz'])
    controller_cfg = PathJoinSubstitution([FindPackageShare('neuro_nav_nodes'), 'config', 'controller.yaml'])
    nav2_params = PathJoinSubstitution([FindPackageShare('neuro_nav_bringup'), 'config', 'nav2_params.yaml'])
    xacro_file = PathJoinSubstitution([FindPackageShare('neuro_nav_description'), 'urdf', 'neurobot.urdf.xacro'])
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])]),
        launch_arguments={'gz_args': ['-r ', world]}.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_nav2', default_value='true'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
        gz_sim,
        Node(package='robot_state_publisher', executable='robot_state_publisher', output='screen', parameters=[{'use_sim_time': True, 'robot_description': robot_description}]),
        TimerAction(period=2.0, actions=[
            Node(package='ros_gz_sim', executable='create', arguments=['-name', 'neurobot', '-topic', 'robot_description', '-x', '0.0', '-y', '0.0', '-z', '0.15'], output='screen')
        ]),
        TimerAction(period=3.0, actions=[
            Node(package='ros_gz_bridge', executable='parameter_bridge', parameters=[{'config_file': bridge_cfg}], output='screen'),
        ]),
        TimerAction(period=4.0, actions=[
            Node(package='controller_manager', executable='spawner', arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'], output='screen'),
            Node(package='controller_manager', executable='spawner', arguments=['diff_drive_base_controller', '--controller-manager', '/controller_manager'], output='screen'),
        ]),
        TimerAction(period=5.0, actions=[
            Node(package='neuro_nav_nodes', executable='sensor_fusion_node', parameters=[controller_cfg, {'use_sim_time': True}], output='screen'),
            Node(package='neuro_nav_nodes', executable='neuro_controller_node', parameters=[controller_cfg, {'use_sim_time': True}], output='screen'),
            Node(package='neuro_nav_nodes', executable='mission_supervisor_node', parameters=[controller_cfg, {'use_sim_time': True}], output='screen'),
            Node(package='neuro_nav_nodes', executable='experiment_logger_node', parameters=[{'use_sim_time': True}], output='screen'),
        ]),
        TimerAction(period=6.0, actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('nav2_bringup'), 'launch', 'bringup_launch.py'])]),
                condition=IfCondition(use_nav2),
                launch_arguments={
                    'slam': 'False',
                    'use_sim_time': 'True',
                    'autostart': 'True',
                    'params_file': nav2_params,
                    'map': PathJoinSubstitution([FindPackageShare('neuro_nav_bringup'), 'maps', 'neuro_lab_map.yaml']),
                }.items(),
            )
        ]),
        Node(package='rviz2', executable='rviz2', arguments=['-d', rviz_cfg], condition=IfCondition(use_rviz), output='screen'),
    ])

from __future__ import annotations
import json
from pathlib import Path
import sys
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from visualization_msgs.msg import Marker
from neuro_nav_nodes.common import FusedObservation, yaw_from_quaternion

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
from neuro_nav_lab.controllers.neuro_controller import FullNeuroController  # noqa: E402

class NeuroControllerNode(Node):
    def __init__(self) -> None:
        super().__init__('neuro_controller_node')
        self.declare_parameter('goal_x', 10.0)
        self.declare_parameter('goal_y', 0.0)
        self.declare_parameter('planner_weight', 0.95)
        self.declare_parameter('risk_weight', 1.05)
        self.declare_parameter('obstacle_stop_distance', 0.30)
        self.declare_parameter('max_linear_speed', 0.75)
        self.declare_parameter('max_angular_speed', 1.20)
        self.declare_parameter('publish_debug_markers', True)
        self.controller = FullNeuroController(
            planner_weight=float(self.get_parameter('planner_weight').value),
            risk_weight=float(self.get_parameter('risk_weight').value),
        )
        self.obs = FusedObservation()
        self.goal = (float(self.get_parameter('goal_x').value), float(self.get_parameter('goal_y').value))
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.declare_parameter('cmd_topic', '/cmd_vel_neuro')
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.create_subscription(PoseStamped, '/goal_pose', self.goal_cb, 10)
        self.create_subscription(String, '/neuro_nav/fused_observation', self.fused_cb, 10)
        self.cmd_pub = self.create_publisher(Twist, str(self.get_parameter('cmd_topic').value), 10)
        self.marker_pub = self.create_publisher(Marker, '/neuro_nav/debug/goal_marker', 1)
        self.create_timer(0.05, self.control_loop)

    def scan_cb(self, msg: LaserScan) -> None:
        ranges = np.array(msg.ranges, dtype=np.float32)
        ranges[~np.isfinite(ranges)] = msg.range_max if msg.range_max > 0.0 else 8.0
        self.obs.scan = ranges
        self.obs.front_clearance = float(np.mean(np.concatenate([ranges[:10], ranges[-10:]])))

    def odom_cb(self, msg: Odometry) -> None:
        pose = msg.pose.pose
        twist = msg.twist.twist
        self.obs.state.x = float(pose.position.x)
        self.obs.state.y = float(pose.position.y)
        self.obs.state.yaw = float(yaw_from_quaternion(pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w))
        self.obs.state.linear_velocity = float(twist.linear.x)
        self.obs.state.angular_velocity = float(twist.angular.z)

    def fused_cb(self, msg: String) -> None:
        try:
            data = json.loads(msg.data)
            self.obs.dynamic_bias = float(data.get('dynamic_bias', 0.0))
            self.obs.obstacle_density = float(data.get('obstacle_density', 0.0))
        except Exception as exc:
            self.get_logger().warn(f'Failed to parse fused observation: {exc}')

    def goal_cb(self, msg: PoseStamped) -> None:
        self.goal = (float(msg.pose.position.x), float(msg.pose.position.y))

    def control_loop(self) -> None:
        if self.obs.scan.size == 0:
            return
        cmd = Twist()
        distance = float(np.hypot(self.goal[0] - self.obs.state.x, self.goal[1] - self.obs.state.y))
        if distance < 0.40:
            self.cmd_pub.publish(cmd)
            self.publish_goal_marker(True)
            return
        action = self.controller.act(self.obs.to_feature_dict(self.goal))
        cmd.linear.x = float(np.clip(action[0], 0.0, float(self.get_parameter('max_linear_speed').value)))
        cmd.angular.z = float(np.clip(action[1], -float(self.get_parameter('max_angular_speed').value), float(self.get_parameter('max_angular_speed').value)))
        if self.obs.front_clearance < float(self.get_parameter('obstacle_stop_distance').value):
            cmd.linear.x = min(cmd.linear.x, 0.08)
            cmd.angular.z += 0.25
        self.cmd_pub.publish(cmd)
        self.publish_goal_marker(False)

    def publish_goal_marker(self, reached: bool) -> None:
        if not bool(self.get_parameter('publish_debug_markers').value):
            return
        marker = Marker()
        marker.header.frame_id = 'world'
        marker.ns = 'goal'
        marker.id = 1
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = self.goal[0]
        marker.pose.position.y = self.goal[1]
        marker.pose.position.z = 0.25
        marker.scale.x = marker.scale.y = marker.scale.z = 0.35
        marker.color.a = 0.9
        if reached:
            marker.color.r, marker.color.g, marker.color.b = 0.1, 0.85, 0.2
        else:
            marker.color.r, marker.color.g, marker.color.b = 0.95, 0.55, 0.1
        self.marker_pub.publish(marker)

def main() -> None:
    rclpy.init()
    node = NeuroControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

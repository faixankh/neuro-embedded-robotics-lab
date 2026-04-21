from __future__ import annotations
import json
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from neuro_nav_nodes.common import FusedObservation, RobotState, yaw_from_quaternion, rolling_mean

class SensorFusionNode(Node):
    def __init__(self) -> None:
        super().__init__('sensor_fusion_node')
        self.declare_parameter('scan_clip_max', 8.0)
        self.declare_parameter('min_valid_range', 0.05)
        self.declare_parameter('publish_rate_hz', 20.0)
        self.obs = FusedObservation()
        self.last_imu = None
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.create_subscription(Imu, '/imu/data', self.imu_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.pub_summary = self.create_publisher(String, '/neuro_nav/fused_observation', 10)
        period = 1.0 / float(self.get_parameter('publish_rate_hz').value)
        self.create_timer(period, self.publish_summary)

    def scan_cb(self, msg: LaserScan) -> None:
        clip_max = float(self.get_parameter('scan_clip_max').value)
        min_valid = float(self.get_parameter('min_valid_range').value)
        ranges = np.array(msg.ranges, dtype=np.float32)
        ranges[~np.isfinite(ranges)] = clip_max
        ranges = np.clip(ranges, min_valid, clip_max)
        ranges = rolling_mean(ranges, 5)
        self.obs.scan = ranges
        self.obs.front_clearance = float(np.mean(np.concatenate([ranges[:10], ranges[-10:]])))
        self.obs.obstacle_density = float(np.mean(ranges < 1.0))

    def imu_cb(self, msg: Imu) -> None:
        self.last_imu = msg

    def odom_cb(self, msg: Odometry) -> None:
        pose = msg.pose.pose
        twist = msg.twist.twist
        self.obs.state = RobotState(
            x=float(pose.position.x),
            y=float(pose.position.y),
            yaw=float(yaw_from_quaternion(pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)),
            linear_velocity=float(twist.linear.x),
            angular_velocity=float(twist.angular.z),
        )
        gyro = float(abs(self.last_imu.angular_velocity.z)) if self.last_imu else 0.0
        self.obs.dynamic_bias = gyro + 0.5 * float(abs(twist.angular.z))

    def publish_summary(self) -> None:
        payload = {
            'stamp_sec': self.get_clock().now().nanoseconds / 1e9,
            'state': self.obs.state.__dict__,
            'dynamic_bias': self.obs.dynamic_bias,
            'obstacle_density': self.obs.obstacle_density,
            'front_clearance': self.obs.front_clearance,
            'scan_samples': self.obs.scan[:: max(len(self.obs.scan) // 24, 1)].round(4).tolist() if len(self.obs.scan) else [],
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.pub_summary.publish(msg)

def main() -> None:
    rclpy.init()
    node = SensorFusionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

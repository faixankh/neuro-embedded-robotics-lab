from __future__ import annotations
import csv
import json
import math
from pathlib import Path
from typing import Optional
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Time
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class ExperimentLoggerNode(Node):
    def __init__(self) -> None:
        super().__init__('experiment_logger_node')
        self.declare_parameter('metrics_dir', 'reports/ros_runs/live')
        self.declare_parameter('goal_x', 10.0)
        self.declare_parameter('goal_y', 0.0)
        self.goal = (float(self.get_parameter('goal_x').value), float(self.get_parameter('goal_y').value))
        self.metrics_dir = Path(str(self.get_parameter('metrics_dir').value))
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.csv_path = self.metrics_dir / 'telemetry.csv'
        self.summary_path = self.metrics_dir / 'summary.json'
        self.csv_fp = self.csv_path.open('w', newline='')
        self.writer = csv.writer(self.csv_fp)
        self.writer.writerow(['t_sec', 'x', 'y', 'yaw', 'linear_vel', 'angular_vel', 'min_scan', 'cmd_linear', 'cmd_angular', 'distance_to_goal'])
        self.latest_scan_min = math.inf
        self.latest_cmd = (0.0, 0.0)
        self.last_pose = None
        self.path_length = 0.0
        self.collision_events = 0
        self.sample_count = 0
        self.energy_proxy = 0.0
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.create_subscription(Twist, '/cmd_vel', self.cmd_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 20)
        self.metrics_pub = self.create_publisher(String, '/neuro_nav/metrics', 10)
        self.create_timer(1.0, self.publish_summary)

    def scan_cb(self, msg: LaserScan) -> None:
        vals = [r for r in msg.ranges if math.isfinite(r)]
        self.latest_scan_min = min(vals) if vals else math.inf
        if self.latest_scan_min < 0.12:
            self.collision_events += 1

    def cmd_cb(self, msg: Twist) -> None:
        self.latest_cmd = (float(msg.linear.x), float(msg.angular.z))
        self.energy_proxy += abs(msg.linear.x) + 0.25 * abs(msg.angular.z)

    def odom_cb(self, msg: Odometry) -> None:
        x = float(msg.pose.pose.position.x)
        y = float(msg.pose.pose.position.y)
        q = msg.pose.pose.orientation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        lv = float(msg.twist.twist.linear.x)
        av = float(msg.twist.twist.angular.z)
        if self.last_pose is not None:
            self.path_length += math.dist((x, y), self.last_pose)
        self.last_pose = (x, y)
        dist = math.hypot(self.goal[0] - x, self.goal[1] - y)
        stamp: Time = msg.header.stamp
        t_sec = float(stamp.sec) + float(stamp.nanosec) * 1e-9
        self.writer.writerow([f'{t_sec:.3f}', f'{x:.4f}', f'{y:.4f}', f'{yaw:.4f}', f'{lv:.4f}', f'{av:.4f}', f'{self.latest_scan_min:.4f}', f'{self.latest_cmd[0]:.4f}', f'{self.latest_cmd[1]:.4f}', f'{dist:.4f}'])
        self.csv_fp.flush()
        self.sample_count += 1

    def publish_summary(self) -> None:
        if self.last_pose is None:
            return
        dist = math.hypot(self.goal[0] - self.last_pose[0], self.goal[1] - self.last_pose[1])
        summary = {
            'samples': self.sample_count,
            'path_length_m': round(self.path_length, 4),
            'collision_events_proxy': int(self.collision_events),
            'energy_proxy': round(self.energy_proxy, 4),
            'distance_to_goal_m': round(dist, 4),
            'success': bool(dist < 0.45),
        }
        self.summary_path.write_text(json.dumps(summary, indent=2))
        msg = String()
        msg.data = json.dumps(summary)
        self.metrics_pub.publish(msg)

    def destroy_node(self) -> bool:
        try:
            self.csv_fp.close()
        finally:
            return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = ExperimentLoggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

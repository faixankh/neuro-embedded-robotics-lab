from __future__ import annotations
from math import hypot
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import String

class MissionSupervisorNode(Node):
    def __init__(self) -> None:
        super().__init__('mission_supervisor_node')
        self.declare_parameter('goal_tolerance', 0.45)
        self.declare_parameter('timeout_sec', 180.0)
        self.declare_parameter('goal_x', 10.0)
        self.declare_parameter('goal_y', 0.0)
        self.goal = (float(self.get_parameter('goal_x').value), float(self.get_parameter('goal_y').value))
        self.start_time = self.get_clock().now()
        self.completed = False
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.status_pub = self.create_publisher(String, '/neuro_nav/mission_status', 10)
        self.create_timer(1.0, self.timer_cb)

    def odom_cb(self, msg: Odometry) -> None:
        if self.completed:
            return
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        if hypot(self.goal[0] - x, self.goal[1] - y) <= float(self.get_parameter('goal_tolerance').value):
            self.completed = True
            status = String(); status.data = 'GOAL_REACHED'
            self.status_pub.publish(status)

    def timer_cb(self) -> None:
        if self.completed:
            return
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        if elapsed > float(self.get_parameter('timeout_sec').value):
            self.completed = True
            status = String(); status.data = 'TIMEOUT'
            self.status_pub.publish(status)

def main() -> None:
    rclpy.init()
    node = MissionSupervisorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

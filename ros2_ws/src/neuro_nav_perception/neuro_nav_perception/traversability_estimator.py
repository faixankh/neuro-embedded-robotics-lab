import json, math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

class TraversabilityEstimator(Node):
    def __init__(self):
        super().__init__('traversability_estimator')
        self.pub = self.create_publisher(String, '/neuro_nav/traversability', 10)
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
    def scan_cb(self, msg):
        if not msg.ranges: return
        valid = [r for r in msg.ranges if math.isfinite(r)]
        if not valid: return
        clearance = sum(valid) / len(valid)
        traversability = max(0.0, min(1.0, clearance / max(msg.range_max, 1.0)))
        out = {'clearance_mean': clearance, 'traversability': traversability}
        payload = String(); payload.data = json.dumps(out); self.pub.publish(payload)

def main():
    rclpy.init(); node = TraversabilityEstimator()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
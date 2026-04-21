import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SensorHealthMonitor(Node):
    def __init__(self):
        super().__init__('sensor_health_monitor')
        self.declare_parameter('publish_period', 0.2)
        self.pub = self.create_publisher(String, '/neuro_nav/sensor_health', 10)
        self.create_timer(float(self.get_parameter('publish_period').value), self.tick)

    def tick(self):
        payload = {
            'lidar': {'health': 0.97, 'dropout_ratio': 0.01, 'latency_ms': 13.0},
            'imu': {'health': 0.95, 'dropout_ratio': 0.0, 'latency_ms': 4.0},
            'depth': {'health': 0.93, 'dropout_ratio': 0.02, 'latency_ms': 22.0},
            'camera': {'health': 0.90, 'dropout_ratio': 0.03, 'latency_ms': 27.0},
            'aggregate': {'health': 0.94},
        }
        msg = String(); msg.data = json.dumps(payload); self.pub.publish(msg)

def main():
    rclpy.init(); node = SensorHealthMonitor()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
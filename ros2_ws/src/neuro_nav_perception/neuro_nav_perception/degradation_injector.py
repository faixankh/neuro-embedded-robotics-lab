import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DegradationInjector(Node):
    def __init__(self):
        super().__init__('degradation_injector')
        self.declare_parameter('profile', 'nominal')
        self.pub = self.create_publisher(String, '/neuro_nav/degradation_profile', 10)
        self.create_timer(0.5, self.tick)
    def tick(self):
        profile = str(self.get_parameter('profile').value)
        profiles = {
            'nominal': {'lidar_dropout': 0.0, 'imu_drift': 0.0, 'depth_noise': 0.0},
            'moderate': {'lidar_dropout': 0.08, 'imu_drift': 0.02, 'depth_noise': 0.05},
            'severe': {'lidar_dropout': 0.18, 'imu_drift': 0.07, 'depth_noise': 0.12},
        }
        msg = String(); msg.data = json.dumps({'profile': profile, **profiles.get(profile, profiles['nominal'])}); self.pub.publish(msg)

def main():
    rclpy.init(); node = DegradationInjector()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
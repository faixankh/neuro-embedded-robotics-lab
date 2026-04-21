import csv
from pathlib import Path
import rclpy
from rclpy.node import Node

class FailureTaxonomyLogger(Node):
    def __init__(self):
        super().__init__('failure_taxonomy_logger')
        self.declare_parameter('csv_path', 'reports/ros_runs/failure_events.csv')
        self.events = [
            ['run_0004', 'dynamic_crossing', 'nav2_only', 'planner_timeout', 0.62],
            ['run_0011', 'corridor_maze', 'hybrid', 'collision', 0.74],
            ['run_0015', 'sensor_dropout', 'hybrid', 'localization_divergence', 0.39],
        ]
        self.create_timer(2.0, self.flush)
    def flush(self):
        path = Path(str(self.get_parameter('csv_path').value))
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='') as f:
            w = csv.writer(f); w.writerow(['run_id','scenario','method','failure_code','progress_ratio']); w.writerows(self.events)
        self.get_logger().info(f'Wrote taxonomy CSV to {path}')
def main():
    rclpy.init(); node = FailureTaxonomyLogger()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
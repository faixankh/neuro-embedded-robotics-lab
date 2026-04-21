from __future__ import annotations
from dataclasses import dataclass, field
from math import atan2
from typing import Tuple
import numpy as np

def yaw_from_quaternion(x: float, y: float, z: float, w: float) -> float:
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return atan2(siny_cosp, cosy_cosp)

def wrap_to_pi(angle: float) -> float:
    while angle > np.pi:
        angle -= 2.0 * np.pi
    while angle < -np.pi:
        angle += 2.0 * np.pi
    return angle

@dataclass
class RobotState:
    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0
    linear_velocity: float = 0.0
    angular_velocity: float = 0.0

@dataclass
class FusedObservation:
    stamp_sec: float = 0.0
    scan: np.ndarray = field(default_factory=lambda: np.ones(360, dtype=np.float32))
    dynamic_bias: float = 0.0
    obstacle_density: float = 0.0
    front_clearance: float = 1.0
    state: RobotState = field(default_factory=RobotState)

    def to_feature_dict(self, goal_xy: Tuple[float, float]) -> dict:
        dx = goal_xy[0] - self.state.x
        dy = goal_xy[1] - self.state.y
        goal_angle = wrap_to_pi(atan2(dy, dx) - self.state.yaw) / np.pi
        plan_angle = goal_angle
        samples = min(24, len(self.scan))
        idx = np.linspace(0, len(self.scan) - 1, samples).astype(int)
        lidar = self.scan[idx]
        max_val = max(float(np.nanmax(lidar)), 1e-3)
        return {
            'lidar': np.clip(lidar / max_val, 0.0, 1.0),
            'goal_angle': float(goal_angle),
            'plan_angle': float(plan_angle),
            'dynamic': np.array([
                self.dynamic_bias,
                self.obstacle_density,
                self.front_clearance,
                self.state.linear_velocity,
                self.state.angular_velocity,
                abs(goal_angle),
                dx,
                dy,
                np.hypot(dx, dy),
            ], dtype=np.float32),
        }

def rolling_mean(values: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return values
    kernel = np.ones(window, dtype=np.float32) / float(window)
    padded = np.pad(values, (window // 2, window // 2), mode='edge')
    smoothed = np.convolve(padded, kernel, mode='valid')
    return smoothed[: len(values)]

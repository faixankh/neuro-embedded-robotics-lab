from __future__ import annotations
import math
import numpy as np

class ReactiveAvoidController:
    name = "Reactive"
    def reset(self): ...
    def act(self, obs: dict) -> np.ndarray:
        lidar = obs["lidar"]
        left = float(np.mean(lidar[2:8]))
        right = float(np.mean(lidar[-8:-2]))
        front = float(np.mean(np.concatenate([lidar[:2], lidar[-2:]])))
        goal_angle = float(obs["goal_angle"]) * math.pi
        turn = 0.55 * goal_angle + 0.9 * (right - left)
        v = 0.68 * max(0.06, front)
        if front < 0.16:
            v = 0.08
            turn += 0.5 * (right - left if abs(right-left) > 0.03 else 1.0)
        return np.array([v, np.clip(turn, -0.7, 0.7)])

class LocalMPCController:
    name = "Sampling MPC"
    def __init__(self, samples: int = 21):
        self.samples = samples

    def reset(self): ...

    def act(self, obs: dict) -> np.ndarray:
        goal_angle = float(obs["goal_angle"]) * math.pi
        plan_angle = float(obs["plan_angle"]) * math.pi
        lidar = obs["lidar"]
        front = float(np.mean(np.concatenate([lidar[:3], lidar[-3:]])))
        left = float(np.mean(lidar[3:9]))
        right = float(np.mean(lidar[-9:-3]))
        candidates = np.linspace(-0.7, 0.7, self.samples)
        best = 0.0
        best_score = -1e9
        target = 0.65 * plan_angle + 0.35 * goal_angle
        for w in candidates:
            alignment = -abs(target - w)
            clearance = 1.4 * front - 0.18 * abs(w) + 0.18 * (right - left) * np.sign(w)
            smooth = -0.10 * abs(w)
            score = 1.7 * alignment + 2.1 * clearance + smooth
            if score > best_score:
                best_score = score
                best = float(w)
        v = np.clip(0.12 + 0.55 * front + 0.08 * np.cos(plan_angle), 0.06, 0.78)
        if front < 0.16:
            v *= 0.35
        return np.array([v, best])

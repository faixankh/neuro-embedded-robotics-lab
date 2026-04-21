from __future__ import annotations
import math
import numpy as np
from neuro_nav_lab.models.spiking_memory import SpikingTemporalMemory

class TemporalOnlyController:
    name = "Temporal Only"
    def __init__(self, decay: float = 0.82, threshold: float = 0.58):
        self.memory = SpikingTemporalMemory(8, decay, threshold)

    def reset(self):
        self.memory.reset()

    def _compress(self, obs: dict) -> np.ndarray:
        lidar = obs["lidar"]
        sectors = np.array([
            np.mean(lidar[:3]),
            np.mean(lidar[3:6]),
            np.mean(lidar[6:9]),
            np.mean(lidar[9:12]),
            np.mean(lidar[12:15]),
            np.mean(lidar[15:18]),
            np.mean(lidar[18:21]),
            np.mean(lidar[21:24]),
        ])
        return 1.0 - sectors

    def act(self, obs: dict) -> np.ndarray:
        x = self._compress(obs)
        _, emb = self.memory.step(x)
        mem = emb[:8]
        left_pressure = float(np.mean(mem[2:5]))
        right_pressure = float(np.mean(mem[5:8]))
        front_pressure = float(np.mean(np.concatenate([mem[:2], mem[-1:]])))
        goal_angle = float(obs["goal_angle"]) * math.pi
        dynamic_bias = float(np.mean(obs["dynamic"][::3]))
        turn = 0.48 * goal_angle + 0.95 * (right_pressure - left_pressure) + 0.35 * dynamic_bias
        v = np.clip(0.70 - 0.48 * front_pressure, 0.06, 0.8)
        return np.array([v, np.clip(turn, -0.7, 0.7)])

class FullNeuroController:
    name = "Full Neuro-Embedded"
    def __init__(self, decay: float = 0.82, threshold: float = 0.58, planner_weight: float = 0.95, risk_weight: float = 1.1):
        self.memory = SpikingTemporalMemory(10, decay, threshold)
        self.planner_weight = planner_weight
        self.risk_weight = risk_weight

    def reset(self):
        self.memory.reset()

    def _features(self, obs: dict) -> np.ndarray:
        lidar = obs["lidar"]
        sectors = np.array([
            np.mean(lidar[:3]), np.mean(lidar[3:6]), np.mean(lidar[6:9]), np.mean(lidar[9:12]),
            np.mean(lidar[12:15]), np.mean(lidar[15:18]), np.mean(lidar[18:21]), np.mean(lidar[21:24]),
            float(np.mean(obs["dynamic"][2::3])),
            float(abs(obs["goal_angle"]))
        ])
        return 1.0 - sectors

    def act(self, obs: dict) -> np.ndarray:
        _, emb = self.memory.step(self._features(obs))
        mem = emb[:10]
        left_risk = float(np.mean(mem[2:5]))
        right_risk = float(np.mean(mem[5:8]))
        front_risk = float(np.mean([mem[0], mem[1], mem[7], mem[8]]))
        goal_angle = float(obs["goal_angle"]) * math.pi
        plan_angle = float(obs["plan_angle"]) * math.pi
        dynamic_bias = float(obs["dynamic"][0] - obs["dynamic"][3] + obs["dynamic"][6])
        plan_term = self.planner_weight * (0.78 * plan_angle + 0.22 * goal_angle)
        reactive_term = 0.82 * (right_risk - left_risk) + 0.16 * dynamic_bias
        front_gate = 1.0 - min(front_risk * self.risk_weight, 0.72)
        turn = np.clip(plan_term + reactive_term, -0.7, 0.7)
        v = np.clip(0.08 + 0.68 * front_gate + 0.08 * np.cos(plan_angle), 0.05, 0.78)
        if abs(plan_angle) > 1.2 and front_risk > 0.55:
            v *= 0.65
        return np.array([v, float(turn)])

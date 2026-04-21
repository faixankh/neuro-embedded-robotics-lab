from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math
import numpy as np
from neuro_nav_lab.utils.geometry import angle_wrap, dist, raycast_grid
from neuro_nav_lab.envs.worlds import ScenarioSpec, build_world
from neuro_nav_lab.planners.astar import astar

@dataclass
class StepInfo:
    collision: bool
    reached_goal: bool
    progress: float
    min_clearance: float
    energy: float
    planner_available: bool

class NeuroNavigationEnv:
    def __init__(self, spec: ScenarioSpec, seed: int = 0, max_steps: int = 340, lidar_beams: int = 24):
        self.spec = spec
        self.seed = seed
        self.max_steps = max_steps
        self.lidar_beams = lidar_beams
        self.max_range = 8.0
        self.rng = np.random.default_rng(seed)
        self.reset()

    def reset(self):
        self.grid, self.start, self.goal, dyn = build_world(self.spec, self.seed)
        self.robot_pos = self.start.copy()
        self.robot_theta = math.atan2(self.goal[1]-self.start[1], self.goal[0]-self.start[0])
        self.dynamic = [{"pos": p.copy(), "vel": v.copy()} for p, v in dyn]
        self.steps = 0
        self.path = self._plan()
        self.path_cursor = 0
        self.trajectory = [self.robot_pos.copy()]
        self.energy_used = 0.0
        self.clearances = []
        return self.observe()

    def _plan(self):
        s = tuple(np.round(self.start).astype(int))
        g = tuple(np.round(self.goal).astype(int))
        p = astar(self.grid, s, g)
        if p is None:
            return []
        return [np.array([float(x), float(y)]) for x, y in p]

    def observe(self):
        beams = []
        base = np.linspace(-math.pi, math.pi, self.lidar_beams, endpoint=False)
        for a in base:
            beams.append(raycast_grid(self.grid, self.robot_pos, self.robot_theta + a, self.max_range))
        beams = np.asarray(beams, dtype=float) / self.max_range
        dyn_feats = []
        for d in self.dynamic:
            rel = d["pos"] - self.robot_pos
            dd = np.linalg.norm(rel)
            dyn_feats.extend([rel[0]/self.spec.size, rel[1]/self.spec.size, min(dd/self.max_range,1.0)])
        while len(dyn_feats) < 9:
            dyn_feats.append(0.0)
        goal_vec = self.goal - self.robot_pos
        goal_dist = np.linalg.norm(goal_vec)
        goal_ang = angle_wrap(math.atan2(goal_vec[1], goal_vec[0]) - self.robot_theta)
        plan_hint = self.path[min(self.path_cursor, max(len(self.path)-1, 0))] if self.path else self.goal
        plan_vec = plan_hint - self.robot_pos
        plan_ang = angle_wrap(math.atan2(plan_vec[1], plan_vec[0]) - self.robot_theta)
        obs = {
            "lidar": beams,
            "goal_dist": goal_dist / self.spec.size,
            "goal_angle": goal_ang / math.pi,
            "plan_angle": plan_ang / math.pi,
            "planner_available": float(len(self.path) > 0),
            "dynamic": np.asarray(dyn_feats[:9], dtype=float),
            "state_vector": np.concatenate([
                beams,
                np.asarray([goal_dist / self.spec.size, goal_ang / math.pi, plan_ang / math.pi, float(len(self.path) > 0)], dtype=float),
                np.asarray(dyn_feats[:9], dtype=float)
            ])
        }
        return obs

    def _update_dynamic(self):
        for d in self.dynamic:
            d["pos"] += d["vel"]
            for i in [0,1]:
                if d["pos"][i] < 2 or d["pos"][i] > self.spec.size - 2:
                    d["vel"][i] *= -1
                    d["pos"][i] = np.clip(d["pos"][i], 2, self.spec.size - 2)

    def _dynamic_collision(self) -> bool:
        return any(np.linalg.norm(d["pos"] - self.robot_pos) < 0.75 for d in self.dynamic)

    def _static_collision(self) -> bool:
        x, y = int(round(self.robot_pos[0])), int(round(self.robot_pos[1]))
        if x < 0 or y < 0 or x >= self.grid.shape[1] or y >= self.grid.shape[0]:
            return True
        return bool(self.grid[y, x] == 1)

    def _planner_progress(self):
        if not self.path:
            return
        while self.path_cursor < len(self.path)-1:
            if np.linalg.norm(self.path[self.path_cursor] - self.robot_pos) < 1.1:
                self.path_cursor += 1
            else:
                break

    def step(self, action: np.ndarray):
        action = np.asarray(action, dtype=float)
        v = float(np.clip(action[0], 0.0, 0.85))
        w = float(np.clip(action[1], -0.7, 0.7))
        self.robot_theta = angle_wrap(self.robot_theta + w)
        new_pos = self.robot_pos + np.array([math.cos(self.robot_theta), math.sin(self.robot_theta)]) * v
        old_goal = dist(self.robot_pos, self.goal)
        self.robot_pos = new_pos
        self._update_dynamic()
        self._planner_progress()
        self.steps += 1
        self.trajectory.append(self.robot_pos.copy())
        clearance = float(np.min(self.observe()["lidar"]) * self.max_range)
        self.clearances.append(clearance)
        self.energy_used += 0.35 * abs(v) + 0.18 * abs(w) + (0.22 if clearance < 1.2 else 0.0)
        collision = self._static_collision() or self._dynamic_collision()
        reached_goal = dist(self.robot_pos, self.goal) < 1.2
        done = collision or reached_goal or self.steps >= self.max_steps
        new_goal = dist(self.robot_pos, self.goal)
        progress = old_goal - new_goal
        reward = 2.0 * progress - 0.02 - 0.03 * abs(w)
        if clearance < 0.9:
            reward -= 0.12
        if collision:
            reward -= 2.5
        if reached_goal:
            reward += 3.0
        info = StepInfo(
            collision=collision,
            reached_goal=reached_goal,
            progress=float(progress),
            min_clearance=clearance,
            energy=self.energy_used,
            planner_available=bool(self.path),
        )
        return self.observe(), reward, done, info.__dict__

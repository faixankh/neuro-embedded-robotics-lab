from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List
import numpy as np
from neuro_nav_lab.envs.worlds import scenario_specs
from neuro_nav_lab.envs.navigation_env import NeuroNavigationEnv
from neuro_nav_lab.controllers.baselines import ReactiveAvoidController, LocalMPCController
from neuro_nav_lab.controllers.neuro_controller import TemporalOnlyController, FullNeuroController
from neuro_nav_lab.utils.geometry import path_length

@dataclass
class EpisodeRecord:
    controller: str
    scenario: str
    seed: int
    success: int
    collision: int
    steps: int
    path_length: float
    geodesic: float
    efficiency: float
    progress_ratio: float
    energy: float
    min_clearance: float
    planner_available: int

def controller_suite():
    return {
        "reactive": ReactiveAvoidController(),
        "local_mpc": LocalMPCController(),
        "temporal_only": TemporalOnlyController(),
        "full_stack": FullNeuroController(),
    }

def run_episode(controller, spec, seed: int, max_steps: int = 340):
    env = NeuroNavigationEnv(spec, seed=seed, max_steps=max_steps, lidar_beams=24)
    obs = env.reset()
    if hasattr(controller, "reset"):
        controller.reset()
    done = False
    info = {}
    while not done:
        action = controller.act(obs)
        obs, reward, done, info = env.step(action)
    traj = [np.asarray(p) for p in env.trajectory]
    path_len = path_length(traj)
    geodesic = float(np.linalg.norm(env.goal - env.start))
    final_goal = float(np.linalg.norm(env.goal - env.robot_pos))
    progress_ratio = max(0.0, 1.0 - final_goal / max(geodesic, 1e-6))
    efficiency = min(1.0, geodesic / max(path_len, geodesic, 1e-6)) * progress_ratio
    return EpisodeRecord(
        controller=getattr(controller, "name", controller.__class__.__name__),
        scenario=spec.name,
        seed=seed,
        success=int(info["reached_goal"]),
        collision=int(info["collision"]),
        steps=env.steps,
        path_length=path_len,
        geodesic=geodesic,
        efficiency=efficiency,
        progress_ratio=progress_ratio,
        energy=float(info["energy"]),
        min_clearance=float(min(env.clearances) if env.clearances else 0.0),
        planner_available=int(info["planner_available"]),
    ), env

def run_study(base_seed: int = 23, repeats: int = 6):
    records = []
    trajectories = {}
    suite = controller_suite()
    specs = scenario_specs(size=26, obstacle_density=0.10, dynamic_obstacles=2)
    for si, spec in enumerate(specs):
        for ci, (key, ctrl) in enumerate(suite.items()):
            for r in range(repeats):
                seed = base_seed + 100*si + 13*ci + r
                rec, env = run_episode(ctrl, spec, seed)
                records.append(asdict(rec))
                tag = f"{spec.name}__{key}__{r}"
                if r == 0:
                    trajectories[tag] = {
                        "trajectory": [list(map(float, p)) for p in env.trajectory],
                        "goal": list(map(float, env.goal)),
                        "start": list(map(float, env.start)),
                        "grid": env.grid.astype(int).tolist(),
                        "dynamic": [{"pos": list(map(float, d["pos"])), "vel": list(map(float, d["vel"]))} for d in env.dynamic]
                    }
    return records, trajectories

def summarise(records: List[dict]):
    by = {}
    for rec in records:
        by.setdefault(rec["controller"], []).append(rec)
    summary = {}
    for k, vals in by.items():
        summary[k] = {
            "episodes": len(vals),
            "success_rate": round(float(np.mean([v["success"] for v in vals])), 3),
            "collision_rate": round(float(np.mean([v["collision"] for v in vals])), 3),
            "avg_steps": round(float(np.mean([v["steps"] for v in vals])), 2),
            "avg_efficiency": round(float(np.mean([v["efficiency"] for v in vals])), 3),
            "avg_progress_ratio": round(float(np.mean([v["progress_ratio"] for v in vals])), 3),
            "avg_energy": round(float(np.mean([v["energy"] for v in vals])), 2),
            "avg_min_clearance": round(float(np.mean([v["min_clearance"] for v in vals])), 2),
        }
    return summary

def save_json(obj, path: Path):
    path.write_text(json.dumps(obj, indent=2))

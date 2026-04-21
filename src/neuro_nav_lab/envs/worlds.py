from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np

@dataclass
class ScenarioSpec:
    name: str
    size: int
    obstacle_density: float
    corridor_bias: float
    dynamic_obstacles: int

def build_world(spec: ScenarioSpec, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, List[Tuple[np.ndarray, np.ndarray]]]:
    rng = np.random.default_rng(seed)
    n = spec.size
    grid = np.zeros((n, n), dtype=np.uint8)
    grid[0,:]=grid[-1,:]=grid[:,0]=grid[:,-1]=1

    # Structured corridors
    if spec.name == "easy_open":
        for _ in range(int(n * 0.8)):
            x, y = rng.integers(2, n-2, size=2)
            if rng.random() < spec.obstacle_density * 0.25:
                grid[y, x] = 1
        start, goal = np.array([2.0, 2.0]), np.array([n-3.0, n-3.0])
    elif spec.name == "bottleneck":
        grid[4:n-4, n//2] = 1
        grid[n//2-1:n//2+2, n//2] = 0
        for _ in range(int(n*n*spec.obstacle_density*0.35)):
            x, y = rng.integers(2, n-2, size=2)
            if abs(x-n//2) > 1:
                grid[y, x]=1
        start, goal = np.array([3.0, n-4.0]), np.array([n-4.0, 3.0])
    elif spec.name == "dead_end":
        grid[5:n-5, 6] = 1
        grid[5,6:n-6]=1
        grid[n-6,6:n-6]=1
        grid[5:n-5,n-6]=1
        grid[n//2-2:n//2+2, n-6] = 0
        for _ in range(int(n*n*spec.obstacle_density*0.18)):
            x, y = rng.integers(2, n-2, size=2)
            if 6 < x < n-6 and 5 < y < n-5:
                continue
            grid[y, x] = 1
        start, goal = np.array([3.0, 3.0]), np.array([n-4.0, n//2])
    elif spec.name == "dynamic_crossing":
        for col in [n//3, 2*n//3]:
            grid[3:n-3, col]=1
            grid[n//2-1:n//2+2,col]=0
        for row in [n//3, 2*n//3]:
            grid[row, 3:n-3]=1
            grid[row, n//2-1:n//2+2]=0
        start, goal = np.array([2.0, n-3.0]), np.array([n-3.0, 2.0])
    elif spec.name == "corridor_maze":
        for col in range(4, n-4, 4):
            grid[2:n-2, col] = 1
            gap = int(rng.integers(4, n-4))
            grid[max(2,gap-1):min(n-2,gap+2), col] = 0
        start, goal = np.array([2.0, 2.0]), np.array([n-3.0, n-3.0])
    elif spec.name == "asym_gap":
        grid[n//2, 3:n-3]=1
        grid[n//2, n//3-1:n//3+2]=0
        grid[n//2, 2*n//3-1:2*n//3+1]=0
        for _ in range(int(n*n*spec.obstacle_density*0.25)):
            x, y = rng.integers(2, n-2, size=2)
            if abs(y-n//2) > 1:
                grid[y, x] = 1
        start, goal = np.array([n-4.0, 3.0]), np.array([3.0, n-4.0])
    else:
        raise ValueError(spec.name)

    # dynamic obstacles defined by center and velocity
    dyn = []
    for i in range(spec.dynamic_obstacles):
        pos = np.array(rng.uniform(4, n-4, size=2), dtype=float)
        vel = rng.normal(size=2)
        vel = vel / (np.linalg.norm(vel) + 1e-6) * rng.uniform(0.04, 0.12)
        dyn.append((pos, vel))
    return grid, start, goal, dyn

def scenario_specs(size: int = 28, obstacle_density: float = 0.14, corridor_bias: float = 0.42, dynamic_obstacles: int = 3):
    names = ["easy_open","bottleneck","dead_end","dynamic_crossing","corridor_maze","asym_gap"]
    return [ScenarioSpec(n, size, obstacle_density, corridor_bias, dynamic_obstacles) for n in names]

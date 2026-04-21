from __future__ import annotations
import math
from typing import Iterable, Tuple
import numpy as np

def unit(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n < 1e-9:
        return np.zeros_like(v)
    return v / n

def angle_wrap(theta: float) -> float:
    return (theta + math.pi) % (2 * math.pi) - math.pi

def dist(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))

def lerp(a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
    return a + (b - a) * t

def path_length(points: Iterable[np.ndarray]) -> float:
    pts = list(points)
    if len(pts) < 2:
        return 0.0
    return float(sum(np.linalg.norm(pts[i+1]-pts[i]) for i in range(len(pts)-1)))

def raycast_grid(grid: np.ndarray, origin: np.ndarray, angle: float, max_range: float, step: float=0.2) -> float:
    direction = np.array([math.cos(angle), math.sin(angle)], dtype=float)
    t = 0.0
    h, w = grid.shape
    while t <= max_range:
        p = origin + direction * t
        x, y = int(round(p[0])), int(round(p[1]))
        if x < 0 or y < 0 or x >= w or y >= h:
            return t
        if grid[y, x] == 1:
            return t
        t += step
    return max_range

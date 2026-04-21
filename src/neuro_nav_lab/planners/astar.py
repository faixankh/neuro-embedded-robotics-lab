from __future__ import annotations
import heapq
from typing import Dict, List, Optional, Tuple
import numpy as np

Coord = Tuple[int, int]

def neighbors(node: Coord):
    x, y = node
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        yield x+dx, y+dy

def heuristic(a: Coord, b: Coord) -> float:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid: np.ndarray, start: Coord, goal: Coord) -> Optional[List[Coord]]:
    h, w = grid.shape
    if grid[start[1], start[0]] == 1 or grid[goal[1], goal[0]] == 1:
        return None
    open_heap: List[Tuple[float, Coord]] = [(0.0, start)]
    came: Dict[Coord, Coord] = {}
    g = {start: 0.0}
    f = {start: heuristic(start, goal)}
    closed = set()
    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        if current == goal:
            path = [current]
            while current in came:
                current = came[current]
                path.append(current)
            return list(reversed(path))
        closed.add(current)
        for nb in neighbors(current):
            x, y = nb
            if x < 0 or y < 0 or x >= w or y >= h or grid[y, x] == 1:
                continue
            tentative = g[current] + 1.0
            if tentative < g.get(nb, 1e9):
                came[nb] = current
                g[nb] = tentative
                f[nb] = tentative + heuristic(nb, goal)
                heapq.heappush(open_heap, (f[nb], nb))
    return None

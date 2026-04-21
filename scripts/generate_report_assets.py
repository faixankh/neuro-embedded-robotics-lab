from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "results"
FIG = ROOT / "assets" / "figures"
ANIM = ROOT / "assets" / "animations"
FIG.mkdir(parents=True, exist_ok=True)
ANIM.mkdir(parents=True, exist_ok=True)

summary = json.loads((RESULTS / "study_summary.json").read_text())
records = json.loads((RESULTS / "study_records.json").read_text())
traj_bank = json.loads((RESULTS / "trajectory_bank.json").read_text())

controllers = list(summary.keys())
success = [summary[c]["success_rate"] for c in controllers]
collisions = [summary[c]["collision_rate"] for c in controllers]
energy = [summary[c]["avg_energy"] for c in controllers]
eff = [summary[c]["avg_efficiency"] for c in controllers]

def save_bar(path, title, values, ylabel):
    plt.figure(figsize=(10,5))
    plt.bar(range(len(values)), values)
    plt.xticks(range(len(values)), controllers, rotation=20, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()

save_bar(FIG / "success_rate.png", "Navigation success across controller families", success, "Success rate")
save_bar(FIG / "collision_rate.png", "Collision rate across controller families", collisions, "Collision rate")
save_bar(FIG / "energy_budget.png", "Energy proxy accumulated over episodes", energy, "Energy proxy")
save_bar(FIG / "path_efficiency.png", "Path efficiency relative to straight-line distance", eff, "Efficiency")

# radar-like profile
metrics = ["success_rate","collision_rate","avg_efficiency","avg_min_clearance"]
angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]
plt.figure(figsize=(7,7))
ax = plt.subplot(111, polar=True)
for c in controllers:
    vals = [summary[c]["success_rate"], 1-summary[c]["collision_rate"], summary[c]["avg_efficiency"], summary[c]["avg_min_clearance"]/3.0]
    vals += vals[:1]
    ax.plot(angles, vals, label=c)
    ax.fill(angles, vals, alpha=0.08)
ax.set_xticks(angles[:-1], ["success","1-collision","efficiency","clearance"])
ax.set_title("Controller profile")
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.15))
plt.tight_layout()
plt.savefig(FIG / "controller_profile.png", dpi=180)
plt.close()

# Scenario heatmap
scenario_names = sorted(set(r["scenario"] for r in records))
data = np.zeros((len(controllers), len(scenario_names)))
for i, c in enumerate(controllers):
    for j, s in enumerate(scenario_names):
        subset = [r for r in records if r["controller"] == c and r["scenario"] == s]
        data[i, j] = np.mean([r["success"] for r in subset]) if subset else 0.0
plt.figure(figsize=(10,4.8))
plt.imshow(data, aspect="auto")
plt.colorbar(label="Success rate")
plt.yticks(range(len(controllers)), controllers)
plt.xticks(range(len(scenario_names)), scenario_names, rotation=25, ha="right")
plt.title("Scenario-conditioned success heatmap")
plt.tight_layout()
plt.savefig(FIG / "scenario_heatmap.png", dpi=180)
plt.close()

# System diagram
svg = f'''
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="800" viewBox="0 0 1400 800">
  <rect width="1400" height="800" fill="white"/>
  <text x="70" y="70" font-size="34" font-family="Arial">Neuro-Embedded Navigation Lab — system overview</text>
  <rect x="60" y="130" width="230" height="120" rx="18" fill="#f2f2f2" stroke="black"/>
  <text x="90" y="180" font-size="24" font-family="Arial">Structured worlds</text>
  <text x="88" y="215" font-size="19" font-family="Arial">corridors • bottlenecks •</text>
  <text x="88" y="240" font-size="19" font-family="Arial">dynamic crossings</text>

  <rect x="360" y="130" width="260" height="120" rx="18" fill="#f2f2f2" stroke="black"/>
  <text x="390" y="180" font-size="24" font-family="Arial">Range + dynamic sensing</text>
  <text x="392" y="215" font-size="19" font-family="Arial">24-beam lidar surrogate</text>
  <text x="392" y="240" font-size="19" font-family="Arial">relative obstacle state</text>

  <rect x="690" y="130" width="260" height="120" rx="18" fill="#f2f2f2" stroke="black"/>
  <text x="740" y="180" font-size="24" font-family="Arial">Temporal spike memory</text>
  <text x="735" y="215" font-size="19" font-family="Arial">membrane • trace • rate</text>
  <text x="735" y="240" font-size="19" font-family="Arial">short-horizon risk state</text>

  <rect x="1020" y="130" width="280" height="120" rx="18" fill="#f2f2f2" stroke="black"/>
  <text x="1050" y="180" font-size="24" font-family="Arial">Planner-aware action fusion</text>
  <text x="1052" y="215" font-size="19" font-family="Arial">A* route prior + risk gating</text>
  <text x="1052" y="240" font-size="19" font-family="Arial">velocity / turn commands</text>

  <line x1="290" y1="190" x2="360" y2="190" stroke="black" stroke-width="3"/>
  <line x1="620" y1="190" x2="690" y2="190" stroke="black" stroke-width="3"/>
  <line x1="950" y1="190" x2="1020" y2="190" stroke="black" stroke-width="3"/>

  <rect x="100" y="360" width="1200" height="320" rx="22" fill="#fafafa" stroke="black"/>
  <text x="130" y="410" font-size="28" font-family="Arial">Experimental programme</text>
  <text x="140" y="470" font-size="22" font-family="Arial">• Controller families: reactive, sampling MPC, temporal-only, full neuro-embedded</text>
  <text x="140" y="515" font-size="22" font-family="Arial">• Scenario suite: easy open, bottleneck, dead-end, dynamic crossing, corridor maze, asymmetric gap</text>
  <text x="140" y="560" font-size="22" font-family="Arial">• Metrics: success, collision, steps, path efficiency, clearance, energy proxy</text>
  <text x="140" y="605" font-size="22" font-family="Arial">• Outputs: figures, animated trajectory playback, interactive HTML dashboard, manuscript draft</text>
</svg>
'''
(FIG / "system_overview.svg").write_text(svg)

# Animation from one trajectory
key = sorted([k for k in traj_bank if "corridor_maze__full_stack__0" in k or "corridor_maze__full_stack" in k])[0]
item = traj_bank[key]
grid = np.array(item["grid"])
traj = item["trajectory"]
scale = 18
frames = []
for t in range(1, len(traj)+1, max(1, len(traj)//70)):
    img = Image.new("RGB", (grid.shape[1]*scale, grid.shape[0]*scale), "white")
    d = ImageDraw.Draw(img)
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y,x] == 1:
                d.rectangle([x*scale, y*scale, (x+1)*scale, (y+1)*scale], fill=(35,35,35))
    # path so far
    pts = [(p[0]*scale, p[1]*scale) for p in traj[:t]]
    if len(pts) > 1:
        d.line(pts, fill=(20,20,20), width=3)
    gx, gy = item["goal"]
    sx, sy = item["start"]
    d.ellipse([gx*scale-6, gy*scale-6, gx*scale+6, gy*scale+6], fill=(70,70,70))
    d.rectangle([sx*scale-5, sy*scale-5, sx*scale+5, sy*scale+5], fill=(130,130,130))
    px, py = traj[t-1]
    d.ellipse([px*scale-5, py*scale-5, px*scale+5, py*scale+5], fill=(0,0,0))
    frames.append(img)
frames[0].save(ANIM / "trajectory_playback.gif", save_all=True, append_images=frames[1:], duration=80, loop=0)

print("assets generated")

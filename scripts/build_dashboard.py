from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "results"
OUT = ROOT / "reports" / "dashboard.html"
summary = json.loads((RESULTS / "study_summary.json").read_text())

cards = []
for name, stats in summary.items():
    cards.append(f'''
    <div class="card">
      <h3>{name}</h3>
      <div class="metric"><span>Success rate</span><strong>{stats["success_rate"]}</strong></div>
      <div class="metric"><span>Collision rate</span><strong>{stats["collision_rate"]}</strong></div>
      <div class="metric"><span>Avg steps</span><strong>{stats["avg_steps"]}</strong></div>
      <div class="metric"><span>Efficiency</span><strong>{stats["avg_efficiency"]}</strong></div>
      <div class="metric"><span>Energy</span><strong>{stats["avg_energy"]}</strong></div>
      <div class="metric"><span>Min clearance</span><strong>{stats["avg_min_clearance"]}</strong></div>
    </div>
    ''')

html = f'''
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<title>Neuro-Embedded Navigation Lab Dashboard</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 0; background: #f3f3f3; color: #111; }}
header {{ padding: 36px 42px; border-bottom: 1px solid #ccc; background: white; }}
main {{ padding: 30px 42px 60px; }}
.grid {{ display: grid; grid-template-columns: repeat(2, minmax(320px, 1fr)); gap: 18px; }}
.card {{ background: white; border: 1px solid #d8d8d8; border-radius: 18px; padding: 20px 22px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); }}
.metric {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px dashed #ddd; }}
.metric:last-child {{ border-bottom: 0; }}
.figure-row {{ display: grid; grid-template-columns: repeat(2, minmax(320px, 1fr)); gap: 18px; margin-top: 22px; }}
img {{ width: 100%; border-radius: 16px; border: 1px solid #ddd; background: white; }}
.note {{ margin-top: 20px; line-height: 1.6; max-width: 900px; }}
</style>
</head>
<body>
<header>
  <h1>Neuro-Embedded Navigation Lab</h1>
  <p>Simulation-first research dashboard for hierarchical neuro-inspired navigation.</p>
</header>
<main>
  <section class="grid">
    {''.join(cards)}
  </section>
  <section class="figure-row">
    <img src="../assets/figures/success_rate.png" alt="success rate"/>
    <img src="../assets/figures/scenario_heatmap.png" alt="scenario heatmap"/>
    <img src="../assets/figures/controller_profile.png" alt="controller profile"/>
    <img src="../assets/animations/trajectory_playback.gif" alt="trajectory playback"/>
  </section>
  <div class="note">
    <p>This dashboard is intentionally restrained in style. The purpose is to make the repository feel like a lab report companion rather than a pitch deck. Claims remain limited to the simulator implemented in this codebase.</p>
  </div>
</main>
</body>
</html>
'''
OUT.write_text(html)
print("dashboard written")

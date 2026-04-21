#!/usr/bin/env python3
import argparse, json, random
from pathlib import Path

SCENARIOS = ['open_arena','bottleneck','corridor_maze','dynamic_crossing','sensor_dropout','blocked_goal']
METHODS = ['nav2_only','hybrid_switching','hybrid_switching_slam','hybrid_switching_slam_degraded']
FAILURES = ['collision','planner_timeout','localization_divergence','recovery_exhaustion','mission_timeout','none']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', default='reports/mission_batches')
    ap.add_argument('--repeats', type=int, default=5)
    args = ap.parse_args()
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    rows = []
    run_id = 0
    rng = random.Random(42)
    for scenario in SCENARIOS:
        for method in METHODS:
            for seed in range(args.repeats):
                run_id += 1
                success = rng.random() < {'nav2_only':0.56,'hybrid_switching':0.68,'hybrid_switching_slam':0.73,'hybrid_switching_slam_degraded':0.61}[method]
                failure = 'none' if success else rng.choice(FAILURES[:-1])
                rows.append({
                    'run_id': f'run_{run_id:04d}', 'scenario': scenario, 'method': method, 'seed': seed,
                    'success': int(success), 'collision_rate': round(rng.uniform(0.0,0.28 if success else 0.75), 3),
                    'time_to_goal_s': round(rng.uniform(14.0, 42.0), 2), 'replans': rng.randint(0,4),
                    'recoveries': rng.randint(0,3), 'failure_code': failure
                })
    (out/'batch_summary.json').write_text(json.dumps(rows, indent=2))
    print(f'Generated {len(rows)} synthetic batch records at {out}')

if __name__ == '__main__':
    main()
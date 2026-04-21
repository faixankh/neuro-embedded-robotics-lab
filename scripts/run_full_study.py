from pathlib import Path
from neuro_nav_lab.evaluation.runner import run_study, summarise, save_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results"
OUT.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    records, trajectories = run_study()
    summary = summarise(records)
    save_json(records, OUT / "study_records.json")
    save_json(summary, OUT / "study_summary.json")
    save_json(trajectories, OUT / "trajectory_bank.json")
    print("study complete")
    for name, stats in summary.items():
        print(name, stats)

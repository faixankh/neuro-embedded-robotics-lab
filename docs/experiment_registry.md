# Experiment registry

## Study identifier
`NEL-2026-main-study-v0.3`

## Fixed settings
- map size: 28 x 28
- lidar beams: 24
- max steps: 340
- dynamic obstacles per scenario: 3
- repeats per controller-scenario pair: 6

## Controller roster
1. Reactive
2. Sampling MPC
3. Temporal Only
4. Full Neuro-Embedded

## Scenario roster
1. easy_open
2. bottleneck
3. dead_end
4. dynamic_crossing
5. corridor_maze
6. asym_gap

## Output contract
The study must regenerate:
- `study_records.json`
- `study_summary.json`
- `trajectory_bank.json`
- figure set in `assets/figures`
- `trajectory_playback.gif`
- `reports/dashboard.html`

## Review checklist
- figures regenerate without manual editing
- tests pass
- controller names match documentation
- no claim exceeds implemented evidence

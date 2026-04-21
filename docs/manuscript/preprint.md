# Neuro-Embedded Navigation Under Structured Clutter

## Abstract
This repository investigates a hierarchical control stack that combines route planning, local obstacle sensing, and a spike-inspired temporal memory for navigation in structured clutter. The study is performed in a reproducible 2D benchmark containing bottlenecks, dead-ends, corridor mazes, and moving obstacles. Four controller families are compared. Results indicate that temporal state improves robustness relative to purely reactive control, while the best overall performance is obtained when temporal state is fused with a route prior and conservative risk gating.

## Main claim
A temporally informed local controller benefits from planner coupling. Temporal state without route guidance improves short-horizon awareness but tends to wander; planner coupling restores task commitment.

## Limitations
The simulator uses simplified nonholonomic motion and a custom sensor model. The work should therefore be read as a controlled systems prototype rather than a claim of field-ready robotics.

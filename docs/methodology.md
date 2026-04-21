# Methodology

## Observation model
Each step exposes:
- 24 range beams normalized by sensor range,
- goal distance and goal-relative heading,
- planner-relative heading,
- dynamic obstacle relative position summaries.

## Temporal representation
The spiking temporal memory maintains three rolling statistics:
- membrane state,
- spike trace,
- firing-rate proxy.

This is used as a compact recent-history descriptor rather than as a claim of biological realism.

## Controller formulation
The full controller produces action `a_t = [v_t, \omega_t]` from
- planner alignment,
- reactive left-right obstacle pressure,
- dynamic obstacle directional bias,
- front-risk velocity gating.

The design intent is to combine route commitment with local caution.

## Metrics
- success rate
- collision rate
- average episode length
- path efficiency
- minimum clearance
- energy proxy

## Why not report reward curves?
This repository is not yet framed as an RL training paper. At this stage, reward is an internal shaping signal, while the public benchmark is stated in task-level metrics.

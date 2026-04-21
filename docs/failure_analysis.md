# Failure analysis

## Reactive controller
Typical failure: oscillation near corridor entries followed by collision. The controller reacts to immediate asymmetry but cannot preserve route commitment.

## Sampling MPC
Typical failure: local indecision under strong planner-reactive disagreement. It is more stable than the reactive baseline but still lacks temporal memory.

## Temporal Only
Typical failure: detours and over-cautious turning. Temporal memory helps avoid repeated contact with the same obstacle pattern, but the absence of a route prior increases wandering.

## Full Neuro-Embedded
Typical failure: conservative slowdown under tightly packed moving obstacles. It generally resolves bottlenecks better than the baselines, but can still hesitate when dynamic risk remains high for many consecutive steps.

## Why this matters
A repository looks more real when it shows where the method breaks. A perfect controller would reduce credibility.

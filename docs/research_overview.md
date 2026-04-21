# Research overview

## Positioning
This repository studies a specific question in autonomous navigation: whether a compact temporal state can repair the brittleness of purely reactive control in structured clutter. The work is framed as a simulation-first precursor to a ROS 2 deployment path.

## Design principles
1. **Local realism over large claims.** The simulator is simple enough to audit yet rich enough to expose meaningful controller failures.
2. **Controller discipline.** Every improvement is judged against named baselines, not against a vague reference.
3. **Readable outputs.** Figures are designed to look like manuscript figures and lab reports, not pitch visuals.
4. **Extensibility.** The source tree is arranged so that ROS integration, trainable SNN modules, and hardware adapters can be added without collapsing the current code.

## Scientific niche
The project lives at the intersection of:
- spiking / neuromorphic temporal state estimation,
- route-aware navigation,
- conservative local control under dynamic clutter,
- reproducible research software.

The simulator is deliberately modest because the repository is intended to be a trustworthy starting point for a more ambitious robotics programme.

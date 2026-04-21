# SLAM and Mission Protocol

## Experimental axes
1. **Backend**: prebuilt map / SLAM Toolbox / Cartographer
2. **Controller mode**: Nav2 only / hybrid arbitration / forced neuro
3. **Degradation**: nominal / moderate / severe
4. **Scenario family**: open, bottleneck, maze, dynamic, blocked goal, sensor dropout

## Run products
Each mission run should produce:
- rosbag directory
- node list
- topic list
- TF export
- telemetry CSV
- mission summary JSON
- evaluation PNG
- failure event CSV

## Failure taxonomy
- collision
- oscillation trap
- dead-end persistence
- planner timeout
- localization divergence
- controller conflict
- sensor blackout failure
- recovery exhaustion
- mission timeout
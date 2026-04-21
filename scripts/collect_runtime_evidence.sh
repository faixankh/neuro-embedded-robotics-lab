#!/usr/bin/env bash
set -euo pipefail
echo "ros2 node list > demo/live_capture/raw/ros2_node_list.txt"
echo "ros2 topic list > demo/live_capture/raw/ros2_topic_list.txt"
echo "ros2 topic hz /scan > demo/live_capture/raw/scan_hz.txt"
echo "ros2 bag info demo/live_capture/raw/bag > demo/live_capture/raw/bag_info.txt"
echo "rqt_graph or equivalent screenshot -> demo/live_capture/raw/graph.png"

#!/usr/bin/env bash
set -e

WORKSPACE="${HOME}/ldlidar_ros2_ws"

cd "$WORKSPACE"
source /opt/ros/jazzy/setup.bash
source "$WORKSPACE/install/setup.bash"

ros2 launch obstacle_monitor rover_lidar_stack.launch.py

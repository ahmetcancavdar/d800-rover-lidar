# D800 Rover LiDAR

A ROS 2 Jazzy-based LiDAR stack for a rover using the LDROBOT D800 / STL-27L LiDAR kit on Raspberry Pi 5 with Ubuntu 24.04.

This project adds an obstacle monitoring layer on top of the LiDAR driver and provides Foxglove visualization support for live monitoring.

## Features

- Live 2D LiDAR scan publishing from D800 / STL-27L
- Obstacle detection based on `sensor_msgs/msg/LaserScan`
- Distance, angle, and side estimation for the closest obstacle
- Alert generation when an obstacle is closer than a configurable threshold
- Foxglove layout support for monitoring
- Single launch file for LiDAR + obstacle monitor + Foxglove bridge

## Hardware

- Raspberry Pi 5
- Ubuntu 24.04
- LDROBOT D800 LiDAR Kit / STL-27L
- Network connection for Foxglove visualization

## Software Requirements

- ROS 2 Jazzy
- `foxglove_bridge`
- Python ROS 2 package support (`ament_python`)
- Upstream LiDAR driver repository:
  - `ldlidar_stl_ros2`

## Repository Structure

```text
.
├── README.md
├── .gitignore
├── foxglove/
│   └── d800_obstacle_layout.json
├── scripts/
│   ├── start_d800_stack.sh
│   └── patch_ldlidar.sh
└── src/
    └── obstacle_monitor/
        ├── launch/
        │   └── rover_lidar_stack.launch.py
        ├── obstacle_monitor/
        │   ├── __init__.py
        │   └── obstacle_alert_node.py
        ├── package.xml
        ├── resource/
        │   └── obstacle_monitor
        └── setup.py

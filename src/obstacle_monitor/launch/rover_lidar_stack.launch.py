import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    threshold_m = LaunchConfiguration("threshold_m")
    monitor_min_deg = LaunchConfiguration("monitor_min_deg")
    monitor_max_deg = LaunchConfiguration("monitor_max_deg")
    foxglove_port = LaunchConfiguration("foxglove_port")

    ldlidar_pkg_share = get_package_share_directory("ldlidar_stl_ros2")
    foxglove_pkg_share = get_package_share_directory("foxglove_bridge")

    ldlidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ldlidar_pkg_share, "launch", "stl27l.launch.py")
        )
    )

    obstacle_node = Node(
        package="obstacle_monitor",
        executable="obstacle_alert_node",
        name="obstacle_alert_node",
        output="screen",
        parameters=[
            {
                "threshold_m": threshold_m,
                "monitor_min_deg": monitor_min_deg,
                "monitor_max_deg": monitor_max_deg,
            }
        ],
    )

    foxglove_launch = IncludeLaunchDescription(
        FrontendLaunchDescriptionSource(
            os.path.join(foxglove_pkg_share, "launch", "foxglove_bridge_launch.xml")
        ),
        launch_arguments={
            "port": foxglove_port,
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument("threshold_m", default_value="0.10"),
        DeclareLaunchArgument("monitor_min_deg", default_value="-90.0"),
        DeclareLaunchArgument("monitor_max_deg", default_value="90.0"),
        DeclareLaunchArgument("foxglove_port", default_value="8765"),

        ldlidar_launch,
        obstacle_node,
        foxglove_launch,
    ])

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Float32, String


def normalize_deg(angle_deg: float) -> float:
    while angle_deg >= 180.0:
        angle_deg -= 360.0
    while angle_deg < -180.0:
        angle_deg += 360.0
    return angle_deg


def angle_in_window(angle_deg: float, min_deg: float, max_deg: float) -> bool:
    angle_deg = normalize_deg(angle_deg)
    min_deg = normalize_deg(min_deg)
    max_deg = normalize_deg(max_deg)

    if min_deg <= max_deg:
        return min_deg <= angle_deg <= max_deg
    else:
        # wrap-around case, e.g. 150 .. -150
        return angle_deg >= min_deg or angle_deg <= max_deg


def classify_side(angle_deg: float) -> str:
    a = normalize_deg(angle_deg)

    if -22.5 <= a <= 22.5:
        return "front"
    elif 22.5 < a <= 67.5:
        return "front-left"
    elif 67.5 < a <= 112.5:
        return "left"
    elif 112.5 < a <= 157.5:
        return "rear-left"
    elif a > 157.5 or a < -157.5:
        return "rear"
    elif -157.5 <= a < -112.5:
        return "rear-right"
    elif -112.5 <= a < -67.5:
        return "right"
    else:
        return "front-right"


class ObstacleAlertNode(Node):
    def __init__(self):
        super().__init__("obstacle_alert_node")

        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("threshold_m", 0.10)
        self.declare_parameter("monitor_min_deg", -180.0)
        self.declare_parameter("monitor_max_deg", 180.0)

        scan_topic = self.get_parameter("scan_topic").value

        self.alert_pub = self.create_publisher(Bool, "/obstacle/alert", 10)
        self.distance_pub = self.create_publisher(Float32, "/obstacle/distance_cm", 10)
        self.angle_pub = self.create_publisher(Float32, "/obstacle/angle_deg", 10)
        self.side_pub = self.create_publisher(String, "/obstacle/side", 10)
        self.status_pub = self.create_publisher(String, "/obstacle/status", 10)

        self.scan_sub = self.create_subscription(
            LaserScan,
            scan_topic,
            self.scan_callback,
            qos_profile_sensor_data,
        )

        self.get_logger().info("obstacle_alert_node started")

    def scan_callback(self, msg: LaserScan):
        threshold_m = float(self.get_parameter("threshold_m").value)
        monitor_min_deg = float(self.get_parameter("monitor_min_deg").value)
        monitor_max_deg = float(self.get_parameter("monitor_max_deg").value)

        best_range = None
        best_angle_deg = None

        for i, r in enumerate(msg.ranges):
            if not math.isfinite(r):
                continue
            if r < msg.range_min or r > msg.range_max:
                continue

            angle_rad = msg.angle_min + i * msg.angle_increment
            angle_deg = normalize_deg(math.degrees(angle_rad))

            if not angle_in_window(angle_deg, monitor_min_deg, monitor_max_deg):
                continue

            if best_range is None or r < best_range:
                best_range = r
                best_angle_deg = angle_deg

        alert_msg = Bool()
        dist_msg = Float32()
        angle_msg = Float32()
        side_msg = String()
        status_msg = String()

        if best_range is None:
            alert_msg.data = False
            dist_msg.data = float("nan")
            angle_msg.data = float("nan")
            side_msg.data = "unknown"
            status_msg.data = "No valid obstacle in monitored sector"
        else:
            side = classify_side(best_angle_deg)
            distance_cm = best_range * 100.0
            is_alert = best_range <= threshold_m

            alert_msg.data = is_alert
            dist_msg.data = float(distance_cm)
            angle_msg.data = float(best_angle_deg)
            side_msg.data = side

            if is_alert:
                status_msg.data = (
                    f"ALERT: obstacle at {distance_cm:.1f} cm, "
                    f"{side}, angle {best_angle_deg:+.1f} deg"
                )
            else:
                status_msg.data = (
                    f"Closest obstacle: {distance_cm:.1f} cm, "
                    f"{side}, angle {best_angle_deg:+.1f} deg"
                )

        self.alert_pub.publish(alert_msg)
        self.distance_pub.publish(dist_msg)
        self.angle_pub.publish(angle_msg)
        self.side_pub.publish(side_msg)
        self.status_pub.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAlertNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

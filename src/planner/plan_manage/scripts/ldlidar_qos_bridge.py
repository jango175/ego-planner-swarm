#!/usr/bin/env python3

"""
QoS bridge ROS 2 package.
"""

import math
import rclpy
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.subscription import Subscription
from sensor_msgs.msg import PointCloud2
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from quadrotor_msgs.msg import PositionCommand
from rclpy.qos import qos_profile_sensor_data, qos_profile_system_default


class LDLidarQoSBridge(Node):
  """
  QoS brigde class for topic relaying with default QoS.
  """

  def __init__(self):
    """
    QoSBridge constructor.
    """

    super().__init__('ldlidar_qos_bridge')

    self.declare_parameter('drone_id', 0)
    self.declare_parameter('input_cloud_topic', '/lidar_mapper_visualizer/global_map')

    self.drone_id: int = self.get_parameter('drone_id').value
    self.input_cloud_topic: str = self.get_parameter('input_cloud_topic').value

    # Odometry bridge (MAVROS -> EGO-Planner)
    self.odom_sub: Subscription = self.create_subscription(
      Odometry,
      '/mavros/local_position/odom',
      self.odom_callback,
      qos_profile_sensor_data
    )
    self.odom_pub: Publisher = self.create_publisher(
      Odometry,
      f'drone_{self.drone_id}_odom',
      qos_profile_system_default
    )

    # PointCloud bridge (LiDAR -> EGO-Planner)
    self.cloud_sub: Subscription = self.create_subscription(
      PointCloud2,
      self.input_cloud_topic,
      self.cloud_callback,
      qos_profile_sensor_data
    )
    self.cloud_pub: Publisher = self.create_publisher(
      PointCloud2,
      f'drone_{self.drone_id}_cloud',
      qos_profile_system_default
    )

    # Command bridge (EGO-Planner -> MAVROS)
    self.cmd_sub: Subscription = self.create_subscription(
      PositionCommand,
      '/planning/pos_cmd',
      self.cmd_callback,
      qos_profile_sensor_data
    )
    self.cmd_pub: Publisher = self.create_publisher(
      PoseStamped,
      '/mavros/setpoint_position/local',
      qos_profile_system_default
    )

    self.get_logger().info('QoS bridge active!')


  def cmd_callback(self, msg: PositionCommand):
    """
    Position command callback.

    :param msg: Position command message.
    """

    pose = PoseStamped()
    pose.header.stamp = msg.header.stamp
    pose.header.frame_id = 'map'

    # Map position
    pose.pose.position.x = msg.position.x
    pose.pose.position.y = msg.position.y
    pose.pose.position.z = msg.position.z
    pose.pose.orientation.w = math.cos(msg.yaw / 2.0)
    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = math.sin(msg.yaw / 2.0)

    self.cmd_pub.publish(pose)

    # self.get_logger().info(f'X: {pose.pose.position.x}, Y: {pose.pose.position.y}, Z: {pose.pose.position.z}')
    # self.get_logger().info(f'Yaw: {msg.yaw * 180.0 / math.pi}')


  def odom_callback(self, msg: Odometry):
    """
    Odometry callback.

    :param msg: Odometry message.
    """

    self.odom_pub.publish(msg)


  def cloud_callback(self, msg: PointCloud2):
    """
    Point cloud callback.

    :param msg: Point cloud message.
    """

    self.cloud_pub.publish(msg)


def main(args: list[str] | None = None):
  """
  Main function.

  :param args: Main arguments.
  """

  rclpy.init(args=args)
  node = LDLidarQoSBridge()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  finally:
    node.destroy_node()
    rclpy.shutdown()


# Entry point
if __name__ == '__main__':
  main()

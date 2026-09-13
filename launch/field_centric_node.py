#!/usr/bin/env python3

import math

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node


class FieldCentricNode(Node):
    def __init__(self):
        super().__init__('field_centric_node')

        self.yaw = None
        self.initial_yaw = None
        self.command_subscriber = self.create_subscription(
            Twist,
            '/cmd_vel_raw',
            self.command_callback,
            10,
        )
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10,
        )
        self.command_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def odom_callback(self, message):
        orientation = message.pose.pose.orientation
        sin_yaw = 2.0 * (orientation.w * orientation.z + orientation.x * orientation.y)
        cos_yaw = 1.0 - 2.0 * (orientation.y * orientation.y + orientation.z * orientation.z)
        self.yaw = math.atan2(sin_yaw, cos_yaw)
        if self.initial_yaw is None:
            self.initial_yaw = self.yaw

    def command_callback(self, message):
        if self.yaw is None:
            return

        relative_yaw = self.yaw - self.initial_yaw
        cos_yaw = math.cos(relative_yaw)
        sin_yaw = math.sin(relative_yaw)

        transformed_command = Twist()
        transformed_command.linear.x = (
            cos_yaw * message.linear.x + sin_yaw * message.linear.y
        )
        transformed_command.linear.y = (
            -sin_yaw * message.linear.x + cos_yaw * message.linear.y
        )
        transformed_command.linear.z = message.linear.z
        transformed_command.angular.x = message.angular.x
        transformed_command.angular.y = message.angular.y
        transformed_command.angular.z = message.angular.z
        self.command_publisher.publish(transformed_command)


def main(args=None):
    rclpy.init(args=args)
    node = FieldCentricNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

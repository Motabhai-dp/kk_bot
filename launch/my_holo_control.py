from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
	teleop_node = Node(
		package='teleop_twist_joy',
		executable='teleop_node',
		name='teleop_twist_joy',
		parameters=[{
			'require_enable_button': True,
			'enable_button': 4,
			'axis_linear.x': 1,
			'axis_linear.y': 0,
			'axis_linear.z': 0,
			'axis_angular.yaw': 3,
			'scale_linear.x': 0.5,
			'scale_linear.y': 0.5,
			'scale_linear.z': 0.0,
			'scale_angular.yaw': 1.0,
		}],
		remappings=[
			('joy', '/joy'),
			('cmd_vel', '/cmd_vel'),
		],
		output='screen')

	return LaunchDescription([
		teleop_node,
	])

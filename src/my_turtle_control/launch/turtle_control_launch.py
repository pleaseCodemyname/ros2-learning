from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
        ),
        Node(
            package='my_turtle_control',
            executable='pose_subscriber',
        ),
        Node(
            package='my_turtle_control',
            executable='wall_avoider',
        ),
    ])
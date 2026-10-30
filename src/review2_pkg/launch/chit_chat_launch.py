from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='review2_pkg', executable='talker'),
        Node(package='review2_pkg', executable='listener'),
    ])


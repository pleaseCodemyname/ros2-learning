from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='review_pkg', executable='talker'),
        Node(package='review_pkg', executable='listener'),
    ])
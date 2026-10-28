from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='step_pkg', executable='talker', parameters=[{'word': "하이"}], name="talker_hi"),
        Node(package='step_pkg', executable='talker', parameters=[{'word': "바이"}], name="talker_bye"),
        Node(package='step_pkg', executable='listener'),
    ])
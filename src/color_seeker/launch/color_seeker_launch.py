import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory("color_seeker")
    world = os.path.join(pkg_share, "worlds", "world.sdf")
    robot = os.path.join(pkg_share, "urdf", "robot.urdf")
    red_box = os.path.join(pkg_share, "worlds", "red_box.sdf")

    return LaunchDescription([
        ExecuteProcess(cmd=["gz", "sim", "-r", world]),
        Node(package="ros_gz_sim", executable="create", arguments=["-file", robot, "-name", "stt_bot", "-z", "0.5"]),
        Node(package="ros_gz_sim", executable="create", arguments=["-file", red_box, "-name", "red_box", "-x", "1.0", "-y", "0.4", "-z", "0.15"]),
        Node(package="ros_gz_bridge", executable="parameter_bridge", arguments=["/camera/image@sensor_msgs/msg/Image[gz.msgs.Image","/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist"]),
        Node(package="color_seeker", executable="color_seeker", parameters=[{"stop_count": 49000, "turn_speed": 0.3, "forward_speed": 0.2}], output="screen")
    ])

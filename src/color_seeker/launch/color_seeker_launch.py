import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_share = get_package_share_directory("color_seeker")
    world = os.path.join(pkg_share, "worlds", "world.sdf")
    robot = os.path.join(pkg_share, "urdf", "robot.urdf")
    red_box = os.path.join(pkg_share, "worlds", "red_box.sdf")
    blue_box = os.path.join(pkg_share, "worlds", "blue_box.sdf")
    green_box = os.path.join(pkg_share, "worlds", "green_box.sdf")
    robot_description = open(robot).read()

    return LaunchDescription([
        DeclareLaunchArgument("detector", default_value="color", choices=["color", "owlv2"], description="물체 찾는 방법: color(색 마스크) 또는 owlv2(글로 찾는 검출 모델)"),
        ExecuteProcess(cmd=["gz", "sim", "-r", world]),
        Node(package="ros_gz_sim", executable="create", arguments=["-file", robot, "-name", "stt_bot", "-z", "0.5"]),
        Node(package="ros_gz_sim", executable="create", arguments=["-file", red_box, "-name", "red_box", "-x", "1.0", "-y", "0.4", "-z", "0.15"]),
        Node(package="ros_gz_sim", executable="create", arguments=["-file", blue_box, "-name", "blue_box", "-x", "1.0", "-y", "-0.4", "-z", "0.15"]),
        Node(package="ros_gz_sim", executable="create", arguments=["-file", green_box, "-name", "green_box", "-x", "-1.0", "-y", "0", "-z", "0.15"]),
        Node(package="ros_gz_bridge", executable="parameter_bridge", arguments=["/camera/image@sensor_msgs/msg/Image[gz.msgs.Image","/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist", "/model/stt_bot/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry", "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan", "/world/empty/model/stt_bot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model", "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock", "/model/stt_bot/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V" ], remappings=[("/world/empty/model/stt_bot/joint_state", "/joint_states"), ("/model/stt_bot/tf", "/tf")]),
        Node(package="color_seeker", executable="color_seeker", parameters=[{"stop_count": 49000, "turn_speed": 0.3, "forward_speed": 0.2, "detector": LaunchConfiguration("detector")}], output="screen"), # "color": "red"는 이제 goal로 받기 때문에 필요없어짐
        Node(package="robot_state_publisher", executable="robot_state_publisher", parameters=[{"robot_description": robot_description, "use_sim_time": True}])
    ])

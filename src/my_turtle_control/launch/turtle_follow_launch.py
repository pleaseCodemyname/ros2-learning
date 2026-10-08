from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
        ),
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn',
                "{x: 4.0, y: 2.0, theta: 0.0, name: 'turtle2'}"],
        ),
        Node(
            package='my_turtle_control',
            executable='turtle_tf_broadcaster',
            name='broadcaster1',
            parameters=[{'turtlename': 'turtle1'}],
        ),
        Node(
            package='my_turtle_control',
            executable='turtle_tf_broadcaster',
            name='broadcaster2',
            parameters=[{'turtlename': 'turtle2'}],
        ),
        Node(
            package='my_turtle_control',
            executable='turtle_follower',
        ),
        Node(
            package='my_turtle_control',
            executable='wall_avoider',
        ),
    ])
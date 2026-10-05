import rclpy
import math
from rclpy.executors import ExternalShutdownException
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from rclpy.node import Node

class WallAvoider(Node):
    def __init__(self):
        super().__init__('wall_avoider')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.pose_callback,
            10)
        self.get_logger().info('Wall Avoider Node has been started.')

    def pose_callback(self, msg):
        cmd = Twist()
        facing_right = msg.x > 9.5 and math.cos(msg.theta) > 0
        facing_left = msg.x < 1.5 and math.cos(msg.theta) < 0
        facing_top = msg.y > 9.5 and math.sin(msg.theta) > 0
        facing_bottom = msg.y < 1.5 and math.sin(msg.theta) < 0
        if facing_right or facing_left or facing_top or facing_bottom:
            cmd.linear.x = 0.5  # Move forward slowly
            cmd.angular.z = 2.0   # Turn left
            self.get_logger().info('Facing wall! Turning away.', throttle_duration_sec=1.0)
        else:
            cmd.linear.x = 1.0   # Move forward
            cmd.angular.z = 0.0   # No turn
            self.get_logger().info('Moving forward.', throttle_duration_sec=1.0)

        self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    wall_avoider = WallAvoider()
    try:
        rclpy.spin(wall_avoider)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        wall_avoider.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
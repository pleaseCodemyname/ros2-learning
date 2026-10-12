import rclpy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

class SpeedChanger(Node):
    def __init__(self):
        super().__init__('speed_changer')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.pose_callback,
            10
        )
        self.get_logger().info('Speed Changer Node has been started')

    def pose_callback(self, msg):
        cmd = Twist()
        half_left = msg.x < 5.54445
        if half_left:
            cmd.linear.x = 10.0
            self.get_logger().info("좌측에 있으니 빨리 직진하세요", throttle_duration_sec=1.0)
        else:
            cmd.linear.x = 1.0
            self.get_logger().info("우측에 있으니 천천히 직진하세요", throttle_duration_sec=1.0)

        self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    speed_changer = SpeedChanger()
    try:
        rclpy.spin(speed_changer)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        speed_changer.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
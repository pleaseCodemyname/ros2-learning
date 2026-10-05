import rclpy
from rclpy.executors import ExternalShutdownException
from turtlesim.msg import Pose
from rclpy.node import Node

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')
        self.subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.pose_callback,
            10)
        self.get_logger().info('Pose Subscriber Node has been started.')

    def pose_callback(self, msg):
        self.get_logger().info('Received Pose: x=%.2f, y=%.2f, theta=%.2f' % (msg.x, msg.y, msg.theta), throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args)
    pose_subscriber = PoseSubscriber()
    try:
        rclpy.spin(pose_subscriber)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        pose_subscriber.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
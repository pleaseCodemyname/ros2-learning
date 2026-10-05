import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher(Node):
    def __init__(self):
        super().__init__('circle_publisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('Circle Publisher Node has been started.')

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 1.0  # Forward speed
        msg.angular.z = 1.0  # Angular speed for circular motion
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: Linear X: %.2f, Angular Z: %.2f' % (msg.linear.x, msg.angular.z))


def main(args=None):
    rclpy.init(args=args)
    circle_publisher = CirclePublisher()
    try:
        rclpy.spin(circle_publisher)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        circle_publisher.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePublisher(Node):
    def __init__(self):
        super().__init__('circle_publisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10) # Twist(토픽으로 주고받는 데이터 양식): 로봇에게 내리는 명령, 'turtle1/cmd_vel'이라는 토픽으로 발행, 10은 큐 사이즈(메시지 버퍼링) 의미
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('Circle Publisher Node has been started.')

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 1.0  # 초당 1만큼 전진
        msg.angular.z = 1.0  # 왼쪽으로 돌기
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
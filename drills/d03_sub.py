import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscriber = self.create_subscription(String, '/chatter', self.listener_callback, 10)

    # 콜백: 이런 일이 생기면 이 함수를 불러주라고 맡겨두는 함수. (Publisher에는 callback이 필요없음, publish()를 부를 때 올리기만 하는 도구이기 때문)
    # ex) create_subscription(..., 콜백, ...) 게시판에 글이 오면
    # ex) create_timer(1.0, 콜백) 1초가 지나면
    def listener_callback(self, msg):
        self.get_logger().info(f'받음: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    try:
        rclpy.spin(listener) # msg가 들어감, 맡겨둔 Subscriber 콜백을 msg와 함께 부름, 1초가 지나면 맡겨 둔 타이머 콜백을 부름.
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        listener.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription=self.create_subscription(String, '/chat', self.listener_callback, 10) # "/chat"에 글이 오면 "listener_callback"을 불러 달라고 등록 (부르는 건 spin)

    def listener_callback(self, msg): # msg는 talker가 보낸 String 봉투. spin이 글이 올 때마다 콜백을 부르면서 넣어 줌
        self.get_logger().info(f"받음: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    try:
        rclpy.spin(listener)
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        listener.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()

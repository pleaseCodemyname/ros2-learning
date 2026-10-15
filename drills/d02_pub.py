import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker') # 노드 이름
        self.publisher_ = self.create_publisher(String, '/chatter', 10) # 콜백을 부르는건 Publisher가 아니라 타이머, Publisher = 게시판에 올리는 도구, 누구도 부르지 않는다. / 타이머: "1초마다 이 함수를 불러 줘" <- 콜백을 부르는 쪽
        self.timer = self.create_timer(1.0, self.talker_callback)

    def talker_callback(self):
        msg = String() # 빈 String 양식 하나 만들기
        msg.data = 'hello'
        self.publisher_.publish(msg)
        self.get_logger().info('보냄: hello')


def main(args=None):
    rclpy.init(args=args)
    talker = Talker()
    try:
        rclpy.spin(talker)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        talker.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
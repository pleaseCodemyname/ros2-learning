import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException

class Hello(Node):
    def __init__(self):
        super().__init__('hello')
        self.get_logger().info("안녕, 나는 hello 노드")


def main(args=None):
    rclpy.init(args=args)
    hello = Hello()
    try:
        rclpy.spin(hello) # 왜 터미널이 안꺼지고 살아있나? spin(hello)가 "일이 생기길 기다리는 무한 대기" 1) 글이오면 -> Subscriber 콜백 부르기 2) 시간이 되면 -> 타이머 콜백 부르기 3) 아무 일도 없으면 -> 조용히 계속 기다리기 4) Ctrl + C가 와야 끝남
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        hello.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
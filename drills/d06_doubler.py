# Q1 내보내는게 있나? (Pub): /doubled 토픽에 올림
# Q2 알아야 할게 있나? (Sub): /number에서 받은 값
# Q3 받는 것 없이 반복할 일이 있나? (타이머): 없음

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import Int32 # std = standard

class Doubler(Node):
    def __init__(self):
        super().__init__('doubler')
        self.subscription = self.create_subscription(Int32, '/number', self.double_callback, 10)
        self.publisher_ = self.create_publisher(Int32, '/doubled', 10)
        
    # 콜백(매번, 글이 올때마다):
    #   받은 숫자 꺼내서 2배
    #   보낼 봉투 만들기 -> 숫자 넣기 -> 보내기 <- 새로
    #   로그 "받음 : 3 -> 보냄: 6"
    def double_callback(self, msg): # 매번 글이 올 때마다
        rec_number = msg.data # 받은 숫자
        doub_number = rec_number * 2 # 받은 숫자 * 2

        out_msg = Int32() # 빈 봉투 만들기
        out_msg.data = doub_number # 봉투의 숫자 칸에 넣기
        self.publisher_.publish(out_msg) # 보내기 -> 어디로? /doubled로 -> spin이 글왔다고 전달 -> 봉투를(msg)에 넣어서 -> /doubled 구독자들에게 배달
        self.get_logger().info(f"받음: {rec_number}, 보냄: {doub_number}")


def main(args=None):
    rclpy.init(args=args)
    doubler = Doubler()
    try:
        rclpy.spin(doubler) # 글이 옴
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        doubler.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
        

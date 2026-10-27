import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher_ = self.create_publisher(String,"/greeting",10) # 10은 큐 깊이(버퍼), 메시지가 아직 전달되지 못했을 때 최대 몇 개까지 쌓아 둘 지 정함. 넘치면 오래된 것부터 버림
        self.timer = self.create_timer(1.0, self.talker_callback)

    def talker_callback(self): # 타이머 콜백에는 받는 글이 없음, self = Talker 클래스로 만든 객체(Talker 인스턴스)
        msg = String()
        msg.data = "안녕"
        self.publisher_.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    talker = Talker() # 인스턴스 생성
    try:
        rclpy.spin(talker)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        talker.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
    
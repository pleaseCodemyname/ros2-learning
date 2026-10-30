import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher_=self.create_publisher(String, '/chat',10) # ros2 interface list | grep String, 인터페이스 리스트 중 String을 포함한 인터페이스 찾기, self.create_publisher(인터페이스명, 토픽명, 버퍼=큐 사이즈)
        self.timer = self.create_timer(1.0, self.talker_callback) # 1초마다 talker_callback을 불러 달라고 등록 (부르는 건 spin)
        self.count = 0 # 최초 생성을 한 후에 넘겨줘야 +1 씩 증가, __init__은 한 번만 실행되니까 0으로 딱 한 번 시작. self.에 저장해서 콜백이 끝나도 값이 남음

    def talker_callback(self):
        # self.count = 0 # 여기에 있으면 계속 "보냄: 안녕 0" 으로 찍힘, 콜백은 1초마다 처음부터 실행됨. self.count = 0 -> 0으로 되돌림 | 안녕 0 보냄 | slef.count += 1 -> 1이 됨 | 1초 뒤 콜백이 다시 처음부터 -> 또 0으로 되돌림
        msg = String() # 빈 String 메시지 객체를 새로 생성
        msg.data = f"안녕 {self.count}" # 객체(String)의 data칸에 보낼 글자 넣음
        self.get_logger().info(f"보냄: {msg.data}")
        self.publisher_.publish(msg) # publish에는 String 객체를 통째로 넘김
        self.count +=1 # self.count = self.count + 1 | 1초마다 실행. self.가 없는 그냥 count면 콜백이 끝날 때 사라짐. self.count는 노드에 저장돼 있어서 다음 콜백(1초 뒤)에서도 남아있음

def main(args=None):
    rclpy.init(args=args) # ros 연결
    talker = Talker() # Talker()인스턴스 생성, 이때 __init__(생성자 함수)가 한 번 실행되어 publisher, timer가 만들어짐, 생성자 함수만 실행
    # for t in talker.timers:
        # print('저장된 콜백:', t.callback)
    try:
        rclpy.spin(talker) # talker를 계속 반복하며 확인, talker에 등록된 타이머를 보며 기다리다가, 때가되면 콜백을 불러줌, Ctrl+C 전까지 안 끝남, 
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        talker.destroy_node() # 노드 종료
        rclpy.try_shutdown() # ros 종료

if __name__ == "__main__": # 여기서부터 시작된다고 보면 됨
    main()



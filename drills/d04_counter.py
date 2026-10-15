import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import Int32

class Counter(Node): # 클래스(Node)상속받은 객체 설계도
    def __init__(self): # 생성자 함수
        super().__init__('counter') # rclpy.node를 물려받아 Node 이름을 'counter로' 지정
        self.publisher_ = self.create_publisher(Int32, '/number', 10) # Publisher 생성(노드의 기능 중 create_publisher(메시지형식, 토픽명, 버퍼(저장소))
        self.timer = self.create_timer(1.0, self.counter_callback) # 알람을 맞춰둠. "1초마다 이 함수를 불러달라" 등록만하고, 실제로 부르는 건 나중에 spin이 함
        self.count = 0 # Counter 인스턴스 초기값 = 0

    # 콜백이 필요한 이유: 언제 생길지 모르는 일에 반응하기 위함.
    # Subriber 콜백 (self, msg): spin이 받은 글을 넣어줌
    # 타이머 콜백(self): 콜백 안에서 Int32()로 직접 만듬
    def counter_callback(self): # 인자에 msg가 없는 이유: 이 콜백을 부르는게 타이머이기 때문에. 타이머는 받은 글이 없으니 줄 msg가 없음. 
        msg = Int32()
        msg.data = self.count # 지금 값을 가져오는 방법
        self.publisher_.publish(msg) # msg를 /number 게시판에 올림, 그 게시판을 구독하는 노드가 있으면 그쪽 spin이 받아서 그쪽 콜백을 부름. 구독하는 노드가 없어도 에러는 나지 않음. 올리기만 하고 끝임
        self.get_logger().info(f"보냄: {msg.data}") 
        self.count += 1   
        

def main(args=None):
    rclpy.init(args=args) # ROS 실행
    counter = Counter() #Counter 호출
    try:
        rclpy.spin(counter) # callback 연결, 콜백을 부르는 쪽
    except(KeyboardInterrupt, ExternalShutdownException): # Ctrl+C나, 갑작스럽게 꺼지는 경우에는
        pass # 생략
    finally: # 마지막으로
        counter.destroy_node() # 노드 종료
        rclpy.try_shutdown() # ROS 종료

if __name__ == "__main__": # 이름이 main이면
    main() # main 함수 호출

import rclpy
from rclpy.executors import ExternalShutdownException
from turtlesim.msg import Pose
from rclpy.node import Node

class HalfTurtleSubscriber(Node): # HalfTurtleSubscriber 클래스 생성 (Node 상속)
    def __init__(self): # __init__은 클래스 안의 생성자. 만들어질 때 한 번 실행됨
        super().__init__('half_turtle') # 부모인 Node의 생성자를 부르면서 이름을 넘김
        self.subscription = self.create_subscription( # Subscriber를 생성함 (Node의 기능 중 하나)
            Pose, # 양식은 Pose이며
            'turtle1/pose', # 게시판은 turtle1/pose에서 읽을 것
            self.pose_callback, # 콜백 함수를 호출이 아닌 등록 (호출이면 괄호가 있어야함), "글이 오면 이 함수를 불러달라"
            10) # 대기 줄 길이. 처리가 밀릴 때 글을 최대 10개까지 쌓아 둠.
        self.get_logger().info('Half Turtle Node has been started.') # 해당 문구를 log 찍을꺼임

    def pose_callback(self, msg): # pose_callback 함수 생성
        half_right = msg.x > 5.54
        if half_right:
            self.get_logger().info("Facing half_right", throttle_duration_sec=1.0)
        else:
            self.get_logger().info("Facing half_left", throttle_duration_sec=1.0)
        # 1초에 한 번씩 해당 로그를 찍을꺼임, 콜백 자체는 1초에 약 60번 돌고, 로그만 1초에 한 번
    

def main(args=None): # main 함수에 args 하나가 있고, 안주면 None이 기본값
    rclpy.init(args=args) # ROS 설정을 한다
    half_turtle_subscriber = HalfTurtleSubscriber() # HalfTurtleSubscriber Class를 호출한다.
    try:
        rclpy.spin(half_turtle_subscriber) # half_turtle_subscriber의 알림을 받을 수 있게 켜고 기다린다.
    except (KeyboardInterrupt, ExternalShutdownException): # 키보드 개입이나 갑자기 꺼지는 경우에는
        pass # pass한다.
    finally:
        half_turtle_subscriber.destroy_node() # half_turtle_subcriber 노드를 종료하다.
        rclpy.try_shutdown() # ROS도 종료한다.

if __name__ == '__main__': # __name__이 main이라면?
    main() # main함수를 실행한다.
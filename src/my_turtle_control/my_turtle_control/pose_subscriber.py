import rclpy
from rclpy.executors import ExternalShutdownException
from turtlesim.msg import Pose # Pose "나 지금 여기있다"라는 메시지 형식, turtlesim 패키지 안에 있음
from rclpy.node import Node

class PoseSubscriber(Node): # Node의 기능을 상속받아 PoseSubscriber라는 클래스를 정의
    def __init__(self): # slef: 지금 다루고 있는 이 객체 자신, 클래스는 설계도이며, 객체는 그것으로 찍어낸 실물임. 설계도에 적힌 함수는 "어느 실물에 대해 일하는지"를 알아야 함. 그 실물을 넘겨받는 지리가 self임.
        super().__init__('pose_subscriber') # 부모의 __init__()를 호출하여 노드 이름을 pose_subscriber로 설정
        self.subscription = self.create_subscription(
            Pose, # Pose: 로봇이 알려주는 상태 메시지 형식
            'turtle1/pose',
            self.pose_callback,
            10)
        self.get_logger().info('Pose Subscriber Node has been started.')

    def pose_callback(self, msg):
        self.get_logger().info('Received Pose: x=%.2f, y=%.2f, theta=%.2f' % (msg.x, msg.y, msg.theta), throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args) # ROS와 연결
    pose_subscriber = PoseSubscriber() # 노드 객체 생성 -> __init__() 실행
    try:
        rclpy.spin(pose_subscriber) # 여기서 멈춰서 계속 기다림, 메시지를 계속 체크, 메시지가 도착하면 spin이 보관해 둔 함수를 꺼내 괄호를 붙여 실행.
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        pose_subscriber.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
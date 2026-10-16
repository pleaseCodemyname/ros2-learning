# Q1 내보내는게 있나? (Pub): 속도
# Q2 알아야 할게 있나? (Sub): 위치
# Q3 받는 것 없이 반복할 일이 있나? (타이머): 없음

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class Stopper(Node):
    def __init__(self):
        super().__init__('stopper')
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.stop_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info("Stopper 노드 생성 완료")

    def stop_callback(self, msg):
        location = msg.x
        cmd = Twist()
        if location > 9: # 오른쪽 벽에 붙으면
            cmd.linear.x = 0.0 # 속도를 줄인다
            self.get_logger().info("오른쪽에 붙었다", throttle_duration_sec = 1.0) # Pose는 1초에 약 60번 오니, throttle 쓰는게 맞음
        else:
            cmd.linear.x = 1.0  # 아니면 속도를 계속 이어간다
            self.get_logger().info("오른쪽에 안붙었다", throttle_duration_sec = 1.0)
        self.publisher_.publish(cmd)
        


def main(args=None):
    rclpy.init(args=args)
    stopper = Stopper()
    try:
        rclpy.spin(stopper)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        stopper.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
        
        

        

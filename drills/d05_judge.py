# Q1 내보내는게 있나? (Pub): 없음
# Q2 알아야 할게 있나? (Sub): /number에서 받은 값
# Q3 받는 것 없이 반복할 일이 있나? (타이머): 없음

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import Int32

class Judge(Node):
    def __init__(self):
        super().__init__('judge')
        self.subscription = self.create_subscription(Int32, '/number', self.number_callback, 10)

    def number_callback(self, msg):
        number = msg.data        
        if number % 2 == 0:
            self.get_logger().info(f"{number}는 짝수")
        else:
            self.get_logger().info(f"{number}는 홀수")

def main(args=None):
    rclpy.init(args=args)
    judge = Judge()
    try:
        rclpy.spin(judge)
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        judge.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
        

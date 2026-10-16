# Q1 내보내는게 있나? (Pub): 속도 → /turtle1/cmd_vel (Twist)
# Q2 알아야 할게 있나? 위치 → /turtle1/pose (turtlesim Pose)
# Q3 받는 것 없이 반복할 일이 있나? (타이머): 없음

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class Arrive(Node):
    def __init__(self):
        super().__init__('arrive')
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.arrive_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('arrive 노드 생성 완료')
        self.logged_count = 0

    def arrive_callback(self, msg):
        location = msg.x
        right_wall = location > 9
        cmd = Twist()
        if right_wall:
            cmd.linear.x = 0.0
            if self.logged_count == 0:
                self.get_logger().info('도착')
                self.logged_count +=1
        else:
            cmd.linear.x = 1.0
            self.get_logger().info("아직 가는중", throttle_duration_sec=1.0)
        self.publisher_.publish(cmd)
        


def main(args=None):
    rclpy.init(args=args)
    arrive = Arrive()
    try:
        rclpy.spin(arrive)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        arrive.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()

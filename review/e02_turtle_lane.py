# Pub: 위치 정보를 받고 속도/회전을 발행해야하니깐, 토픽: /turtle1/cmd_vel, 인터페이스: geometry_msgs/msg/Twist
# Sub: 위치 정보를 알아야 하니깐, 토픽: /turtle1/pose, 인터페이스: turtlesim/msg/Pose
# 값은 내가 가늠이 안가서 그냥 넣었음

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class Lane(Node):
    def __init__(self):
        super().__init__('lane')
        self.subscription = self.create_subscription(Pose, "/turtle1/pose", self.lane_callback, 10)
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

    def lane_callback(self, msg):
        cmd = Twist()
        if msg.y > 7:
            cmd.linear.x = 1.0
            cmd.angular.z = -0.5
            self.get_logger().info(f"{msg.y}는 7을 넘어서 전진속도 1.0, 회전은 시계(오른쪽)로 -0.5 꺾음", throttle_duration_sec=1.0)
        elif msg.y < 3:
            cmd.linear.x = 1.0
            cmd.angular.z = 0.5
            self.get_logger().info(f"{msg.y}는 3 미만이여서 전진속도 1.0, 회전은 반시계(왼쪽)로 0.5 꺾음", throttle_duration_sec=1.0)
        else:
            cmd.linear.x = 1.0
            self.get_logger().info(f"그냥 계속 직진", throttle_duration_sec=1.0)
        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    lane = Lane()
    try:
        rclpy.spin(lane)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        lane.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
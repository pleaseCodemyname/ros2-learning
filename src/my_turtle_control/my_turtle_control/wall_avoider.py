import rclpy
import math
from rclpy.executors import ExternalShutdownException
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from rclpy.node import Node

class WallAvoider(Node):
    def __init__(self):
        super().__init__('wall_avoider') # Node의 준비를 하고 이름을 'wall_avoider'로 설정
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10) # pub: 양식, 게시판, 값 (게시판에 올림), 만든다
        self.subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.pose_callback,
            10) # sub: 양식, 게시판, 콜백함수, 값 (게시판에서 읽음)
        self.get_logger().info('Wall Avoider Node has been started.')

    def pose_callback(self, msg):
        cmd = Twist()
        facing_right = msg.x > 9.5 and math.cos(msg.theta) > 0 # math.cos(msg.theta) > 0: 오른쪽을 보고 있는가
        facing_left = msg.x < 1.5 and math.cos(msg.theta) < 0 # math_cos(msg.theta) < 0: 왼쪽을 보고 있는가
        facing_top = msg.y > 9.5 and math.sin(msg.theta) > 0
        facing_bottom = msg.y < 1.5 and math.sin(msg.theta) < 0
        if facing_right or facing_left or facing_top or facing_bottom:
            cmd.linear.x = 0.5  # Move forward slowly
            cmd.angular.z = 2.0   # Turn left
            self.get_logger().info('Facing wall! Turning away.', throttle_duration_sec=1.0)
        else:
            cmd.linear.x = 1.0   # Move forward
            cmd.angular.z = 0.0   # No turn
            self.get_logger().info('Moving forward.', throttle_duration_sec=1.0)

        self.publisher_.publish(cmd) # 쓴다


def main(args=None):
    rclpy.init(args=args) # ROS를 켠다 (명령 줄 옵션을 넘김)
    wall_avoider = WallAvoider() # Node 객체 생성 -> __init__() 실행
    try:
        rclpy.spin(wall_avoider)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        wall_avoider.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
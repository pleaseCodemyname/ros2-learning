import rclpy
import math
from rclpy.executors import ExternalShutdownException
from tf2_ros import Buffer, TransformListener, TransformException
from rclpy.time import Time
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleFollower(Node):
    def __init__(self):
        super().__init__('turtle_follower')
        self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 10) # 움직일 대상이 turtle2이기 때문에
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(0.1, self.timer_callback) # 초당 10번 호출

    def timer_callback(self):
        try:
            t = self.tf_buffer.lookup_transform('turtle2', 'turtle1', Time())
        except TransformException as ex:
            self.get_logger().info(f'tf 기다리는중: {ex}', throttle_duration_sec=1.0)
            return

        x = t.transform.translation.x
        y = t.transform.translation.y
        cmd = Twist()
        cmd.linear.x = 0.5 * math.hypot(x, y) # 0.5 * 1.0 *: 얼마나 민감하게 반응할지 정하는 배율. 
        cmd.angular.z = 1.0 * math.atan2(y, x) # 거리와 각도에 비례해서 속도를 정하므로, 가까워 질수록 천천히 움직이다가 멈춤
        self.publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    turtle_follower = TurtleFollower()
    try:
        rclpy.spin(turtle_follower)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        turtle_follower.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
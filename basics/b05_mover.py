import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class Mover(Node):
    def __init__(self):
        super().__init__('mover')
        self.subscription = self.create_subscription(Pose, "/turtle1/pose", self.mover_callback, 10)
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

    def mover_callback(self, msg):
        cmd = Twist()
        x = msg.x
        if x < 8.0:
            cmd.linear.x = 1.0
        else:
            cmd.linear.x = 0.0
        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    mover = Mover()
    try:
        rclpy.spin(mover)
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        mover.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
            


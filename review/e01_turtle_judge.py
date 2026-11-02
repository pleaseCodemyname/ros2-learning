import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class Judge(Node):
    def __init__(self):
        super().__init__('judge')
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.judge_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
    
    def judge_callback(self, msg):
        cmd = Twist()
        if msg.x > 9.0:
            self.publisher_.publish(cmd)
            return 
        elif msg.y > 9.0:
            self.publisher_.publish(cmd)
            return
        else:
            cmd.linear.x = 1.0
            self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    judge = Judge()
    try:
        rclpy.spin(judge)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        judge.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
            

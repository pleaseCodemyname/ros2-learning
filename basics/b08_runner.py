import rclpy 
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class Runner(Node):
    def __init__(self):
        super().__init__('runner')
        self.cli = self.create_client(Spawn, "/spawn")
        self.cli.wait_for_service()
        self.subscription = self.create_subscription(Pose, "/runner/pose", self.runner_callback, 10)
        self.publisher_ = self.create_publisher(Twist, "/runner/cmd_vel",10)

    def runner_callback(self, msg):
        cmd = Twist()
        if msg.x < 8.0:
            cmd.linear.x = 1.5
        else:
            cmd.linear.x = 0.0
        self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    runner = Runner()
    req = Spawn.Request(x=1.0, y=5.0, theta=0.0, name="runner")
    future = runner.cli.call_async(req)
    try:
        rclpy.spin_until_future_complete(runner,future)
        name = future.result().name
        if name == '':
            runner.get_logger().error(f"에러입니다.")

        else:
            runner.get_logger().info(f"성공: {name}")
            rclpy.spin(runner)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        runner.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
        
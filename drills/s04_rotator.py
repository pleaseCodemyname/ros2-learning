import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.action import ActionClient
from turtlesim.action import RotateAbsolute

class Rotator(Node):
    def __init__(self):
        super().__init__('rotator')
        self.cli = ActionClient(self, RotateAbsolute, '/turtle1/rotate_absolute')
        self.cli.wait_for_server()

    def feedback_callback(self, feedback_msg):
        msg = feedback_msg.feedback.remaining
        self.get_logger().info(f"remaining: {msg}")

def main(args=None):
    rclpy.init(args=args)
    rotator = Rotator()
    try:
        req = RotateAbsolute.Goal(theta=1.57)
        future = rotator.cli.send_goal_async(req, feedback_callback=rotator.feedback_callback)
        rclpy.spin_until_future_complete(rotator, future) # future가 끝날 때까지 spin
        goal_handle = future.result()
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(rotator, result_future)
        output = result_future.result()
        rotator.get_logger().info(f"delta: {output.result.delta}, status: {output.status}")
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        rotator.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()

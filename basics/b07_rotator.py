import rclpy 
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.action import ActionClient
from turtlesim.action import RotateAbsolute

class Rotator(Node):
    def __init__(self):
        super().__init__('rotator')
        self.cli = ActionClient(self, RotateAbsolute, "/turtle1/rotate_absolute")
        self.cli.wait_for_server()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f"remaining: {feedback_msg.feedback.remaining}")



def main(args=None):
    rclpy.init(args=args)
    rotator = Rotator()
    goal = RotateAbsolute.Goal(theta = 1.57)
    future = rotator.cli.send_goal_async(goal,feedback_callback=rotator.feedback_callback )
    try:
        rclpy.spin_until_future_complete(rotator, future)
        goal_handle = future.result()
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(rotator, result_future)
        output = result_future.result()
        rotator.get_logger().info(f"output status: {output.status}, output.result.delta: {output.result.delta}")
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        rotator.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from nav2_msgs.action import NavigateToPose

class NavClient(Node):
    def __init__(self):
        super().__init__('nav_client')
        self.cli = ActionClient(self, NavigateToPose, '/navigate_to_pose') # 액션 이름 ros2 action list -t
        self.cli.wait_for_server()   

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f"distance_remaining: {feedback_msg.feedback.distance_remaining:.2f}, number_of_recoveries: {feedback_msg.feedback.number_of_recoveries}", throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args)
    nav_client = NavClient() 
    try:
        goal = NavigateToPose.Goal() # action 하나에는 Goal, Result, Feedback이 있는데, 지금 여기서 보낼 건 Goal
        goal.pose.header.frame_id = "map"
        goal.pose.pose.position.x = 0.0
        goal.pose.pose.position.y = -0.9
        future = nav_client.cli.send_goal_async(goal, feedback_callback=nav_client.feedback_callback)
        rclpy.spin_until_future_complete(nav_client, future)
        goal_handle = future.result()
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(nav_client, result_future)
        output = result_future.result()
        nav_client.get_logger().info(f"status: {output.status}")
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        nav_client.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
    

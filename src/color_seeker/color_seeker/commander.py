import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.action import ActionClient
from color_seeker_interfaces.action import GoToColor

class Commander(Node):
    def __init__(self):
        super().__init__('commander')
        self.cli = ActionClient(self, GoToColor, "go_to_color")
        self.cli.wait_for_server()

    def feedback_callback(self, feedback_msg):
        msg = feedback_msg.feedback.pixel_count
        self.get_logger().info(f"칸 수: {msg}")


def main(args=None):
    rclpy.init(args=args)
    commander = Commander()
    try:
        while True:
            command = input("명령: ")
            commander.get_logger().info(f"{command}")
            if "파란" in command or "파랑" in command:
                color = "blue"
            elif "빨간" in command or "빨강" in command:
                color = "red"
            elif "초록" in command:
                color = "green"
            else:
                color = "unknown"
            commander.get_logger().info(f"{color}")
            goal = GoToColor.Goal(color=color) # Goal 객체 만들기
            send_goal_future = commander.cli.send_goal_async(goal, feedback_callback=commander.feedback_callback) # send_goal_async가 goal 객체를 서버로 보냄, 결과는 future, feedback_callbakc에는 클래스에 만든 메서드를 괄호 없이 넘김
            rclpy.spin_until_future_complete(commander,send_goal_future) # 접수 기다리기
            goal_handle = send_goal_future.result() 
            get_result_future = goal_handle.get_result_async() # 결과 요청
            rclpy.spin_until_future_complete(commander, get_result_future) # 결과 기다리기
            response = get_result_future.result() # 결과 객체 꺼내기
            commander.get_logger().info(f"{response.status}, {response.result.success}")
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        commander.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
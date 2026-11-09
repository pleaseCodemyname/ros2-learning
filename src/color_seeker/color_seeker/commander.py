import rclpy
import requests
import json
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

def choose_color(command):
    body = {
            "model": "llama3.1:8b",
            "prompt": f"Classify the color in the Korean sentence. Answer with exactly one word: red, blue, green, or unknown.\nExamples:\n빨간 컵으로 가 -> red\n하늘색 공 찾아 -> blue\n풀색 상자 -> green\n노란 거 -> unknown\nSentence: {command}",
            "stream": False,
            "options": {"temperature": 0},
            "format": {
                "type": "object",
                "properties": {"color": {"type": "string", "enum": ["red", "blue", "green", "unknown"]}},
                "required": ["color"]
                        }
            }
    http_response = requests.post("http://localhost:11434/api/generate", json=body, timeout=30) # body(딕셔너리)를 JSON(문자열)로 바꿔 Ollama에 POST로 보내고, 답이 올 때까지(최대 30초) 기다려서 HTTP 응답을 받음
    answer_text = http_response.json()["response"] # http_response.json()으로 그 body(json)를 딕셔너리로 바꾼 후, 그 중 "response"칸만 꺼낸거. 그런데 아직 문자열임 '{ "color": "blue" }
    color = json.loads(answer_text)["color"] # 그 문자열을 딕셔너리 {"color": "blue"}로 바꾸고(loads), ["color"]로 "blue"를 꺼낸 것
    return color 


def main(args=None):
    rclpy.init(args=args)
    commander = Commander()
    try:
        while True:
            command = input("명령: ")
            commander.get_logger().info(f"{command}")
            color = choose_color(command)
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
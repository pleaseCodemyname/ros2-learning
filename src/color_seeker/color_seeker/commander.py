import rclpy
import requests
import json
import threading
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.action import ActionClient
from color_seeker_interfaces.action import GoToColor

class Commander(Node):
    def __init__(self):
        super().__init__('commander')
        self.cli = ActionClient(self, GoToColor, "go_to_color")
        self.cli.wait_for_server()
        self.goal_handle = None
        self.result_future = None

    # 메서드: 클래스 안의 함수
    def feedback_callback(self, feedback_msg):
        msg = feedback_msg.feedback.pixel_count
        self.get_logger().info(f"칸 수: {msg}")

    def goal_response_callback(self, future):
        self.goal_handle = future.result()
        self.result_future = self.goal_handle.get_result_async()
        self.result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        if future is self.result_future:
            self.goal_handle = None # goal이 끝났으니 None으로 → 진행 중인 goal 없음
        response = future.result()
        self.get_logger().info(f"{response.status}, {response.result.success}")

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
                        },
            "keep_alive": "30m",
            }
    try:
        http_response = requests.post("http://localhost:11434/api/generate", json=body, timeout=30) # body(딕셔너리)를 JSON(문자열)로 바꿔 Ollama에 POST로 보내고, 답이 올 때까지(최대 30초) 기다려서 HTTP 응답을 받음
        data = http_response.json() # http_response.json()으로 그 body(json)를 딕셔너리로 바꿈
        answer_text = data["response"] # data에서 response칸을 꺼냄, 그런데 아직 문자열임 '{ "color": "blue" }, 
        # print(f'토큰: {data["eval_count"]}, 시간: {data["eval_duration"]/1e9}, 답: {answer_text!r}')
        color = json.loads(answer_text)["color"] # 그 문자열을 딕셔너리 {"color": "blue"}로 바꾸고(loads), ["color"]로 "blue"를 꺼낸 것
        return color 
    except requests.exceptions.RequestException: # RequestException은 requests 에러들의 부모클래스. 그래서 ConnectionError(꺼짐)뿐 아니라 Timeout(30초 초과)도 같이 잡힘
        return None # None = 답이 없다고 돌려주는 값. unknown은 "LLM이 보고 모르겠다고 함"이고, None은 "LLM에 물어보지도 못함"임

def main(args=None):
    rclpy.init(args=args)
    commander = Commander()
    threading.Thread(target=rclpy.spin, args=(commander,), daemon=True).start() # target에는 실행할 함수를 괄호없이 넘김. args는 그 함수에 넘길 인자(튜플이라 쉼표 필요). daemon=True는 메인이 끝나면 이 스레드도 같이 끝나게 해줌
    commander.get_logger().info("LLM 준비 중...")
    warmup = choose_color("빨간 거")
    if warmup is None:
        commander.get_logger().warn("LLM 연결 실패, 명령할 때 다시시도")
    else:
        commander.get_logger().info("LLM 준비 완료")
    try:
        while True:
            command = input("명령: ")
            if command == "멈춰":
                if commander.goal_handle is None:
                    commander.get_logger().warn("진행 중인 goal 없음")
                else:
                    commander.goal_handle.cancel_goal_async()
                    commander.get_logger().info("취소 요청")
                continue
            commander.get_logger().info(f"{command}")
            color = choose_color(command)
            if color is None:
                commander.get_logger().error("LLM 연결 실패")
                continue
            commander.get_logger().info(f"{color}")
            goal = GoToColor.Goal(color=color) # Goal 객체 만들기
            if commander.goal_handle is not None:        
                commander.goal_handle.cancel_goal_async()
                commander.get_logger().info("취소 요청")
            send_goal_future = commander.cli.send_goal_async(goal, feedback_callback=commander.feedback_callback) # send_goal_async가 goal 객체를 서버로 보냄, 결과는 future, feedback_callbakc에는 클래스에 만든 메서드를 괄호 없이 넘김
            send_goal_future.add_done_callback(commander.goal_response_callback)
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        commander.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
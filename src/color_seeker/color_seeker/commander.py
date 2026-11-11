import rclpy
import requests
import json
import threading
import time
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException, SingleThreadedExecutor
from rclpy.action import ActionClient
from rclpy.signals import SignalHandlerOptions
from color_seeker_interfaces.action import GoToColor

class Commander(Node):
    def __init__(self):
        super().__init__('commander')
        self.cli = ActionClient(self, GoToColor, "go_to_color")
        self.cli.wait_for_server()
        self.goal_handle = None
        self.result_future = None
        self.queue = []

    # 메서드: 클래스 안의 함수
    def feedback_callback(self, feedback_msg):
        msg = feedback_msg.feedback.pixel_count
        self.get_logger().info(f"칸 수: {msg}")

    def goal_response_callback(self, future):
        self.goal_handle = future.result()
        self.result_future = self.goal_handle.get_result_async()
        self.result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        response = future.result()
        if future is self.result_future:
            self.goal_handle = None # goal이 끝났으니 None으로 → 진행 중인 goal 없음
            if response.result.success:
                if self.queue:
                    next_color = self.queue.pop(0)
                    self.send_color(next_color)
        self.get_logger().info(f"{response.status}, {response.result.success}")

    def send_color(self,color):
        goal = GoToColor.Goal(color=color) # Goal 객체 만들기
        if self.goal_handle is not None:        
            self.goal_handle.cancel_goal_async()
            self.get_logger().info("취소 요청")
        send_goal_future = self.cli.send_goal_async(goal, feedback_callback=self.feedback_callback) # send_goal_async가 goal 객체를 서버로 보냄, 결과는 future, feedback_callbakc에는 클래스에 만든 메서드를 괄호 없이 넘김
        send_goal_future.add_done_callback(self.goal_response_callback)

def choose_color(command):
    # 괄호 안에 문자열을 나란히 쓰면 하나로 이어 붙음(줄 사이에 쉼표 없음). 줄바꿈은 각 줄 끝의 \n
    prompt = (
        "You control a robot that drives to a colored box. Read the Korean command and decide what the robot should do.\n"
        "- Answer the colors the robot should go to: red, blue, or green.\n"
        "- If the command says NOT to go to a color (말고, 아니라, 가지 마), leave that color out of the list completely. The list has only colors the robot should actually visit.\n"
        "- If the command means stop or wait (멈춰, 그만, 서, 기다려, 대기), answer stop.\n"
        "- Only red, blue, and green boxes exist. Any other color (yellow, purple, orange, black, white, ...) -> unknown.\n"
        "- If the command is not about going to a color at all, answer unknown. Do not guess a color.\n"
        "Answer a list of colors in the order the robot should visit them. Each item is one of: red, blue, green, unknown, or stop.\n"
        "Examples:\n"
        "빨간 컵으로 가 -> ['red']\n"
        "하늘색 공 찾아 -> ['blue']\n"
        "풀색 상자 -> ['green']\n"
        "노란 거 -> ['unknown']\n"
        "주황색 공으로 가 -> ['unknown']\n"
        "뭐 하고 있어? -> ['unknown']\n"
        "파란 거 말고 초록 상자로 -> ['green']\n"
        "빨강 아니라 하늘색 -> ['blue']\n"
        "그만 -> ['stop']\n"
        "잠시 대기 -> ['stop']\n"
        "빨간거 갔다가 초록으로 -> ['red', 'green']\n"
        f"Sentence: {command}"
    )
    body = {
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
            "format": {
                "type": "object",
                "properties": {"colors": {"type": "array", "items": {"type": "string", "enum": ["red", "blue", "green", "unknown", "stop"]}}},
                "required": ["colors"]
                        },
            "keep_alive": "30m",
            }
    try:
        http_response = requests.post("http://localhost:11434/api/generate", json=body, timeout=30) # body(딕셔너리)를 JSON(문자열)로 바꿔 Ollama에 POST로 보내고, 답이 올 때까지(최대 30초) 기다려서 HTTP 응답을 받음
        data = http_response.json() # http_response.json()으로 그 body(json)를 딕셔너리로 바꿈
        answer_text = data["response"] # data에서 response칸을 꺼냄, 그런데 아직 문자열임 '{ "color": "blue" }, 
        # print(f'토큰: {data["eval_count"]}, 시간: {data["eval_duration"]/1e9}, 답: {answer_text!r}')
        colors = json.loads(answer_text)["colors"] # 그 문자열을 딕셔너리 {"colors": ["blue"]}로 바꾸고(loads), ["colors"]로 ["blue"]를 꺼낸 것
        return colors
    except requests.exceptions.RequestException: # RequestException은 requests 에러들의 부모클래스. 그래서 ConnectionError(꺼짐)뿐 아니라 Timeout(30초 초과)도 같이 잡힘
        return None # None = 답이 없다고 돌려주는 값. unknown은 "LLM이 보고 모르겠다고 함"이고, None은 "LLM에 물어보지도 못함"임

# 정지는 안전 기능이라 LLM보다 먼저, 단어가 들어 있기만 하면 stop(Ollama가 꺼져 있어도 동작)
# "잠깐 멈춰봐", "잠깐 서봐"를 LLM이 blue로 읽은 적이 있음. 다른 뜻의 문장도 stop으로 잡힐 수 있지만, 멈추는 쪽으로 틀리는 게 안전함
STOP_WORDS = ["멈춰", "그만", "정지", "스톱", "서봐", "서 봐"]

def interpret(command):
    # 문장 → ["red"]/["blue"]/["green"]/["unknown"]/["stop"], LLM에 못 물어보면 None
    # main과 tools/eval_commands.py가 같이 쓴다(테스트하는 것과 로봇이 쓰는 것이 같아야 해서)
    if any(word in command for word in STOP_WORDS):
        return ['stop']
    return choose_color(command)

def main(args=None):
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    commander = Commander()
    executor = SingleThreadedExecutor()
    executor.add_node(commander)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start() 
    commander.get_logger().info("LLM 준비 중...")
    warmup = choose_color("빨간 거")
    if warmup is None:
        commander.get_logger().warn("LLM 연결 실패, 명령할 때 다시시도")
    else:
        commander.get_logger().info("LLM 준비 완료")
    try:
        while True:
            command = input("명령: ")
            commander.get_logger().info(f"{command}")
            colors = interpret(command) # 정지 단어면 LLM 없이 바로 ['stop'], 아니면 LLM
            if colors is None:
                commander.get_logger().error("LLM 연결 실패")
                continue
            commander.get_logger().info(f"{colors}")
            if "stop" in colors:
                if commander.goal_handle is None:
                    commander.get_logger().warn("진행 중인 goal 없음")
                else:
                    commander.goal_handle.cancel_goal_async()
                    commander.get_logger().info("취소 요청")
                commander.queue = []
                continue
            if "unknown" in colors: # 알아듣지 못한 말 때문에 하던 goal을 취소하지 않도록, goal을 보내지 않고 넘어감
                commander.get_logger().warn("알 수 없는 명령, 하던 일 계속")
                continue
            commander.queue = colors[1:]
            commander.send_color(colors[0])
    except(KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        if commander.goal_handle is not None:
            cancel_future = commander.goal_handle.cancel_goal_async()
            start_time = time.time()
            while not cancel_future.done() and time.time() - start_time < 1.0: # time.time() = 지금 잰 시간, start_time = while 전에 잰 시간
                time.sleep(0.05)
            if cancel_future.done():
                commander.get_logger().info("종료: goal 취소 응답 받음")
            else:
                commander.get_logger().warn("종료: 1초 동안 취소 응답 없음")
        commander.queue = []
        executor.shutdown() # spin 루프를 멈추라고 알림
        spin_thread.join(timeout=1.0) # 그 스레드가 실제로 끝날 때까지 최대 1초 기다림
        commander.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
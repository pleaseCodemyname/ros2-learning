# Pub(무엇을 내보내나?): 속도/회전 명령, 인터페이스: geometry_msgs/msg/Twist, 토픽: /cmd_vel
# Sub(무엇을 알아야 하나?): 로봇 카메라 사진, 인터페이스: sensor_msgs/msg/Image, 토픽: /camera/image
# 타이머(받는 것 없이 반복할 일이 있나?): 없음, 사진이 올 때마다(약 29번/초) 콜백에서 판단하면 됨

import rclpy
import numpy as np
import cv2
import time
import math
import torch
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from rclpy.action import ActionServer, CancelResponse
from color_seeker_interfaces.action import GoToColor
from nav_msgs.msg import Odometry
from transformers import Owlv2Processor, Owlv2ForObjectDetection
from rcl_interfaces.msg import ParameterDescriptor

class ColorSeeker(Node):
    def __init__(self):
        super().__init__('color_seeker')
        self.subscription = self.create_subscription(Image, '/camera/image',self.color_seeker_callback, 1, callback_group=MutuallyExclusiveCallbackGroup())
        self.odom_subscription = self.create_subscription(Odometry, "/model/stt_bot/odometry", self.odom_callback, 10, callback_group=MutuallyExclusiveCallbackGroup())
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()
        self.action_server = ActionServer(self, GoToColor, "go_to_color", self.execute_callback, callback_group=ReentrantCallbackGroup(), cancel_callback=self.cancel_callback)
        self.declare_parameter("stop_count", 49000)
        self.declare_parameter("turn_speed", 0.3)
        self.declare_parameter("forward_speed", 0.2)
        self.declare_parameter("detector", "color", ParameterDescriptor(read_only=True)) # param set 거절됨
        self.target_color = None
        self.pixel_count = 0
        self.arrived = False
        self.current_goal = None
        self.yaw = 0.0
        self.color_ranges = {"blue": (np.array([60, 0, 0]), np.array([255, 50, 50])), "green": (np.array([0, 60, 0]), np.array([50, 255, 50])), "red": (np.array([0, 0, 60]), np.array([50, 50, 255]),)}
        self.seen_yaw = {}
        self.target_yaw = None # 0개 갈래와 멈춤 갈래: 각각 publish 전에 self.target_yaw = None 추가 b/c odometry가 예전 방향으로 계속 조종하지 않게 | cx 갈래: 1단계의 지역 변수 target_yaw를 self.target_yaw에 저장. 그 아래 cx로 왼쪽/오른쪽/직진을 정하고 publish하던 부분은 지움. 이제 그 일은 odometry 콜백이 함
        self.detector = self.get_parameter("detector").value
        if self.detector == "owlv2":
            start = time.perf_counter()
            name = "google/owlv2-base-patch16-ensemble"
            self.processor = Owlv2Processor.from_pretrained(name)
            self.model = Owlv2ForObjectDetection.from_pretrained(name).to("cuda")
            image = np.zeros((240, 320, 3), np.uint8) # frame.shape와 같은 순서(세로, 가로, 3)
            inputs = self.processor(text=[["red box"]], images=image, return_tensors="pt").to("cuda") # __init__ 에서만 사용하고 버리는 값이라, self.을 안 붙임
            with torch.no_grad():
                self.model(**inputs)
            self.get_logger().info(f"OWLv2 준비: {time.perf_counter() - start:.2f}초")

    def color_seeker_callback(self, msg):
        capture_yaw = self.yaw # sleep(=검출)동안 로봇이 돌아서 slef.yaw가 바뀌니까, 사진을 받은 순간의 yaw를 지역 변수에 먼저 적어둠. "찍었을 때 yaw"
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8') # msg를 -> Opencv로 바꾸는 함수: imgmsg_to_cv2
        for name, (lower, upper) in self.color_ranges.items(): # items()는 딕셔너리의 (키, 값) 쌍을 하나씩 꺼내줌. 값이 튜플이라 (lower, upper)로 바로 나눠받을 수 있음
            m = cv2.inRange(frame, lower, upper)
            m_ys, m_xs = np.nonzero(m)
            if len(m_xs) > 20: # 기억 기준을 낮춤: cx 갈래는 1칸만 보여도 동작하는데 기억은 500칸이어야 갱신돼서, 가장자리에서 둘이 반대 방향을 가리켰음
                m_cx = m_xs.mean() # 물체가 가로 몇 번째 칸에 있나
                direction = self.yaw + (160 - m_cx ) / 320 * 1.047 # 물체가 얼마나 벗어났는지 계산하는 자리
                self.seen_yaw[name] = direction
        self.get_logger().debug(f"seen: {self.seen_yaw}", throttle_duration_sec=1.0)
        if self.target_color is None:
            return
        stop_count = self.get_parameter("stop_count").value
        turn_speed = self.get_parameter("turn_speed").value
        forward_speed = self.get_parameter("forward_speed").value
        color = self.target_color # color = self.get_parameter("color").value 이제 색은 goal로 오니까 이 줄을 수첩에서 읽도록 바꾸기
        self.get_logger().debug(f"{frame.shape}", throttle_duration_sec=1.0)
        if color not in self.color_ranges:
            self.get_logger().warn(f"{color} 파랑, 초록, 빨강에 맞지 않는 색이 들어왔습니다.", throttle_duration_sec=1.0)
            cmd = Twist()
            self.publisher_.publish(cmd)
            return 
        lower, upper = self.color_ranges[color]
        mask = cv2.inRange(frame, lower, upper)
        num, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
        self.get_logger().debug(f"num: {num}, stats: {stats}, centroids: {centroids}", throttle_duration_sec=1.0)
        if num == 1:
            area = 0
        else:
            biggest = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1 # 가장 큰 덩어리 번호 찾기
            area = int(stats[biggest, cv2.CC_STAT_AREA])
            cx = centroids[biggest][0]
            self.target_yaw = capture_yaw + (160 - cx) / 320 * 1.047
            self.get_logger().info(f"cx: {cx:.0f}, target_yaw: {self.target_yaw:.2f}", throttle_duration_sec=1.0) # .0f = 소수점 아래 0자리, .2f: 소수점 아래 2자리까지만 보여주는 형식
        self.pixel_count = area # 사진마다 칸 수를 수첩에 적음(지금까지 계산한 칸 수)
        self.get_logger().info(f"{area}", throttle_duration_sec=1.0) # 8950: 로봇 카메라 사진 한 장 안에서 빨간 범위를 통과한 픽셀(칸)수. 가로320칸, 세로 240칸 모두 76800칸(URDF 센서에 적은 <width><height>)
        cmd = Twist()
        if area == 0: # 빨간 칸 0개: 제자리에서 왼쪽으로 천천히 회전
            if color in self.seen_yaw: # 기억이 있으면
                diff = self.seen_yaw[color] - self.yaw # 물체 방향 - 지금 방향 = 얼마나 더 돌아야 하나?
                diff = math.atan2(math.sin(diff), math.cos(diff)) # 빼기 결과는 -6.28 ~ 6.28이 될 수 있음. 이 줄이 그걸 -3.14 ~ 3.14로 바꿔줌. 같은 방향을 가리키는 각도 중 가장 짧은 쪽으로 정리하는 것.
                self.get_logger().info(f"diff: {diff}", throttle_duration_sec=1.0)
                if abs(diff) < 0.1:
                    self.get_logger().warn("기억한 방향에 없음, 다시 찾기")
                    del self.seen_yaw[color]
                if diff > 0:
                    cmd.angular.z = turn_speed
                else:
                    cmd.angular.z = -turn_speed
            else:
                cmd.angular.z = turn_speed # 반시계방향(왼쪽)으로 회전
            self.target_yaw = None
            self.publisher_.publish(cmd)
            return
        elif area > stop_count: # 빨간 칸 stop_count(기본 49000)초과: 멈춤 | 320 * 240 = 76,800칸(카메라의 절반 이상이 빨간색으로 가득차면)
            self.target_yaw = None
            self.arrived = True # 멈추는 순간 도착을 표시
            self.publisher_.publish(cmd) # 빨간 칸이 많음 = 아주 가까움: 멈춤
            return

    def execute_callback(self, goal_handle):
        if goal_handle.request.color not in self.color_ranges:
            self.get_logger().warn(f"{goal_handle.request.color}: red, blue, green 중 하나여야 합니다.")
            goal_handle.abort()
            result = GoToColor.Result()
            result.success = False
            return result
            
        self.pixel_count = 0
        self.target_color = goal_handle.request.color
        self.current_goal = goal_handle
        self.arrived = False
        
        while not self.arrived:
            if self.current_goal is not goal_handle: # 다른 goal이 들어와서 이 goal은 더 이상 지금 goal이 아니라는 뜻, 해당 경우 target_color와 Twist를 건드리지 않고 goal_handle.abort() -> result success False -> return만 함. 공유하는 값은 이제 새 goal 것이니깐, 이렇게하면 client가 취소를 안 보내도 이전 goal이 스스로 끝남
                goal_handle.abort()
                result = GoToColor.Result()
                result.success = False
                return result
            if goal_handle.is_cancel_requested:
                cmd = Twist()
                self.publisher_.publish(cmd)
                self.target_color = None
                self.target_yaw = None
                goal_handle.canceled()
                result = GoToColor.Result()
                result.success = False
                return result
            feedback = GoToColor.Feedback()
            feedback.pixel_count = self.pixel_count
            goal_handle.publish_feedback(feedback)
            time.sleep(0.5)

        self.target_color = None
        self.target_yaw = None
        goal_handle.succeed()
        result = GoToColor.Result()
        result.success = True
        return result

    def cancel_callback(self, goal_handle):
        return CancelResponse.ACCEPT

    def odom_callback(self, msg):
        z = msg.pose.pose.orientation.z
        w = msg.pose.pose.orientation.w
        self.yaw = math.atan2(2*w*z, 1 - 2*(z**2))
        if self.target_color is None or self.target_yaw is None:
            return
        diff = self.target_yaw - self.yaw
        diff = math.atan2(math.sin(diff), math.cos(diff))
        cmd = Twist()
        if diff > 0.065:
            cmd.angular.z = self.get_parameter("turn_speed").value
        elif diff < -0.065:
            cmd.angular.z = -self.get_parameter("turn_speed").value
        else:
            cmd.linear.x = self.get_parameter("forward_speed").value
        self.publisher_.publish(cmd)            
        self.get_logger().debug(f"yaw: {self.yaw}", throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args)
    color_seeker = ColorSeeker()
    try:
        executor = MultiThreadedExecutor()
        executor.add_node(color_seeker)
        executor.spin()
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        color_seeker.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()

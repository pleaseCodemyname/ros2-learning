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
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge
from rclpy.action import ActionServer, CancelResponse, ActionClient
from color_seeker_interfaces.action import GoToColor
from nav_msgs.msg import Odometry
from transformers import Owlv2Processor, Owlv2ForObjectDetection
from rcl_interfaces.msg import ParameterDescriptor
from tf2_ros import Buffer, TransformListener, TransformException
from nav2_msgs.action import NavigateToPose

class ColorSeeker(Node):
    def __init__(self):
        super().__init__('color_seeker')
        self.subscription = self.create_subscription(Image, '/camera/image',self.color_seeker_callback, 1, callback_group=MutuallyExclusiveCallbackGroup())
        self.odom_subscription = self.create_subscription(Odometry, "/odom", self.odom_callback, 10, callback_group=MutuallyExclusiveCallbackGroup())
        self.scan_subscription = self.create_subscription(LaserScan, "/scan", self.scan_callback, 10, callback_group=MutuallyExclusiveCallbackGroup())
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.nav_client = ActionClient(self, NavigateToPose, '/navigate_to_pose', callback_group=ReentrantCallbackGroup())
        self.bridge = CvBridge()
        self.action_server = ActionServer(self, GoToColor, "go_to_color", self.execute_callback, callback_group=ReentrantCallbackGroup(), cancel_callback=self.cancel_callback)
        self.declare_parameter("stop_count", 49000)
        self.declare_parameter("turn_speed", 0.3)
        self.declare_parameter("forward_speed", 0.2)
        self.declare_parameter("detector", "color", ParameterDescriptor(read_only=True)) # param set 거절됨
        self.tf_buffer = Buffer() # Buffer는 들어온 tf를 쌓아두는 곳
        self.tf_listener = TransformListener(self.tf_buffer, self) # TransformListener는 /tf를 구독해서 Buffer에 넣어 줌
        self.target_color = None
        self.pixel_count = 0
        self.arrived = False
        self.current_goal = None
        self.scan = None
        self.yaw = 0.0
        self.x = 0.0
        self.y = 0.0
        self.color_ranges = {"blue": (np.array([60, 0, 0]), np.array([255, 50, 50])), "green": (np.array([0, 60, 0]), np.array([50, 255, 50])), "red": (np.array([0, 0, 60]), np.array([50, 50, 255]),)}
        self.target_texts = {"blue": "blue box", "green": "green box", "red": "red box"}
        self.text_to_name = {text: name for name, text in self.target_texts.items()}
        self.get_logger().debug(f"{self.text_to_name}")
        self.last_time = None # None인 이유: 첫 콜백에는 "직전"이 없어서 빼기를 할 수 없음
        self.seen_pos = {}
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
            self.targets = self.target_texts
        else:
            self.targets = self.color_ranges

    def color_seeker_callback(self, msg):
        now = time.perf_counter()
        if self.last_time is not None:
            self.get_logger().debug(f"간격: {now - self.last_time:.2f}")
        self.last_time = now
        capture_yaw = self.yaw # sleep(=검출)동안 로봇이 돌아서 slef.yaw가 바뀌니까, 사진을 받은 순간의 yaw를 지역 변수에 먼저 적어둠. "찍었을 때 yaw"
        map_pose = self.get_map_pose()
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8') # msg를 -> Opencv로 바꾸는 함수: imgmsg_to_cv2
        if self.detector == "owlv2":
            texts = list(self.target_texts.values())
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            inputs = self.processor(text=[texts], images=rgb, return_tensors="pt").to("cuda")
            with torch.no_grad():
                outputs = self.model(**inputs)
            results = self.processor.post_process_grounded_object_detection(
                outputs, threshold=0.05, target_sizes=[(240, 320)], text_labels=[texts])[0]
            found = {}
            for score, label, box in zip(results["scores"], results["text_labels"], results["boxes"]):
                name = self.text_to_name[label]
                score = score.item() # 텐서 -> 숫자
                if name not in found or score > found[name][0]:
                    found[name] = (score, box)
            self.get_logger().debug(f"found: {found}", throttle_duration_sec=1.0)
            for name, (score, box) in found.items():
                xmin, ymin, xmax, ymax = box.tolist()
                cx = (xmin + xmax) / 2
                self.seen_yaw[name] = capture_yaw + (160 - cx) / 320 * 1.047
        else:
            for name, (lower, upper) in self.color_ranges.items(): # items()는 딕셔너리의 (키, 값) 쌍을 하나씩 꺼내줌. 값이 튜플이라 (lower, upper)로 바로 나눠받을 수 있음
                m = cv2.inRange(frame, lower, upper)
                m_ys, m_xs = np.nonzero(m)
                if len(m_xs) > 20: # 기억 기준을 낮춤: cx 갈래는 1칸만 보여도 동작하는데 기억은 500칸이어야 갱신돼서, 가장자리에서 둘이 반대 방향을 가리켰음
                    m_cx = m_xs.mean() # 물체가 가로 몇 번째 칸에 있나
                    direction = capture_yaw + (160 - m_cx) / 320 * 1.047 # 물체가 얼마나 벗어났는지 계산하는 자리
                    self.seen_yaw[name] = direction
        self.get_logger().debug(f"seen: {self.seen_yaw}", throttle_duration_sec=1.0)
        if self.target_color is None or self.arrived == True:
            return
        stop_count = self.get_parameter("stop_count").value
        turn_speed = self.get_parameter("turn_speed").value
        forward_speed = self.get_parameter("forward_speed").value
        color = self.target_color # color = self.get_parameter("color").value 이제 색은 goal로 오니까 이 줄을 수첩에서 읽도록 바꾸기
        self.get_logger().debug(f"{frame.shape}", throttle_duration_sec=1.0)
        if color not in self.targets:
            self.get_logger().warn(f"{color} 파랑, 초록, 빨강에 맞지 않는 색이 들어왔습니다.", throttle_duration_sec=1.0)
            cmd = Twist()
            self.publisher_.publish(cmd)
            return 
        if self.detector == "owlv2":
            if color not in found:
                area = 0
            else:
                score, box = found[color]
                xmin, ymin, xmax, ymax = box.tolist()
                cx = (xmin + xmax) / 2
                area = int(xmax - xmin) * int(ymax - ymin)
                self.target_yaw = capture_yaw + (160 - cx) / 320 * 1.047
                self.get_logger().info(f"cx: {cx:.0f}, target_yaw: {self.target_yaw:.2f}", throttle_duration_sec=1.0) # .0f = 소수점 아래 0자리, .2f: 소수점 아래 2자리까지만 보여주는 형식
        else:
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
                angle = (160 -cx) /320 * 1.047
                if self.scan is not None:
                    space_num = round((angle - self.scan.angle_min)/ self.scan.angle_increment)
                    distance = self.scan.ranges[space_num]
                    self.get_logger().info(f"cx: {cx}, angle: {angle}, space_num: {space_num}, distance: {distance}", throttle_duration_sec=1.0)
                    if math.isfinite(distance) and map_pose is not None:
                        map_x, map_y, map_yaw = map_pose
                        box_x = map_x + distance * math.cos(map_yaw + angle)
                        box_y = map_y + distance * math.sin(map_yaw + angle)
                        self.seen_pos[color] = (box_x, box_y)
                        self.get_logger().info(f"{color} 위치: ({box_x:.2f}, {box_y:.2f})", throttle_duration_sec=1.0)
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
        if goal_handle.request.color not in self.targets:
            self.get_logger().warn(f"{goal_handle.request.color}: red, blue, green 중 하나여야 합니다.")
            goal_handle.abort()
            result = GoToColor.Result()
            result.success = False
            return result
            
        color = goal_handle.request.color
        map_pose = self.get_map_pose()
        if color in self.seen_pos and map_pose is not None:
            rx, ry, _ = map_pose
            bx, by = self.seen_pos[color]
            yaw = math.atan2(by - ry, bx- rx)
            gx = bx - 0.6 * math.cos(yaw)
            gy = by -0.6 * math.sin(yaw) 
            self.get_logger().info(f"Nav2로 {color} 앞 ({gx:.2f}, {gy:.2f}), yaw {yaw:.2f}")
            status = self.nav_to(gx, gy, yaw)
            self.get_logger().info(f"Nav2 결과: {status}")
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

        cmd = Twist()
        self.publisher_.publish(cmd)
        self.target_color = None
        self.target_yaw = None
        goal_handle.succeed()
        result = GoToColor.Result()
        result.success = True
        return result

    def cancel_callback(self, goal_handle):
        return CancelResponse.ACCEPT

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
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

    def scan_callback(self, msg):
        self.scan = msg

    def get_map_pose(self):
        try:
            t = self.tf_buffer.lookup_transform("map", "base_link", rclpy.time.Time())
        except TransformException:
            return None
        x = t.transform.translation.x
        y = t.transform.translation.y
        z = t.transform.rotation.z
        w = t.transform.rotation.w
        yaw = math.atan2(2*w*z, 1 - 2*(z**2))
        return (x, y, yaw)

    def nav_to(self, x, y, yaw):
        if not self.nav_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().warn("Nav2 서버 없음")
            return None
        goal = NavigateToPose.Goal() # frame_id: "map", position: x, y
        goal.pose.header.frame_id = "map"
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.orientation.z = math.sin(yaw/2)
        goal.pose.pose.orientation.w = math.cos(yaw/2)
        future = self.nav_client.send_goal_async(goal)
        while not future.done():
            time.sleep(0.1)
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("Nav2가 goal 거절")
            return None
        result_future = goal_handle.get_result_async()
        while not result_future.done():
            time.sleep(0.1)
        return result_future.result().status


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

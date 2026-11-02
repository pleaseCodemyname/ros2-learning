# 알아야할 것 (Sub): 토픽: /camera/image 인터페이스: @sensor_msgs/msg/Image [gz.msgs.Image
# 내보내는 것 (Pub): 토픽: /cmd_vel 인터페이스: @geometry_msgs/msg/Twist ]gz.msgs.Twist
# 타이머: 필요없음. 사진이 올 때마다 콜백이 불리니깐 타이머는 필요없음 (왜?)
import rclpy
import numpy as np
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class Follow(Node):
    def __init__(self):
        super().__init__('follow')
        self.bridge = CvBridge() # cv_bridge 초기화, ROS Image 메시지를 OpenCV 이미지로 변환하기 위해 CvBridge 객체 생성
        self.subscription = self.create_subscription(Image, "/camera/image", self.follow_callback, 10) # 카메라에서 이미지를 받아옴, 토픽: /camera/image, 콜백함수: image_callback, 인터페이스: @sensor_msgs/msg/Image
        self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10) # 카메라로부터 받아온 이미지를 바탕으로 로봇을 움직이기 위해 cmd_vel 토픽에 Twist 메시지를 발행, 토픽: /cmd_vel, 인터페이스: @geometry_msgs/msg/Twist

    def follow_callback(self, msg):
        cmd = Twist() # Twist 메시지 생성
        # self.get_logger().info(f"가로: {msg.width}, 세로: {msg.height}") #  가로 320, 세로 240
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8") # msg를 bgr8로 전환, 받은 msg를 OpenCV가 쓸 수 있는 데이터 형식으로 변환(bridge)
        lower = np.array([0, 0, 100]) # 색의 최소값은 np.array([b:0, g:0, r:100]) 
        upper = np.array([80, 80, 255]) # 색의 최대 값은 np.array([b: 80, g:80, r:255 ])
        mask = cv2.inRange(frame, lower, upper) # 마스크 생성: cv2의 inRange라는 기능을 활용. (이미지, 최소값, 최대값)

        ys, xs = np.nonzero(mask) # 흰 부분 위치 찾음, 칸마다 줄 번호, 칸 번호를 적음
        self.get_logger().info(f"빨간칸: {len(xs)}", throttle_duration_sec=1.0)
        if len(xs) == 0: # 흰색이 화면에 있으면, 왼쪽으로 회전
            cmd.angular.z = 0.3
            self.publisher_.publish(cmd)
            return
        cx = xs.mean() # 흰 부분의 평균 x좌표를 구함
        self.get_logger().info(f"cx: {cx}", throttle_duration_sec=1.0)
        if len(xs) > 49000:
            self.publisher_.publish(cmd) # cmd_vel에 Twist 메시지를 발행
            return
        if cx < 140:
            cmd.angular.z = 0.3
        elif cx < 180:
            cmd.linear.x = 0.2
        else:
            cmd.angular.z = -0.3
        self.publisher_.publish(cmd) # cmd_vel에 Twist 메시지를 발행

def main(args=None):
    rclpy.init(args=args)
    follow = Follow() # 인스턴스 생성
    try:
        rclpy.spin(follow) # follow 노드를 계속 반복하면서 확인, follow에 등록된 콜백을 보며 기다리다가, 때가되면 콜백을 불러줌, Ctrl+C 전까지 안 끝남
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        follow.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
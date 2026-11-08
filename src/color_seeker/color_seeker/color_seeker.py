# Pub(무엇을 내보내나?): 속도/회전 명령, 인터페이스: geometry_msgs/msg/Twist, 토픽: /cmd_vel
# Sub(무엇을 알아야 하나?): 로봇 카메라 사진, 인터페이스: sensor_msgs/msg/Image, 토픽: /camera/image
# 타이머(받는 것 없이 반복할 일이 있나?): 없음, 사진이 올 때마다(약 29번/초) 콜백에서 판단하면 됨

import rclpy
import numpy as np
import cv2
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ColorSeeker(Node):
    def __init__(self):
        super().__init__('color_seeker')
        self.subscription = self.create_subscription(Image, '/camera/image',self.color_seeker_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()

    def color_seeker_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8') # msg를 -> Opencv로 바꾸는 함수: imgmsg_to_cv2
        self.get_logger().info(f"{frame.shape}", throttle_duration_sec=1.0)
        lower = np.array([0, 0, 60])
        upper = np.array([50, 50, 255])
        mask = cv2.inRange(frame, lower, upper)
        ys, xs = np.nonzero(mask)
        self.get_logger().info(f"{len(xs)}", throttle_duration_sec=1.0) # 8950: 로봇 카메라 사진 한 장 안에서 빨간 범위를 통과한 픽셀(칸)수. 가로320칸, 세로 240칸 모두 76800칸(URDF 센서에 적은 <width><height>)
        cmd = Twist()
        if len(xs) == 0: # 빨간 칸 0개: 제자리에서 왼쪽으로 천천히 회전
            cmd.angular.z = 0.3 # 반시계방향(왼쪽)으로 회전
            self.publisher_.publish(cmd)
            return
        elif len(xs) > 49000: # 빨간 칸 49000초과: 멈춤 | 320 * 240 = 76,800칸(카메라의 절반 이상이 빨간색으로 가득차면)
            self.publisher_.publish(cmd) # 빨간 칸이 많음 = 아주 가까움: 멈춤
            return
        cx = xs.mean() # 빨간 칸들이 가로로 어디쯤 모여 있는지, 가운데 위치를 구한 것, xs에는 빨간 칸 9850개의 칸 번호가 하나씩 들어있는데, xs.mean()은 그 8950개 번호의 평균임. 다 더해서 8950으로 나눈 값임. 그래서 cx는 빨간 덩어리의 가로 가운데임
        self.get_logger().info(f"cx: {cx}", throttle_duration_sec=1.0) # cx: 41.54223(가로 320칸 중 41번 쯤에 위치해있음, 왼쪽 끝)
        if cx < 140:
            cmd.angular.z = 0.3
        elif cx > 180:
            cmd.angular.z = -0.3
        else:
            cmd.linear.x = 0.2
        self.publisher_.publish(cmd)
        

def main(args=None):
    rclpy.init(args=args)
    color_seeker = ColorSeeker()
    try:
        rclpy.spin(color_seeker)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        color_seeker.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()

# Q1 내보내는 게 있나? (Pub): 속도
# Q2 알아야 할 게 있나? (Sub): 사진 -> (콜백에서 계산) -> cx
# Q3 받는 것 없이 반복할 일이 있나? (타이머): 없음
# 이 노드는: 카메라로 흰색 물체(햄버거)를 찾고, 그게 화면 어디 있는지(cx) 계산해서, cx 위치(왼쪽/가운데/오른쪽)에 따라 거북이를 왼쪽으로 돌리거나, 직진하거나, 오른쪽으로 돌린다.

import rclpy 
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2

class Follow(Node): # Follow 설계도 생성 (Node 상속)
    def __init__(self): # 생성자 함수
        super().__init__('follow') # Node를 상속받아 이름을 'follow'노드로 정함
        self.bridge = CvBridge() # CVBridge()를 self.bridge에 할당
        self.subscription = self.create_subscription(Image, '/image', self.follow_callback, 10) # subscriber 생성(양식=Image, 토픽:'/image', 콜백: follow_callback, 버퍼: 10)
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10) # publisher 생성(양식: Twist, 토픽: '/turtle1/cmd_vel', 버퍼: 10)
        self.frame_count = 0 # 갯수를 세기위해 초기값 0으로 세팅

    def follow_callback(self, msg): # follow_callback 생성
        self.frame_count +=1 # 콜백이 불릴때마다(spin) +1씩 진행
        cmd = Twist() # 빈 봉투 하나를 새로 만듬
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8') # frame은 bridge에 존재하는 imgmsg_to_cv2기능을 활용하여, msg를 bgr8로 전환할 것이다.) 여기서 msg는 subscription에 있는 Image 양식의 '/image' 토픽을 통해 받아옴
        # cv2.imwrite('burger.png', frame)
        lower = np.array([200,200,200]) # 색의 최소값은 np.array([b:50, g:50, r:50])
        upper = np.array([255, 255, 255]) # 색의 최대 값은 np.array([b: 255, g:255, r:255 ])
        mask = cv2.inRange(frame, lower, upper) # 마스크 생성: cv2의 inRange라는 기능을 활용. (이미지, 최소값, 최대값)

        ys, xs = np.nonzero(mask) # 흰 부분 위치 찾음 (근데 이걸 왜 찾아야해?)
        cx = xs.mean() # x의 평균값을 cx 변수에 할당
        frame[0:240, int(cx)] = [0, 0,255]
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.waitKey(1)
        self.get_logger().info(f'{self.frame_count}번째 사진, cx: {cx}', throttle_duration_sec=1.0)
        # cy = ys.mean() # 그럼 여기서 이건 필요없는건가?

        if cx < 140: # 가로 길이가 140 미만이면
            cmd.linear.x = 0.0 # 전진: 0 m/s
            cmd.angular.z = 1.0 # 회전: z축(위) 왼쪽, 1.0 rad/s, 1초에 57도 도는 속도
        elif cx < 180: # 가로 길이가 180 미만이면
            cmd.linear.x = 1.0 # 전진: 1.0 m/s
        else: 
            cmd.linear.x = 0.0 # 가로길이가 180 이상이면
            cmd.angular.z = -1.0 # 회전: z축(아래) 오른쪽 1.0 rad/s
        self.publisher_.publish(cmd) # cmd 발행 (/turtle1/cmd_vel 게시판)


def main(args=None):
    rclpy.init(args=args)
    follow = Follow()
    try:
        rclpy.spin(follow)
    except(KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        follow.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()
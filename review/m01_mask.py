import numpy as np
import cv2
from geometry_msgs.msg import Twist

# img = np.array([[[0, 0, 200], [255, 0, 0], [0, 0, 90]]], np.uint8) # lower와 upper에 해당되면 255, 해당되지 않으면 0인 칸을 찾음
img = np.array([[[0, 0, 200], [255, 0, 0], [0, 0, 200], [0, 0, 200], [255, 0, 0]]], np.uint8)
lower = np.array([0, 0, 100])
upper = np.array([80, 80, 255])
 
mask = cv2.inRange(img, lower, upper) # 범위에 해당하는 칸을 찾음, 칸마다 통과 255, 탈락 0
print(mask) # [[ 255, 0, 255, 255, 0]]

ys, xs = np.nonzero(mask) # 0이 아닌 칸을 찾음, 통과한 칸의 번호
print(xs) # [0 2 3]

cx = xs.mean # xs는 숫자가 여러개라 그대로는 if로 판단할 수 없음. 그래서 평균을 내서 숫자 하나로 만듬. 이 숫자가 빨간칸들이 가로로 어디쯤 모여있는지를 나타냄
print(cx) # (0 + 1 + 2) / 3 = 1.67

cmd = Twist()
if cx < 140:
    cmd.angular.z = 0.3    # 왼쪽으로 회전
elif cx < 180:
    cmd.linear.x = 0.2     # 직진
else:
    cmd.angular.z = -0.3   # 오른쪽으로 회전

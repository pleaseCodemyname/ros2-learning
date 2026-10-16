'''
OpenCV
흰 부분은 어디에 있나?
마스크는 흰 칸(255)과 검은 칸(0)로 된 표임. 흰 칸이 어디에 모여있는지 알고싶을 때
1. 흰 칸들의 가로 위치를 전부 모은다.
2. 그 숫자들의 평균을 낸다 -> 그게 흰 덩어리 가운데

가로: ... 260 261 262 ... 299 ...
흰 칸:     ■   ■   ■       ■
평균: 약 280 <- 빨간 네모의 가운데

개념 1: np.nonzero
ys, xs = np.nonzero(mask)
마스크에서 0이 아닌 칸(흰 칸)의 위치를 전부 찾아줌. 세로 위치 목록은 ys, 가로 위치는 xs에 담김.

평균 값 내기
cx = xs.mean() # 가로 위치들의 평균
cy = ys.mean() # 세로 위치들의 평균
'''

import cv2 # computer vision
import numpy as np # Numerical Python(수치 계산)

# 검은 사진 만들기 (세로 240, 가로 320, 컬러)
img = np.zeros((240, 320, 3), np.uint8) # np.zeros((세로, 가로, 점), 하나에 숫자 몇 개?)

# 빨간 네모 칠하기
img[20:60, 140:180] = [0, 0, 255] # img[세로20:60, 가로260:300] = [B:0, G:0, R:255]
'''
가로범위    흰 칸 개수      cx      cy      왼쪽/오른쪽
260:300     1600        279.5   39.5        오른쪽
40:80       1600        59.5    39.5        왼쪽
140:180     1600        159.5   39.5        가운데
'''

# 빨간 곳만 골라내는 마스크, 마스크란? 내가 관심 있는 곳만 표시한 예/아니오 표
# 원래 사진은 칸마다 "무슨 색이냐"(숫자 3개)를 담음.
# 마스크는 칸마다 "내가 찾는 색이냐 아니야" (255 또는 0)만 담음
# cv2.inRange는 사진을 칸마다 보면서 "예/아니오"를 정함.  Blue인지, Green인지, Red인지
lower = np.array([0, 0, 200]) # 이 색보다 같거나 크고 b: 0, g: 0, r: 200
upper = np.array([50, 50, 255]) # 이 색보다 같거나 작으면  b:50, g: 50, r: 255
mask = cv2.inRange(img, lower, upper) # cv2.inRange(검사할 사진, 아래한계, 위한계), img검사할 사진에서, lower 이상이거나 upper 사이에 들면 흰색으로 바꿈
print('img', img[40, 280])     # inRange 한 뒤에도 원래 사진은?
print('mask', mask[40, 280])   # 새 표의 같은 자리는?

# np.nonzero() 흰 부분 위치 찾기
# 흰 칸 위치를 전부 찾기
ys, xs = np.nonzero(mask)

# 흰 칸이 몇 개 인지
print('흰 칸 개수:', len(xs))

cx = xs.mean() # xs = 가로 위치 mean() 평균
cy = ys.mean() # ys = 세로 위치 mean() 평균
print('가운데:', cx, cy)

# 왼쪽? 오른쪽?
if cx < 160: # 가로 길이 320의 절반
    print("왼쪽")
else:
    print("오른쪽")

# 창 띄우기
cv2.imshow('img', img)
cv2.imshow('mask', mask)
cv2.waitKey(0)
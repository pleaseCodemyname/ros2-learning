import numpy as np
import cv2

img = np.zeros((2, 3, 3))
img[0, 0] = [0, 0, 255] # 빨강
img[0, 1] = [0, 0, 150] # 어두운 빨강
img[0, 2] = [255, 255, 255] # 흰색
img[1, 0] = [0, 255, 0] # 초록
img[1, 1] = [30, 30, 220] # 살짝 섞인 빨강
img[1, 2] = [0, 0, 0] # 검정

# 빨강 기준으로 마스크 만들기
lower = np.array([0, 0, 140])
upper = np.array([50, 50, 255])
mask = cv2.inRange(img, lower, upper)

print(mask)
print(mask.shape)

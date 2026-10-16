import numpy as np
import cv2

img = np.zeros((100,300, 3), np.uint8)
img[0:100, 0:100] = [255, 0, 0]
img[0:100, 100:200] = [0, 255, 0]
img[0:100, 200:300] = [0, 0, 255]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print('파랑', gray[50, 50])
print('초록', gray[50, 150])
print('빨강', gray[50, 250])
print(img.shape, gray.shape) # (100(세로), 300(가로), 3(칸) (100, 300)) 칸마다 숫자 1개 (밝기)
cv2.imshow('shy', img)
cv2.imshow('dope', gray)
cv2.waitKey(0)
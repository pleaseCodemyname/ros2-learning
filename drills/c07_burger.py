import numpy as np
import cv2

img = cv2.imread('burger.png')
print(img.shape) # (240, 320, 3) 위에서 240줄, 왼쪽에서 320칸, 칸마다 숫자 3개(컬러)
print('구석', img[0, 0])
print('햄버거', img[80, 200])

lower = np.array([50, 50, 50]) 
upper = np.array([255, 255, 255])
mask = cv2.inRange(img, lower, upper)

ys, xs = np.nonzero(mask)
print('흰 칸 개수', len(xs)) # 240: 3602, 200: 4635, 50: 7693
print('cx', xs.mean())
cx = xs.mean()

img[0:240, int(cx)] = [0,0,255]
cv2.imshow('burger', img)
cv2.imshow('mask', mask)
cv2.waitKey(0)

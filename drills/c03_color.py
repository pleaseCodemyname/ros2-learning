import numpy as np
import cv2

img = np.zeros((100,300,3))
img[0:100, 0:100] = [255, 0, 0] # 위에서 100, 왼쪽에서 99칸 까지는 Blue
img[0:100, 100:200] = [0, 255, 0] # 위에서 100, 왼쪽에서 100-199칸 까지는 Green
img[0:100, 200:300] = [0, 255, 255] # 위에서 100, 왼쪽에서 200-299칸 까지는 Red

cv2.imshow('shy', img) # cv2.imshow("창 이름", mat=띄울 사진(변수))
cv2.waitKey(0) # wiatKey(0)이면 Ctrl + C 불가, waitKey(1)이면 Ctrl+C로 종료 가능
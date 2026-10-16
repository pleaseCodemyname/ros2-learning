import numpy as np
import cv2

mask = np.zeros((3, 5), np.uint8)

mask[0,3] = 255
mask[1,3] = 255
mask[1,4] = 255
mask[2,0] = 255

# 흰 칸 = np.nonzero 위치 찾기
ys, xs = np.nonzero(mask)
print('ys', ys) # ys [0 1 1]
print('xs', xs) # xs [3 3 4]
print('흰 칸 개수', len(xs))
cx = xs.mean()
print(cx) # (3 + 3 + 4) / 3 = 3.33, 흰 덩어리가 가운데 선(2.5)보다 오른쪽에 있으니 오른쪽임
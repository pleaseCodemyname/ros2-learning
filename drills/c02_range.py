import numpy as np
import cv2

img = np.zeros((5,6), np.uint8) # np.zeros((세로, 가로, 칸)) # 흑백이면 하나, 컬러면 3개
# np.zeroes((세로, 가로, 칸)) 이면 컬러에 해당
# np.zeros((세로, 가로), uint8) 이면 흑백에 해당
img[1:3, 2:5] = 255 # 흑백이니깐 하나만 (세로 2번째칸에서 3번째 칸, 가로 3번째칸에서 5번째칸)
# [세로에서 몇 칸 내려가나, 가로에서 몇 칸] | img[ 위에서 몇 번 째, 왼쪽에서 몇 번째]
print(img)
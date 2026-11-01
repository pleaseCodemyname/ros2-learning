import numpy as np

mask = np.array([[255, 255, 0, 0],
                 [0, 0, 0, 0],
                 [0, 255, 255, 255]], np.uint8)

ys, xs = np.nonzero(mask)
print(ys) # [0 0 2 2 2]
print(xs) # [0 1 1 2 3]
print(xs.mean()) # 1.4
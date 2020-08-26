import numpy as np
import cv2
import time

img_back = cv2.imread('img_back.png')
img = np.ones((300, 3), dtype=np.uint8)
img[0, 0] = 255
img[0, 1] = 255
img[0, 2] = 255
cv2.imshow('img', img)

bgr_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
bgr_img[:,:,0] = 255
bgr_img[:,:,1] = 255
bgr_img[:,:,2] = 255
cv2.imshow('bgr_img2',bgr_img)
time.sleep(3)
cv2.destroyAllWindows()

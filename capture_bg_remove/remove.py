# -*- coding: utf-8 -*-
"""
视频背景替换
"""
# from PIL import Image
import numpy as np
import cv2

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('C:\\Users\\heyon\\Videos\\WeChat_20200223164534.mp4')
cap.set(5, 10)

# 要替换的背景
img_back = cv2.imread('img_back.png')
img = np.ones((3,3),dtype=np.uint8)
img[0,0]=100
img[0,1]=150
img[0,2]=255

# 保存
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('camera_test.avi', fourcc, fps, size)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    # 获取图片的尺寸
    rows, cols, channels = frame.shape

    lower_color = np.array([150, 150, 150])
    upper_color = np.array([255, 255, 255])
    # 创建掩图
    fgmask = cv2.inRange(frame, lower_color, upper_color)
    cv2.imshow('Mask', fgmask)

    # 腐蚀膨胀
    erode = cv2.erode(fgmask, None, iterations=1)
    # cv2.imshow('erode', erode)
    dilate = cv2.dilate(erode, None, iterations=1)
    # cv2.imshow('dilate', dilate)

    rows, cols = dilate.shape
    img_back = img_back[0:rows, 0:cols]
    # print(img_back)
    # #根据掩图和原图进行抠图
    img2_fg = cv2.bitwise_and(img_back, img_back, mask=dilate)
    Mask_inv = cv2.bitwise_not(dilate)
    img3_fg = cv2.bitwise_and(frame, frame, mask=Mask_inv)
    finalImg = img2_fg + img3_fg
    cv2.imshow('res', finalImg)

    # 保存
    # out.write(finalImg)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

out.release()
cap.release()
cv2.destroyAllWindows()

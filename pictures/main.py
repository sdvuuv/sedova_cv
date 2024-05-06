import numpy as np
import cv2
from skimage.measure import regionprops
import matplotlib.pyplot as plt
from skimage import draw
from skimage.measure import label
from skimage.filters import threshold_otsu
from collections import defaultdict

cv2.namedWindow("Frame", cv2.WINDOW_GUI_NORMAL)
capt = cv2.VideoCapture('pictures.avi')
image1 = cv2.imread("sedova.png")
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
#gray1 = cv2.bitwise_not(gray1)
_, thresh1 = cv2.threshold(gray1, 200, 255, cv2.THRESH_BINARY)
labeled = label(thresh1)
max_ = np.max(labeled)
#print(max_)

if not capt.isOpened():
    print("ERRROR")

cnt = 0
while capt.isOpened():
    ret, image = capt.read()
    if not ret:
        break
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray = cv2.bitwise_not(gray)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    #contours, _ = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    labeled_video = label(thresh)

    maximal = np.max(labeled_video)
    if abs(maximal - max_) <= 2:
        cnt+=1

print(cnt)

# Ответ 46
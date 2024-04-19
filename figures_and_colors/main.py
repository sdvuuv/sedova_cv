import numpy as np
import cv2
from skimage.measure import regionprops
import matplotlib.pyplot as plt
from skimage import draw
from skimage.measure import label
from skimage.filters import threshold_otsu
from collections import defaultdict

img = cv2.imread(r"balls_and_rects.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

colors_dict_circles = {}
colors_dict_rectangles = {}

output = cv2.connectedComponentsWithStats(gray, 4, cv2.CV_32S)
(countLabels, labels, stats, centroids) = output

for i in range(1, countLabels):

    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    area = stats[i, cv2.CC_STAT_AREA]
    (cX, cY) = centroids[i]

    part = img[y:y + h, x:x + w]
    hue = part[h // 2, w // 2, 0]
    if area == w * h:
        if hue not in colors_dict_rectangles.keys():
            colors_dict_rectangles[hue] = 1
        else:
            colors_dict_rectangles[hue] += 1

    else:
        if hue not in colors_dict_circles.keys():
            colors_dict_circles[hue] = 1
        else:
            colors_dict_circles[hue] += 1

print("Circles: ", colors_dict_rectangles)
print("Rectangles: ", colors_dict_circles)
cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
cv2.imshow("Output", img_hsv)
cv2.waitKey(0)
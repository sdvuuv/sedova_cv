import numpy as np
import cv2
from skimage.measure import regionprops
import matplotlib.pyplot as plt
from skimage import draw
from skimage.measure import label
from skimage.filters import threshold_otsu
from collections import defaultdict

all_pencils = 0
for i in range(1, 13):
    pencils_count = 0
    image = cv2.imread(f"images/img ({i}).jpg",  cv2.IMREAD_GRAYSCALE)
    thresh = cv2.erode(cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)[1], None, iterations=40)
    thresh = cv2.bitwise_not(thresh)

    mask = np.zeros(thresh.shape, dtype="uint8")

    output = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
    (countLabels, labels, stats, centroids) = output
    for i in range(1, countLabels):

        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[i]

        keepArea = area > 520_000 and area < 680_000

        if (keepArea):
            pencils_count += 1
            all_pencils += 1
    print(f"На картинке № {i} количество карандашей: {pencils_count}")
    cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
    cv2.imshow("Output", image)
    cv2.waitKey(0)

print(f"На всех картинках {all_pencils} карандашей")
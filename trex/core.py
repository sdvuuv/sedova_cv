import cv2
import numpy as np

class Object:
    def __init__(self, path, name):
        img = cv2.imread(path, 0)
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.location = None
        self.name = name
    def match(self, screen):
        res = cv2.matchTemplate(screen, self.img, cv2.TM_CCOEFF_NORMED)

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        startLoc = maxLoc
        endLoc = (startLoc[0] + self.width, startLoc[1]+self.height)

        if maxVal > 0.5:
            self.location = (startLoc, endLoc)
            return True
        else:
            self.location = None
            return False


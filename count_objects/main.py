# ping 192.168.0.111
import cv2
import zmq #pip install pyzmq
import numpy as np

from skimage.measure import regionprops

def filling_factor(region):
    return np.sum(region.image) / region.image.size

def eccentricity(region):
    return region.eccentricity

def area(region):
    return region.area / region.image.size

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5055
socket.connect(f"tcp://192.168.0.113:{port}")
n = 0
while True:
    bts = socket.recv()
    n += 1
    arr = np.frombuffer(bts, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    blured = cv2.GaussianBlur(image, (11, 11), 0)

    hsv = cv2.cvtColor(blured, cv2.COLOR_BGR2HSV)
    ret, thresh = cv2.threshold(hsv[:, :, 1], 60, 255, cv2.THRESH_BINARY)
    dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    dist = cv2.normalize(dist, None, 0, 1.0, cv2.NORM_MINMAX)
    ret, fg = cv2.threshold(dist, 0.45 * dist.max(), 255, cv2.THRESH_BINARY)
    confuse = cv2.subtract(thresh, fg.astype("uint8"))
    ret, markers = cv2.connectedComponents(fg.astype("uint8"))
    markers += 1
    markers[confuse == 255] = 0

    segments = cv2.watershed(blured, markers)
    cnts, hierrachy = cv2.findContours(segments, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(cnts)):
        if hierrachy[0][i][3] == -1:
            cv2.drawContours(blured, cnts, i, (0, 255, 0), 5)
    arr = []
    for i, region in enumerate(regionprops(segments)):
        arr.append((eccentricity(region), area(region)))
    circles = 0
    for i in arr:
        if i[0] > 0.42 and i[1] > 0.7:
            circles += 1
    print(arr)

    key = cv2.waitKey(10)
    if key == ord("q"):
        break
    cv2.putText(image, f"Image = {markers.max()-1}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (127, 255, 255))

    cv2.putText(image, f"Cubes = {markers.max()- 1 - circles}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (127, 255, 255))

    cv2.putText(image, f"Circles = {circles}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (127, 255, 255))
    cv2.imshow("Image", image)
    cv2.imshow("Mask", (segments/segments.max()))

cv2.destroyAllWindows()
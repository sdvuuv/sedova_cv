from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
from skimage.measure import regionprops
from skimage import draw
from skimage.measure import label
from skimage.filters import threshold_otsu
from collections import defaultdict
from pathlib import Path
import numpy as np

def filling_factor(region):
    return np.sum(region.image) / region.image.size

def hav_hline(region):
    return 1. in np.mean(region.image, 1)

def hav_vline(region):
    return 1. in np.mean(region.image, 0)

def has_line(region, horizontal = True):
    return 1. in np.mean(region.image, int(horizontal))

def count_holes(region):
    holes = 0
    labeled = label(np.logical_not(region.image))
    regions = regionprops(labeled)
    for region in regions:
        not_bound = True
        coords = np.where(labeled == region.label)
        for y, x in zip(*coords):
            if y == 0 or x == 0 or y == labeled.shape[0] - 1 or x == labeled.shape[1] - 1:
                not_bound = False
        holes += not_bound
    return holes

def recognize(region):
    if filling_factor(region) == 1.0:
        return "-"
    else:

        holes = count_holes(region)
        if holes == 2:
            if has_line(region, False) and region.image[0, 0] > 0:
                return "B"
            else:
                return "8"
        if holes == 1:
            ny, nx = (region.centroid_local[0] / region.image.shape[0],
                  region.centroid_local[1] / region.image.shape[1])

            if has_line(region, False) and region.image[0, 0] > 0 and np.isclose(ny, nx, 0.09):
                return "P"
            elif has_line(region, False) and not np.isclose(ny, nx, 0.07):
                return "D"
            elif np.isclose(ny, nx, 0.07):
                return "0"
            else:
                return "A"


        else:
            if has_line(region, False):
                return "1"
            if has_line(region):
                return "*"
            inv = np.logical_not(region.image)
            labeled = label(inv)
            holes = np.max(labeled)
            match holes:
                case 2: return "/"
                case 4: return "X"
                case 5: return "W"
                case _: return "*"
    return "_"


image = plt.imread(r"symbols.png")

image = np.mean(image, 2)
image[image > 0] = 1


labeled = label(image)
all_figures = labeled.max()
regions = regionprops(labeled)
result = defaultdict(lambda : 0)
path = Path(".") / "result"
path.mkdir(exist_ok=True)

plt.figure()
for i, region in enumerate(regionprops(labeled)):
#  print(i)
    symbol = recognize(region)
#
    result[symbol] += 1
#    plt.clf()
#    plt.title(f"{symbol=}")
#    plt.imshow(region.image)
#    plt.tight_layout()
#    plt.savefig(path / f"{i}.png")



num = 161
print(result)
#plt.show()

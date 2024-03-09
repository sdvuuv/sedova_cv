from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np


image = np.load("wires6npy.txt")
labeled = label(image)
for i in range(1, np.max(labeled)+1):
    im = np.zeros_like(image)
    im += binary_erosion(labeled == i)
    max_ = np.max(im2)
    im2 = label(im)
    if max_ == 1:
        print("Провод не порван")
    elif max_ == 0:
        print(f"Провода не существует он совсем порван((")
    else:
        print(f"Провод {i} порван на {max_} штук")

plt.imshow(image)
plt.show()
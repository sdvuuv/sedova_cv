import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label


def object(obj):
    idx = np.argwhere(obj)
    min_idx = idx.min(axis=0)
    max_idx = idx.max(axis=0)
    new_obj = obj[min_idx[0]:max_idx[0] +
                             1, min_idx[1]:max_idx[1]+1]

    return new_obj


image = np.load("ps.npy.txt")
labeled = label(image)
count = labeled.max()
structures = []

for i in range(1, count+1):
    cur = object(labeled == i)
    k = False
    for i, j in enumerate(structures):
        if cur.shape[0] != j[0].shape[0] or cur.shape[1] != j[0].shape[1]:
            continue
        if np.all(j[0] == cur):
            k = True
            structures[i][1] += 1
            break
    if not k:
        structures.append([cur, 1])

print(f"Number of objects: {count}")
print(f"Types of objects: {len(structures)}")
print(*[f"Object {i+1}: {x[1]} times" for i,
      x in enumerate(structures)], sep='\n')

plt.imshow(labeled)
plt.show()

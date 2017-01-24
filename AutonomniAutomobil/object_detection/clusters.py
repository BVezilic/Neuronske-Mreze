import numpy as np
from scipy import ndimage
import cv2

def image_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
def image_bin(image_gs):
    ret,image_bin = cv2.threshold(image_gs, 150, 255, cv2.THRESH_BINARY)
    return image_bin


def find_clusters(array):
    clustered = np.empty_like(array)
    unique_vals = np.unique(array)
    cluster_count = 0
    for val in unique_vals:
        labelling, label_count = ndimage.label(array == val)
        for k in range(1, label_count + 1):
            clustered[labelling == k] = cluster_count
            cluster_count += 1
    return clustered, cluster_count


image = cv2.imread('C:\\Users\\Komp\\Desktop\\NM\\TestGitCars\\Cars\\car1.jpg')
img = image_bin(image_gray(image))

clustered, cluster_count = find_clusters(img)
print cluster_count
print clustered
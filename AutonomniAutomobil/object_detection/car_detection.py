import cv2
import numpy as np
import matplotlib.pyplot as plt
import cnn
import rc_car.lane_detector as fl
from scipy import ndimage
car_height = 58.5 #fiksan
camera_height = 90 #promenljiv
image_height = 144 #fiksan
focal_length = 40 #fiksan
known_width = 75 #fiksan

def load_image(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
def image_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
def image_bin(image_gs):
    ret,image_bin = cv2.threshold(image_gs, 120, 255, cv2.THRESH_BINARY)
    return image_bin
def invert(image):
    return 255-image
def display_image(image, color= False):
    if color:
        plt.imshow(image)
    else:
        plt.imshow(image, 'gray')

#Funkcionalnost implementirana u V2
def resize_region(region):
    resized = cv2.resize(region,(28,28), interpolation = cv2.INTER_NEAREST)
    return resized
def scale_to_range(image):
    return image / 255
def matrix_to_vector(image):
    return image.flatten()
def prepare_for_ann(regions):
    ready_for_ann = []
    for region in regions:
        ready_for_ann.append(matrix_to_vector(scale_to_range(region)))
    return ready_for_ann
def convert_output(outputs):
    return np.eye(len(outputs))
def winner(output):
    return max(enumerate(output), key=lambda x: x[1])[0]

#model = cnn.load_predictor()

def select_roi(image_orig):

    img_bin = image_bin(image_gray(image_orig))

    img_bin = cv2.dilate(img_bin, None, iterations=2)
    img_bin = cv2.erode(img_bin, None, iterations=2)
    img_bin = cv2.dilate(img_bin, None, iterations=3)
    img_bin = cv2.erode(img_bin, None, iterations=2)
    img_bin = cv2.dilate(img_bin, None, iterations=2)
    img_bin = cv2.erode(img_bin, None, iterations=2)

    #img_bin = cv2.dilate(img_bin, None, iterations=3)
    #img_bin = cv2.erode(img_bin, None, iterations=2)

    #img_bin = cv2.dilate(img_bin, None, iterations=6)
    #img_bin = cv2.erode(img_bin, None, iterations=6)

    img, contours, hierarchy = cv2.findContours(img_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best_contour = []
    min = 176
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if(np.abs((88-(x+x+w)/2)) < min):
            min = np.abs((88-(x+x+w)/2))
            best_contour = contour
    x, y, w, h = cv2.boundingRect(best_contour)
    region = image_orig[y:y + h, x:x + w]
    cv2.rectangle(image_orig, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), 2)
    distance_t = (known_width * focal_length) / w  # slicnost trouglova
    print distance_t
    return np.array(image_orig)#, sorted_regions[:, 0], region_distances
    #return np.array(img_bin)
    #return np.array(edges)


'''
#distance_f = (focal_length*car_height*image_height)/(car_height*camera_height)

focal length (mm) * real height of the object (mm) * image height (pixels)
    ----------------------------------------------------------------
            object height (pixels) * sensor height (mm)
'''
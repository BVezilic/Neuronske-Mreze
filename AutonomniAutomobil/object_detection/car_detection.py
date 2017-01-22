import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    ret,image_bin = cv2.threshold(image_gs, 127, 255, cv2.THRESH_BINARY)
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


def select_roi(image_orig):
    img_bin = image_bin(image_gray(image_orig))
    img, contours, hierarchy = cv2.findContours(img_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        #if area > 100 and x > 60 and x < 150 and w > 20 and w < 100 and h < 15 and h < 100:
        #if area > 100 and h < 100 and h > 15 and w > 20 and w < 110 and x > 40:
        if h < 100 and h > 15 and w > 20 and w < 110 and x > 40 and y < 100:
        #if area > 100 and area < 200:
            #region = img_bin[y:y + h + 1, x:x + w + 1]
            print '{}{}{}{}{}{}{}{}'.format("X: ",x, " Y: ", y, " W: ", w, " H: ",h)
            cv2.rectangle(image_orig, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #distance_f = (focal_length*car_height*image_height)/(car_height*camera_height)
            distance_t = (known_width*focal_length)/w # slicnost trouglova
            #print distance_f
           # print distance_t

    return image_orig#, sorted_regions[:, 0], region_distances


'''
focal length (mm) * real height of the object (mm) * image height (pixels)
    ----------------------------------------------------------------
            object height (pixels) * sensor height (mm)
'''
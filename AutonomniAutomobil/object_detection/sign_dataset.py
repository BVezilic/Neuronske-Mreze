# Branislav Vezilic

import os
import numpy as np
from scipy.misc import imread, imresize


def load_data(root_directory='D:/FTN/Master/Neuronske mreze/sign_train_dataset/GTSRB/Final_Training/Images',
              valid_directory=('14', '15', '16')):
    images = []
    classes = []
    test_images = []
    test_classes = []
    class_flag = 0
    for subdir, dirs, files in os.walk(root_directory):
        if subdir.endswith(valid_directory):
            for file in os.listdir(subdir):
                if file.endswith('.ppm'):
                    img = imread(os.path.join(subdir, file))
                    resized_img = imresize(img, (224, 224))
                    if file[9:11] not in ('27', '28', '29'):
                        images.append(resized_img)
                        classes.append(class_flag)
                    else:
                        test_images.append(resized_img)
                        test_classes.append(class_flag)

            class_flag += 1
    return (np.array(images), np.array(classes)), (np.array(test_images), np.array(test_classes))

def test():
    data = load_data('D:/FTN/Master/Neuronske mreze/sign_train_dataset/GTSRB/Final_Training/Images',
                     ('14','15','16','17','18','19','20','21','22','23'))
    return data

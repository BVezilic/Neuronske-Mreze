#autori Bane i Nemanja

from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint
from keras.utils.np_utils import to_categorical
import numpy as np
import os
import cv2

K.set_image_dim_ordering('tf')


def load(path):
    x_train = []
    y_train = []
    vehicle_path = os.path.join(path, "vehicles")
    for folder in os.listdir(vehicle_path):
        for image in os.listdir(os.path.join(vehicle_path, folder)):
            img = cv2.imread(os.path.join(os.path.join(vehicle_path, folder), image))
            x_train.append(img)
            y_train.append(0)
    non_vehicle_path = os.path.join(path, "non-vehicles")
    for folder in os.listdir(non_vehicle_path):
        for image in os.listdir(os.path.join(non_vehicle_path, folder)):
            img = cv2.imread(os.path.join(os.path.join(non_vehicle_path, folder), image))
            x_train.append(img)
            y_train.append(1)
    return np.array(x_train, np.float32), np.array(y_train, np.float32)


def load_data(data_path):
    (x_train, y_train) = load(data_path)
    y_train = to_categorical(y_train, 2)
    return x_train, y_train


def get_model():
    model = Sequential()

    model.add(Convolution2D(32, 3, 3, border_mode='same',
                            input_shape=(64, 64, 3)))
    model.add(Activation('relu'))
    model.add(Convolution2D(32, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(64, 3, 3, border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2))
    model.add(Activation('softmax'))

    return model


def train():
    (x_train, y_train)= load_data("D:\FTN\Master\Neuronske mreze\OwnCollection")
    x_train = x_train.astype('float32')
    x_train /= 255

    model = get_model()
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    # callback koji snima tezine modela
    mc = ModelCheckpoint('weights.h5', save_weights_only=True, save_best_only=True)

    # ucitavanje tezina sa najboljim rezultatom
    #model.load_weights('weights.h5')

    # sada radimo fine-tuning celog modela
    model.fit(x_train, y_train,
              batch_size=32,
              nb_epoch=20,
              shuffle=True,
              callbacks=[mc])

    model.save_weights("tezine.h5")


def is_car(image):
    model = get_model()
    model.load_weights('tezine.h5')
    return model.predict(np.array(cv2.resize(image, (64, 64))).reshape(1, 64, 64, 3))


if __name__ == '__main__':
    #train()
    img = cv2.imread('D:\\FTN\\Master\\Neuronske mreze\\OwnCollection\\non-vehicles\\MiddleClose\\image0100.png')
    print is_car(img)


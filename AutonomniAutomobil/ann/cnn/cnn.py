#autori: Branislav Vezilic, Nemanja Rasajski

from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint
from keras.utils.np_utils import to_categorical
import numpy as np
import os
import cv2

K.set_image_dim_ordering('tf')


def load(path, split_data = 0.1):
    '''
    :param path: string, path to 'OwnCollection' folder
    :return: tuple -> (images for training, labels [0,1])
    '''
    x_train, y_train, x_test, y_test = [], [], [], []
    counter = 0
    vehicle_path = os.path.join(path, "vehicles")
    for folder in os.listdir(vehicle_path):
        for image in os.listdir(os.path.join(vehicle_path, folder)):
            img = cv2.imread(os.path.join(os.path.join(vehicle_path, folder), image))
            if counter % int(split_data*100) != 0:
                x_train.append(img)
                y_train.append(0)
            else:
                x_test.append(img)
                y_test.append(0)
            counter += 1
    counter = 0
    non_vehicle_path = os.path.join(path, "non-vehicles")
    for folder in os.listdir(non_vehicle_path):
        for image in os.listdir(os.path.join(non_vehicle_path, folder)):
            img = cv2.imread(os.path.join(os.path.join(non_vehicle_path, folder), image))
            if counter % int(split_data*100) != 0:
                x_train.append(img)
                y_train.append(1)
            else:
                x_test.append(img)
                y_test.append(1)
            counter += 1

    x_train = np.array(x_train, np.float32)
    y_train = np.array(y_train, np.int0)
    x_test = np.array(x_test, np.float32)
    y_test = np.array(y_test, np.int0)
    return (x_train, y_train), (x_test, y_test)


def load_data(data_path):
    (x_train, y_train) , (x_test, y_test) = load(data_path)
    # Process label data from [0, 1] -> [1 0],[0 1]
    y_train = to_categorical(y_train, 2)
    y_test = to_categorical(y_test, 2)
    return (x_train, y_train), (x_test, y_test)


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
    (x_train, y_train), (x_test, y_test) = load_data("D:\FTN\Master\Neuronske mreze\OwnCollection")
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    model = get_model()
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    # ucitavanje tezina sa najboljim rezultatom
    # model.load_weights('weights.h5')

    # callback koji snima tezine modela
    mc = ModelCheckpoint('weights.h5', monitor='val_loss', save_weights_only=True, save_best_only=True)

    # sada radimo fine-tuning celog modela
    model.fit(x_train, y_train,
              batch_size=32,
              nb_epoch=5,
              shuffle=True,
              validation_data=(x_test, y_test),
              callbacks=[mc])

    #model.save_weights("tezine.h5")


def load_model():
    model = get_model()
    model.load_weights('../ann/cnn/tezine.h5')
    return model


def is_car(image, model):
    image /= 255
    retVal = model.predict(np.array(cv2.resize(image, (64, 64))).reshape(1, 64, 64, 3))
    return True if retVal[0][0] > retVal[0][1] else False


def test():
    img = cv2.imread('D:/FTN/Master/Neuronske mreze/OwnCollection/vehicles/MiddleClose/image0195.png')
    print is_car(img, load_model())

#test()
#train()


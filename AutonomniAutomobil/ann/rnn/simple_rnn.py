# Author: Nina Marjanovic
# Simple RNN
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, TimeDistributed, SimpleRNN, Dropout
import util.csv_reader as reader
from keras.callbacks import ModelCheckpoint



"""
testX = trainX[30:40]
testY = trainY[30:40]
trainX = trainX[:30] + trainX[40:]
trainY = trainY[:30] + trainY[40:]
"""

# create and fit the RNN network
def create_model():
    model = Sequential()
    model.add(SimpleRNN(8, input_shape=(None,2), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(8,  return_sequences=True))
    model.add(Dropout(0.2))
    model.add(TimeDistributed(Dense(units=3)))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


def train_model(model):
    trainX = reader.read_inputs("training_data_new")
    trainY = reader.read_outputs("training_data_new")

    #mc = ModelCheckpoint('weights.h5', monitor='precision', save_best_only=True)
    model.fit(np.expand_dims(np.array(trainX), axis=0), np.expand_dims(np.array(trainY), axis=0),
              batch_size=16, epochs=4000)
    model.save_weights("weights_new.h5")
    return model


def test():
    simpleRNN = create_model()
    simpleRNN = train_model(simpleRNN)
    #simpleRNN.load_weights("weights_right.h5")
    #print testY
    #print simpleRNN.evaluate(np.expand_dims(np.array(testX),axis=0),np.expand_dims(np.array(testY), axis=0))
    #print simpleRNN.predict(np.expand_dims(np.array(testX),axis=0))

#test()
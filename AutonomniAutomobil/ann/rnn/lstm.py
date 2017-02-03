# Author: Nina Marjanovic
# LSTM
import numpy as np
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, TimeDistributed, Flatten, Embedding
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import util.csv_reader as reader
import random
from keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger
import sklearn.preprocessing as sp



trainX = reader.read_inputs("training_data_left")
trainY = reader.read_outputs("training_data_left")


testX = trainX[30:40]
testY = trainY[30:40]
trainX = trainX[:30] + trainX[40:]
trainY = trainY[:30] + trainY[40:]

# create and fit the LSTM network
"""
model = Sequential()
model.add(LSTM(2, input_dim=2, activation="relu"))
model.add(Dense(3))
model.add(Activation('softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
model.fit(np.expand_dims(np.array(trainX), axis=0).shape, np.expand_dims(np.array(trainY), axis=0).shape, nb_epoch=10, batch_size=1, verbose=2)
"""



# build the model: 2 stacked LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(3, return_sequences=True, input_dim=2, activation="sigmoid"))  # returns a sequence of vectors of dimension 32
#model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
#model.add(LSTM(32))  # return a single vector of dimension 32
#model.add(Dense(3, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

mc = ModelCheckpoint('weights.h5', monitor='val_loss', save_best_only=True)
# callback koji prekida obucavanje u slucaju overfitting-a
es = EarlyStopping(monitor='val_loss', patience=10)

model.fit(np.expand_dims(np.array(trainX),axis=0),np.expand_dims(np.array(trainY), axis=0),
          batch_size=10, nb_epoch=5000, shuffle=True, callbacks=[mc, es],
          validation_data=(np.expand_dims(np.array(testX),axis=0),np.expand_dims(np.array(testY), axis=0)))

data = [0, 890]
data_normalized = sp.normalize([data], norm='l2')
print data_normalized
print model.predict(np.expand_dims(np.array(data_normalized),axis=0))
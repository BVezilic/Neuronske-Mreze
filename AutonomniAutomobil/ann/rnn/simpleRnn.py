# Author: Nina Marjanovic
# Simple RNN
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, TimeDistributed, SimpleRNN, Dropout
import util.csv_reader as reader
from keras.callbacks import ModelCheckpoint




trainX = reader.read_inputs("training_data_left")
trainY = reader.read_outputs("training_data_left")


testX = trainX[30:40]
testY = trainY[30:40]
trainX = trainX[:30] + trainX[40:]
trainY = trainY[:30] + trainY[40:]


# create and fit the RNN network
model = Sequential()
model.add(SimpleRNN(8, input_dim=2, return_sequences=True))
model.add(Dropout(0.2))
model.add(SimpleRNN(8,  return_sequences=True))
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(output_dim=3)))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['precision'])

mc = ModelCheckpoint('weights.h5', monitor='precision', save_best_only=True)

model.fit(np.expand_dims(np.array(trainX), axis=0),np.expand_dims(np.array(trainY), axis=0),
          batch_size=4, nb_epoch=2000, callbacks=[mc])

print testY
print model.evaluate(np.expand_dims(np.array(testX),axis=0),np.expand_dims(np.array(testY), axis=0))
print model.predict(np.expand_dims(np.array(testX),axis=0))
from keras.layers               import Input, Dense, SimpleRNN, GRU, LSTM, CuDNNLSTM, RepeatVector
from keras.models               import Model
from keras.layers.core          import Flatten
from keras.callbacks            import LambdaCallback 
from keras.optimizers           import SGD, RMSprop, Adam
from keras.layers.wrappers      import Bidirectional as Bi
from keras.layers.wrappers      import TimeDistributed as TD
from keras.layers               import merge
from keras.applications.vgg16   import VGG16 
from keras.layers.normalization import BatchNormalization as BN
from keras.layers.noise         import GaussianNoise as GN
from keras.layers.merge         import Concatenate
from keras.layers.core          import Dropout
from keras.layers.merge         import Concatenate as Concat
from keras.layers.noise         import GaussianNoise as GN
from keras.layers.merge         import Dot,Multiply
from keras import backend as K


import numpy as np
import random
import sys
import pickle
import glob
import copy
import os
import re
import time
import json
import gzip
from sklearn.cross_validation import KFold


def root_mean_squared_error(y_true, y_pred):
  return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1)) 

def getModel():
  TIME_SIZE     = 20
  PERD_SIZE     = 4
  input_tensor1 = Input(shape=(1, 20))

  x             = input_tensor1
  x             = Bi(GRU(300, dropout=0.0, recurrent_dropout=0.2, activation='relu', recurrent_activation='tanh', return_sequences=False))(x)
  #x             = Bi(GRU(300, dropout=0.0, recurrent_dropout=0.2, activation='relu', recurrent_activation='tanh', return_sequences=True))(x)

  #x             = Flatten()(x)
  x             = Dense(1000, activation='relu')(x)
  x             = Dropout(0.1)(x)
  x             = Dense(1000, activation='relu')(x)
  x             = Dropout(0.1)(x)
  x             = Dense(1000, activation='relu')(x)
  prediction    = Dense(PERD_SIZE, activation='linear')(x)

  model         = Model(input_tensor1, prediction)
  model.compile(Adam(), loss=root_mean_squared_error)
  #model.compile(Adam(), loss='mse')
  return model

if '--train' in sys.argv:
  tds, Tds, tbs, tas = pickle.load(open('ds_tuple.pkl', 'rb'))

  kf = KFold(len(tds), n_folds=7, shuffle=True, random_state=777)

  for tindex, vindex in kf:
    model = getModel()
    model.fit(tds[tindex], Tds[tindex], validation_data=(tds[vindex], Tds[vindex]), epochs=30, batch_size=300)



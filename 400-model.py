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
from keras.layers import Concatenate
from keras.layers import Reshape
buff = None
def callbacks(epoch, logs):
  global buff
  buff = copy.copy(logs)
  print("epoch" ,epoch)
  print("logs", logs)
callback = LambdaCallback( on_epoch_end=callbacks )

def root_mean_squared_error(y_true, y_pred):
  return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1)) 

def getModel():
  TIME_SIZE     = 20
  PERD_SIZE     = 14
  input_tensor1 = Input(shape=(1, 20))
  x1             = Bi(LSTM(256, dropout=0.0, recurrent_dropout=0.1, activation='relu', recurrent_activation='tanh', return_sequences=False))(input_tensor1)

  input_tensor2 = Input(shape=(5, 20))
  x2             = Bi(LSTM(256, dropout=0.0, recurrent_dropout=0.2, activation='relu', recurrent_activation='tanh', return_sequences=False))(input_tensor2)
  
  input_tensor3 = Input(shape=(5, 20))
  x3             = Bi(LSTM(256, dropout=0.0, recurrent_dropout=0.2, activation='relu', recurrent_activation='tanh', return_sequences=False))(input_tensor3)
  
  x             = Concatenate(axis=1)([x1, x2, x3])
  x             = Dense(1024, activation='relu')(x)
  #x             = x1
  print(x.shape)
  x             = RepeatVector(14)(x)
  x             = Bi(LSTM(256, return_sequences=True))(x)
  x             = Dense(256, activation='relu')(x)
  x             = Dense(1, activation='linear')(x)
  prediction    = Reshape( (1, 14) )(x)

  print(prediction.shape)
  model         = Model([input_tensor1, input_tensor2, input_tensor3], prediction)
  #model.compile(Adam(), loss=root_mean_squared_error)
  model.compile(Adam(), loss='mae')
  return model

if '--train' in sys.argv:
  tds, Tds, tbs, tas = pickle.load(open('tmp/ds_tuple.pkl', 'rb'))

  kf = KFold(len(tds), n_folds=7, shuffle=True, random_state=777)

  for tindex, vindex in kf:
    model = getModel()
    for epoch in range(100):
      model.fit([tds[tindex], tbs[tindex], tas[tindex]], Tds[tindex], validation_data=([tds[vindex], tbs[vindex], tas[vindex]], Tds[vindex]), \
                  epochs=1, shuffle=True, batch_size=4, callbacks=[callback])
      lr = K.get_value(model.optimizer.lr)
      K.set_value(model.optimizer.lr, 0.950 * K.get_value(model.optimizer.lr))
      log = f'epoch_{epoch:03d}_val_loss_{buff["val_loss"]:03.6f}_loss_{buff["loss"]:03.6f}_lr_{lr:0.06f}'
      model.save_weights(f'tmp/weights/{log}.h5')
      print(log) 
    exit()

if '--predict' in sys.argv:
  tds, Tds, tbs, tas = pickle.load(open('tmp/ds_tuple.pkl', 'rb'))
  model = getModel()

  model.load_weights('tmp/weights/epoch_056_val_loss_284.182861_loss_180.860878_lr_0.000057.h5')
  yps = model.predict([tds, tbs, tas])
  for yp in yps:
    print(yp)

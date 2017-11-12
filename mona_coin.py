import pickle
import gzip

import os
import sys
import statistics
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model, load_model
from keras.layers import Lambda, Input, Activation, Dropout, Flatten, Dense, Reshape, merge
from keras.layers import Concatenate, Multiply, Conv1D, MaxPool1D, BatchNormalization
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization as BN
from keras.layers.core import Dropout
from keras.optimizers import SGD, Adam
from keras import backend as K

def CBRD(inputs, filters=64, kernel_size=3, droprate=0.5):
  x = Conv1D(filters, kernel_size, padding='same',
            kernel_initializer='random_normal')(inputs)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  return x


def DBRD(inputs, units=4096, droprate=0.35):
  x = Dense(units)(inputs)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  x = Dropout(droprate)(x)
  return x

input_tensor = Input( shape=(19, 40) )

x = Dense(3000, activation='relu')(input_tensor)
x = CBRD(x, 32)
x = CBRD(x, 32)
x = MaxPool1D()(x)

x = CBRD(x, 64)
x = CBRD(x, 64)
x = MaxPool1D()(x)

x = CBRD(x, 128)
x = CBRD(x, 128)
x = CBRD(x, 128)
x = MaxPool1D()(x)

x = Flatten()(x)
x1 = Dense(1000, activation='relu')(x)
x2 = Dense(1000, activation='relu')(x)


h = Dense(1, activation='linear')(x1)
m = Dense(1, activation='linear')(x2)

epsilon_std = 1.0
def sampling(args):
  z_mean, z_log_var = args
  epsilon = K.random_normal(shape=(K.shape(z_mean)[0], 1), mean=0., stddev=epsilon_std)
  return z_mean + K.exp(z_log_var / 2) * epsilon
z = Lambda(sampling, output_shape=(1,))([m, h])

model = Model(inputs=input_tensor, outputs=z)
model.compile(loss='mae', optimizer='sgd')

if '--train' in sys.argv:
  ys, Xs, origXs = pickle.loads( gzip.decompress( open('tmp/data.pkl', 'rb').read() ) )
  max_ = ys.max()
  #ys = ys / max_
  print(Xs.shape)
  print(ys.shape)
  print(ys)
  for i in range(100):
    model.fit(Xs, ys, batch_size=128, epochs=100)
    model.save_weights('models/model_{:09d}.h5'.format(i))

if '--predict' in sys.argv:
  import numpy as np
  import json
  ys, Xs, origXs = pickle.loads( gzip.decompress( open('tmp/data.pkl', 'rb').read() ) )

  key_perf = {}
 
  model.load_weights('models/model_000000099.h5')
  for i in range(10):
    yp = model.predict(Xs)
    for x, p,y in zip(origXs, ys.tolist(), yp.tolist()):
      key = x
      #print(key, 'yp', p, y)
      if key_perf.get(key) is None:
        key_perf[key] = [ 0.0, [] ]
      key_perf[key][0] = y
      key_perf[key][1].append( p )

  ys_ = []
  for key, perf in sorted( key_perf.items(), key=lambda x:x[0]):
    y = perf[0]
    ys_.append( y[0] )
    ps = perf[1]
    print(y, y, statistics.mean(ps))

  keys = key.split(',')
  mine = int(keys.pop()) + 5
  if mine != 60:
    keys.append(str(mine))
    predkey = ','.join( keys )
    print( predkey )
    key_index, size = json.loads( open('tmp/key_index.json').read() )
    
    Xs_ = []
    # 最後に時系列情報を入れる
    base = [ [0.0]*len(key_index) for i in range(size+1) ]
    for index, ch in enumerate(list(predkey)):
      key = '%s-%s'%(index, ch)
      cursol = key_index[key]
      base[index][cursol] = 1.0

    for indexY, cur in enumerate(range(-15, 0)):
      print(cur)
      print(indexY, ys_[cur])
      base[-1][indexY] =  ys_[cur]
    Xs_.append( base )
    print(Xs_)
    Xs_ = np.array(Xs_)
    ps = model.predict(Xs_)
    print( 'next key', predkey,'predict value', ps)

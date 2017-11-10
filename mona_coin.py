import pickle
import gzip

import os
import sys

import keras

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model, load_model
from keras.layers import Lambda, Input, Activation, Dropout, Flatten, Dense, Reshape, merge
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization as BN
from keras.layers.core import Dropout
from keras.applications.vgg19 import VGG19
from keras.applications.vgg16 import VGG16
from keras.applications.resnet50 import ResNet50
from keras.optimizers import SGD, Adam
from keras import backend as K

#input_tensor = Input( shape=(10, 35) )
input_tensor = Input( shape=(19, 86) )

x = Dense(3000, activation='relu')(input_tensor)
x = Dropout(0.3)(x)
x = Dense(3000, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(3000, activation='relu')(x)
x = Dropout(0.3)(x)
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
  ys, Xs = pickle.loads( gzip.decompress( open('tmp/data.pkl', 'rb').read() ) )
  max_ = ys.max()
  #ys = ys / max_
  print(Xs.shape)
  print(ys.shape)
  print(ys)
  model.fit(Xs, ys, batch_size=32, epochs=1000)
  model.save_weights('model.h5')

if '--predict' in sys.argv:
  ys, Xs = pickle.loads( gzip.decompress( open('tmp/data.pkl', 'rb').read() ) )
  model.load_weights('model.h5')

  yp = model.predict(Xs)
  for p,y in zip(ys.tolist(), yp.tolist()):
    print('yp', p, y)


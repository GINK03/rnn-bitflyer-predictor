import pickle
import gzip

import os
import sys

import keras

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model, load_model
from keras.layers import Input, Activation, Dropout, Flatten, Dense, Reshape, merge
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization as BN
from keras.layers.core import Dropout
from keras.applications.vgg19 import VGG19
from keras.applications.vgg16 import VGG16
from keras.applications.resnet50 import ResNet50
from keras.optimizers import SGD, Adam


input_tensor = Input( shape=(10, 35) )

x = Dense(3000, activation='relu')(input_tensor)
x = Dropout(0.3)(x)
x = Dense(3000, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(3000, activation='relu')(x)
x = Dropout(0.3)(x)
x = Flatten()(x)
x = Dense(3000, activation='relu')(x)
x = Dense(1, activation='linear')(x)

model = Model(inputs=input_tensor, outputs=x)
model.compile(loss='mae', optimizer='sgd')

ys, Xs = pickle.loads( gzip.decompress( open('tmp/data.pkl', 'rb').read() ) )
max_ = ys.max()
#ys = ys / max_
print(Xs.shape)
print(ys.shape)
print(ys)
model.fit(Xs, ys, batch_size=32, epochs=1000)

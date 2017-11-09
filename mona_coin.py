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

x = Dense(1000, activation='relu')(input_tensor)
x = Dense(1000, activation='relu')(x)
x = Flatten()(x)
x = Dense(1, activation='linear')(x)

model = Model(inputs=input_tensor, outputs=x)
model.compile(loss='mse', optimizer='adam')

ys, Xs = pickle.loads( gzip.decompress( open('tmp/data.pkl', 'rb').read() ) )
print(Xs.shape)
print(ys.shape)
model.fit(Xs, ys, epochs=1000)

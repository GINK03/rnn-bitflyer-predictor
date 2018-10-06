
import pickle
from math import sqrt

tds, Tds, tbs, tas = pickle.load(open('tmp/ds_tuple.pkl', 'rb')) 

a1 = Tds[:, 0, 0].mean()
SIZE = len(Tds[:, 0, 0])

print(a1)
print(SIZE)

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

score = 0
for i in range(1):
  #score += sqrt(mean_squared_error(Tds[:, i], zeros[i]))
  score += mean_absolute_error(Tds[:, 0, 0], [ a1 for x in range(SIZE) ] )
  #print( Tds[:, i][:,0] )
  #print( zeros[i].shape )
print( score  )

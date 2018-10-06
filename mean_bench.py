
import pickle
from math import sqrt

tds, Tds, tbs, tas = pickle.load(open('tmp/ds_tuple.pkl', 'rb')) 

a1 = Tds[:, 0].mean()
a2 = Tds[:, 1].mean()
a3 = Tds[:, 2].mean()
a4 = Tds[:, 3].mean()

import numpy as np
print(Tds.shape[0])
zeros = np.zeros((Tds.shape[0], 4))
for i, a in enumerate([a1, a2, a3, a4]):
  zeros[:,i] = a

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
score = 0
for i in range(4):
  #score += sqrt(mean_squared_error(Tds[:, i], zeros[i]))
  #score += mean_absolute_error(Tds[:, i][:,0], [zeros[i] for x in range(len(Tds[:, i][:,0]))] )
  print( Tds[:, i][:,0] )
  #print( zeros[i].shape )
print( score / 4 )

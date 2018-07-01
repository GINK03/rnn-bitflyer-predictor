
import pickle
from math import sqrt

tds, Tds, tbs, tas = pickle.load(open('ds_tuple.pkl', 'rb')) 

a1 = Tds[:, 0].mean()
a2 = Tds[:, 1].mean()
a3 = Tds[:, 2].mean()
a4 = Tds[:, 3].mean()


import numpy as np

zeros = np.zeros((len(Tds), 4))
for i, a in enumerate([a1, a2, a3, a4]):
  zeros[:,i] = a

from sklearn.metrics import mean_squared_error
score = 0
for i in range(len(Tds)):
  score += sqrt(mean_squared_error(Tds[i], zeros[i]))
print( score / len(Tds) )

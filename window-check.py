import pickle

cas = pickle.load(open("objs.pkl", "rb"))

from datetime import datetime

timestamps = list(map(list, zip(*cas)))[0]
bids       = list(map(list, zip(*cas)))[1]
asks       = list(map(list, zip(*cas)))[2]

import json
from hashlib import sha256
for i in range(0, len(timestamps)-50):
  slice = timestamps[i:i+50]
  slice_bids = bids[i:i+50]
  slice_asks = asks[i:i+50]

  start = datetime.strptime(slice[0], '%Y_%m_%d %H:%M:%S') 
  
  t_series = {}
  for k in range(1, 50):
    next_ = datetime.strptime(slice[k], '%Y_%m_%d %H:%M:%S')
    t = (next_ - start).seconds
    #print(t//10)
    t = t//10
    if t_series.get(t) is None:
      t_series[t] = ( slice_bids, slice_asks )

  union = set(t_series.keys()) & set(list(range(25)))
  if len(union) != 24:
    continue
  for k in list(t_series.keys()):
    if k not in set(list(range(25))):
      del t_series[k] 
  #print( t_series )
  obj = json.dumps(t_series)
  hash = sha256(bytes(obj, 'utf8') ).hexdigest()

  with open(f'flagments/{hash}.json', 'w') as fp:
    fp.write( obj )
  #print( len(union) )

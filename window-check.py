import pickle
import json
from hashlib import sha256
from datetime import datetime

cas = pickle.load(open("tmp/objs.pkl", "rb"))

timestamps   = list(map(list, zip(*cas)))[0]
deltas       = list(map(list, zip(*cas)))[1]
bids         = list(map(list, zip(*cas)))[2]
asks         = list(map(list, zip(*cas)))[3]

for i in range(0, len(timestamps)-50):
  slice = timestamps[i:i+50]
  print(slice)
  slice_deltas = deltas[i:i+50]
  slice_bids = [ b[:5] for b in bids[i:i+50] ]
  slice_asks = [ a[:5] for a in asks[i:i+50] ]
  
  start = datetime.strptime(slice[0], '%Y_%m_%d %H:%M:%S') 
  t_series = {}
  for k in range(1, 50):
    next_ = datetime.strptime(slice[k], '%Y_%m_%d %H:%M:%S')
    t = (next_ - start).seconds
    #print(t//10)
    t = t//10
    if t_series.get(t) is None:
      t_series[t] = ( slice_deltas[k], slice_bids[k], slice_asks[k] )
  union = set(t_series.keys()) & set(list(range(30)))
  if len(union) != 30 :
    continue
  for k in list(t_series.keys()):
    if k not in set(list(range(30))):
      del t_series[k] 
  #print( t_series )
  obj = json.dumps(t_series)
  hash = sha256(bytes(obj, 'utf8') ).hexdigest()
  with open(f'tmp/flagments/{hash}.json', 'w') as fp:
    fp.write( obj )
  #print( len(union) )

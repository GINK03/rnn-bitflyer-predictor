import pickle
import json
from hashlib import sha256
from datetime import datetime
import pandas as pd
df = pd.read_csv('tmp/board-check.csv')

timestamps   = df['timestamp'].tolist()
deltas       = df['delata'].tolist()
bids         = df['bids'].apply(json.loads).tolist()
asks         = df['anks'].apply(json.loads).tolist()

for i in range(0, len(timestamps)-50):
  slice = timestamps[i:i+50]
  print(slice)
  slice_deltas = deltas[i:i+50]
  slice_bids = [ b[:5] for b in bids[i:i+50] ]
  slice_asks = [ a[:5] for a in asks[i:i+50] ]
  
  start = datetime.strptime(slice[0], '%Y_%m_%d %H:%M:%S') 
  t_series = {}
  for k in range(1, 35):
    #next_ = datetime.strptime(slice[k], '%Y_%m_%d %H:%M:%S')
    #t = (next_ - start).seconds
    if t_series.get(k) is None:
      t_series[k] = ( slice_deltas[k], slice_bids[k], slice_asks[k] )
  #print( t_series )
  obj = json.dumps(t_series)
  hash = sha256(bytes(obj, 'utf8') ).hexdigest()
  with open(f'tmp/flagments/{hash}.json', 'w') as fp:
    fp.write( obj )
  #print( len(union) )

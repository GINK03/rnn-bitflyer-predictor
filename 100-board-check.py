import glob
from pathlib import Path
import json
import math
import re
from concurrent.futures import ProcessPoolExecutor as PPE

def pmap(name):
  try:
    o = json.load(open(name))
  except:
    Path(name).unlink()
    return None
  # エラーメッセージがあるとき
  if o.get('error_message') is not None:
    Path(name).unlink()
    return None 
  try:
    '''
    bids =  [ [math.log(x['price']), x['size']] for x in o['bids'] ][:20]
    asks =  [ [math.log(x['price']), x['size']] for x in o['asks'] ][:20]
    '''
    bids =  [ x['size'] for x in o['bids'] ][:20]
    asks =  [ x['size'] for x in o['asks'] ][:20]
    delta = o['asks'][0]['price'] - o['bids'][0]['price'] + 1
    
    timestamp = re.search(r'../.*?/(.*?).json', name).group(1)
    
    obj = {'timestamp':timestamp, 'delata':delta, 'bids':bids, 'anks':asks}

    #objs.append( obj )
    return obj
  except Exception as ex:
    print(ex)
    print(o)
    return None

names = [ name for name in sorted(glob.glob('../boards/*.json')) ]
objs = []
with PPE(max_workers=20) as exe:
  for obj in exe.map(pmap, names):
    if obj is not None:
      objs.append(obj) 

import pandas as pd
df = pd.DataFrame(objs)
df.to_csv('tmp/board-check.csv', index=None)

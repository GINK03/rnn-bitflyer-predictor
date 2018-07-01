
import glob

from pathlib import Path

import json

import math

import re

objs = []
for name in sorted(glob.glob('boards/*.json')):
  try:
    o = json.load(open(name))
  except:
    Path(name).unlink()

  try:
    bids =  [ [math.log(x['price']), x['size']] for x in o['bids'] ][:20]

    asks =  [ [math.log(x['price']), x['size']] for x in o['asks'] ][:20]

    delta = o['asks'][0]['price'] - o['bids'][0]['price'] + 1
    
    timestamp = re.search(r'/(.*?).json', name).group(1)
    
    obj = [timestamp, delta, bids, asks]

    objs.append( obj )
  except Exception as ex:
    print(ex)

import pickle

open('objs.pkl', 'wb').write( pickle.dumps(objs) )

import gzip
import datetime
import csv
import json
f = gzip.open('btceUSD.csv.gz', 'rt')

f = csv.reader(f)

time_price = {}
for index, es in enumerate(f):
  if index%100000 == 0:
    print( index )
  #print(es)
  unix = int(es[0])
  time = datetime.datetime.fromtimestamp(unix)
  price = float(es[1])
  time = str(time)
  time_price[time] = price 
  #print(time, price)

open('time_price.json', 'w').write( json.dumps(time_price, indent=2) )

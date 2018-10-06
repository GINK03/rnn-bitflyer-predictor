import numpy as np
from pathlib import Path
import json
import pickle

tds = []
Tds = []
tbs = []
tas = []

for path in list(Path('tmp/flagments').glob('*'))[:1024*10]:
  obj = json.load( path.open() )
  print(path)
  objs = [obj[key] for key in sorted(obj.keys(), key=lambda x:int(x))]
  td = [obj[0] for obj in objs]
  tb = [obj[1] for obj in objs]
  ta = [obj[2] for obj in objs]
  
  td, Td = td[:20], td[20:]
  tb, Tb = tb[:20], tb[20:]
  ta, Ta = ta[:20], ta[20:]
  #print(tb) 
  print(td)
  print(Td)
  Td = np.array(Td).reshape(1, 14).tolist()
  print(Td)
  td = np.array(td).reshape(1, 20).tolist()
  #print(len(Td))
  tds.append( td )
  Tds.append( Td )
  tbs.append( tb )
  tas.append( ta )
   

tds = np.array(tds)
Tds = np.array(Tds)
tbs = np.array(tbs)
print(tbs.shape)
tbs = tbs.reshape(len(tbs), 5, 20)
tas = np.array(tas)
tas = tas.reshape(len(tas), 5, 20)
data = pickle.dumps( (tds, Tds, tbs, tas))
open('tmp/ds_tuple.pkl', 'wb').write( data )
    

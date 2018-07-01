import numpy as np
from pathlib import Path
import json
import pickle

tds = []
Tds = []
tbs = []
tas = []

for path in Path('flagments').glob('*'):
  obj = json.load( path.open() )
  print(path)
  objs = [obj[key] for key in sorted(obj.keys(), key=lambda x:int(x))]
  td = [obj[0] for obj in objs]
  tb = [obj[1] for obj in objs]
  ta = [obj[2] for obj in objs]
  
  td, Td = td[:20], td[20:]
  tb, Tb = tb[:20], tb[20:]
  ta, Ta = ta[:20], ta[20:]
  
  tds.append( td )
  Tds.append( Td )

  tbs.append( tb )

  tas.append( ta )
   

tds = np.array(tds)
tds = tds.reshape(len(tds), 1, 20)

Tds = np.array(Tds)
Tds = Tds.reshape(len(Tds), 4)

tbs = np.array(tbs)
tbs = tbs.reshape(len(tbs), 5, 20)

tas = np.array(tas)
tas = tas.reshape(len(tas), 5, 20)

data = pickle.dumps( (tds, Tds, tbs, tas))
open('ds_tuple.pkl', 'wb').write( data )
    

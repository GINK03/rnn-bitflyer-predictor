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
Tds = np.array(Tds)
tbs = np.array(tbs)
tas = np.array(tas)

data = pickle.dumps( (tds, Tds, tbs, tas))
open('ds_tuple.pkl', 'wb').write( data )
    

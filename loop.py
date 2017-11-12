import os
import sys
import time

f = open('predict.log', 'a')
while True:
  os.system('python3 prepare.py --key_vec_sql') 
  os.system('python3 prepare.py --to_vec') 
  os.system('python3 mona_coin.py --train') 
  text = os.popen('python3 mona_coin.py --predict').read() 
  for line in text.split('\n'):
    if '[OUTPUT]' in line:
      es = line.strip().split('/')
      key = es[1].strip()
      val = es[3].strip()
      buff = '%s %s\n'%(key, val)
      f.write( buff )


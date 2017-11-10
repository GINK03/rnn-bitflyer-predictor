
import os
import sys

"""
http://mona-coin.com/charts_m5_jpy.html
このURLを5分おきに、スクレイピンして以下のようなJSのリストの値を取り出す
[new Date(2017,11-1,10,15,10), 318.15], 
KVSは安定性の視点から、1系統にせずに、LevelDBとgdbmのデュアルチャンネルで運用する

leveldbはarchlinuxはデフォルトで対応していた
python3バインディングはplyvelを用いる
sudo pip3 install plyvel
"""

import dbm
import plyvel

#rdb = rocksdb.DB("mona_coin.rocksdb", rocksdb.Options(create_if_missing=True))
dbm = dbm.open("mona_coin.gdbm", "c")
ldb = plyvel.DB("mona_coin.leveldb", create_if_missing=True)

import requests
import pickle
import gzip
import re
import time as Time

while True:
  r = requests.get("http://mona-coin.com/charts_m5_jpy.html")
  html = r.text
  for line in html.split('\n'):
    #print(line)
    time = re.search(r'new Date\((.*?)\)', line)
    num = re.search(r'(\d{1,}.\d{1,})\]', line)
    if time is None or num is None:
      continue
    time = time.group(1)
    num = num.group(1)
    print(time, num)
    
    # time key example. 2017,11-1,10,16,05
    key = bytes(time, 'utf8')
    val = pickle.dumps( float(num) )
    ldb.put( key, val )

    key_str = key.decode('utf8')
    val_str = str(num)
    dbm[key_str] = val_str

  print("Now Sleeping to time")
  Time.sleep(100)
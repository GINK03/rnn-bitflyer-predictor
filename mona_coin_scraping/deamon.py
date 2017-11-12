
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
import sqlite3


#rdb = rocksdb.DB("mona_coin.rocksdb", rocksdb.Options(create_if_missing=True))

import requests
import pickle
import gzip
import re
import time as Time
if '--scan' in sys.argv:
  conn = sqlite3.connect('mona_coin.db')
  cur = conn.cursor()
  print('tsu')
  for date, price in cur.execute('select * from mona_coin'):
    print(row)

  
if '--scrape' in sys.argv:
  dbm = dbm.open("mona_coin.gdbm", "c")
  ldb = plyvel.DB("mona_coin.leveldb", create_if_missing=True)
  conn = sqlite3.connect('mona_coin.db')
  cur = conn.cursor()
  try:
    cur.execute("create table mona_coin (key varchar(64), val varchar(64))")
  except sqlite3.OperationalError as e:
    ...

  while True:
    try:
      r = requests.get("http://mona-coin.com/charts_m5_jpy.html")
    except Exception as e:
      print('Error', e)
      Time.sleep(10)
      continue
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
      
      cur.execute('insert into mona_coin (key, val) values (?, ?)', (key_str, val_str))
      try:
        conn.commit()
      except Exception as e:
        print(e)
        ...

    print("Now Sleeping to time")
    Time.sleep(10)

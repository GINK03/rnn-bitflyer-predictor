import json
import time
import pybitflyer
from datetime import datetime
import schedule

def job():
  ticker = api.ticker(product_code="FX_BTC_JPY")
  board  = api.board(product_code="BTC_JPY")
  date_time = datetime.now().strftime("%Y_%m_%d %H:%M:%S")
  print( ticker )
  print( board )
  
  json.dump( ticker, fp=open(f'tickers/{date_time}.json', 'w'), indent=2 ) 
  json.dump( board,  fp=open(f'boards/{date_time}.json', 'w'), indent=2 ) 
  print('売値:' + str(ticker['best_bid']))
  print('買値:' + str(ticker['best_ask']))
    
if __name__ == '__main__':
  api = pybitflyer.API()
  schedule.every(10).seconds.do(job)
  job()
  while True:
    schedule.run_pending()
    time.sleep(1)

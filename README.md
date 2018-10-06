# bitflyer auto bit and sell 

## BIDとASKについて
<div align="center">
  <img width="600px" src="https://d2mxuefqeaa7sj.cloudfront.net/s_3A7AF7713DCD72B55C56C67EC74231E0AA5475959E8D5F94A00EC0CFD8EAA0EE_1530429886760_image.png">
</div>

大規模資本が資本を投下すると、成行きで購入することが多く、えぐるように、多くの板（BidとAskに挿している数）が、溶けて消えるとそうです。

このとき、成行きの範囲に収まっていれば売れて消えるので、戦略的には、この乖離が発生する箇所を予想すればいいとわかります。  

## モデル1(RNN)
系列情報なので、RNNで予想を行います。
<div align="center">
  <img width="600px" src="https://d2mxuefqeaa7sj.cloudfront.net/s_3A7AF7713DCD72B55C56C67EC74231E0AA5475959E8D5F94A00EC0CFD8EAA0EE_1530431038030_image.png">
</div>

どうせ板情報が複雑過ぎて、上手く行かないので、板情報の次元を予め、FCを通して落としておく
<div align="center">
  <img width="450px" src="https://d2mxuefqeaa7sj.cloudfront.net/s_3A7AF7713DCD72B55C56C67EC74231E0AA5475959E8D5F94A00EC0CFD8EAA0EE_1530433750649_image.png">
</div>

## RMSEを目的関数に先の150秒を予想する

40ごとの定点観測の4点についてのASK, BIDの乖離量を計算すると、7holdしたMAEで、`1.559`程度の差になる

ベンチマークとして平均との差を計算すると、`1.896`程度であり、学習できていることがわかる。  

この時の、平均値からの差を答えとした場合のMAEの計算はとなります。  

```python
import pickle
from math import sqrt

tds, Tds, tbs, tas = pickle.load(open('tmp/ds_tuple.pkl', 'rb'))

a1 = Tds[:, 0, 0].mean()
SIZE = len(Tds[:, 0, 0])

print(a1)
print(SIZE)

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

score = 0
for i in range(1):
  #score += sqrt(mean_squared_error(Tds[:, i], zeros[i]))
  score += mean_absolute_error(Tds[:, 0, 0], [ a1 for x in range(SIZE) ] )
  #print( Tds[:, i][:,0] )
  #print( zeros[i].shape )
print( score  )

```

## Next Action
 - どこで売って、どこで買うかのルール策定
 - BitFlyerでの実正試験

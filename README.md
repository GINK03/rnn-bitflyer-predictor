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

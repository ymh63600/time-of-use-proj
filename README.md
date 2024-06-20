# 時間電價系統

# nilm

與nilm相關的部分在/backend/nilm 中
主要有更改的部分是nilmtk-contrib的部分我更改了一下把train好的model存起來，並另外多加了pred的部分需要使用的參數，pred所使用的nilmfunc是基於nilmtk的api.py去做修改

reference: 
[nilmtk](https://github.com/nilmtk/nilmtk/blob/master/README.md)
[nilmtk-contrib](https://github.com/nilmtk/nilmtk-contrib)

# 合成資料
裡面的code有一些是python2的語法，需要自己稍微修改

github: [smartsim](https://github.com/sustainablecomputinglab/smartsim)

生成出來的結果可以用nilmtk裡面的套件轉成 .h5 file，以便之後可以放到nilm裡面進行訓練

 ```python
from nilmtk.dataset_converters import convert_redd

convert_redd(r'.\smartsim\redd\low_freq', r'house_1.h5')
```

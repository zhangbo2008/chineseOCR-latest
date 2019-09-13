import t
import t
import t
import t
import t2
import t
import t
import t
import t
import t
import t
import t

import requests
tmp2='https://gss1.bdstatic.com/-vo3dSag_xI4khGkpoWK1HF6hhy/baike/whfpf%3D268%2C152%2C50/sign=df23b72c44fbfbeddc0c653f1ecdc500/9358d109b3de9c8254d4df9c6381800a19d8436b.jpg'
r = requests.get(tmp2)
with open('tmp.jpg','wb') as f:
    f.write(r.content)
print('over')





#把引入模块都放入静态区域!!!!!!!!!!!!!
#他们在的区域是堆中,因为服务一直没停,所以一直占用内存.正好是我们需要的效果!!!!!!!!!!!!!!!!!!!!
#发现会重复引入下面的库包,加一个引用计数.也不行,用locals加flag也不行!!!

"""这个文件是用于测试"""
## 如果修改了原来的模块,那么就del 然后再import?????好像还是不行.
#只能点击pycharm 里面的+号按钮,重新建立一个python console
##
if 'flag'  not in   locals():
    flag=1

    import os

    GPUID = '0'  ##调用GPU序号
    os.environ["CUDA_VISIBLE_DEVICES"] = GPUID
    import torch
    from apphelper.image import xy_rotate_box, box_rotate, solve
    import model

    #注意目前只支持4个方向,我要做成8个方向的,只是图片预处理时候多算几个方向即可.4个感觉不够.
    import cv2
    import numpy as np









#下面是函数主体.

##

    '''
先打开url  1种是下载,1种是直接打开.

:param url:
:return:
'''
url='http://pics.sc.chinaz.com/files/pic/pic9/201909/zzpic20026.jpg'
tmp2=url
print(url,"url...........")
import requests
r = requests.get(tmp2)
with open('tmp.jpg', 'wb') as f:
    f.write(r.content)
print('图片下载完成')

picName=url.split('/')[-1].split('.')[-2]


##


import time
from PIL import Image
import os,sys
p = 'tmp.jpg'
img = cv2.imread(p)


h,w = img.shape[:2]
timeTake = time.time()
print(111111111111)
#这个scores1,socres2. 直接sum效果不好.因为很多差的边框会扰乱结果.所以需要先nms再算score
_,result1,angle1,scores1,tex_rec,newBox= model.model(img,
                                    detectAngle=True,##是否进行文字方向检测
                                    config=dict(MAX_HORIZONTAL_GAP=50,##字符之间的最大间隔，用于文本行的合并
                                    MIN_V_OVERLAPS=0.6,
                                    MIN_SIZE_SIM=0.6,
                                    TEXT_PROPOSALS_MIN_SCORE=0.1,
                                    TEXT_PROPOSALS_NMS_THRESH=0.3,
                                    TEXT_LINE_NMS_THRESH = 0.7,##文本行之间测iou值

                ),
                                    leftAdjust=True,##对检测的文本行进行向左延伸
                                    rightAdjust=True,##对检测的文本行进行向右延伸
                                    alph=0.01,##对检测的文本行进行向右、左延伸的倍数

                                   )
##
_, result2, angle2, scores2,tex_rec,newBox2 = model.model(cv2.imread(p)   ,
                                       detectAngle=False,  ##是否进行文字方向检测
                                       config=dict(MAX_HORIZONTAL_GAP=50,  ##字符之间的最大间隔，用于文本行的合并
                                                   MIN_V_OVERLAPS=0.6,
                                                   MIN_SIZE_SIM=0.6,
                                                   TEXT_PROPOSALS_MIN_SCORE=0.1,
                                                   TEXT_PROPOSALS_NMS_THRESH=0.3,
                                                   TEXT_LINE_NMS_THRESH=0.7,  ##文本行之间测iou值

                                                   ),
                                       leftAdjust=True,  ##对检测的文本行进行向左延伸
                                       rightAdjust=True,  ##对检测的文本行进行向右延伸
                                       alph=0.01,  ##对检测的文本行进行向右、左延伸的倍数

                                       )
##
if scores1.sum()>scores2.sum():

    out={}

    out['picName']=picName
    out['parser']=result1
    out['angle']=angle1

##
out={}

out['picName']=picName
out['parser']=result2
out['angle2']=angle2



    # In[ ]:




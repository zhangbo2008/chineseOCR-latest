#把引入模块都放入静态区域!!!!!!!!!!!!!
#他们在的区域是堆中,因为服务一直没停,所以一直占用内存.正好是我们需要的效果!!!!!!!!!!!!!!!!!!!!
#发现会重复引入下面的库包,加一个引用计数.也不行,用locals加flag也不行!!!


import os

GPUID = '0'  ##调用GPU序号
os.environ["CUDA_VISIBLE_DEVICES"] = GPUID
import torch
from apphelper.image import xy_rotate_box, box_rotate, solve
import model

###########################注意目前只支持4个方向,我要做成8个方向的,只是图片预处理时候多算几个方向即可.4个感觉不够.
import cv2
import numpy as np









#下面是函数主体.


def main(url):
    '''
    先打开url  1种是下载,1种是直接打开.

    :param url:
    :return:
    '''
    tmp2=url
    import requests
    r = requests.get(tmp2)
    with open('tmp.jpg', 'wb') as f:
        f.write(r.content)
    print('图片下载完成')

    picName=url.split('/')[-1].split('.')[-2]







    def plot_box(img,boxes):
        blue = (0, 0, 0) #18
        tmp = np.copy(img)
        for box in boxes:
             cv2.rectangle(tmp, (int(box[0]),int(box[1])), (int(box[2]), int(box[3])), blue, 1) #19

        return Image.fromarray(tmp)

    def plot_boxes(img,angle, result,color=(0,0,0)):
        tmp = np.array(img)
        c = color
        h,w = img.shape[:2]
        thick = int((h + w) / 300)
        i = 0
        if angle in [90,270]:
            imgW,imgH = img.shape[:2]

        else:
            imgH,imgW= img.shape[:2]

        for line in result:
            cx =line['cx']
            cy = line['cy']
            degree =line['degree']
            w  = line['w']
            h = line['h']

            x1,y1,x2,y2,x3,y3,x4,y4 = xy_rotate_box(cx, cy, w, h, degree/180*np.pi)

            x1,y1,x2,y2,x3,y3,x4,y4 = box_rotate([x1,y1,x2,y2,x3,y3,x4,y4],angle=(360-angle)%360,imgH=imgH,imgW=imgW)
            cx  =np.mean([x1,x2,x3,x4])
            cy  = np.mean([y1,y2,y3,y4])
            cv2.line(tmp,(int(x1),int(y1)),(int(x2),int(y2)),c,1)
            cv2.line(tmp,(int(x2),int(y2)),(int(x3),int(y3)),c,1)
            cv2.line(tmp,(int(x3),int(y3)),(int(x4),int(y4)),c,1)
            cv2.line(tmp,(int(x4),int(y4)),(int(x1),int(y1)),c,1)
            mess=str(i)
            cv2.putText(tmp, mess, (int(cx), int(cy)),0, 1e-3 * h, c, thick // 2)
            i+=1
        out=Image.fromarray(tmp).convert('RGB')
        out.save("保存的图片.jpg")
        return out


    # In[3]:


    import time
    from PIL import Image
    import os,sys
    p = os.path.dirname(os.path.abspath( __file__ ))+'/tmp.jpg'
    img = cv2.imread(p)

    h,w = img.shape[:2]
    timeTake = time.time()
    _,result,angle= model.model(img,
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

    timeTake = time.time()-timeTake

    print('It take:{}s'.format(timeTake))
    for line in result:
        print(line['text'])
    plot_boxes(img,angle, result,color=(0,0,0))
    out={}

    out['picName']=picName
    out['parser']=result
    out['angle']=angle         #这个角度表示逆时针.
    return out


    # In[ ]:





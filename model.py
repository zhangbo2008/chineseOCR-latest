# -*- coding: utf-8 -*-
from config import opencvFlag,GPU,IMGSIZE,ocrFlag
if not GPU:
    import os
    os.environ["CUDA_VISIBLE_DEVICES"]=''##不启用GPU
    
if ocrFlag=='torch':
    from crnn.crnn_torch import crnnOcr as crnnOcr ##torch版本ocr
elif ocrFlag=='keras':
     from crnn.crnn_keras import crnnOcr as crnnOcr ##keras版本OCR
    
import time
import cv2
import numpy as np
from PIL import Image
from glob import glob

from text.detector.detectors import TextDetector
from apphelper.image import get_boxes,letterbox_image

from text.opencv_dnn_detect import angle_detect##文字方向检测,支持dnn/tensorflow
from apphelper.image import estimate_skew_angle ,rotate_cut_img,xy_rotate_box,sort_box,box_rotate,solve

if opencvFlag=='opencv':
    from text import opencv_dnn_detect as detect ##opencv dnn model for darknet
elif opencvFlag=='darknet':
    from text import darknet_detect as detect
else:
    ## keras版本文字检测
    from text import keras_detect as detect

print("Text detect engine:{}".format(opencvFlag))

def text_detect(img,
                MAX_HORIZONTAL_GAP=30,
                MIN_V_OVERLAPS=0.6,
                MIN_SIZE_SIM=0.6,
                TEXT_PROPOSALS_MIN_SCORE=0.7,
                TEXT_PROPOSALS_NMS_THRESH=0.3,
                TEXT_LINE_NMS_THRESH = 0.3,
                ):
    boxes, scores = detect.text_detect(np.array(img))
    boxes = np.array(boxes,dtype=np.float32)
    scores = np.array(scores,dtype=np.float32)#下面要做的就是该下行代码支持竖直方向书写.
    '''
    已经想到了最好的解决方法:
    
    因为已经得到了所有的字的box.
    那么所有的汉子都顺时针旋转90度,
    然后再图片整体逆时针旋转90度,就可以把整个图片变成横向书写的图片了.
    在套用原来的检测算法,得到的结果跟把图片看做横向书写来比较就可以,双向识别书写了!!!!!!
    '''


    textdetector  = TextDetector(MAX_HORIZONTAL_GAP,MIN_V_OVERLAPS,MIN_SIZE_SIM)#crnn识别汉子,这里面是算法核心,最难的地方.跟yolo一起就是全部了.
    shape = img.shape[:2]
    boxes = textdetector.detect(boxes,
                                scores[:, np.newaxis],
                                shape,
                                TEXT_PROPOSALS_MIN_SCORE,
                                TEXT_PROPOSALS_NMS_THRESH,
                                TEXT_LINE_NMS_THRESH,
                                )
    
    text_recs = get_boxes(boxes)
    newBox = []
    rx = 1
    ry = 1
    for box in text_recs:
           x1,y1 = (box[0],box[1])
           x2,y2 = (box[2],box[3])
           x3,y3 = (box[6],box[7])
           x4,y4 = (box[4],box[5])
           newBox.append([x1*rx,y1*ry,x2*rx,y2*ry,x3*rx,y3*ry,x4*rx,y4*ry])
    if len(boxes)>0:
        return newBox, boxes[:, 4]  # 把分数也返回做比较用.
    else:

         return newBox,np.array([]) #把分数也返回做比较用.


def text_detect2(img,
                MAX_HORIZONTAL_GAP=30,
                MIN_V_OVERLAPS=0.6,
                MIN_SIZE_SIM=0.6,
                TEXT_PROPOSALS_MIN_SCORE=0.7,
                TEXT_PROPOSALS_NMS_THRESH=0.3,
                TEXT_LINE_NMS_THRESH=0.3,
                ):#cv2.imwrite(img,"test.png")
    boxes, scores = detect.text_detect(np.array(img))
    boxes = np.array(boxes, dtype=np.float32)
    scores = np.array(scores, dtype=np.float32)  # 下面要做的就是该下行代码支持竖直方向书写.


    #第一步每一个boxes右转90度.
    #boxes: (1456,4)   scores    (1456)

    from PIL import Image

    from PIL import Image
    from apphelper import image
    import matplotlib.pyplot as plt
    newboxes=[]
    tmpOld = np.zeros_like(img)
    tmpOld.fill(255)  # 用一个白板来做最后的图片展示.
    tmpOld=Image.fromarray(tmpOld)
    for i in boxes:


        tmp = tmpOld.crop(i)
        tmp=np.array(tmp)
        dat = Image.fromarray(tmp).transpose(Image.ROTATE_270)     #逆时针zhuan270
        newLeftUppoint=image.rotate(i[0],i[1],270,int((i[0]+i[2])/2),int((i[1]+i[3])/2)) #逆时针
        newLeftUppoint=[int(i)for i in newLeftUppoint]
        tmpOld.paste(dat, newLeftUppoint)
        newbox=image.rotate_boxshunshi90(i)
        tmp1=[]
        tmp1.append(newbox[0][0])
        tmp1.append(newbox[0][1])
        tmp1.append(newbox[1][1])
        tmp1.append(newbox[1][0])
        newboxes.append(tmp1)
    tmpOld=tmpOld.transpose(Image.ROTATE_90)
    boxes=[[i[1], img.shape[1]-i[2]+1,i[3],img.shape[0]-i[0]+1] for i in newboxes]#这个地方是不是差1?
    boxes=np.array(boxes).astype(np.float32) #一定要float32.

















    '''
    已经想到了最好的解决方法:!!!!!!!!!不对,因为box不是最后的文字,所以box都旋转会让最后的文字都转废了!!!!!!!!!!!!!!!!!!!!!!!!!1;
    2019-09-14,1点13

    因为已经得到了所有的字的box.
    那么所有的汉子都顺时针旋转90度,
    然后再图片整体逆时针旋转90度,就可以把整个图片变成横向书写的图片了.
    在套用原来的检测算法,得到的结果跟把图片看做横向书写来比较就可以,双向识别书写了!!!!!!
    '''

    textdetector = TextDetector(MAX_HORIZONTAL_GAP, MIN_V_OVERLAPS,
                                MIN_SIZE_SIM)  # crnn识别汉子,这里面是算法核心,最难的地方.跟yolo一起就是全部了.
    shape = img.shape[:2][::-1] #衡中交替.
    boxes = textdetector.detect(boxes,
                                scores[:, np.newaxis],
                                shape,
                                TEXT_PROPOSALS_MIN_SCORE,
                                TEXT_PROPOSALS_NMS_THRESH,
                                TEXT_LINE_NMS_THRESH,
                                )#boxes 里面第二位,第五个数是score

    text_recs = get_boxes(boxes)
    newBox = []
    rx = 1
    ry = 1
    for box in text_recs:
        x1, y1 = (box[0], box[1])
        x2, y2 = (box[2], box[3])
        x3, y3 = (box[6], box[7])
        x4, y4 = (box[4], box[5])
        newBox.append([x1 * rx, y1 * ry, x2 * rx, y2 * ry, x3 * rx, y3 * ry, x4 * rx, y4 * ry])
    if len(boxes)>0:
             return newBox,boxes[:,4],tmpOld
    else:
        return newBox,np.array([]),tmpOld
def crnnRec(im,boxes,leftAdjust=False,rightAdjust=False,alph=0.2,f=1.0):
   """
   crnn模型，ocr识别
   leftAdjust,rightAdjust 是否左右调整box 边界误差，解决文字漏检
   """
   results = []
   im = Image.fromarray(im) 
   for index,box in enumerate(boxes):
       degree,w,h,cx,cy = solve(box)
       partImg,newW,newH = rotate_cut_img(im,degree,box,w,h,leftAdjust,rightAdjust,alph)
       text = crnnOcr(partImg.convert('L'))
       if text.strip()!=u'':
            results.append({'cx':cx*f,'cy':cy*f,'text':text,'w':newW*f,'h':newH*f,'degree':degree*180.0/np.pi})
 #degree表示顺时针转多少度.
   return results




def eval_angle(im,detectAngle=False):
    """
    估计图片偏移角度
    @@param:im
    @@param:detectAngle 是否检测文字朝向
    """
    angle = 0
    img = np.array(im)
    if detectAngle:
        angle = angle_detect(img=np.copy(img))##文字朝向检测
        if angle==90:
            im = Image.fromarray(im).transpose(Image.ROTATE_90)
        elif angle==180:
            im = Image.fromarray(im).transpose(Image.ROTATE_180)
        elif angle==270:
            im = Image.fromarray(im).transpose(Image.ROTATE_270)
        img = np.array(im)
        #这里面表示单个文字的偏斜角度,文字的书写方向还是只有水平向右书写.
    return  angle,img


def model(img,detectAngle=False,config={},leftAdjust=False,rightAdjust=False,alph=0.2):
    """
    @@param:img,
    @@param:ifadjustDegree 调整文字识别倾斜角度
    @@param:detectAngle,是否检测文字朝向
    """
    angle,img = eval_angle(img,detectAngle=detectAngle)##文字方向检测# 注意cv读取就是行列反过来.

    if opencvFlag!='keras':
       img,f =letterbox_image(Image.fromarray(img), IMGSIZE)## pad
       img = np.array(img)
    else:
        f=1.0##解决box在原图坐标不一致问题
    
    config['img'] = img
    #第一种横向书写:
    text_recs,scoreAll1 = text_detect(**config)##文字检测
    #返回的text_recs是一个seq图片



    #第二种竖向书写:   2019-09-14,1点14 发现这么写是错的/11111111111111
    # text_recs2,scoreAll2,newpic = text_detect2(**config)  ##文字检测

    '''
    无奈,还是找不到处理竖着写文字的方法,只能以后再说,现在先代码回滚/    1111
    '''

    if 1!=1:
        print("文字是竖着的概率高!!!!!!")
        text_recs=text_recs2
        newBox = sort_box(text_recs)  # 按照列高排序,符合我们阅读顺序!     ##下行行文本识别
        result = crnnRec(np.array(newpic), newBox, leftAdjust, rightAdjust, alph, 1.0 / f)

    else:
        newBox = sort_box(text_recs)  #按照列高排序,符合我们阅读顺序!     ##下行行文本识别
        result = crnnRec(np.array(img),newBox,leftAdjust,rightAdjust,alph,1.0/f)








    return img,result,angle



